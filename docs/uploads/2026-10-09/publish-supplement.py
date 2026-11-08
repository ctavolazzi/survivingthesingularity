#!/usr/bin/env python3
"""Verify the supplement; publish its archival prerelease only with --publish."""

import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REPO = "ctavolazzi/survivingthesingularity"
TAG = "book-work-archive-2026-10-09"
ANCHOR = "4e3c934966c286969df720d73738cc2a4385b11c"
MAIN = "0c70e94380df8fba373e5c6ce0d3410f9d20441c"
LATEST = {"id": 364617820, "tag": "v0.7.5"}
ARCHIVE = {"name": "Surviving-the-Singularity-supplement-2026-10-09.tar.zst", "bytes": 123741800,
           "sha256": "db1da47195f82bec1f7fd3ca1ceb5d7db17568fe4f38cf99a49480c50dd6ccaa"}
PAYLOAD_BYTES = 380405614
PART_COUNT = 30
RECEIPT = HERE / "supplement-publication-receipt.json"
STAGE = ROOT / "book-build" / "supplement-final-metadata-2026-10-09"
METADATA = {name: name for name in ("supplement-transport.json", "download-supplement.py",
            "supplement-inventory.json", "supplement-build-receipt.json", "supplement-upload-receipt.json")}
METADATA["SUPPLEMENT-README.md"] = "supplement-release-notes.md"
spec = importlib.util.spec_from_file_location("supplement_checks", HERE.parent / "2026-10-08/chunk-upload.py")
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)
checks.ROOT, checks.REPO, checks.TAG, checks.TIMEOUT = ROOT, REPO, TAG, 420
checks.ARCHIVE, checks.ARCHIVE_BYTES, checks.ARCHIVE_SHA = ARCHIVE["name"], ARCHIVE["bytes"], ARCHIVE["sha256"]


def require(condition, message):
    if not condition:
        raise checks.CheckError(message)


def encode(document):
    return (json.dumps(document, indent=2, ensure_ascii=False) + "\n").encode()


def local_checks(build, transport, upload, inventory_bytes):
    inventory = json.loads(inventory_bytes)
    for document, schema in ((build, "sts-supplement-build/v1"), (transport, "sts-supplement-transport/v1"),
                             (upload, "sts-supplement-upload/v1"), (inventory, "sts-supplement-inventory/v1")):
        require(document.get("schema") == schema and document.get("repository") == REPO
                and document.get("tag") == TAG, "Local document identity differs")
    require(build.get("passed") is True and build.get("archive") == ARCHIVE, "Verified build identity differs")
    require(transport.get("archive") == ARCHIVE and upload.get("archive") == ARCHIVE, "Transport archive differs")
    require(hashlib.sha256(inventory_bytes).hexdigest() == build.get("inventory_sha256"), "Inventory bytes differ from verified build")
    require(inventory.get("payload_count") == 147 and len(inventory.get("files", [])) == 147
            and inventory.get("payload_bytes") == PAYLOAD_BYTES, "Inventory payload scope differs")
    require(build.get("payload_count") == 147 and build.get("payload_bytes") == PAYLOAD_BYTES
            and build.get("verified_tar_members") == 149, "Build payload verification is incomplete")
    records = inventory["files"]
    require(len({item["path"] for item in records}) == 147 and sum(item["bytes"] for item in records) == PAYLOAD_BYTES,
            "Inventory paths or sizes differ")
    portable = {key: value for key, value in inventory.items() if key != "files"}
    portable["files"] = [{key: value for key, value in item.items() if key not in ("source", "source_paths")}
                         for item in records]
    require(hashlib.sha256(encode(portable)).hexdigest() == build.get("portable_manifest_sha256"),
            "Portable inventory differs from verified archive manifest")
    require(transport.get("payload_count") == 147 and transport.get("payload_bytes") == PAYLOAD_BYTES
            and transport.get("payloads") == [{key: item[key] for key in ("path", "bytes", "sha256")} for item in records],
            "Transport payload records differ from bound inventory")
    require(transport.get("base_url") == f"https://github.com/{REPO}/releases/download/{TAG}"
            and transport.get("chunk_bytes") == checks.CHUNK_BYTES, "Transport location or chunk size differs")
    checks.validate_layout(transport)
    for index, part in enumerate(transport["parts"], 1):
        canonical = f"{ARCHIVE['name']}.part{index:03d}"
        require(type(part["index"]) is int and part.get("canonical_name") == canonical
                and re.fullmatch(re.escape(canonical) + r"(?:\.attempt-[0-9a-f]+)?", part["name"]), "Unexpected part naming/order")
    require(transport.get("transport_verified") is True, "Transport completion is pending")
    require(upload.get("passed") is True and upload.get("expected_parts") == PART_COUNT
            and upload.get("verified_parts") == PART_COUNT and not upload.get("errors")
            and set(upload.get("parts", {})) == {str(i) for i in range(1, PART_COUNT + 1)},
            f"Upload receipt is incomplete ({upload.get('verified_parts', 0)}/{PART_COUNT})")
    for part in transport["parts"]:
        recorded = upload["parts"][str(part["index"])]
        require(all(recorded.get(key) == part[key] for key in ("index", "name", "bytes", "sha256"))
                and recorded.get("state") == "uploaded" and recorded.get("verified_digest") == "sha256:" + part["sha256"],
                "Upload receipt differs from selected transport part")
    return inventory


