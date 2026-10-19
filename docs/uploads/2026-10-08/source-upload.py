#!/usr/bin/env python3
"""Upload edition branches over a slow link in small pushes.

Each target branch is one large commit on top of history the remote already
has. One push of it outlasts the server's request timeout at ~52 KB/s. So the
file contents go up first, in batches, through a retained staging ref:

  batch commits   tree = every new file sent so far for this target (flat)
                  parents = previous staging commit + every edition tip the
                            remote already has
  closing commit  parents = last batch + the real target commit + those tips

Why the parents matter: when git builds a push it only treats the trees of the
*parents* of the commits being sent as already present on the server. A file
that lives on some other remote branch is sent again unless that branch's tip
is a parent. The closing commit has the real commit as a parent, so pushing it
carries the real commit and its trees up; the branch push that follows then
has nothing left to send.

Modes:
  --simulate   build the commits locally, compute the exact pack git would
               send for every push, print the sizes. Pushes nothing.
  (default)    do it, reading each remote ref back after each push.

Nothing here rewrites or force-pushes. The staging ref is preserved after
completion. Adapted from the source uploader used by the parallel Claude session.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = str(HERE.parents[2])
STAGING = "refs/heads/upload-staging-codex-2026-10-08"
RESUME_STAGING = "refs/remotes/origin/upload-staging-2026-10-08"
# 1.5 MB: the link fell from ~60 KB/s to 3-9 KB/s with stalls partway through the
# first run, and 6-8 MB batches were being cut off. A lost batch now costs less.
CHUNK = int(1.5 * 1024 * 1024)
DEADLINE = 105 * 60          # stop cleanly before the 2 h job limit; the run resumes
SLOWEST_BYTES_PER_SEC = 2500 # a push slower than this is treated as stalled
ALREADY_UP = ["book-v0.10.0"]
TARGETS = ["book-v0.10.1", "book-v0.10.2", "book-v0.10.3", "book-v0.10.4", "book-v0.11.0"]
PUSH = ["-c", "http.version=HTTP/1.1", "push", "--quiet"]
MAX_PUSH_BYTES = 12 * 1024 * 1024          # the 11 MB push took 228 s and went through
STATUS_PATH = sys.argv[sys.argv.index("--status") + 1] if "--status" in sys.argv else None
SIMULATE = "--simulate" in sys.argv
T0 = time.time()


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')} +{int(time.time() - T0):>5}s] {msg}", flush=True)


class OutOfTime(Exception):
    pass


def git(*args, inp=None, check=True, binary=False, timeout=None):
    try:
        r = subprocess.run(["git", "-C", REPO, *args], input=inp, capture_output=True,
                           text=not binary, timeout=timeout)
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(args, 124, "", f"stalled: killed after {timeout}s")
    if check and r.returncode != 0:
        err = r.stderr if not binary else r.stderr.decode(errors="replace")
        raise RuntimeError(f"git {' '.join(args[:4])} failed ({r.returncode}): {err.strip()[-300:]}")
    return r


def sha(rev):
    return git("rev-parse", rev).stdout.strip()


def remote_sha(ref):
    out = git("ls-remote", "origin", ref).stdout.split()
    return out[0] if out else None


def tree_blobs(commit):
    """{sha: size} for every file in a commit's tree."""
    out = {}
    for ln in git("ls-tree", "-r", "-l", commit).stdout.splitlines():
        meta, _path = ln.split("\t", 1)
        _mode, typ, obj, size = meta.split()
        if typ == "blob":
            out[obj] = int(size)
    return out


def remote_tips():
    """sha of every branch tip the remote has, as last fetched or pushed."""
    return set(git("for-each-ref", "--format=%(objectname)", "refs/remotes/origin").stdout.split())


