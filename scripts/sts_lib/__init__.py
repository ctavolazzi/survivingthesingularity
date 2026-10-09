"""Internals of scripts/sts.py, split out by concern.

sts.py stays the ONE entry point - `sts.py <command>` is the documented surface
and nothing here is meant to be run directly. The modules exist so that a
concern can be read, tested and changed without loading the other twenty-two
commands, not so that callers can start reaching past the CLI.

sts.py adds its own directory to sys.path automatically (it is the __main__
script), so `from sts_lib.manifest import ...` resolves with no packaging step,
no install, and no PYTHONPATH set by the caller. scripts/build-epub.sh invokes
`python3 scripts/sts.py`, which gets the same treatment.
"""