def invariant_issues(refs, latest):
    tag = "refs/tags/" + TAG
    issues = []
    if refs.get("refs/heads/main") != MAIN:
        issues.append("main differs from fixed target")
    if refs.get(tag + "^{}", refs.get(tag)) != ANCHOR:
        issues.append("tag is missing or differs from fixed anchor")
    if latest != LATEST:
        issues.append("latest release differs from v0.7.5")
    return issues


def live_invariants():
    text = checks.command(["git", "ls-remote", f"https://github.com/{REPO}.git", "refs/heads/main",
                           "refs/tags/" + TAG, "refs/tags/" + TAG + "^{}"])
    refs = {line.split()[1]: line.split()[0] for line in text.splitlines()}
    latest = checks.gh_json(["api", "--hostname", "github.com", f"repos/{REPO}/releases/latest"])
    latest = {"id": latest["id"], "tag": latest["tag_name"]}
    require(not invariant_issues(refs, latest), "; ".join(invariant_issues(refs, latest)))
    return {"main": refs["refs/heads/main"], "tag_anchor": ANCHOR, "latest_release": latest}


def release_details():
    basic = checks.release_info()
    return checks.gh_json(["api", "--hostname", "github.com", f"repos/{REPO}/releases/{basic['id']}"])


def expected_metadata(metadata_bytes, stage=False):
    expected = []
    if stage:
        checks.command(["git", "check-ignore", "--quiet", str(STAGE / "SUPPLEMENT-README.md")])
        STAGE.mkdir(parents=True, exist_ok=True)
    for name in METADATA:
        content = metadata_bytes[name]
        if stage:
            target = STAGE / name
            require(not target.is_symlink(), "Staged metadata is a symlink: " + name)
            require(not target.exists() or target.read_bytes() == content, "Existing staged metadata differs; preserved: " + name)
            if not target.exists():
                with target.open("xb") as stream:
                    stream.write(content)
        expected.append({"index": 0, "name": name, "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()})
    return expected


def metadata_checks(expected, release, assets, receipt, save, upload):
    for item in expected:
        asset = assets.get(item["name"])
        if asset is None:
            require(upload, "Missing metadata: " + item["name"])
            checks.command(["gh", "release", "upload", TAG, str(STAGE / item["name"]), "--repo", REPO])
            assets = checks.assets_for({"id": release["id"]})
            asset = assets.get(item["name"])
            require(asset is not None, "Uploaded metadata is not visible: " + item["name"])
        # A mismatching or incomplete existing asset raises without clobbering it.
        receipt["metadata"][item["name"]] = checks.verify(item, asset, item["name"])
        save("metadata-verification")


def self_test():
    inventory = {"schema": "sts-supplement-inventory/v1", "repository": REPO, "tag": TAG,
                 "payload_count": 147, "payload_bytes": PAYLOAD_BYTES,
                 "files": [{"path": f"files/control-{i}", "bytes": PAYLOAD_BYTES if i == 0 else 0, "sha256": "a" * 64}
                           for i in range(147)]}
    content = encode(inventory)
    build = {"schema": "sts-supplement-build/v1", "repository": REPO, "tag": TAG, "passed": True,
             "archive": ARCHIVE, "payload_count": 147, "payload_bytes": PAYLOAD_BYTES, "verified_tar_members": 149,
             "inventory_sha256": hashlib.sha256(content).hexdigest(), "portable_manifest_sha256": hashlib.sha256(content).hexdigest()}
    parts = [{"index": i, "name": f"{ARCHIVE['name']}.part{i:03d}", "canonical_name": f"{ARCHIVE['name']}.part{i:03d}",
              "bytes": min(checks.CHUNK_BYTES, ARCHIVE["bytes"] - (i - 1) * checks.CHUNK_BYTES), "sha256": "b" * 64}
             for i in range(1, PART_COUNT + 1)]
    transport = {"schema": "sts-supplement-transport/v1", "repository": REPO, "tag": TAG,
                 "archive": ARCHIVE, "payload_count": 147, "payload_bytes": PAYLOAD_BYTES,
                 "payloads": inventory["files"], "chunk_bytes": checks.CHUNK_BYTES, "parts": parts,
                 "base_url": f"https://github.com/{REPO}/releases/download/{TAG}", "transport_verified": True}
    upload = {"schema": "sts-supplement-upload/v1", "repository": REPO, "tag": TAG, "passed": True,
              "archive": ARCHIVE, "expected_parts": 30, "verified_parts": 30, "errors": [],
              "parts": {str(p["index"]): {**p, "state": "uploaded", "verified_digest": "sha256:" + p["sha256"]} for p in parts}}
    local_checks(build, transport, upload, content)
    controls = [(0, "passed", False), (0, "portable_manifest_sha256", "c" * 64),
                (1, "transport_verified", False), (1, "payloads", []), (2, "passed", False),
                (2, "verified_parts", 29), (2, "parts", {}), (2, "archive", {})]
    for which, key, wrong in controls:
        docs = copy.deepcopy([build, transport, upload])
        docs[which][key] = wrong
        try:
            local_checks(*docs, content)
        except checks.CheckError:
            continue
        raise AssertionError("Readiness negative control accepted: " + key)
    try:
        local_checks(build, transport, upload, content + b" ")
    except checks.CheckError:
        pass
    else:
        raise AssertionError("Changed inventory bytes accepted")
    refs = {"refs/heads/main": MAIN, "refs/tags/" + TAG + "^{}": ANCHOR}
    require(not invariant_issues(refs, LATEST), "Matching invariants rejected")
    for key in refs:
        require(invariant_issues({**refs, key: "wrong"}, LATEST), "Wrong remote ref accepted")
    require(invariant_issues(refs, {"id": 0, "tag": "other"}), "Wrong latest accepted")
    part = parts[0]
    good = {"name": part["name"], "size": part["bytes"], "state": "uploaded", "digest": "sha256:" + part["sha256"]}
    for key, value in (("name", "other"), ("size", 1), ("state", "starter"), ("digest", "sha256:" + "c" * 64)):
        try:
            checks.compare(part, {**good, key: value}, part["name"])
        except checks.CheckError:
            continue
        raise AssertionError("Remote asset negative control accepted: " + key)
    snapshots = {name: b"validated original bytes" for name in METADATA}
    expected = expected_metadata(snapshots)
    changed = expected_metadata({**snapshots, "supplement-inventory.json": b"changed source bytes"})
    require(len(expected) == 6 and all(item["sha256"] == hashlib.sha256(b"validated original bytes").hexdigest()
                                    for item in expected), "Metadata snapshots were not used")
    require(next(item for item in changed if item["name"] == "supplement-inventory.json")["sha256"]
            != next(item for item in expected if item["name"] == "supplement-inventory.json")["sha256"],
            "Changed metadata bytes did not produce a different expected digest")
    print("Self-test passed: inventory/build/transport/upload binding, incomplete receipts, remote refs/latest and asset mismatches rejected.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--self-test", action="store_true", help="In-memory controls only, no network or file writes")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    os.environ["GODEBUG"] = "http2client=0"
    receipt = {"schema": "sts-supplement-publication/v1", "repository": REPO, "tag": TAG,
               "started_utc": checks.stamp(), "mode": "publish" if args.publish else "verify-only",
               "passed": False, "published": False, "parts": [], "metadata": {}, "errors": []}

    def save(phase):
        receipt["phase"], receipt["updated_utc"] = phase, checks.stamp()
        checks.atomic_json(RECEIPT, receipt)

    try:
        save("local-checks")
        inputs = {name: (HERE / name).read_bytes() for name in ("supplement-build-receipt.json", "supplement-transport.json",
                  "supplement-upload-receipt.json", "supplement-inventory.json")}
        metadata_bytes = {name: inputs[source] if source in inputs else (HERE / source).read_bytes()
                          for name, source in METADATA.items()}
        receipt["input_sha256"] = {name: hashlib.sha256(content).hexdigest() for name, content in inputs.items()}
        receipt["metadata_source_sha256"] = {name: hashlib.sha256(content).hexdigest() for name, content in metadata_bytes.items()}
        build, transport, upload = [json.loads(inputs[name]) for name in ("supplement-build-receipt.json", "supplement-transport.json", "supplement-upload-receipt.json")]
        local_checks(build, transport, upload, inputs["supplement-inventory.json"])
        receipt["invariants"] = live_invariants()
        release = release_details()
        require(release["tag_name"] == TAG and (release["draft"] or (release["prerelease"] and release.get("published_at"))), "Unexpected release state")
        require(upload.get("release_id") == release["id"], "Upload receipt belongs to another release")
        assets = checks.assets_for({"id": release["id"]})
        for part in transport["parts"]:
            require(part["name"] in assets, "Missing remote part: " + part["name"])
            receipt["parts"].append(checks.verify(part, assets[part["name"]], part["name"]))
        require(len(receipt["parts"]) == 30, "Remote verification is incomplete")
        receipt["published"], receipt["release_url"] = not release["draft"], release["html_url"]
        save("remote-parts-verified")
        if args.publish or not release["draft"]:
            expected = expected_metadata(metadata_bytes, stage=args.publish)
            metadata_checks(expected, release, assets, receipt, save, upload=args.publish and release["draft"])
        if args.publish:
            receipt["prepublication_invariants"] = live_invariants()
            save("ready-to-publish")
            if release["draft"]:
                checks.command(["gh", "release", "edit", TAG, "--repo", REPO, "--draft=false", "--prerelease",
                                "--latest=false", "--notes-file", str(STAGE / "SUPPLEMENT-README.md")])
            save("publication-command-complete")
            final = release_details()
            require(final["tag_name"] == TAG and not final["draft"] and final["prerelease"] and final.get("published_at"), "Publication readback failed")
            receipt["postpublication_invariants"] = live_invariants()
            receipt["published"], receipt["release_url"] = True, final["html_url"]
        receipt["passed"] = True
        save("complete" if receipt["published"] else "ready")
    except Exception as exc:
        receipt["errors"].append(str(exc))
        save("pending-or-failed")
    print(f"{'PASS' if receipt['passed'] else 'PENDING'}: {len(receipt['parts'])}/30 remote parts; phase={receipt['phase']}; receipt={RECEIPT}")
    for error in receipt["errors"]:
        print(error, file=sys.stderr)
    return 0 if receipt["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
