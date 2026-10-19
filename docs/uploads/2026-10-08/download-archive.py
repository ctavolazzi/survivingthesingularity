#!/usr/bin/env python3
"""Download, resume and verify the 2026-10-08 book archive using Python's stdlib."""
from __future__ import annotations

import argparse
import copy
import hashlib
import http.client
import io
import json
import os
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://github.com/ctavolazzi/survivingthesingularity/releases/download/book-archive-2026-10-08"
ARCHIVE_NAME = "Surviving-the-Singularity-all-editions-2026-10-08.tar.zst"
ARCHIVE_BYTES = 379175616
ARCHIVE_SHA256 = "8812195af8cdfde5c776222bd0869cd61a8dd486bdd403d6eb8b594ecc1977ce"
CHUNK_BYTES = 4194304
PAYLOAD_BYTES = 3041969876
BLOCK_BYTES = 1024 * 1024


def require(condition, message):
    if not condition:
        raise ValueError(message)


def safe_name(value):
    require(isinstance(value, str) and bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,254}", value)), "Unsafe filename")
    require(not value.endswith("."), "Filename must not end with a dot")
    return value


def valid_hash(value):
    require(isinstance(value, str) and bool(re.fullmatch(r"[0-9a-f]{64}", value)), "Invalid SHA256")


def validate_manifest(data):
    require(isinstance(data, dict), "Manifest must be an object")
    require(data.get("schema") == "sts-chunked-archive/v1", "Unexpected manifest schema")
    require(data.get("base_url") == BASE_URL, "Manifest must use the intended GitHub release base")
    archive = data.get("archive", {})
    require(isinstance(archive, dict), "Invalid archive record")
    safe_name(archive.get("name"))
    require(archive.get("name") == ARCHIVE_NAME, "Unexpected archive filename")
    require(archive.get("bytes") == ARCHIVE_BYTES and archive.get("sha256") == ARCHIVE_SHA256, "Archive differs from the verified original")
    require(data.get("chunk_bytes") == CHUNK_BYTES, "Unexpected chunk size")
    parts = data.get("parts")
    require(isinstance(parts, list) and len(parts) == 91, "Expected 91 ordered archive parts")
    names = set()
    for index, part in enumerate(parts, 1):
        require(isinstance(part, dict), "Invalid part record")
        name = safe_name(part.get("name"))
        canonical = f"{ARCHIVE_NAME}.part{index:03d}"
        require(type(part.get("index")) is int and part["index"] == index, "Part indexes must follow manifest array order")
        require(part.get("canonical_name", canonical) == canonical, "Unexpected canonical part name")
        require(bool(re.fullmatch(re.escape(canonical) + r"(?:\.attempt-[0-9a-f]+)?", name)), "Unexpected part filename")
        require(name not in names, "Duplicate part filename")
        names.add(name)
        expected_bytes = CHUNK_BYTES if index < 91 else ARCHIVE_BYTES - CHUNK_BYTES * 90
        require(type(part.get("bytes")) is int and part["bytes"] == expected_bytes, "Unexpected part size")
        valid_hash(part.get("sha256"))
    require(sum(part["bytes"] for part in parts) == ARCHIVE_BYTES, "Part sizes do not equal archive size")
    payloads = data.get("payloads149")
    require(data.get("payload_count") == 149 and isinstance(payloads, list) and len(payloads) == 149, "Expected 149 archived files")
    payload_names = set()
    for payload in payloads:
        require(isinstance(payload, dict), "Invalid archived file record")
        safe_name(payload.get("name"))
        require(payload["name"] not in payload_names, "Duplicate archived filename")
        payload_names.add(payload["name"])
        require(type(payload.get("bytes")) is int and payload["bytes"] > 0, "Invalid archived file size")
        valid_hash(payload.get("sha256"))
    require(sum(payload["bytes"] for payload in payloads) == PAYLOAD_BYTES, "Archived file sizes differ from inventory")
    return data


def checked_copy(source, destination, record):
    """Read until EOF and verify both length and hash before callers accept a file."""
    digest = hashlib.sha256()
    size = 0
    while True:
        block = source.read(BLOCK_BYTES)
        if not block:
            break
        size += len(block)
        require(size <= record["bytes"], "Received more bytes than declared")
        digest.update(block)
        if destination is not None:
            destination.write(block)
    require(size == record["bytes"] and digest.hexdigest() == record["sha256"], "Size or SHA256 mismatch")
    return size


