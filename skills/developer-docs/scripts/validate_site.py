"""Validate a static documentation site for offline use.

Usage: python -I -X utf8 validate_site.py --site <site dir> [--out VALIDATION.json]
                                          [--index <hash index.json> ... --root <repo root>]
                                          [--allow-outside <dir> ...]

Checks every *.html under --site:
  - local href/src/srcset/poster/data/xlink:href targets exist (relative to the page);
  - in-page and cross-page #anchors exist (id= or name=);
  - external references (http:, https:, //) in HTML attributes, and http(s):// URLs or @import in
    the site's .css and .js files, are failures: the site must work offline (XML namespace URLs
    such as http://www.w3.org/... are ignored);
  - optional: entries of one or more hash indexes still match the files on disk.
Links generated at run time by JavaScript are not checked. Links that leave the site directory
(e.g. into the source tree) are counted separately and fail only when the target is missing;
--allow-outside lists folders that may legitimately be missing (sibling repositories that open
only when cloned side by side). Writes a JSON report with counts and a failures list; exit code 1
when failures is not empty.
"""
import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

LINK_ATTRS = {"href", "src", "poster", "data", "xlink:href"}
NAMESPACE_URL = re.compile(r"^https?://www\.w3\.org/")
TEXT_URL = re.compile(r"""(?:url\(\s*['"]?|@import\s+['"]|['"`])(https?://[^'"`)\s]+)""")


class Collector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for key in ("id", "name"):
            if a.get(key):
                self.ids.add(a[key])
        for key, value in attrs:
            if not value:
                continue
            if key in LINK_ATTRS:
                self.refs.append(value.strip())
            elif key == "srcset":
                self.refs += [part.strip().split()[0] for part in value.split(",") if part.strip()]


def parse(path):
    c = Collector()
    try:
        c.feed(path.read_text(encoding="utf-8", errors="replace"))
    except Exception as e:
        c.refs.append(f"!parse-error {e}")
    return c


def sha256(path):
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def inside(path, folder):
    try:
        path.relative_to(folder)
        return True
    except ValueError:
        return False


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--site", required=True)
    ap.add_argument("--out")
    ap.add_argument("--index", action="append", default=[])
    ap.add_argument("--root")
    ap.add_argument("--allow-outside", action="append", default=[])
    args = ap.parse_args()
    site = Path(args.site).resolve()
    pages = sorted(site.rglob("*.html"))
    parsed = {p: parse(p) for p in pages}
    failures, outside = [], 0
    counts = {"html": len(pages), "localLinks": 0, "anchors": 0, "externalRefs": 0}
    allow = [Path(a).resolve() for a in args.allow_outside]
    id_cache = {p: c.ids for p, c in parsed.items()}

    def ids_of(target):
        if target not in id_cache:
            id_cache[target] = parse(target).ids if target.exists() else set()
        return id_cache[target]

    for page, c in parsed.items():
        rel_page = page.relative_to(site).as_posix()
        for ref in c.refs:
            if ref.startswith("!parse-error"):
                failures.append(f"{rel_page}: {ref[1:]}")
                continue
            if ref.startswith(("mailto:", "tel:", "javascript:", "data:", "blob:", "#!")):
                continue
            parts = urlsplit(ref)
            if parts.scheme in ("http", "https") or ref.startswith("//"):
                if NAMESPACE_URL.match(ref):
                    continue
                counts["externalRefs"] += 1
                failures.append(f"{rel_page}: external reference {ref}")
                continue
            path_part, frag = unquote(parts.path), unquote(parts.fragment)
            target = page if not path_part else (page.parent / path_part).resolve()
            if path_part:
                counts["localLinks"] += 1
                if not target.exists():
                    if any(inside(target, a) for a in allow):
                        outside += 1
                        continue
                    failures.append(f"{rel_page}: missing target {ref}")
                    continue
                if not inside(target, site):
                    outside += 1
            if frag:
                counts["anchors"] += 1
                if target.is_dir():
                    target = target / "index.html"
                if target.suffix.lower() in (".html", ".htm") and frag not in ids_of(target):
                    failures.append(f"{rel_page}: missing anchor #{frag} in {target.name}")
    for asset in sorted(list(site.rglob("*.css")) + list(site.rglob("*.js"))):
        text = asset.read_text(encoding="utf-8", errors="replace")
        for url in TEXT_URL.findall(text):
            if NAMESPACE_URL.match(url):
                continue
            counts["externalRefs"] += 1
            failures.append(f"{asset.relative_to(site).as_posix()}: external reference {url}")
    report = {"date": dt.date.today().isoformat(), **counts, "linksOutsideSite": outside}
    if args.index:
        root = Path(args.root or ".").resolve()
        hashed, stale = 0, []
        for idx in args.index:
            index = json.loads(Path(idx).read_text(encoding="utf-8"))
            for e in index.get("files", []):
                hashed += 1
                p = root / e["file"]
                if not p.exists() or sha256(p) != e.get("hash"):
                    stale.append(e["file"])
        report["hashedSources"] = hashed
        report["staleSources"] = len(stale)
        failures += [f"stale or missing source: {s}" for s in stale]
    report["failures"] = failures
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "failures"}, ensure_ascii=False))
    for f in failures[:40]:
        print("failure:", f)
    if len(failures) > 40:
        print(f"... {len(failures) - 40} more")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
