"""Build or check a content-hash index of source files.

build: python -I -X utf8 hash_index.py build --root <repo> --include "<glob>" [--include ...]
                                        [--exclude "<glob>"] [--no-default-excludes]
                                        [--merge] --out <index.json> [--date YYYY-MM-DD]
check: python -I -X utf8 hash_index.py check --root <repo> --index <index.json>

Examples of --include: "src/**/*.java", "**/*.cs", "app/**/*.py", "proto/**/*.proto".
Default excludes: **/target/**, **/build/**, **/node_modules/**, **/.git/**, **/bin/**, **/obj/**
(turn them off with --no-default-excludes when sources live in such folders).

The index is {date, scope, files:[{file, hash, lines, ...}]}, sorted by path so rebuilds are
deterministic. Hashes are SHA-256 over the file with CRLF normalised to LF, so a checkout with
git autocrlf hashes the same on every machine. Language-specific fields (types, fields, methods,
flow) may be added to each entry by another tool; --merge keeps those fields from the existing
index for files whose hash did not change. check compares hash and existence and exits 1 when a
file changed or disappeared. Run check against the OLD index before rebuilding: a fresh index
always matches the disk and hides stale lessons.
"""
import argparse
import datetime as dt
import fnmatch
import hashlib
import json
import sys
from pathlib import Path

DEFAULT_EXCLUDES = ["**/target/**", "**/build/**", "**/node_modules/**", "**/.git/**", "**/bin/**", "**/obj/**"]


def sha256(path):
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def count_lines(path):
    with open(path, "rb") as f:
        return sum(1 for _ in f)


def matches(rel, patterns):
    return any(fnmatch.fnmatch(rel, p) or fnmatch.fnmatch("/" + rel, p) for p in patterns)


def build(args):
    root = Path(args.root).resolve()
    excludes = ([] if args.no_default_excludes else DEFAULT_EXCLUDES) + (args.exclude or [])
    seen = {}
    for pattern in args.include:
        for p in root.glob(pattern):
            if p.is_file():
                rel = p.relative_to(root).as_posix()
                if not matches(rel, excludes):
                    seen[rel] = p
    old = {}
    if args.merge and Path(args.out).exists():
        old = {e["file"]: e for e in json.loads(Path(args.out).read_text(encoding="utf-8")).get("files", [])}
    files = []
    for rel, p in sorted(seen.items()):
        entry = {"file": rel, "hash": sha256(p), "lines": count_lines(p)}
        prev = old.get(rel)
        if prev and prev.get("hash") == entry["hash"]:
            entry = {**prev, **entry}
        files.append(entry)
    index = {"date": args.date or dt.date.today().isoformat(), "scope": args.include, "files": files}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(index, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{len(files)} files -> {out}")


def check(args):
    root = Path(args.root).resolve()
    index = json.loads(Path(args.index).read_text(encoding="utf-8"))
    stale, missing = [], []
    for entry in index.get("files", []):
        p = root / entry["file"]
        if not p.exists():
            missing.append(entry["file"])
        elif sha256(p) != entry.get("hash"):
            stale.append(entry["file"])
    print(json.dumps({"checked": len(index.get("files", [])), "stale": stale, "missing": missing}, ensure_ascii=False, indent=1))
    sys.exit(1 if stale or missing else 0)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--root", required=True)
    b.add_argument("--include", action="append", required=True)
    b.add_argument("--exclude", action="append")
    b.add_argument("--no-default-excludes", action="store_true")
    b.add_argument("--merge", action="store_true")
    b.add_argument("--out", required=True)
    b.add_argument("--date")
    c = sub.add_parser("check")
    c.add_argument("--root", required=True)
    c.add_argument("--index", required=True)
    args = ap.parse_args()
    build(args) if args.cmd == "build" else check(args)


if __name__ == "__main__":
    main()