def batches(blobs):
    out, cur, cur_bytes = [], [], 0
    for obj, size in blobs:
        if cur and cur_bytes + size > CHUNK:
            out.append((cur, cur_bytes))
            cur, cur_bytes = [], 0
        cur.append(obj)
        cur_bytes += size
    if cur:
        out.append((cur, cur_bytes))
    return out


def pack_bytes(new, advertised):
    """Size of the pack `git push` would send for `new` given the remote's refs."""
    inp = "".join(f"^{s}\n" for s in sorted(advertised)) + new + "\n"
    r = git("pack-objects", "--revs", "--stdout", "--thin", "--delta-base-offset", "-q",
            inp=inp.encode(), binary=True)
    return len(r.stdout)


def commit_tree(tree, parents, message):
    args = ["commit-tree", tree]
    for p in parents:
        args += ["-p", p]
    return git(*args, "-m", message).stdout.strip()


def flat_tree(shas):
    return git("mktree", inp="".join(f"100644 blob {s}\t{s}\n" for s in shas)).stdout.strip()


def push_verified(refspec, ref, expect, what, size=0):
    """Push, then read the remote ref back. The push's exit code is not the proof.

    Keeps trying until it lands or the run's deadline passes. A stalled push is
    killed; after three failures in a row it waits five minutes for the link.
    """
    limit = max(240, int(size / SLOWEST_BYTES_PER_SEC) + 90)
    attempt = 0
    while True:
        if time.time() - T0 > DEADLINE:
            raise OutOfTime(what)
        attempt += 1
        started = time.time()
        r = git(*PUSH, "origin", refspec, check=False, timeout=limit)
        try:
            got = remote_sha(ref)
        except RuntimeError as e:
            got = None
            log(f"  could not read {ref} back: {str(e)[-80:]}")
        took = int(time.time() - started)
        if got == expect:
            rate = f", {size / max(took, 1) / 1000:.0f} KB/s" if size else ""
            log(f"  ok   {what} in {took}s{rate}" + ("" if attempt == 1 else f" (attempt {attempt})"))
            return True
        last = r.stderr.strip().splitlines()[-1][:110] if r.stderr.strip() else "no stderr"
        log(f"  FAIL {what} attempt {attempt} after {took}s: rc={r.returncode} {last}")
        time.sleep(300 if attempt % 3 == 0 else 20)


