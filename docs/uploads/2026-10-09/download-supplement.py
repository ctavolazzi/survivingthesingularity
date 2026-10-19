#!/usr/bin/env python3
"""Download, resume and verify the 2026-10-09 book-work supplement using Python's stdlib."""
from __future__ import annotations

import argparse
import contextlib
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

REPOSITORY = "ctavolazzi/survivingthesingularity"
RELEASE_TAG = "book-work-archive-2026-10-09"
BASE_URL = f"https://github.com/{REPOSITORY}/releases/download/{RELEASE_TAG}"
ARCHIVE_NAME = "Surviving-the-Singularity-supplement-2026-10-09.tar.zst"
CHUNK_BYTES = 4194304
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


def safe_payload_path(value):
    """Accept relative POSIX paths, including original names with spaces."""
    require(isinstance(value, str) and bool(value), "Invalid payload path")
    require(not value.startswith("/") and "\\" not in value and ":" not in value,
            "Payload path must be relative and use POSIX separators")
    require(not any(ord(character) < 32 or ord(character) == 127 for character in value),
            "Payload path contains control characters")
    components = value.split("/")
    require(all(component not in ("", ".", "..") for component in components),
            "Unsafe payload path component")
    require(all(not component.endswith((".", " ")) for component in components),
            "Payload path component must not end with a dot or space")
    return value


def validate_manifest(data):
    require(isinstance(data, dict), "Manifest must be an object")
    require(data.get("schema") == "sts-supplement-transport/v1", "Unexpected manifest schema")
    require(data.get("repository") == REPOSITORY, "Unexpected GitHub repository")
    require(data.get("tag") == RELEASE_TAG, "Unexpected GitHub release tag")
    require(data.get("base_url", BASE_URL) == BASE_URL, "Unexpected GitHub release base")
    archive = data.get("archive", {})
    require(isinstance(archive, dict), "Invalid archive record")
    safe_name(archive.get("name"))
    require(archive.get("name") == ARCHIVE_NAME, "Unexpected archive filename")
    require(type(archive.get("bytes")) is int and archive["bytes"] > 0,
            "Archive size must be a positive integer")
    valid_hash(archive.get("sha256"))
    require(type(data.get("chunk_bytes")) is int and data["chunk_bytes"] == CHUNK_BYTES,
            "Unexpected chunk size")
    require(type(data.get("transport_verified")) is bool, "Invalid transport verification state")
    part_count = (archive["bytes"] + CHUNK_BYTES - 1) // CHUNK_BYTES
    parts = data.get("parts")
    require(isinstance(parts, list) and len(parts) == part_count,
            "Part count differs from declared archive size")
    names = set()
    for index, part in enumerate(parts, 1):
        require(isinstance(part, dict), "Invalid part record")
        name = safe_name(part.get("name"))
        canonical = f"{ARCHIVE_NAME}.part{index:03d}"
        require(type(part.get("index")) is int and part["index"] == index,
                "Part indexes must follow manifest array order")
        require(part.get("canonical_name") == canonical, "Unexpected canonical part name")
        require(bool(re.fullmatch(re.escape(canonical) + r"(?:\.attempt-[0-9a-f]+)?", name)),
                "Unexpected part filename")
        require(name not in names, "Duplicate part filename")
        names.add(name)
        expected_bytes = min(CHUNK_BYTES, archive["bytes"] - CHUNK_BYTES * (index - 1))
        require(type(part.get("bytes")) is int and part["bytes"] == expected_bytes,
                "Unexpected part size")
        valid_hash(part.get("sha256"))
    require(sum(part["bytes"] for part in parts) == archive["bytes"],
            "Part sizes do not equal archive size")
    payloads = data.get("payloads")
    require(type(data.get("payload_count")) is int and data["payload_count"] > 0
            and isinstance(payloads, list) and len(payloads) == data["payload_count"],
            "Payload count differs from archived path records")
    payload_names = set()
    for payload in payloads:
        require(isinstance(payload, dict), "Invalid archived file record")
        path = safe_payload_path(payload.get("path"))
        require(path not in payload_names, "Duplicate archived path")
        payload_names.add(path)
        require(type(payload.get("bytes")) is int and payload["bytes"] >= 0,
                "Invalid archived file size")
        valid_hash(payload.get("sha256"))
        if payload["bytes"] == 0:
            require(payload["sha256"] == hashlib.sha256(b"").hexdigest(),
                    "Empty archived file must have the empty-file SHA256")
    require(not any(parent in payload_names for path in payload_names
                    for parent in ("/".join(path.split("/")[:index])
                                   for index in range(1, len(path.split("/"))))),
            "An archived file path cannot also be a parent directory")
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
    request = urllib.request.Request(url, headers={"User-Agent": "STS-book-work-supplement-downloader/1", "Accept": "application/octet-stream"})
    response = urllib.request.urlopen(request, timeout=timeout)
    final = urllib.parse.urlsplit(response.geturl())
    # Public GitHub downloads redirect to its release-asset storage.
    allowed_hosts = {"github.com", "release-assets.githubusercontent.com", "objects.githubusercontent.com"}
    if final.scheme != "https" or final.hostname not in allowed_hosts or (final.hostname == "github.com" and not response.geturl().startswith(BASE_URL + "/")):
        response.close()
        raise ValueError("Unexpected download redirect")
    return response


