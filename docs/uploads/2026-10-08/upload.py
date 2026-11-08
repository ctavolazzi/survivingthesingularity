#!/usr/bin/env python3
"""Verify an existing book archive release; upload missing assets only with --upload.

Creates neither tags nor releases, never clobbers assets, and never publishes.
All network requests go through authenticated gh commands to GitHub.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import errno
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import quote


REPO = "ctavolazzi/survivingthesingularity"
TAG = "book-archive-2026-10-08"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CHUNK = 1024 * 1024


class VerificationError(RuntimeError):
    pass


def run(args: list[str]) -> str:
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        # Do not echo environment variables, auth credentials, or binary output.
        raise VerificationError(f"{args[0]} {args[1]} failed ({result.returncode}): "
                                f"{result.stderr.strip()[:600]}")
    return result.stdout


def gh_json(args: list[str]):
    return json.loads(run(["gh", *args]))


def hash_file(path: Path) -> tuple[int, str]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(CHUNK), b""):
            size += len(chunk)
            digest.update(chunk)
    return size, digest.hexdigest()


def validate_inventory(document: dict) -> list[dict]:
    artifacts = document.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise VerificationError("Inventory has no artifacts")
    names = set()
    for item in artifacts:
        name = item.get("candidate_asset_name", "")
        # '#' is gh's display-label delimiter, not a way to rename an asset.
        if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name):
            raise VerificationError(f"Unsafe candidate asset name: {name!r}")
        if name in names:
            raise VerificationError(f"Duplicate candidate asset name: {name}")
        names.add(name)
        if not re.fullmatch(r"[0-9a-f]{64}", item.get("sha256", "")):
            raise VerificationError(f"Invalid inventory SHA256: {name}")
        if type(item.get("bytes")) is not int or item["bytes"] < 0:
            raise VerificationError(f"Invalid inventory size: {name}")
        if not isinstance(item.get("preferred_source_path"), str):
            raise VerificationError(f"Missing source path: {name}")
    return artifacts


def compare_remote(item: dict, asset: dict) -> bool:
    """Reject bad metadata; return True when a download hash is still needed."""
    name = item["candidate_asset_name"]
    if asset.get("name") != name:
        raise VerificationError(f"Remote name mismatch: {name}")
    if type(asset.get("size")) is not int or asset["size"] != item["bytes"]:
        raise VerificationError(f"Remote size mismatch: {name}")
    if asset.get("state") != "uploaded":
        raise VerificationError(f"Remote asset is not uploaded: {name}")
    digest = asset.get("digest")
    if digest is None or digest == "":
        return True
    if digest != "sha256:" + item["sha256"]:
        raise VerificationError(f"Remote SHA256 mismatch: {name}")
    return False


def get_release() -> dict:
    release = gh_json(["release", "view", TAG, "--repo", REPO, "--json",
                       "apiUrl,isDraft,tagName,url"])
    if release.get("tagName") != TAG:
        raise VerificationError("Release tag does not match requested archive")
    api_prefix = f"https://api.github.com/repos/{REPO}/releases/"
    api_url = release.get("apiUrl", "")
    if not api_url.startswith(api_prefix) or not api_url[len(api_prefix):].isdigit():
        raise VerificationError("Unexpected release API URL")
    release["id"] = int(api_url[len(api_prefix):])
    return release


def get_assets(release: dict) -> dict[str, dict]:
    # gh api has no --repo flag. This endpoint specifies the owner/repo literally.
    assets = {}
    page_number = 1
    while True:
        page = gh_json(["api", "--hostname", "github.com",
                        f"repos/{REPO}/releases/{release['id']}/assets?per_page=100&page={page_number}"])
        for asset in page:
            name = asset.get("name")
            if name in assets:
                raise VerificationError(f"Duplicate remote asset name: {name}")
            assets[name] = asset
        if len(page) < 100:
            break
        page_number += 1
    return assets


def download_hash(asset: dict) -> tuple[int, str]:
    asset_id = asset.get("id")
    if type(asset_id) is not int or asset_id <= 0:
        raise VerificationError("Invalid remote asset id")
    command = ["gh", "api", "--hostname", "github.com",
               f"repos/{REPO}/releases/assets/{asset_id}",
               "-H", "Accept: application/octet-stream"]
    digest = hashlib.sha256()
    size = 0
    # Stream the download through stdout; no second 3 GB archive is written.
    with tempfile.TemporaryFile() as errors:
        process = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=errors)
        assert process.stdout is not None
        with process.stdout:
            for chunk in iter(lambda: process.stdout.read(CHUNK), b""):
                size += len(chunk)
                digest.update(chunk)
        code = process.wait()
        if code:
            errors.seek(0)
            message = errors.read(600).decode("utf-8", errors="replace").strip()
            raise VerificationError(f"GitHub download failed ({code}): {message}")
    return size, digest.hexdigest()


def verify_asset(item: dict, asset: dict, download_cache: dict) -> dict:
    needs_download = compare_remote(item, asset)
    method = "github-sha256-digest"
    verified_digest = asset.get("digest")
    if needs_download:
        key = (asset["id"], asset.get("updated_at"), asset["size"], asset["name"])
        if key not in download_cache:
            download_cache[key] = download_hash(asset)
        actual_size, actual_sha = download_cache[key]
        if actual_size != item["bytes"] or actual_sha != item["sha256"]:
            raise VerificationError(f"Downloaded remote bytes mismatch: {item['candidate_asset_name']}")
        verified_digest = "sha256:" + actual_sha
        method = "authenticated-stream-sha256"
    return {
        "name": asset["name"], "id": asset["id"], "bytes": asset["size"],
        "sha256": item["sha256"], "state": asset["state"],
        "github_digest": asset.get("digest"), "verified_digest": verified_digest,
        "verification_method": method, "api_url": asset.get("url"),
        "download_url": asset.get("browser_download_url"), "verified": True,
    }


def upload_asset(item: dict, stage_dir: Path) -> str:
    name = item["candidate_asset_name"]
    source = Path(item["preferred_source_path"])
    expected = (item["bytes"], item["sha256"])
    # Hash immediately before this individual upload, even after global preflight.
    if hash_file(source) != expected:
        raise VerificationError(f"Source changed before upload: {name}")
    staged = stage_dir / name
    run(["git", "check-ignore", "--quiet", str(staged)])
    stage_dir.mkdir(parents=True, exist_ok=True)
    if staged.exists() or staged.is_symlink():
        if not staged.is_file() or staged.is_symlink() or hash_file(staged) != expected:
            raise VerificationError(f"Existing staged asset differs; preserved: {name}")
    else:
        try:
            os.link(source, staged)
        except OSError as exc:
            if exc.errno != errno.EXDEV:
                raise
            shutil.copyfile(source, staged)
            if hash_file(staged) != expected:
                raise VerificationError(f"Staged copy differs; preserved: {name}")
    # The actual staged basename is the asset name. There is no --clobber flag.
    run(["gh", "release", "upload", TAG, str(staged), "--repo", REPO])
    return name


def save_receipt(path: Path, receipt: dict) -> None:
    receipt["updated_utc"] = datetime.now(timezone.utc).isoformat()
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(receipt, indent=2) + "\n")
    os.replace(temporary, path)


def self_test() -> None:
    sha = "a" * 64
    item = {"candidate_asset_name": "book.pdf", "bytes": 123, "sha256": sha}
    good = {"name": "book.pdf", "size": 123, "state": "uploaded", "digest": "sha256:" + sha}
    if compare_remote(item, good):
        raise AssertionError("Matching digest unexpectedly needs download")
    for field, wrong in [("name", "other.pdf"), ("size", 124),
                         ("state", "starter"), ("digest", "sha256:" + "b" * 64)]:
        bad = dict(good, **{field: wrong})
        try:
            compare_remote(item, bad)
        except VerificationError:
            pass
        else:
            raise AssertionError(f"Negative control did not fail: {field}")
    if not compare_remote(item, dict(good, digest=None)):
        raise AssertionError("Missing digest did not require streamed verification")
    print("Self-test passed: wrong name, size, state and SHA256 rejected; missing digest requires download.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upload", action="store_true", help="Upload missing assets to the existing draft")
    parser.add_argument("--self-test", action="store_true", help="In-memory negative controls, with no network or files written")
    parser.add_argument("--inventory", type=Path, default=HERE / "artifact-inventory.json")
    parser.add_argument("--receipt", type=Path, default=HERE / "upload-receipt.json")
    parser.add_argument("--jobs", type=int, default=4, choices=range(1, 5))
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    receipt = {"schema": "sts-upload-receipt/v1", "repository": REPO, "tag": TAG,
               "mode": "upload" if args.upload else "verify-only", "passed": False,
               "assets": [], "errors": [], "upload_command_errors": []}
    try:
        inventory_bytes = args.inventory.read_bytes()
        receipt["inventory_sha256"] = hashlib.sha256(inventory_bytes).hexdigest()
        artifacts = validate_inventory(json.loads(inventory_bytes))
        receipt["expected_assets"] = len(artifacts)
        receipt["expected_bytes"] = sum(item["bytes"] for item in artifacts)
        for item in artifacts:
            if hash_file(Path(item["preferred_source_path"])) != (item["bytes"], item["sha256"]):
                raise VerificationError(f"Local source differs from inventory: {item['candidate_asset_name']}")
        receipt["local_sources_verified"] = len(artifacts)
        print(f"Verified {len(artifacts)} local source hashes.", flush=True)
        release = get_release()
        receipt["release"] = release
        if args.upload and not release["isDraft"]:
            raise VerificationError("--upload requires the existing release to remain a draft")
        assets = get_assets(release)
        download_cache = {}
        missing = []
        # Reject every existing collision before any upload is allowed to begin.
        for item in artifacts:
            asset = assets.get(item["candidate_asset_name"])
            if asset is None:
                missing.append(item)
            else:
                verify_asset(item, asset, download_cache)
        if args.upload and missing:
            stage_dir = ROOT / "book-build" / "upload-archive-2026-10-08" / "assets"
            with ThreadPoolExecutor(max_workers=args.jobs) as executor:
                futures = {executor.submit(upload_asset, item, stage_dir): item for item in missing}
                for future in as_completed(futures):
                    item = futures[future]
                    try:
                        print(f"Uploaded {future.result()}", flush=True)
                    except Exception as exc:
                        receipt["upload_command_errors"].append({"name": item["candidate_asset_name"], "error": str(exc)})
                        print(f"Upload command failed: {item['candidate_asset_name']}; final verification will check remote state.", file=sys.stderr, flush=True)
            # Fresh listing verifies the full archive, including reused assets.
            release = get_release()
            receipt["release"] = release
            assets = get_assets(release)
        for item in artifacts:
            name = item["candidate_asset_name"]
            asset = assets.get(name)
            try:
                if asset is None:
                    raise VerificationError(f"Missing remote asset: {name}")
                receipt["assets"].append(verify_asset(item, asset, download_cache))
            except VerificationError as exc:
                receipt["errors"].append({"name": name, "error": str(exc)})
        receipt["unexpected_remote_assets"] = sorted(set(assets) - {item["candidate_asset_name"] for item in artifacts})
        receipt["verified_assets"] = len(receipt["assets"])
        receipt["passed"] = not receipt["errors"] and receipt["verified_assets"] == len(artifacts)
    except Exception as exc:
        receipt["errors"].append({"error": str(exc)})
    save_receipt(args.receipt, receipt)
    print(f"Verified {len(receipt['assets'])}/{receipt.get('expected_assets', '?')} remote assets; "
          f"result={'PASS' if receipt['passed'] else 'FAIL'}; receipt={args.receipt}")
    if receipt["errors"]:
        for error in receipt["errors"]:
            print(error["error"], file=sys.stderr)
    return 0 if receipt["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