def main():
    fixed = json.loads((HERE / "source-upload-targets.json").read_text())["source_branches"]
    for branch, expected in fixed.items():
        if sha(branch) != expected:
            raise RuntimeError(f"Local source branch changed from recorded upload target: {branch}")
    report = {"mode": "simulate" if SIMULATE else "push", "targets": {},
              "largest_push_bytes": 0, "staging_deleted": False}
    done_tips = [sha(b) for b in ALREADY_UP]
    advertised = remote_tips()                      # what the server would list
    have = set()
    for tip in advertised:
        have |= set(tree_blobs(tip))
    staging_tip = git("rev-parse", "-q", "--verify",
                      "refs/remotes/origin/" + STAGING.split("/", 2)[2],
                      check=False).stdout.strip() or None
    if staging_tip is None:
        staging_tip = git("rev-parse", "-q", "--verify", RESUME_STAGING,
                          check=False).stdout.strip() or None
    log(f"remote holds {len(have)} distinct files across {len(advertised)} branch tips")
    total = 0

    def send(commit, refspec, ref, what):
        nonlocal total
        size = pack_bytes(commit, advertised)
        total += size
        report["largest_push_bytes"] = max(report["largest_push_bytes"], size)
        flag = "  <-- OVER LIMIT" if size > MAX_PUSH_BYTES else ""
        if SIMULATE:
            log(f"  sim  {what}: pack {size / 1048576:6.2f} MB{flag}")
            return True
        if size > MAX_PUSH_BYTES:
            log(f"  REFUSING {what}: pack would be {size / 1048576:.1f} MB")
            return False
        return push_verified(refspec, ref, commit, f"{what} [{size / 1048576:.2f} MB]", size)

    for target in TARGETS:
        want = sha(target)
        files = tree_blobs(target)
        entry = report["targets"][target] = {"commit": want, "batches_planned": 0,
                                             "batches_done": 0, "verified": False}
        if not SIMULATE and remote_sha("refs/heads/" + target) == want:
            entry["verified"] = True
            have |= set(files)
            done_tips.append(want)
            advertised.add(want)
            log(f"{target}: already on the remote at {want[:7]}")
            continue
        missing = sorted((o, s) for o, s in files.items() if o not in have)
        plan = batches(missing)
        entry["batches_planned"] = len(plan)
        log(f"{target}: {len(missing)} files the remote lacks, "
            f"{sum(s for _, s in missing) / 1048576:.1f} MB, {len(plan)} batches")
        # Seed with what an earlier run already uploaded for this target, so the
        # closing commit's parent tree still covers every file. Without this a
        # resumed run would resend the earlier batches in the closing push.
        sofar = sorted(o for o in (tree_blobs(staging_tip) if staging_tip else {}) if o in files)
        if sofar:
            log(f"  resuming: {len(sofar)} files for this target are already on the staging ref")
        for i, (shas, _nbytes) in enumerate(plan, 1):
            sofar.extend(shas)
            parents = ([staging_tip] if staging_tip else []) + done_tips
            commit = commit_tree(flat_tree(sofar), parents,
                                 f"chunk upload {target} {i}/{len(plan)}")
            if not send(commit, f"{commit}:{STAGING}", STAGING, f"{target} batch {i}/{len(plan)}"):
                return finish(report, 1, total)
            if staging_tip:
                advertised.discard(staging_tip)
            staging_tip = commit
            advertised.add(commit)
            entry["batches_done"] = i
            write_status(report)
        # Closing commit: carries the real commit and its trees up.
        parents = ([staging_tip] if staging_tip else []) + [want] + done_tips
        closing = commit_tree(flat_tree(sofar) if sofar else git(
            "rev-parse", want + "^{tree}").stdout.strip(), parents, f"chunk upload {target} close")
        if not send(closing, f"{closing}:{STAGING}", STAGING, f"{target} closing commit"):
            return finish(report, 1, total)
        if staging_tip:
            advertised.discard(staging_tip)
        staging_tip = closing
        advertised.add(closing)
        if not send(want, target, "refs/heads/" + target, f"{target} branch itself"):
            return finish(report, 1, total)
        advertised.add(want)
        entry["verified"] = not SIMULATE
        have |= set(files)
        done_tips.append(want)
        write_status(report)

    if SIMULATE:
        log(f"SIMULATION: {total / 1048576:.1f} MB over all pushes, largest "
            f"{report['largest_push_bytes'] / 1048576:.2f} MB, about "
            f"{total / 52000 / 60:.0f} minutes at 52 KB/s. Nothing was pushed.")
        return finish(report, 0 if report["largest_push_bytes"] <= MAX_PUSH_BYTES else 2, total)
    if all(t["verified"] for t in report["targets"].values()):
        log("All targets verified; staging ref preserved.")
    return finish(report, 0, total)


def write_status(report):
    if STATUS_PATH:
        path = Path(STATUS_PATH)
        temporary = path.with_name(path.name + ".tmp")
        temporary.write_text(json.dumps(report, indent=2) + "\n")
        temporary.replace(path)


def finish(report, rc, total):
    report["total_bytes"] = total
    write_status(report)
    done = sum(1 for t in report["targets"].values() if t["verified"])
    log(f"SUMMARY: targets planned {len(report['targets'])}, verified on remote {done}, exit {rc}")
    return rc


if __name__ == "__main__":
    try:
        sys.exit(main())
    except OutOfTime as e:
        log(f"DEADLINE: stopped cleanly while sending {e}. Run again to resume.")
        sys.exit(3)
