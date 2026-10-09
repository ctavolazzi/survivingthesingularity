"""The preorder bundle: publishing it, and proving what is published.

WHY THIS MODULE EXISTS

Two different programs need the same three facts about the bundle: where it
lives in Supabase Storage, what its manifest says it contains, and whether the
object sitting at that path right now actually matches. build_bonus.py needed
the first to upload what it builds; sts.py needs all three to answer "is the
live bundle the one we think it is". Before this module, only the first existed,
and it existed as a private function inside a build script, so the second
question had no answer at all.

That gap was not academic. The live object went months without anyone being
able to say what was inside it, because the last program that wrote it
(scripts/update-bundle.mjs, now deleted) read its credentials and its payload
out of a DIFFERENT repository, added a v0.2 draft PDF to whatever was already
there, and left no record. "Verify by breaking it" cannot be applied to a check
that was never written.

THE THREE MANIFESTS, AND WHY VERIFY COMPARES THEM

There are three descriptions of one bundle and they can drift apart:

  1. manuscript/bonus/dist/manifest.json   the BUILD-time record, beside the zip
  2. src/lib/data/bundleManifest.js        the DEPLOY-time record, in the bundle
                                           the site ships (offer.js, the page and
                                           the confirmation email all read it)
  3. the object in Supabase Storage        the RUN-time record, what a customer
                                           actually downloads

1 and 2 are written from a single dict in one pass of build_bonus.py, so they
can only disagree if something wrote one without the other. `--no-pdf` used to
do exactly that. 3 can disagree with both whenever someone uploads without
deploying, or deploys without uploading, and nothing in the build can see it.

`verify` compares 1 against 2 and against the zip on disk. `verify --remote`
compares 3 against 2. Neither is redundant: the offline pass runs in CI with no
credentials, and the remote pass is the only thing that can catch a stale live
object.

STDLIB ONLY, matching scripts/sts.py and scripts/build_bonus.py.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import os
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

# The storage path is not configurable here on purpose. DOWNLOAD_BUNDLE_PATH in
# the production environment points at it and every signed URL already sitting
# in a customer's inbox resolves through it, so a rename is a customer-visible
# break, not a refactor.
DEFAULT_BUCKET = "downloads"
DEFAULT_OBJECT = "research-bundle-v1.zip"

SITE_MANIFEST_REL = "src/lib/data/bundleManifest.js"
DIST_MANIFEST_REL = "manuscript/bonus/dist/manifest.json"
ZIP_REL = "manuscript/bonus/dist/research-bundle-v1.zip"


# ---------------------------------------------------------------------------
# reading the two local manifests
# ---------------------------------------------------------------------------

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_site_manifest(root: Path) -> dict:
    """Parse src/lib/data/bundleManifest.js back into a dict.

    The file is generated as `export default Object.freeze({...});`, so the JSON
    body is everything between the first `Object.freeze(` and the last `)`.
    Reading it back rather than trusting the build's in-memory copy is the whole
    point: this is the artifact that actually ships.
    """
    src = (root / SITE_MANIFEST_REL).read_text(encoding="utf8")
    marker = "Object.freeze("
    start = src.index(marker) + len(marker)
    return json.loads(src[start:src.rindex(")")])


def read_dist_manifest(root: Path) -> dict:
    return json.loads((root / DIST_MANIFEST_REL).read_text(encoding="utf8"))


# ---------------------------------------------------------------------------
# Supabase Storage
# ---------------------------------------------------------------------------

CREDENTIAL_KEYS = (
    "SUPABASE_URL",
    "SUPABASE_SERVICE_KEY",
    "SUPABASE_SECRET_KEY",
    "DOWNLOAD_BUCKET",
    "DOWNLOAD_BUNDLE_PATH",
)


def env(root: Path) -> dict:
    """Credentials: the process environment first, then .env. Empty means unset.

    Three deliberate choices, each paid for:

    The process environment WINS, so a one-off run can supply a key without
    anything being written to disk. The deleted update-bundle.mjs instead
    hardcoded an absolute path to a DIFFERENT repository's .env, which is how
    the live bundle ended up published by a program no one could audit from
    here. A credential this command needs should be visible in the command.

    An EMPTY value counts as absent. This repo's own .env declares all three
    Supabase keys with empty values, so a plain `k in env` test reports
    credentials that are not there and the failure surfaces later as a KeyError
    or a 401 rather than as "you have not set this".

    A MISSING .env is not an error. The offline half of `bundle verify` needs no
    credentials at all and must keep running in a fresh clone and in CI.
    """
    out = {}
    path = root / ".env"
    if path.exists():
        for line in path.read_text(encoding="utf8").split("\n"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                if v.strip():
                    out[k.strip()] = v.strip()
    for k in CREDENTIAL_KEYS:
        v = os.environ.get(k)
        if v and v.strip():
            out[k] = v.strip()
    return out


class CredentialsMissing(Exception):
    """Raised instead of a KeyError so callers can report it as a finding."""


class Storage:
    """A minimal authenticated client for one bucket, on urllib.

    Deliberately not @supabase/supabase-js and not the Python SDK: this repo's
    Python half is stdlib only so that any checkout can run it with no install
    step, and the three calls needed here are three HTTP requests.
    """

    def __init__(self, root: Path):
        e = env(root)
        self.base = e.get("SUPABASE_URL")
        self.key = e.get("SUPABASE_SERVICE_KEY") or e.get("SUPABASE_SECRET_KEY")
        missing = []
        if not self.base:
            missing.append("SUPABASE_URL")
        if not self.key:
            missing.append("SUPABASE_SERVICE_KEY (or SUPABASE_SECRET_KEY)")
        if missing:
            raise CredentialsMissing(
                "no Supabase credentials: " + ", ".join(missing) + ".\n"
                "  This repo's .env declares those names with EMPTY values, so "
                "they are not set.\n"
                "  Supply them for one run without writing anything to disk:\n"
                "    SUPABASE_URL=... SUPABASE_SERVICE_KEY=... "
                "python3 scripts/sts.py bundle verify --remote")
        self.bucket = e.get("DOWNLOAD_BUCKET", DEFAULT_BUCKET)
        self.object = e.get("DOWNLOAD_BUNDLE_PATH", DEFAULT_OBJECT)

    def call(self, method, path, data=None, ctype=None, extra=None):
        h = {"apikey": self.key, "Authorization": f"Bearer {self.key}"}
        if ctype:
            h["Content-Type"] = ctype
        if extra:
            h.update(extra)
        req = urllib.request.Request(self.base + path, data=data, method=method, headers=h)
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read()

    def signed_url(self, expires=300):
        """A customer's actual download URL, or (None, error)."""
        status, body = self.call(
            "POST", f"/storage/v1/object/sign/{self.bucket}/{self.object}",
            json.dumps({"expiresIn": expires}).encode(), "application/json",
        )
        if status != 200:
            return None, f"signed url failed (HTTP {status}): {body[:200]!r}"
        return self.base + "/storage/v1" + json.loads(body)["signedURL"], None

    def fetch_live(self):
        """Download the live bundle THROUGH a signed URL, as a customer does.

        Not the authenticated object endpoint. The signed URL is the door
        customers come through, so verifying the bytes behind it also verifies
        that the door opens, which is a second failure mode the service-role
        fetch would hide.
        """
        url, err = self.signed_url()
        if err:
            return None, err
        try:
            with urllib.request.urlopen(url, timeout=300) as r:
                return r.read(), None
        except urllib.error.HTTPError as e:
            return None, f"signed URL fetch failed (HTTP {e.code})"


