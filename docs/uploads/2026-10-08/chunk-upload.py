#!/usr/bin/env python3
"""Prepare/verify a chunked book archive; upload only with explicit --upload.

Never creates, publishes, edits or deletes a release. Existing assets are preserved.
Retries use unique names and the transport manifest records their exact order.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import threading
import time
import uuid


REPO = "ctavolazzi/survivingthesingularity"
TAG = "book-archive-2026-10-08"
ARCHIVE = "Surviving-the-Singularity-all-editions-2026-10-08.tar.zst"
ARCHIVE_BYTES = 379175616
ARCHIVE_SHA = "8812195af8cdfde5c776222bd0869cd61a8dd486bdd403d6eb8b594ecc1977ce"
CHUNK_BYTES = 4 * 1024 * 1024
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PARTS_DIR = ROOT / "book-build" / "archive-chunks-2026-10-08"
MANIFEST = HERE / "archive-transport.json"
RECEIPT = HERE / "chunk-upload-receipt.json"
TIMEOUT = 220
MAX_ATTEMPTS = 5


class CheckError(RuntimeError):
    pass


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def command(args: list[str]) -> str:
    try:
        result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired as exc:
        raise CheckError(f"{args[0]} {args[1]} exceeded {TIMEOUT}s; remote state will be checked") from exc
    if result.returncode:
        raise CheckError(f"{args[0]} {args[1]} failed ({result.returncode}): {result.stderr.strip()[:500]}")
    return result.stdout


def gh_json(args: list[str]):
    return json.loads(command(["gh", *args]))


def atomic_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w") as stream:
        stream.write(json.dumps(data, indent=2) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def file_hash(path: Path) -> tuple[int, str]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        for data in iter(lambda: stream.read(1024 * 1024), b""):
            size += len(data)
            digest.update(data)
    return size, digest.hexdigest()


def validate_layout(manifest: dict) -> None:
    parts = manifest["parts"]
    if len(parts) != (ARCHIVE_BYTES + CHUNK_BYTES - 1) // CHUNK_BYTES:
        raise CheckError("Incorrect part count")
    if sum(part["bytes"] for part in parts) != ARCHIVE_BYTES:
        raise CheckError("Combined part size does not equal archive size")
    names = set()
    for index, part in enumerate(parts, 1):
        if part["index"] != index:
            raise CheckError("Parts are out of order")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", part["name"]):
            raise CheckError("Unsafe part name")
        if part["name"] in names:
            raise CheckError("Duplicate part name")
        names.add(part["name"])
        expected_size = min(CHUNK_BYTES, ARCHIVE_BYTES - (index - 1) * CHUNK_BYTES)
        if part["bytes"] != expected_size:
            raise CheckError("Unexpected individual part size")
        if not re.fullmatch(r"[0-9a-f]{64}", part["sha256"]):
            raise CheckError("Invalid part SHA256")


def prepare() -> dict:
    bundle = ROOT / "book-build" / ARCHIVE
    if file_hash(bundle) != (ARCHIVE_BYTES, ARCHIVE_SHA):
        raise CheckError("Solid archive bytes differ from verified bundle")
    inventory_path = HERE / "artifact-inventory.json"
    inventory_bytes = inventory_path.read_bytes()
    artifacts = json.loads(inventory_bytes)["artifacts"]
    if len(artifacts) != 149:
        raise CheckError("Expected the 149-payload archive inventory")
    payloads = [{"name": item["candidate_asset_name"], "bytes": item["bytes"],
                 "sha256": item["sha256"]} for item in artifacts]
    if len({item["name"] for item in payloads}) != 149:
        raise CheckError("Duplicate payload names")
    previous = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else None
    if previous and previous.get("archive") != {"name": ARCHIVE, "bytes": ARCHIVE_BYTES, "sha256": ARCHIVE_SHA}:
        raise CheckError("Existing transport manifest describes a different archive; preserved")
    command(["git", "check-ignore", "--quiet", str(PARTS_DIR / (ARCHIVE + ".part001"))])
    PARTS_DIR.mkdir(parents=True, exist_ok=True)
    parts = []
    combined = hashlib.sha256()
    with bundle.open("rb") as stream:
        index = 0
        while True:
            data = stream.read(CHUNK_BYTES)
            if not data:
                break
            index += 1
            combined.update(data)
            canonical = f"{ARCHIVE}.part{index:03d}"
            digest = hashlib.sha256(data).hexdigest()
            path = PARTS_DIR / canonical
            if path.exists() or path.is_symlink():
                if path.is_symlink() or not path.is_file() or file_hash(path) != (len(data), digest):
                    raise CheckError(f"Existing local part differs; preserved: {canonical}")
            else:
                with path.open("xb") as out:
                    out.write(data)
                    out.flush()
                    os.fsync(out.fileno())
            name = canonical
            if previous:
                old = next((p for p in previous["parts"] if p["index"] == index), None)
                if old and old["sha256"] == digest and old["bytes"] == len(data):
                    name = old["name"]
            parts.append({"index": index, "name": name, "canonical_name": canonical,
                          "bytes": len(data), "sha256": digest})
    if combined.hexdigest() != ARCHIVE_SHA:
        raise CheckError("Archive changed while splitting")
    manifest = {
        "schema": "sts-chunked-archive/v1", "repository": REPO, "tag": TAG,
        "base_url": f"https://github.com/{REPO}/releases/download/{TAG}",
        "archive": {"name": ARCHIVE, "bytes": ARCHIVE_BYTES, "sha256": ARCHIVE_SHA},
        "chunk_bytes": CHUNK_BYTES, "parts": parts,
        "payload_count": 149, "payload_bytes": sum(item["bytes"] for item in payloads),
        "inventory_sha256": hashlib.sha256(inventory_bytes).hexdigest(),
        "payloads149": payloads,
        "payload_assurance": "The verified solid archive contains the 149 inventory payloads. Verify extracted names, sizes and SHA256 values against payloads149.",
        "extraction_instructions": [
            "Download and verify each part using its exact name, size and SHA256 in parts.",
            "Concatenate parts in the listed array order, not a wildcard glob; verify the combined archive size and SHA256 before extraction.",
            f"mkdir -p extracted && zstd --long=29 -dc {ARCHIVE} | tar -xf - -C extracted",
            "Verify the extracted 149 payloads against payloads149; keep archive metadata and source provenance alongside them.",
        ],
        "transport_verified": False, "updated_utc": stamp(),
    }
    validate_layout(manifest)
    atomic_json(MANIFEST, manifest)
    return manifest


def release_info() -> dict:
    release = gh_json(["release", "view", TAG, "--repo", REPO, "--json", "apiUrl,isDraft,tagName,url"])
    prefix = f"https://api.github.com/repos/{REPO}/releases/"
    url = release.get("apiUrl", "")
    if release.get("tagName") != TAG or not url.startswith(prefix) or not url[len(prefix):].isdigit():
        raise CheckError("Unexpected release identity")
    release["id"] = int(url[len(prefix):])
    return release


def assets_for(release: dict) -> dict[str, dict]:
    assets = {}
    page_number = 1
    while True:
        # Explicit owner/repo endpoint; gh api has no --repo flag or required --slurp support.
        page = gh_json(["api", "--hostname", "github.com",
                        f"repos/{REPO}/releases/{release['id']}/assets?per_page=100&page={page_number}"])
        if not isinstance(page, list):
            raise CheckError("Unexpected GitHub asset listing")
        for asset in page:
            if asset["name"] in assets:
                raise CheckError("Duplicate remote asset names")
            assets[asset["name"]] = asset
        if len(page) < 100:
            return assets
        page_number += 1


def compare(part: dict, asset: dict, name: str) -> bool:
    if asset.get("name") != name:
        raise CheckError("Remote name mismatch")
    if type(asset.get("size")) is not int or asset["size"] != part["bytes"]:
        raise CheckError("Remote size mismatch")
    if asset.get("state") != "uploaded":
        raise CheckError("Remote asset is not uploaded")
    digest = asset.get("digest")
    if digest is None or digest == "":
        return True
    if digest != "sha256:" + part["sha256"]:
        raise CheckError("Remote SHA256 mismatch")
    return False


def verify(part: dict, asset: dict, name: str) -> dict:
    method = "github-sha256-digest"
    if compare(part, asset, name):
        # Parts are only 4 MiB. A bounded subprocess download avoids pipe deadlocks.
        if type(asset.get("id")) is not int:
            raise CheckError("Invalid remote asset id")
        try:
            downloaded = subprocess.run(
                ["gh", "api", "--hostname", "github.com",
                 f"repos/{REPO}/releases/assets/{asset['id']}", "-H", "Accept: application/octet-stream"],
                cwd=ROOT, capture_output=True, timeout=TIMEOUT)
        except subprocess.TimeoutExpired as exc:
            raise CheckError("Remote digest fallback download timed out") from exc
        if downloaded.returncode:
            raise CheckError("Remote digest fallback download failed")
        if len(downloaded.stdout) != part["bytes"] or hashlib.sha256(downloaded.stdout).hexdigest() != part["sha256"]:
            raise CheckError("Downloaded remote bytes mismatch")
        method = "authenticated-download-sha256"
    return {"index": part["index"], "name": name, "id": asset["id"],
            "bytes": asset["size"], "sha256": part["sha256"], "state": asset["state"],
            "github_digest": asset.get("digest"), "verified_digest": "sha256:" + part["sha256"],
            "verification_method": method, "api_url": asset.get("url"),
            "download_url": asset.get("browser_download_url"), "verified_utc": stamp()}


def candidate_names(part: dict, assets: dict) -> list[str]:
    canonical = part["canonical_name"]
    ordered = [part["name"], canonical]
    ordered.extend(sorted(name for name in assets if name.startswith(canonical + ".attempt-")))
    return list(dict.fromkeys(ordered))


def find_matching(part: dict, assets: dict) -> dict | None:
    for name in candidate_names(part, assets):
        asset = assets.get(name)
        if asset is None:
            continue
        try:
            return verify(part, asset, name)
        except CheckError:
            # Starters and mismatches are preserved, never removed or overwritten.
            continue
    return None


def upload_one(part: dict, release: dict, assets: dict, progress) -> dict:
    matched = find_matching(part, assets)
    if matched:
        return matched
    canonical = part["canonical_name"]
    source = PARTS_DIR / canonical
    for attempt in range(1, MAX_ATTEMPTS + 1):
        # Refresh before retry: the previous timed-out backend may have finished.
        if attempt > 1:
            assets = assets_for(release)
            matched = find_matching(part, assets)
            if matched:
                return matched
        name = canonical if attempt == 1 and canonical not in assets else f"{canonical}.attempt-{uuid.uuid4().hex[:16]}"
        staged = PARTS_DIR / name
        if name != canonical:
            os.link(source, staged)
        if file_hash(staged) != (part["bytes"], part["sha256"]):
            raise CheckError(f"Local chunk changed before upload: {canonical}")
        progress(part, {"attempt": attempt, "name": name, "status": "uploading", "utc": stamp()})
        error = None
        try:
            command(["gh", "release", "upload", TAG, str(staged), "--repo", REPO])
        except CheckError as exc:
            error = str(exc)
        # Check immediately and allow an incomplete backend a short settling period.
        for poll in range(3):
            if poll:
                time.sleep(5)
            try:
                assets = assets_for(release)
                matched = find_matching(part, assets)
                if matched:
                    return matched
            except CheckError as exc:
                error = str(exc)
        progress(part, {"attempt": attempt, "name": name, "status": "not-verified",
                        "error": error or "Remote upload did not become verifiable", "utc": stamp()})
    raise CheckError(f"No verified remote copy after {MAX_ATTEMPTS} attempts: {canonical}")


def self_test() -> None:
    part = {"bytes": 4, "sha256": "a" * 64}
    good = {"name": "archive.part001", "size": 4, "state": "uploaded", "digest": "sha256:" + "a" * 64}
    if compare(part, good, good["name"]):
        raise AssertionError("Matching remote digest requested fallback")
    for field, bad in [("name", "wrong"), ("size", 5), ("state", "starter"), ("digest", "sha256:" + "b" * 64)]:
        try:
            compare(part, dict(good, **{field: bad}), "archive.part001")
        except CheckError:
            continue
        raise AssertionError(f"Negative control was accepted: {field}")
    if not compare(part, dict(good, digest=None), good["name"]):
        raise AssertionError("Missing digest did not require download")
    layout = {"parts": [{"index": i, "name": f"archive.part{i:03d}",
                         "bytes": min(CHUNK_BYTES, ARCHIVE_BYTES - (i - 1) * CHUNK_BYTES),
                         "sha256": "a" * 64} for i in range(1, 92)]}
    validate_layout(layout)
    layout["parts"][0], layout["parts"][1] = layout["parts"][1], layout["parts"][0]
    try:
        validate_layout(layout)
    except CheckError:
        pass
    else:
        raise AssertionError("Reordered manifest was accepted")
    print("Self-test passed: bad name/size/state/SHA rejected; missing digest needs download; order matters.")


def main() -> int:
    global TIMEOUT
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--upload", action="store_true", help="Upload missing chunks to existing draft")
    modes.add_argument("--prepare-only", action="store_true", help="Split/hash locally and write manifest without network")
    modes.add_argument("--self-test", action="store_true", help="In-memory negative controls, no files or network")
    parser.add_argument("--workers", "--jobs", dest="jobs", type=int, default=4, choices=range(1, 5))
    parser.add_argument("--limit", type=int, help="Probe only the first N parts; full manifest remains intact")
    parser.add_argument("--timeout", type=int, default=TIMEOUT, help="Per-gh-command timeout in seconds (default: 220)")
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be positive")
    if args.timeout < 1:
        parser.error("--timeout must be positive")
    TIMEOUT = args.timeout
    if args.self_test:
        self_test()
        return 0
    receipt = {"schema": "sts-chunk-upload-receipt/v1", "repository": REPO, "tag": TAG,
               "archive_sha256": ARCHIVE_SHA, "started_utc": stamp(), "passed": False,
               "mode": "upload" if args.upload else "verify-only", "parts": {}, "attempts": [], "errors": []}
    try:
        manifest = prepare()
        print(f"Prepared {len(manifest['parts'])} verified parts; {ARCHIVE_BYTES} combined bytes.", flush=True)
        if args.prepare_only:
            return 0
        selected_parts = manifest["parts"][:args.limit] if args.limit else manifest["parts"]
        receipt["part_limit"] = args.limit
        receipt["workers"] = args.jobs
        receipt["timeout_seconds"] = TIMEOUT
        release = release_info()
        receipt["release"] = release
        if args.upload and not release["isDraft"]:
            raise CheckError("Upload requires the existing draft release")
        assets = assets_for(release)
        receipt["expected_parts"] = len(selected_parts)
        lock = threading.RLock()

        def persist():
            receipt["updated_utc"] = stamp()
            receipt["verified_parts"] = len(receipt["parts"])
            manifest["updated_utc"] = stamp()
            atomic_json(MANIFEST, manifest)
            atomic_json(RECEIPT, receipt)

        def progress(part, event):
            with lock:
                receipt["attempts"].append({"index": part["index"], **event})
                persist()

        def completed(part, remote):
            with lock:
                part["name"] = remote["name"]
                receipt["parts"][str(part["index"])] = remote
                persist()
            print(f"Verified {part['index']:03d}/{len(manifest['parts'])}: {remote['name']}", flush=True)

        persist()
        if args.upload:
            with ThreadPoolExecutor(max_workers=args.jobs) as executor:
                tasks = {executor.submit(upload_one, part, release, assets, progress): part for part in selected_parts}
                for future in as_completed(tasks):
                    part = tasks[future]
                    try:
                        completed(part, future.result())
                    except Exception as exc:
                        with lock:
                            receipt["errors"].append({"index": part["index"], "error": str(exc)})
                            persist()
        else:
            for part in selected_parts:
                remote = find_matching(part, assets)
                if remote:
                    completed(part, remote)
                else:
                    receipt["errors"].append({"index": part["index"], "error": "No matching uploaded asset"})
                    persist()
        # Fresh final metadata verifies all exact manifest-selected asset names.
        assets = assets_for(release)
        final = {}
        for part in selected_parts:
            try:
                asset = assets.get(part["name"])
                if asset is None:
                    raise CheckError("Manifest-selected asset is missing")
                final[str(part["index"])] = verify(part, asset, part["name"])
            except CheckError as exc:
                receipt["errors"].append({"index": part["index"], "error": str(exc)})
        receipt["parts"] = final
        receipt["passed"] = len(final) == len(selected_parts) and not receipt["errors"]
        manifest["transport_verified"] = receipt["passed"] and len(selected_parts) == len(manifest["parts"])
        validate_layout(manifest)
        persist()
    except Exception as exc:
        receipt["errors"].append({"error": str(exc)})
        receipt["updated_utc"] = stamp()
        atomic_json(RECEIPT, receipt)
    print(f"{'PASS' if receipt['passed'] else 'FAIL'}: verified {len(receipt['parts'])}/{receipt.get('expected_parts', 91)} requested parts; receipt={RECEIPT}")
    if receipt["passed"]:
        print(f"Transport manifest {'fully verified' if manifest['transport_verified'] else 'partially verified'}: {MANIFEST}")
    else:
        for error in receipt["errors"]:
            print(error["error"], file=sys.stderr)
    return 0 if receipt["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