def file_matches(path, record):
    if path.is_symlink() or not path.is_file() or path.stat().st_size != record["bytes"]:
        return False
    try:
        with path.open("rb") as source:
            checked_copy(source, None, record)
        return True
    except (ValueError, OSError):
        return False


def choose_path(directory, record):
    """Reuse valid files and preserve any existing file whose bytes do not match."""
    base = directory / record["name"]
    if not base.exists() and not base.is_symlink():
        return base, False
    if file_matches(base, record):
        return base, True
    suffix = f".verified-{record['sha256'][:12]}"
    counter = 0
    while True:
        candidate = directory / (record["name"] + suffix + (f"-{counter}" if counter else ""))
        if not candidate.exists() and not candidate.is_symlink():
            print(f"Preserving unmatched file: {base}", flush=True)
            return candidate, False
        if file_matches(candidate, record):
            return candidate, True
        counter += 1


def open_download(name, timeout):
    url = BASE_URL + "/" + urllib.parse.quote(safe_name(name), safe="")
    request = urllib.request.Request(url, headers={"User-Agent": "STS-book-archive-downloader/1", "Accept": "application/octet-stream"})
    response = urllib.request.urlopen(request, timeout=timeout)
    final = urllib.parse.urlsplit(response.geturl())
    # Public GitHub downloads redirect to its release-asset storage.
    allowed_hosts = {"github.com", "release-assets.githubusercontent.com", "objects.githubusercontent.com"}
    if final.scheme != "https" or final.hostname not in allowed_hosts or (final.hostname == "github.com" and not response.geturl().startswith(BASE_URL + "/")):
        response.close()
        raise ValueError("Unexpected download redirect")
    return response


def finish_temp(temporary, target):
    require(not target.exists() and not target.is_symlink(), f"Destination appeared while downloading: {target}")
    # Move only this run's verified temporary file. Existing user files are preserved.
    os.rename(temporary, target)


def get_part(part, directory, timeout, retries, offline):
    canonical = part.get("canonical_name", part["name"])
    if canonical != part["name"] and file_matches(directory / canonical, part):
        return directory / canonical, "reused"
    target, ready = choose_path(directory, part)
    if ready:
        return target, "reused"
    if offline:
        raise ValueError(f"Missing valid offline part: {part['name']}")
    temporary = target.with_name(target.name + ".download-tmp")
    require(not temporary.is_symlink(), "Temporary path must not be a symlink")
    for attempt in range(1, retries + 1):
        try:
            with open_download(part["name"], timeout) as source, temporary.open("wb") as destination:
                checked_copy(source, destination, part)
            finish_temp(temporary, target)
            return target, "downloaded"
        except (ValueError, OSError, urllib.error.URLError, http.client.HTTPException) as error:
            if attempt == retries:
                raise ValueError(f"Could not verify {part['name']}: {error}") from error
            print(f"Retry {attempt}/{retries}: {part['name']}: {error}", flush=True)
            time.sleep(min(2 ** attempt, 10))
    raise AssertionError("Unreachable")


def combine_parts(paths, record, destination=None):
    digest = hashlib.sha256()
    size = 0
    for path in paths:
        with path.open("rb") as source:
            for block in iter(lambda: source.read(BLOCK_BYTES), b""):
                size += len(block)
                require(size <= record["bytes"], "Combined archive is larger than declared")
                digest.update(block)
                if destination is not None:
                    destination.write(block)
    require(size == record["bytes"] and digest.hexdigest() == record["sha256"], "Combined archive SHA256 or size mismatch")
    return size