def upload(zip_path: Path, root: Path) -> int:
    """Replace the live bundle in place, keeping a dated backup.

    Order matters and is not negotiable: pull the current object down and shelve
    a dated copy BEFORE overwriting. If the backup does not land, nothing is
    overwritten. The previous bundle is the only copy of what past customers
    were sold.
    """
    s = Storage(root)

    # 1. Pull the live bundle down and shelve a dated copy of it.
    status, current = s.call("GET", f"/storage/v1/object/{s.bucket}/{s.object}")
    if status != 200:
        print(f"error: could not download live bundle (HTTP {status})")
        return 1
    stamp = datetime.datetime.now().strftime("%Y%m%d")
    backup = s.object.replace(".zip", f"-backup-{stamp}.zip")
    status, body = s.call(
        "POST", f"/storage/v1/object/{s.bucket}/{backup}", current,
        "application/zip", {"x-upsert": "true"},
    )
    print(f"backup {backup}: HTTP {status} ({len(current):,} bytes preserved)")
    if status not in (200, 201):
        print("  refusing to overwrite without a backup:", body[:200])
        return 1

    # 2. Replace in place.
    new = zip_path.read_bytes()
    status, body = s.call(
        "POST", f"/storage/v1/object/{s.bucket}/{s.object}", new,
        "application/zip", {"x-upsert": "true"},
    )
    print(f"upload {s.object}: HTTP {status} ({len(new):,} bytes)")
    if status not in (200, 201):
        print("  upload failed:", body[:300])
        return 1

    # 3. Prove it by fetching it back the way a customer would, and opening the
    #    zip. An upload that returns 200 and stores nothing readable is exactly
    #    the class of green-check-over-a-dead-pipe this repo has already paid for.
    fetched, err = s.fetch_live()
    if err:
        print("  ", err)
        return 1
    check = zip_path.parent / "verify-roundtrip.zip"
    check.write_bytes(fetched)
    with zipfile.ZipFile(check) as z:
        bad = z.testzip()
        names = z.namelist()
    check.unlink()
    print(f"verified via signed URL: {len(fetched):,} bytes, {len(names)} entries, "
          f"integrity {'OK' if bad is None else 'CORRUPT: ' + bad}")
    if bad is not None or len(fetched) != len(new):
        return 1
    if hashlib.sha256(fetched).hexdigest() != hashlib.sha256(new).hexdigest():
        print("  live object hash does not match what was just uploaded")
        return 1
    return 0


