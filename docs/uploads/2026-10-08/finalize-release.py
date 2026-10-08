#!/usr/bin/env python3
"""Verify archive readiness. Publish only when explicitly invoked with --publish."""

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("archive_chunks", HERE / "chunk-upload.py")
chunks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chunks)
chunks.TIMEOUT = 420
ROOT, REPO, TAG = chunks.ROOT, chunks.REPO, chunks.TAG
TARGETS = HERE / "source-upload-targets.json"
RECEIPT = HERE / "final-release-receipt.json"
STAGE = ROOT / "book-build" / "upload-archive-2026-10-08" / "final-metadata"


def read(path):
    return json.loads(path.read_bytes())


def remote_refs(targets):
    names = ["refs/heads/main", "refs/tags/" + TAG, "refs/tags/" + TAG + "^{}"]
    names += ["refs/heads/" + name for name in targets["source_branches"]]
    output = chunks.command(["git", "ls-remote", "https://github.com/" + REPO + ".git", *names])
    return {line.split()[1]: line.split()[0] for line in output.splitlines()}


def refs_issues(targets, refs):
    issues = []
    if refs.get("refs/heads/main") != targets["main"]:
        issues.append("main differs from fixed target")
    tag = "refs/tags/" + TAG
    if refs.get(tag + "^{}", refs.get(tag)) != targets["archive_tag_commit"]:
        issues.append("archive tag is missing or differs from fixed anchor")
    pending = [name for name, sha in targets["source_branches"].items()
               if refs.get("refs/heads/" + name) != sha]
    if pending:
        issues.append("source branches pending: " + ", ".join(pending))
    return issues


def latest_release():
    release = chunks.gh_json(["api", "--hostname", "github.com", f"repos/{REPO}/releases/latest"])
    return {"id": release["id"], "tag": release["tag_name"]}


def release_details():
    basic = chunks.release_info()
    return chunks.gh_json(["api", "--hostname", "github.com", f"repos/{REPO}/releases/{basic['id']}"])


def fresh_checks(targets, manifest, transfer):
    issues = []
    refs = remote_refs(targets)
    issues.extend(refs_issues(targets, refs))
    latest = latest_release()
    if latest != targets["latest_release"]:
        issues.append("latest release differs from fixed v0.7.5 target")
    release = release_details()
    if release.get("tag_name") != TAG:
        issues.append("release tag differs")
    if not release["draft"] and (not release["prerelease"] or not release.get("published_at")):
        issues.append("release is neither a draft nor the published archival prerelease")
    if not (transfer.get("passed") is True and transfer.get("expected_parts") == 91
            and transfer.get("verified_parts") == 91 and len(transfer.get("parts", {})) == 91
            and transfer.get("archive_sha256") == chunks.ARCHIVE_SHA):
        issues.append("chunk receipt is pending (requires passed 91/91)")
    if manifest.get("transport_verified") is not True:
        issues.append("transport manifest is pending")
    if manifest.get("archive") != {"name": chunks.ARCHIVE, "bytes": chunks.ARCHIVE_BYTES, "sha256": chunks.ARCHIVE_SHA}:
        issues.append("transport archive identity differs")
    chunks.validate_layout(manifest)
    if manifest.get("payload_count") != 149 or len(manifest.get("payloads149", [])) != 149:
        issues.append("transport payload inventory differs")
    assets = chunks.assets_for({"id": release["id"]})
    verified, missing, invalid = [], [], []
    for part in manifest["parts"]:
        asset = assets.get(part["name"])
        if asset is None:
            missing.append(part["index"])
            continue
        try:
            verified.append(chunks.verify(part, asset, part["name"]))
        except chunks.CheckError:
            invalid.append(part["index"])
    if missing or invalid:
        issues.append(f"remote parts pending: {len(missing)} missing, {len(invalid)} invalid")
    checks = {"release_id": release["id"], "release_draft": release["draft"],
              "main": refs.get("refs/heads/main"), "archive_tag_commit": targets["archive_tag_commit"],
              "latest_release": latest, "source_branches": {name: refs.get("refs/heads/" + name)
                                                           for name in targets["source_branches"]},
              "verified_remote_parts": len(verified), "missing_part_indices": missing,
              "invalid_part_indices": invalid, "issues": issues, "parts": verified}
    return checks, release, assets