def self_test():
    failures = []

    def rejected(label, action):
        try:
            action()
        except (ValueError, OSError):
            failures.append(label)
            return
        raise AssertionError(f"Negative control was accepted: {label}")

    body = b"book archive checksum control"
    record = {"bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()}
    destination = io.BytesIO()
    checked_copy(io.BytesIO(body), destination, record)
    assert destination.getvalue() == body
    rejected("wrong bytes with matching length", lambda: checked_copy(io.BytesIO(b"x" * len(body)), None, record))
    rejected("truncated bytes", lambda: checked_copy(io.BytesIO(body[:-1]), None, record))
    rejected("extra bytes", lambda: checked_copy(io.BytesIO(body + b"x"), None, record))
    for name in ["../outside", "/absolute", "a/b", "a\\b", ".", "..", "https://other", "bad name"]:
        rejected(f"unsafe filename {name}", lambda name=name: safe_name(name))
    fixture = {
        "schema": "sts-chunked-archive/v1", "base_url": BASE_URL,
        "archive": {"name": ARCHIVE_NAME, "bytes": ARCHIVE_BYTES, "sha256": ARCHIVE_SHA256},
        "chunk_bytes": CHUNK_BYTES, "payload_count": 149,
        "payloads149": [{"name": f"payload{i}.pdf", "bytes": 1 if i else PAYLOAD_BYTES - 148, "sha256": "a" * 64} for i in range(149)],
        "parts": [{"index": i, "name": f"{ARCHIVE_NAME}.part{i:03d}", "bytes": CHUNK_BYTES if i < 91 else ARCHIVE_BYTES - CHUNK_BYTES * 90, "sha256": "b" * 64} for i in range(1, 92)],
    }
    validate_manifest(fixture)
    bad = copy.deepcopy(fixture); bad["base_url"] = BASE_URL.replace("ctavolazzi", "other")
    rejected("different GitHub repository", lambda: validate_manifest(bad))
    bad = copy.deepcopy(fixture); bad["parts"][0], bad["parts"][1] = bad["parts"][1], bad["parts"][0]
    rejected("reordered parts", lambda: validate_manifest(bad))
    bad = copy.deepcopy(fixture); bad["parts"][0]["name"] = "../outside"
    rejected("manifest path traversal", lambda: validate_manifest(bad))
    bad = copy.deepcopy(fixture); bad["parts"][0]["bytes"] -= 1
    rejected("wrong part length", lambda: validate_manifest(bad))
    bad = copy.deepcopy(fixture); bad["archive"]["sha256"] = "0" * 64
    rejected("changed archive identity", lambda: validate_manifest(bad))
    fixture["parts"][0]["name"] += ".attempt-abc123"
    validate_manifest(fixture)

    class BufferPath:
        def __init__(self, body):
            self.body = body

        def open(self, mode):
            assert mode == "rb"
            return io.BytesIO(self.body)

    chunks = [BufferPath(b"first"), BufferPath(b"second")]
    combined = b"firstsecond"
    combined_record = {"bytes": len(combined), "sha256": hashlib.sha256(combined).hexdigest()}
    output = io.BytesIO()
    combine_parts(chunks, combined_record, output)
    assert output.getvalue() == combined
    rejected("wrong concatenation order", lambda: combine_parts(list(reversed(chunks)), combined_record))
    rejected("omitted part", lambda: combine_parts(chunks[:1], combined_record))
    rejected("corrupted combined bytes", lambda: combine_parts([BufferPath(b"xxxxx"), chunks[1]], combined_record))
    print(json.dumps({"passed": True, "negative_controls": failures, "positive_controls": ["exact streamed bytes", "complete transport structure", "retry asset name", "ordered byte concatenation"]}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path("archive-transport.json"))
    parser.add_argument("--directory", type=Path, default=Path("sts-book-archive-2026-10-08"))
    parser.add_argument("--parts-directory", type=Path, help="Read cached parts from this directory")
    parser.add_argument("--offline", action="store_true", help="Use local verified parts only")
    parser.add_argument("--verify-only", action="store_true", help="Verify the combined stream without writing another archive")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--self-test", action="store_true", help="Run in-memory positive and negative controls")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    require(args.timeout > 0 and args.retries > 0, "Timeout and retries must be positive")
    data = validate_manifest(json.loads(args.manifest.read_text(encoding="utf-8")))
    if not data.get("transport_verified", False):
        print("Manifest marks upload as in progress. Some parts may not be available yet.", flush=True)
    parts_directory = args.parts_directory or args.directory / "parts"
    parts_directory.mkdir(parents=True, exist_ok=True)
    paths = []
    for index, part in enumerate(data["parts"], 1):
        path, state = get_part(part, parts_directory, args.timeout, args.retries, args.offline)
        paths.append(path)
        print(f"{index}/91 {state}: {part['name']}", flush=True)
    archive = data["archive"]
    if args.verify_only:
        combine_parts(paths, archive)
        print(f"Verified combined stream: {archive['bytes']} bytes, SHA256 {archive['sha256']}")
        return
    args.directory.mkdir(parents=True, exist_ok=True)
    target, ready = choose_path(args.directory, archive)
    if not ready:
        temporary = target.with_name(target.name + ".download-tmp")
        require(not temporary.is_symlink(), "Temporary path must not be a symlink")
        with temporary.open("wb") as destination:
            combine_parts(paths, archive, destination)
        finish_temp(temporary, target)
    print(f"Verified archive: {target}\nSHA256: {archive['sha256']}")
    print("Extract with: zstd --long=29 -dc <verified archive> | tar -xf - -C <extraction directory>")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, json.JSONDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