# ---------------------------------------------------------------------------
# verification
# ---------------------------------------------------------------------------

def verify_local(root: Path) -> tuple[list[str], dict]:
    """Compare the two local manifests and the zip on disk. Returns findings.

    Every check here runs with no credentials and no network, so it is safe in
    CI and safe in a fresh clone. Findings are returned rather than printed so
    the caller owns the output format (human or --json).
    """
    findings: list[str] = []
    site_path = root / SITE_MANIFEST_REL
    dist_path = root / DIST_MANIFEST_REL
    zip_path = root / ZIP_REL

    if not site_path.exists():
        findings.append(f"{SITE_MANIFEST_REL} missing: the site has nothing to itemise from")
        return findings, {}
    try:
        site = read_site_manifest(root)
    except Exception as exc:
        findings.append(f"{SITE_MANIFEST_REL} does not parse: {exc}")
        return findings, {}

    # The shipped manifest must describe a shippable bundle. A --no-pdf build
    # produces a real, self-consistent manifest with the headline file missing,
    # which every other check here would happily call clean.
    pdfs = [f for f in site["files"] if f["path"].endswith("The-Precedent-File.pdf")]
    if not pdfs:
        findings.append(
            "site manifest has no The-Precedent-File.pdf: this looks like a "
            "--no-pdf build and must not be what the site ships from")

    if not dist_path.exists():
        findings.append(f"{DIST_MANIFEST_REL} missing: nothing to cross-check the site manifest against")
    else:
        dist = read_dist_manifest(root)
        for key in ("sha256", "bytes", "entries"):
            if site["bundle"][key] != dist["bundle"][key]:
                findings.append(
                    f"bundle.{key} disagrees: site manifest {site['bundle'][key]!r} "
                    f"vs build manifest {dist['bundle'][key]!r}")
        if site["generated_at"] != dist["generated_at"]:
            findings.append(
                f"generated_at disagrees: site manifest {site['generated_at']} vs "
                f"build manifest {dist['generated_at']}. One was written without "
                f"the other, so they describe different builds.")

    if not zip_path.exists():
        findings.append(f"{ZIP_REL} missing: run `sts.py bundle build` before verifying")
        return findings, site

    if zip_path.stat().st_size != site["bundle"]["bytes"]:
        findings.append(
            f"zip is {zip_path.stat().st_size:,} bytes, manifest says "
            f"{site['bundle']['bytes']:,}")
    actual = sha256(zip_path)
    if actual != site["bundle"]["sha256"]:
        findings.append(
            f"zip sha256 {actual[:16]}... does not match manifest "
            f"{site['bundle']['sha256'][:16]}...")

    with zipfile.ZipFile(zip_path) as z:
        bad = z.testzip()
        if bad is not None:
            findings.append(f"zip is corrupt at member {bad}")
        names = set(z.namelist())
        claimed = {f["path"] for f in site["files"]}
        for missing in sorted(claimed - names):
            findings.append(f"manifest lists {missing} but the zip does not contain it")
        for extra in sorted(names - claimed):
            findings.append(f"zip contains {extra} but the manifest does not list it")
        if len(names) != site["bundle"]["entries"]:
            findings.append(
                f"zip holds {len(names)} entries, manifest says "
                f"{site['bundle']['entries']}")
        # Per-file hashes. This is what makes the itemised file table in the
        # confirmation email a claim about the archive rather than about a dict.
        for rec in site["files"]:
            if rec["path"] not in names:
                continue
            data = z.read(rec["path"])
            if len(data) != rec["bytes"]:
                findings.append(
                    f"{rec['path']}: {len(data):,} bytes in the zip, manifest "
                    f"says {rec['bytes']:,}")
            got = hashlib.sha256(data).hexdigest()
            if got != rec["sha256"]:
                findings.append(
                    f"{rec['path']}: sha256 {got[:16]}... in the zip, manifest "
                    f"says {rec['sha256'][:16]}...")

    # Input drift. The bundle can be internally perfect and still describe a
    # casebook that has since been edited, which is the "committed manifest is
    # stale" case that no amount of self-consistency can detect.
    for name, rec in site.get("inputs", {}).items():
        src = root / rec["path"]
        if not src.exists():
            findings.append(f"input {name} ({rec['path']}) no longer exists")
        elif sha256(src) != rec["sha256"]:
            findings.append(
                f"input {name} ({rec['path']}) has changed since the bundle was "
                f"built: rebuild before shipping")

    return findings, site