def write_bytes(path, data):
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(data)
    temporary.replace(path)


def complete_documents():
    path = HERE / "README.md"
    old = path.read_text()
    pending = "**Status: upload in progress.** The compressed archive has been verified locally. Remote completion remains pending."
    complete = "**Status: complete.** All 91 remote parts and required source branches have been verified."
    if pending not in old and complete not in old:
        raise chunks.CheckError("README status line differs; review before publication")
    write_bytes(path, old.replace(pending, complete).encode())
    path = HERE / "RELEASE-NOTES.md"
    notes = "\n".join(line for line in path.read_text().splitlines()
                      if not line.startswith("Publication status:"))
    write_bytes(path, (notes.lstrip() + "\n").encode())
    for name in ["book-archive-manifest.json", "solid-archive-report.json"]:
        path = HERE / name
        document = read(path)
        document["transport_status"] = "complete"
        chunks.atomic_json(path, document)


def stage_metadata(checks):
    chunks.command(["git", "check-ignore", "--quiet", str(STAGE / "ARCHIVE-INDEX.md")])
    STAGE.mkdir(parents=True, exist_ok=True)
    verification = {"schema": "sts-final-verification/v1", "repository": REPO, "tag": TAG,
                    "passed": True, "archive_sha256": chunks.ARCHIVE_SHA,
                    "main": checks["main"], "archive_tag_commit": checks["archive_tag_commit"],
                    "latest_release": checks["latest_release"], "source_branches": checks["source_branches"],
                    "release_id": checks["release_id"],
                    "parts": [{key: part[key] for key in ("index", "name", "id", "bytes", "sha256", "verified_digest")}
                              for part in checks["parts"]]}
    mappings = {"ARCHIVE-INDEX.md": "README.md", "book-catalog.json": "book-archive-manifest.json",
                "archive-transport.json": "archive-transport.json", "download-archive.py": "download-archive.py",
                "solid-archive-report.json": "solid-archive-report.json",
                "chunk-upload-receipt.json": "chunk-upload-receipt.json"}
    data = {name: (HERE / source).read_bytes() for name, source in mappings.items()}
    data["final-verification-receipt.json"] = (json.dumps(verification, indent=2) + "\n").encode()
    expected = []
    for name, content in data.items():
        path = STAGE / name
        if path.exists() and path.read_bytes() != content:
            raise chunks.CheckError(f"Existing staged metadata differs; preserved: {name}")
        if not path.exists():
            with path.open("xb") as stream:
                stream.write(content)
        expected.append({"index": 0, "name": name, "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()})
    return expected


def ensure_metadata(expected, release, assets, receipt, save, allow_upload):
    for item in expected:
        asset = assets.get(item["name"])
        if asset is None:
            if not allow_upload:
                raise chunks.CheckError("Missing final metadata: " + item["name"])
            chunks.command(["gh", "release", "upload", TAG, str(STAGE / item["name"]), "--repo", REPO])
            assets = chunks.assets_for({"id": release["id"]})
            asset = assets.get(item["name"])
            if asset is None:
                raise chunks.CheckError("Uploaded metadata not visible: " + item["name"])
        # Existing starter/mismatching metadata raises; no clobber or deletion.
        receipt["metadata"][item["name"]] = chunks.verify(item, asset, item["name"])
        save("metadata-verification")


def self_test():
    target = {"main": "a", "archive_tag_commit": "b", "source_branches": {"book-v0.11.0": "c"}}
    refs = {"refs/heads/main": "a", "refs/tags/" + TAG + "^{}": "b", "refs/heads/book-v0.11.0": "c"}
    if refs_issues(target, refs):
        raise AssertionError("Good ref targets rejected")
    for name in refs:
        bad = dict(refs, **{name: "wrong"})
        if not refs_issues(target, bad):
            raise AssertionError("Changed remote ref accepted: " + name)
    chunks.self_test()
    print("Finalizer self-test passed: wrong main, tag anchor and source branch rejected.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publish", action="store_true", help="Complete docs, verify metadata and publish archival prerelease")
    parser.add_argument("--self-test", action="store_true", help="In-memory checks; no network, files or publication")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    # This connection survived the observed HTTP/2 upload inactivity failures.
    os.environ["GODEBUG"] = "http2client=0"
    receipt = {"schema": "sts-final-release-receipt/v1", "repository": REPO, "tag": TAG,
               "mode": "publish" if args.publish else "verify-only", "started_utc": chunks.stamp(),
               "passed": False, "published": False, "metadata": {}, "errors": []}

    def save(phase):
        receipt["phase"] = phase
        receipt["updated_utc"] = chunks.stamp()
        chunks.atomic_json(RECEIPT, receipt)

    try:
        save("checking")
        targets, manifest, transfer = read(TARGETS), read(HERE / "archive-transport.json"), read(HERE / "chunk-upload-receipt.json")
        checks, release, assets = fresh_checks(targets, manifest, transfer)
        receipt["checks"] = checks
        save("readiness")
        if checks["issues"]:
            raise chunks.CheckError("; ".join(checks["issues"]))
        receipt["published"] = not release["draft"]
        receipt["release_url"] = release["html_url"]
        if not args.publish and not release["draft"]:
            names = ["ARCHIVE-INDEX.md", "book-catalog.json", "archive-transport.json", "download-archive.py",
                     "solid-archive-report.json", "chunk-upload-receipt.json", "final-verification-receipt.json"]
            expected = [{"index": 0, "name": name, "bytes": (STAGE / name).stat().st_size,
                         "sha256": chunks.file_hash(STAGE / name)[1]} for name in names]
            ensure_metadata(expected, release, assets, receipt, save, allow_upload=False)
        if args.publish:
            complete_documents()
            save("documents-complete")
            expected = stage_metadata(checks)
            ensure_metadata(expected, release, assets, receipt, save, allow_upload=release["draft"])
            # Verify publication invariants again after the metadata transfers.
            if refs_issues(targets, remote_refs(targets)) or latest_release() != targets["latest_release"]:
                raise chunks.CheckError("Remote ref/latest invariants changed during metadata transfer")
            save("ready-to-publish")
            if release["draft"]:
                chunks.command(["gh", "release", "edit", TAG, "--repo", REPO, "--draft=false",
                                "--prerelease", "--latest=false", "--notes-file", str(HERE / "RELEASE-NOTES.md")])
            save("publication-command-complete")
            final = release_details()
            if final["draft"] or not final["prerelease"] or not final.get("published_at"):
                raise chunks.CheckError("Published release readback failed")
            if refs_issues(targets, remote_refs(targets)) or latest_release() != targets["latest_release"]:
                raise chunks.CheckError("Post-publication remote ref/latest readback failed")
            receipt["published"] = True
            receipt["release_url"] = final["html_url"]
        receipt["passed"] = True
        save("complete" if args.publish else "ready")
    except Exception as exc:
        receipt["errors"].append(str(exc))
        save("pending-or-failed")
    checks = receipt.get("checks", {})
    print(f"{'PASS' if receipt['passed'] else 'PENDING'}: remote parts {checks.get('verified_remote_parts', 0)}/91; "
          f"phase={receipt['phase']}; receipt={RECEIPT}")
    for error in receipt["errors"]:
        print(error, file=sys.stderr)
    return 0 if receipt["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