def open_temporary(target):
    """Create a run-owned file exclusively, preserving earlier partial downloads."""
    counter = 0
    while True:
        suffix = ".download-tmp" + (f"-{counter}" if counter else "")
        temporary = target.with_name(target.name + suffix)
        try:
            return temporary, temporary.open("xb")
        except FileExistsError:
            counter += 1


def finish_temp(temporary, target):
    # Linking fails atomically if another file appeared at the destination.
    # Only this run's exclusively created temporary pathname is removed.
    os.link(temporary, target)
    temporary.unlink()


def get_part(part, directory, timeout, retries, offline):
    canonical = part["canonical_name"]
    if canonical != part["name"] and file_matches(directory / canonical, part):
        return directory / canonical, "reused"
    target, ready = choose_path(directory, part)
    if ready:
        return target, "reused"
    if offline:
        raise ValueError(f"Missing valid offline part: {part['name']}")
    for attempt in range(1, retries + 1):
        temporary, destination = open_temporary(target)
        try:
            with destination, open_download(part["name"], timeout) as source:
                checked_copy(source, destination, part)
            finish_temp(temporary, target)
            return target, "downloaded"
        except (ValueError, OSError, urllib.error.URLError, http.client.HTTPException) as error:
            destination.close()
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
    positives = []

    def rejected(label, action):
        try:
            action()
        except (ValueError, OSError):
            failures.append(label)
            return
        raise AssertionError(f"Negative control was accepted: {label}")

    body = b"supplement archive checksum control"
    record = {"bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()}
    destination = io.BytesIO()
    checked_copy(io.BytesIO(body), destination, record)
    assert destination.getvalue() == body
    positives.append("exact streamed bytes")
    rejected("wrong bytes with matching length", lambda: checked_copy(io.BytesIO(b"x" * len(body)), None, record))
    rejected("truncated bytes", lambda: checked_copy(io.BytesIO(body[:-1]), None, record))
    rejected("extra bytes", lambda: checked_copy(io.BytesIO(body + b"x"), None, record))
    for name in ["../outside", "/absolute", "a/b", "a\\b", ".", "..", "https://other", "bad name"]:
        rejected(f"unsafe filename {name}", lambda name=name: safe_name(name))
    for path in ["../outside", "/absolute", "a/../b", "a//b", "a/./b", "a\\b", "C:/outside", "a/", "a\x00b", "a\nb", "a."]:
        rejected(f"unsafe payload path {path!r}", lambda path=path: safe_payload_path(path))
    safe_payload_path("sources/Original draft é.txt")
    positives.append("original relative paths with spaces and Unicode")

    fixture = {
        "schema": "sts-supplement-transport/v1", "repository": REPOSITORY, "tag": RELEASE_TAG,
        "base_url": BASE_URL, "transport_verified": True,
        "archive": {"name": ARCHIVE_NAME, "bytes": CHUNK_BYTES + len(body), "sha256": "a" * 64},
        "chunk_bytes": CHUNK_BYTES, "payload_count": 2,
        "payloads": [
            {"path": "sources/draft.txt", "bytes": len(body), "sha256": record["sha256"]},
            {"path": "sources/__init__.py", "bytes": 0, "sha256": hashlib.sha256(b"").hexdigest()},
        ],
        "parts": [
            {"index": 1, "name": f"{ARCHIVE_NAME}.part001", "canonical_name": f"{ARCHIVE_NAME}.part001", "bytes": CHUNK_BYTES, "sha256": "b" * 64},
            {"index": 2, "name": f"{ARCHIVE_NAME}.part002", "canonical_name": f"{ARCHIVE_NAME}.part002", "bytes": len(body), "sha256": "c" * 64},
        ],
    }
    validate_manifest(fixture)
    positives.append("dynamic archive and payload counts including empty files")

    def changed(label, mutate):
        bad = copy.deepcopy(fixture)
        mutate(bad)
        rejected(label, lambda: validate_manifest(bad))

    changed("different GitHub repository", lambda d: d.update(repository="other/repo"))
    changed("different release tag", lambda d: d.update(tag="other"))
    changed("different download base", lambda d: d.update(base_url="https://example.com"))
    changed("different schema", lambda d: d.update(schema="sts-chunked-archive/v1"))
    changed("different archive filename", lambda d: d["archive"].update(name="other.tar.zst"))
    changed("pending archive digest", lambda d: d["archive"].update(sha256="pending"))
    changed("nonpositive archive length", lambda d: d["archive"].update(bytes=0))
    changed("boolean archive length", lambda d: d["archive"].update(bytes=True))
    changed("wrong chunk length", lambda d: d.update(chunk_bytes=CHUNK_BYTES - 1))
    changed("reordered parts", lambda d: d["parts"].reverse())
    changed("omitted part", lambda d: d["parts"].pop())
    changed("manifest name traversal", lambda d: d["parts"][0].update(name="../outside"))
    changed("wrong canonical name", lambda d: d["parts"][0].update(canonical_name="other"))
    changed("wrong part index", lambda d: d["parts"][0].update(index=2))
    changed("wrong part length", lambda d: d["parts"][0].update(bytes=CHUNK_BYTES - 1))
    changed("invalid part digest", lambda d: d["parts"][0].update(sha256="not-a-digest"))
    changed("wrong payload count", lambda d: d.update(payload_count=3))
    changed("payload traversal", lambda d: d["payloads"][0].update(path="../outside"))
    changed("duplicate payload path", lambda d: d["payloads"][1].update(path="sources/draft.txt"))
    changed("file and parent path collision", lambda d: d["payloads"][1].update(path="sources"))
    changed("negative payload length", lambda d: d["payloads"][0].update(bytes=-1))
    changed("wrong empty file digest", lambda d: d["payloads"][1].update(sha256="a" * 64))
    changed("nonboolean transport state", lambda d: d.update(transport_verified="true"))
    fixture["parts"][0]["name"] += ".attempt-abc123"
    validate_manifest(fixture)
    positives.append("retry asset name")
    one_part = copy.deepcopy(fixture)
    one_part["archive"]["bytes"] = CHUNK_BYTES
    one_part["parts"] = one_part["parts"][:1]
    validate_manifest(one_part)
    positives.append("single exact-chunk archive")

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
    positives.append("ordered byte concatenation")
    rejected("wrong concatenation order", lambda: combine_parts(list(reversed(chunks)), combined_record))
    rejected("omitted combined part", lambda: combine_parts(chunks[:1], combined_record))
    rejected("corrupted combined bytes", lambda: combine_parts([BufferPath(b"xxxxx"), chunks[1]], combined_record))
    rejected("incorrect declared combined digest", lambda: combine_parts(chunks, {**combined_record, "sha256": "0" * 64}))

    # Exercise production file selection and offline lookup without filesystem writes.
    class MemoryPath:
        def __init__(self, files, name=""):
            self.files, self.name = files, name

        def __truediv__(self, name):
            return MemoryPath(self.files, name)

        def __str__(self):
            return self.name

        def with_name(self, name):
            return MemoryPath(self.files, name)

        def exists(self):
            return self.name in self.files

        def is_symlink(self):
            return self.files.get(self.name) == "symlink"

        def is_file(self):
            return isinstance(self.files.get(self.name), bytes)

        def stat(self):
            class Stat:
                st_size = len(self.files[self.name])
            return Stat()

        def open(self, mode):
            if mode == "rb":
                return io.BytesIO(self.files[self.name])
            assert mode == "xb"
            if self.exists():
                raise FileExistsError(self.name)
            self.files[self.name] = b""
            path = self

            class Writer(io.BytesIO):
                def close(self):
                    if not self.closed:
                        path.files[path.name] = self.getvalue()
                    super().close()

            return Writer()

        def unlink(self):
            del self.files[self.name]

    part = {**record, "name": "part.attempt-abc", "canonical_name": "part"}
    files = {part["name"]: b"invalid existing bytes"}
    directory = MemoryPath(files)
    with contextlib.redirect_stdout(io.StringIO()):
        chosen, ready = choose_path(directory, part)
    assert not ready and chosen.name != part["name"] and files[part["name"]] == b"invalid existing bytes"
    with contextlib.redirect_stdout(io.StringIO()):
        rejected("offline missing valid part", lambda: get_part(part, directory, 1, 1, True))
    files[chosen.name] = body
    assert get_part(part, directory, 1, 1, True)[0].name == chosen.name
    files["part"] = body
    assert get_part(part, directory, 1, 1, True)[0].name == "part"
    files["part"] = "symlink"
    assert not file_matches(directory / "part", part)
    positives.extend(["invalid cached bytes preserved", "verified cache sibling reused", "offline canonical part reused", "cached symlink rejected"])

    def memory_link(source, target):
        if target.exists():
            raise FileExistsError(target.name)
        target.files[target.name] = source.files[source.name]

    original_link = os.link
    original_download = globals()["open_download"]
    original_sleep = time.sleep
    try:
        os.link = memory_link
        files = {"fresh.download-tmp": b"earlier partial bytes"}
        target = MemoryPath(files, "fresh")
        temporary, writer = open_temporary(target)
        assert temporary.name != "fresh.download-tmp"
        with writer:
            writer.write(body)
        finish_temp(temporary, target)
        assert files["fresh"] == body and files["fresh.download-tmp"] == b"earlier partial bytes"
        positives.append("existing temporary bytes preserved")

        temporary, writer = open_temporary(target)
        with writer:
            writer.write(b"different bytes")
        rejected("concurrent destination preserved", lambda: finish_temp(temporary, target))
        assert files["fresh"] == body and files[temporary.name] == b"different bytes"

        attempts = []

        def retry_download(name, timeout):
            attempts.append(name)
            return io.BytesIO(b"x" * len(body) if len(attempts) == 1 else body)

        globals()["open_download"] = retry_download
        time.sleep = lambda seconds: None
        part = {**record, "name": "retry", "canonical_name": "retry"}
        files = {}
        with contextlib.redirect_stdout(io.StringIO()) as retry_log:
            path, state = get_part(part, MemoryPath(files), 1, 2, False)
        assert len(attempts) == 2 and state == "downloaded" and files[path.name] == body
        assert "Retry 1/2" in retry_log.getvalue()
        assert files["retry.download-tmp"] == b"x" * len(body)
        positives.append("corrupt download retried and partial bytes preserved")
    finally:
        os.link = original_link
        globals()["open_download"] = original_download
        time.sleep = original_sleep

    print(json.dumps({"passed": True, "negative_controls": failures, "positive_controls": positives}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path("supplement-transport.json"))
    parser.add_argument("--directory", type=Path, default=Path("sts-book-work-supplement-2026-10-09"))
    parser.add_argument("--parts-directory", type=Path, help="Read cached parts from this directory")
    parser.add_argument("--offline", action="store_true", help="Use local verified parts only")
    parser.add_argument("--verify-only", action="store_true", help="Verify the combined stream without writing another archive")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--self-test", action="store_true", help="Run local positive and negative controls without network or filesystem writes")
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
        print(f"{index}/{len(data['parts'])} {state}: {part['name']}", flush=True)
    archive = data["archive"]
    if args.verify_only:
        combine_parts(paths, archive)
        print(f"Verified combined stream: {archive['bytes']} bytes, SHA256 {archive['sha256']}")
        return
    args.directory.mkdir(parents=True, exist_ok=True)
    target, ready = choose_path(args.directory, archive)
    if not ready:
        temporary, destination = open_temporary(target)
        with destination:
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