def verify_remote(root: Path, site: dict) -> list[str]:
    """Compare the LIVE object against the manifest the site ships from.

    This is the only check that can see the failure the bundle spent months in:
    a live object nobody could describe. It needs credentials, so it is opt-in
    rather than part of the offline pass.
    """
    findings: list[str] = []
    try:
        s = Storage(root)
    except CredentialsMissing as exc:
        return [str(exc)]

    live, err = s.fetch_live()
    if err:
        return [err]

    print(f"  live object     : {s.bucket}/{s.object}")
    print(f"  live bytes      : {len(live):,}")
    got = hashlib.sha256(live).hexdigest()
    print(f"  live sha256     : {got}")
    print(f"  manifest sha256 : {site['bundle']['sha256']}")

    if got != site["bundle"]["sha256"]:
        findings.append(
            "the live bundle is NOT the bundle this site describes. Customers "
            "are downloading something other than what the page and the "
            "confirmation email itemise.")
    if len(live) != site["bundle"]["bytes"]:
        findings.append(
            f"live object is {len(live):,} bytes, manifest says "
            f"{site['bundle']['bytes']:,}")

    scratch = root / "manuscript" / "bonus" / "dist" / "verify-remote.zip"
    scratch.parent.mkdir(parents=True, exist_ok=True)
    scratch.write_bytes(live)
    try:
        with zipfile.ZipFile(scratch) as z:
            names = sorted(z.namelist())
        print(f"  live entries    : {len(names)}")
        for n in names:
            print(f"      {n}")
        claimed = {f["path"] for f in site["files"]}
        for missing in sorted(claimed - set(names)):
            findings.append(f"live bundle is missing {missing}")
        for extra in sorted(set(names) - claimed):
            findings.append(f"live bundle carries {extra}, which the manifest does not list")
    except zipfile.BadZipFile:
        findings.append("the live object is not a readable zip")
    finally:
        scratch.unlink(missing_ok=True)

    return findings
