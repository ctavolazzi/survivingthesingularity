#!/usr/bin/env python3
"""Prepare, upload or verify supplemental archive parts without deleting assets."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location("archive_transfer", HERE.parent / "2026-10-08/chunk-upload.py")
transfer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(transfer)
TAG = "book-work-archive-2026-10-09"
MANIFEST = HERE / "supplement-transport.json"
RECEIPT = HERE / "supplement-upload-receipt.json"
PARTS = ROOT / "book-build/supplement-parts-2026-10-09"


def read(path):
    return json.loads(path.read_bytes())


def bound_inventory(build, content):
    assert hashlib.sha256(content).hexdigest() == build["inventory_sha256"], "Inventory differs from the verified archive build"
    inventory = json.loads(content)
    assert inventory["payload_count"] == build["payload_count"]
    assert inventory["payload_bytes"] == build["payload_bytes"]
    return inventory


def prepare():
    build = read(HERE / "supplement-build-receipt.json")
    inventory = bound_inventory(build, (HERE / "supplement-inventory.json").read_bytes())
    assert build["passed"] is True and build["tag"] == TAG
    archive = build["archive"]
    assert archive["name"] == "Surviving-the-Singularity-supplement-2026-10-09.tar.zst"
    source = ROOT / "book-build" / archive["name"]
    assert transfer.file_hash(source) == (archive["bytes"], archive["sha256"])
    transfer.TAG, transfer.TIMEOUT = TAG, 420
    transfer.ARCHIVE, transfer.ARCHIVE_BYTES, transfer.ARCHIVE_SHA = archive["name"], archive["bytes"], archive["sha256"]
    transfer.PARTS_DIR = PARTS
    old = read(MANIFEST) if MANIFEST.exists() else None
    if old:
        assert old["archive"] == archive, "Existing manifest preserved: archive identity changed"
    transfer.command(["git", "check-ignore", "--quiet", str(PARTS / "part001")])
    PARTS.mkdir(parents=True, exist_ok=True)
    parts = []
    combined = hashlib.sha256()
    with source.open("rb") as stream:
        while data := stream.read(transfer.CHUNK_BYTES):
            combined.update(data)
            index = len(parts) + 1
            name = f"{archive['name']}.part{index:03d}"
            part = {"index": index, "name": name, "canonical_name": name,
                    "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
            path = PARTS / name
            if path.exists() or path.is_symlink():
                assert not path.is_symlink() and transfer.file_hash(path) == (len(data), part["sha256"])
            else:
                with path.open("xb") as output:
                    output.write(data)
            if old:
                previous = old["parts"][index - 1]
                assert previous["index"] == index and previous["sha256"] == part["sha256"]
                part["name"] = previous["name"]
            parts.append(part)
    assert combined.hexdigest() == archive["sha256"]
    manifest = {"schema": "sts-supplement-transport/v1", "repository": transfer.REPO, "tag": TAG,
                "base_url": f"https://github.com/{transfer.REPO}/releases/download/{TAG}",
                "archive": archive, "chunk_bytes": transfer.CHUNK_BYTES, "parts": parts,
                "payload_count": inventory["payload_count"], "payload_bytes": inventory["payload_bytes"],
                "payloads": [{k: item[k] for k in ("path", "bytes", "sha256")} for item in inventory["files"]],
                "transport_verified": False, "updated_utc": transfer.stamp()}
    transfer.validate_layout(manifest)
    transfer.atomic_json(MANIFEST, manifest)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--prepare-only", action="store_true")
    modes.add_argument("--upload", action="store_true", help="Requires an existing draft release")
    modes.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        transfer.self_test()
        content = b'{"payload_count": 1, "payload_bytes": 4}'
        fixture = {"payload_count": 1, "payload_bytes": 4, "inventory_sha256": hashlib.sha256(content).hexdigest()}
        bound_inventory(fixture, content)
        try:
            bound_inventory(fixture, content.replace(b'4', b'5'))
        except AssertionError:
            pass
        else:
            raise AssertionError("Changed inventory accepted")
        print("Inventory binding negative control passed.")
        return 0
    os.environ["GODEBUG"] = "http2client=0"
    receipt = {"schema": "sts-supplement-upload/v1", "repository": transfer.REPO, "tag": TAG,
               "started_utc": transfer.stamp(), "passed": False, "parts": {}, "attempts": [], "errors": []}
    try:
        manifest = prepare()
        if args.prepare_only:
            print(f"Prepared {len(manifest['parts'])} parts, {manifest['archive']['bytes']} bytes.")
            return 0
        receipt["archive"] = manifest["archive"]
        receipt["expected_parts"] = len(manifest["parts"])
        release = transfer.release_info()
        receipt["release_id"] = release["id"]
        assert not args.upload or release["isDraft"], "Uploads require a draft release"
        assets = transfer.assets_for(release)

        def save():
            receipt["verified_parts"] = len(receipt["parts"])
            receipt["updated_utc"] = transfer.stamp()
            transfer.atomic_json(MANIFEST, manifest)
            transfer.atomic_json(RECEIPT, receipt)

        def progress(part, event):
            receipt["attempts"].append({"index": part["index"], **event})
            save()

        save()
        for part in manifest["parts"]:
            remote = transfer.upload_one(part, release, assets, progress) if args.upload else transfer.find_matching(part, assets)
            assert remote is not None, f"No matching remote part {part['index']}"
            part["name"] = remote["name"]
            receipt["parts"][str(part["index"])] = remote
            save()
            print(f"Verified {part['index']}/{len(manifest['parts'])}: {remote['name']}", flush=True)
        assets = transfer.assets_for(release)
        for part in manifest["parts"]:
            receipt["parts"][str(part["index"])] = transfer.verify(part, assets[part["name"]], part["name"])
        receipt["passed"] = True
        manifest["transport_verified"] = True
        save()
    except Exception as error:
        receipt["errors"].append(str(error))
        transfer.atomic_json(RECEIPT, receipt)
    print(f"{'PASS' if receipt['passed'] else 'FAIL'}: {len(receipt['parts'])}/{receipt.get('expected_parts', '?')} parts", flush=True)
    if receipt["errors"]:
        print(json.dumps(receipt["errors"]), flush=True)
    return 0 if receipt["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
