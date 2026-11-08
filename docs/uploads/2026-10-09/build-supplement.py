#!/usr/bin/env python3
"""Preserve supplemental project files and verify every compressed archive member."""
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tarfile
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
STAGE = ROOT / "book-build/supplement-2026-10-09"
ARCHIVE = ROOT / "book-build/Surviving-the-Singularity-supplement-2026-10-09.tar.zst"
TAG = "book-work-archive-2026-10-09"
REPO = "ctavolazzi/survivingthesingularity"


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def save(path, value):
    data = (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()
    if path.exists():
        assert path.read_bytes() == data, f"Existing file differs: {path}"
    else:
        path.write_bytes(data)
    assert path.read_bytes() == data


def safe(path):
    p = PurePosixPath(path)
    assert not p.is_absolute() and ".." not in p.parts
    assert "\\" not in path and all(ord(c) >= 32 for c in path)
    return path


def main():
    audit = json.loads((HERE / "artifact-coverage.json").read_text())
    records = []
    project_classes = {"pixel_video_source_or_final_export", "pixel_video_review_export", "production_tracker_scaffold"}
    for item in audit["supplemental_candidates"]:
        if item["classification"] in project_classes:
            continue
        source = Path(item["source_paths"][0])
        relative = source.relative_to(Path.home()).as_posix()
        records.append({"path": safe("files/" + relative), "source": str(source),
                        "source_paths": item["source_paths"], "bytes": item["bytes"],
                        "sha256": item["sha256"], "classification": item["classification"],
                        "coverage_note": item["coverage_note"]})
    for project, details in audit["non_repo_project_manifests"].items():
        for item in details["files"]:
            source = Path(details["source_root"]) / item["relative_path"]
            records.append({"path": safe(f"projects/{project}/" + item["relative_path"]),
                            "source": str(source), "source_paths": [str(source)],
                            "bytes": item["bytes"], "sha256": item["sha256"],
                            "classification": "standalone_project_source_or_export",
                            "coverage_note": "Preserve complete selected project paths, including repeated empty files."})
    assert len({r["path"] for r in records}) == len(records)
    expected_hashes = {r["sha256"] for r in audit["supplemental_candidates"]}
    assert expected_hashes <= {r["sha256"] for r in records}
    records.sort(key=lambda r: (Path(r["path"]).suffix.lower(), r["path"]))
    STAGE.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "check-ignore", "--quiet", str(STAGE / "manifest.json")], cwd=ROOT, check=True)
    for record in records:
        source, target = Path(record["source"]), STAGE / record["path"]
        assert source.is_file() and not source.is_symlink(), source
        assert source.stat().st_size == record["bytes"] and digest(source) == record["sha256"], source
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            shutil.copyfile(source, target)
        assert target.stat().st_size == record["bytes"] and digest(target) == record["sha256"], target
    inventory = {"schema": "sts-supplement-inventory/v1", "repository": REPO, "tag": TAG,
                 "payload_count": len(records), "payload_bytes": sum(r["bytes"] for r in records),
                 "unique_payload_hashes": len({r["sha256"] for r in records}),
                 "scope": "Supplemental project work identified by the October 9 coverage audit. Includes original text bytes, artwork, production intermediates, bonus packages, research drafts, and standalone project sources and final exports.",
                 "research_note": "Local research drafts are preserved as recovered. Authorship and claims are not newly validated by archival inclusion.",
                 "exclusions": audit["notable_exclusions"], "files": records}
    save(HERE / "supplement-inventory.json", inventory)
    portable = {key: value for key, value in inventory.items() if key != "files"}
    portable["files"] = [{key: value for key, value in r.items() if key not in ("source", "source_paths")}
                         for r in records]
    save(STAGE / "manifest.json", portable)
    checksums = "".join(f"{r['sha256']}  {r['path']}\n" for r in records).encode()
    checksum_path = STAGE / "SHA256SUMS"
    if checksum_path.exists():
        assert checksum_path.read_bytes() == checksums
    else:
        checksum_path.write_bytes(checksums)
    print(f"Staged and verified {len(records)} files, {inventory['payload_bytes']} bytes.", flush=True)
    scan = subprocess.run(["gitleaks", "dir", str(STAGE), "--redact", "--no-banner",
                           "--max-archive-depth", "2"], cwd=ROOT)
    assert scan.returncode == 0, "Review secret-scan findings before compressing/uploading"
    assert not ARCHIVE.exists(), "Existing archive preserved; review before rebuilding"
    members = [r["path"] for r in records] + ["manifest.json", "SHA256SUMS"]
    compressor = subprocess.Popen(["zstd", "-19", "--long=29", "-T2", "-o", str(ARCHIVE)],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with tarfile.open(fileobj=compressor.stdin, mode="w|", format=tarfile.PAX_FORMAT) as tar:
        for name in members:
            path = STAGE / name
            info = tarfile.TarInfo(name)
            info.size, info.mode, info.mtime = path.stat().st_size, 0o644, 0
            with path.open("rb") as stream:
                tar.addfile(info, stream)
    compressor.stdin.close()
    compressor.stdin = None
    stdout, stderr = compressor.communicate()
    assert compressor.returncode == 0, stderr.decode(errors="replace")
    print(f"Compressed archive: {ARCHIVE.stat().st_size} bytes. Verifying extracted stream.", flush=True)
    expected = {r["path"]: (r["bytes"], r["sha256"]) for r in records}
    for name in ("manifest.json", "SHA256SUMS"):
        expected[name] = ((STAGE / name).stat().st_size, digest(STAGE / name))
    decoder = subprocess.Popen(["zstd", "--long=29", "-dc", str(ARCHIVE)], stdout=subprocess.PIPE)
    seen = set()
    with tarfile.open(fileobj=decoder.stdout, mode="r|") as tar:
        for member in tar:
            assert member.isfile() and member.name in expected and member.name not in seen
            stream = tar.extractfile(member)
            actual_hash = hashlib.file_digest(stream, "sha256").hexdigest()
            assert (member.size, actual_hash) == expected[member.name], member.name
            seen.add(member.name)
    decoder.stdout.close()
    assert decoder.wait() == 0 and seen == set(expected)
    receipt = {"schema": "sts-supplement-build/v1", "verified_utc": datetime.now(timezone.utc).isoformat(),
               "passed": True, "repository": REPO, "tag": TAG,
               "archive": {"name": ARCHIVE.name, "bytes": ARCHIVE.stat().st_size, "sha256": digest(ARCHIVE)},
               "payload_count": len(records), "payload_bytes": inventory["payload_bytes"],
               "inventory_sha256": digest(HERE / "supplement-inventory.json"),
               "portable_manifest_sha256": digest(STAGE / "manifest.json"),
               "verified_tar_members": len(seen), "secret_scan": "gitleaks dir, archive depth 2, no findings",
               "verification": "Every original source, staged file and decompressed tar member matched its exact size and SHA256; member set and regular-file types also checked.",
               "decoder": "zstd --long=29 -dc"}
    save(HERE / "supplement-build-receipt.json", receipt)
    print(json.dumps(receipt, indent=2), flush=True)


if __name__ == "__main__":
    main()
