#!/usr/bin/env python3
"""
VALIDATE THE SQL MIGRATIONS WITHOUT A DATABASE.

Two checks, both static, both cheap:

  1. Every migration parses under libpg_query, which is Postgres's own grammar.
     This catches real syntax errors, not regex approximations of them.
  2. Every column the `unreconciled_paid_sessions` view reads actually exists on
     the table it reads it from, and every field the JavaScript reads is actually
     emitted by the view. Cross-checked through the parse tree, not by grepping.

WHY THIS EXISTS

There is no local Postgres on this machine and the Docker daemon is usually off,
so migrations get written and shipped unexecuted. That is a genuine gap, and this
narrows it: a typo'd column name in a view is the most likely defect in that
situation and it is exactly what check 2 catches. This does NOT replace running
the migration. It cannot see that a table already exists, that a constraint
conflicts, or that a grant fails.

SETUP

    pip install pglast          # binding to libpg_query, Postgres's real parser

Absent that, this script exits 3 and says so rather than passing vacuously. A
checker that reports success when it could not run is the failure mode this whole
project keeps tripping over.

USAGE

    python3 scripts/check-sql.py                 # all sql/*.sql plus the cross-check
    python3 scripts/check-sql.py sql/014_*.sql   # just these files, parse only
"""
import glob
import os
import re
import sys

try:
    from pglast import parse_sql
    from pglast.parser import ParseError
except ImportError:
    print("check-sql: pglast is not installed, so NOTHING WAS CHECKED.")
    print("           pip install pglast")
    print("           Exiting 3 rather than reporting a pass it did not earn.")
    sys.exit(3)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# Which alias in the view maps to which real table.
ALIAS_MAP = {"t": "checkout_transactions", "f": "fulfilled_sessions", "e": "webhook_events"}
SCHEMA_FILES = [
    "sql/003_preorders.sql",
    "sql/004_fulfilled_sessions.sql",
    "sql/013_checkout_durability.sql",
    "sql/014_webhook_events.sql",
]
JS_FILES = ["src/lib/server/reconcile.js", "src/lib/server/reconcileFormat.js"]
VIEW_SQL = "sql/014_webhook_events.sql"
MIN_JS_FIELD_READS = 8


def parse_file(path):
    """Parse one file. Returns statement count, or raises."""
    with open(path) as fh:
        return parse_sql(fh.read())


def check_parses(paths):
    ok = True
    for path in paths:
        try:
            stmts = parse_file(path)
            print(f"  PASS  {path}  ({len(stmts)} statements)")
        except ParseError as exc:
            print(f"  FAIL  {path}\n        {exc}")
            ok = False
    return ok


def columns_by_table(paths):
    """Build {table: {columns}} from CREATE TABLE and ALTER TABLE ADD COLUMN."""
    tables = {}
    for path in paths:
        for raw in parse_file(path):
            st = raw.stmt
            kind = type(st).__name__
            if kind == "CreateStmt" and st.relation is not None:
                cols = tables.setdefault(st.relation.relname, set())
                for el in st.tableElts or ():
                    if type(el).__name__ == "ColumnDef" and el.colname:
                        cols.add(el.colname)
            elif kind == "AlterTableStmt" and st.relation is not None:
                cols = tables.setdefault(st.relation.relname, set())
                for cmd in st.cmds or ():
                    d = getattr(cmd, "def_", None)
                    if d is not None and type(d).__name__ == "ColumnDef" and d.colname:
                        cols.add(d.colname)
    return tables


def view_columns_and_refs(path):
    """Output column names of the view, plus every (alias, column) it reads."""
    out_cols, refs = [], []

    def walk(node):
        if type(node).__name__ == "ColumnRef":
            parts = [f.sval for f in node.fields if hasattr(f, "sval")]
            if len(parts) == 2:
                refs.append(tuple(parts))
        for slot in getattr(node, "__slots__", ()) or ():
            v = getattr(node, slot, None)
            if hasattr(v, "__slots__"):
                walk(v)
            elif isinstance(v, tuple):
                for item in v:
                    if hasattr(item, "__slots__"):
                        walk(item)

    for raw in parse_file(path):
        st = raw.stmt
        if type(st).__name__ != "ViewStmt":
            continue
        for tgt in st.query.targetList:
            name = tgt.name
            if not name and type(tgt.val).__name__ == "ColumnRef":
                name = tgt.val.fields[-1].sval
            out_cols.append(name)
            walk(tgt)
    return out_cols, refs


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]

    print("== 1. syntax, via libpg_query (Postgres's own grammar) ==")
    paths = args or sorted(glob.glob("sql/*.sql"))
    ok = check_parses(paths)

    if args:
        print("\n(file arguments given, skipping the view cross-check)")
        return 0 if ok else 1

    print("\n== 2. the reconciliation view against the real schema ==")
    tables = columns_by_table(SCHEMA_FILES)
    for t in ("checkout_transactions", "fulfilled_sessions", "webhook_events"):
        print(f"  {t}: {len(tables.get(t, ()))} columns")

    out_cols, refs = view_columns_and_refs(VIEW_SQL)
    if not out_cols:
        print("  FAIL  no CREATE VIEW found; this checker is looking at the wrong file")
        return 2
    print(f"  view emits {len(out_cols)}: {', '.join(out_cols)}")

    bad = []
    for alias, col in sorted(set(refs)):
        table = ALIAS_MAP.get(alias)
        if table and col not in tables.get(table, set()):
            bad.append(f"{alias}.{col} -> {table} has no column {col}")
    for b in bad:
        print(f"  FAIL  {b}")
    if not bad:
        print(f"  PASS  all {len(set(refs))} qualified refs exist on their tables")

    print("\n== 3. the JavaScript against the view ==")
    js = "".join(open(f).read() for f in JS_FILES)
    read = set(re.findall(r"\br\.([a-z_]+)\b", js))
    # Refuse an empty read set. The formatter moved files once already, which
    # turned this into a vacuous PASS over a file with zero reads. A checker whose
    # passing state is reachable by measuring nothing is not a checker.
    if len(read) < MIN_JS_FIELD_READS:
        print(f"  FAIL  only {len(read)} field reads found in {JS_FILES}; expected {MIN_JS_FIELD_READS}+.")
        print("        The checker is looking at the wrong files, so it checked nothing.")
        return 2

    missing = sorted(read - set(out_cols))
    for m in missing:
        print(f"  FAIL  JS reads r.{m}, which the view does not emit")
    if not missing:
        print(f"  PASS  all {len(read)} fields the JS reads are emitted by the view")

    for col in ("minutes_outstanding", "paid_at"):
        present = col in out_cols
        print(f"  {'PASS' if present else 'FAIL'}  supabase query column '{col}' {'present' if present else 'MISSING'}")
        if not present:
            missing.append(col)

    print("\nNOTE: none of this proves the migration APPLIES. Syntax and column")
    print("      names only. Run it against real Postgres before trusting it.")
    return 0 if (ok and not bad and not missing) else 1


if __name__ == "__main__":
    sys.exit(main())
