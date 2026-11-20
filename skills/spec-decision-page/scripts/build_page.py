"""Embed a seed JSON into the decision page template.

Usage: python -I -X utf8 build_page.py <template.html> <seed.json> <out.html>

The output is the page body (no doctype); run build_offline.py on it to get a standalone file.
seed.meta.title sets the page title; seed.meta.storeKey separates browser storage between pages.
"""
import html
import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 4 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(2)
    template, seed_path, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    seed = json.loads(seed_path.read_text(encoding="utf-8"))
    title = (seed.get("meta") or {}).get("title") or "Spesifikasyon Kararları"
    data = json.dumps(seed, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    page = template.read_text(encoding="utf-8")
    page = page.replace("__PAGE_TITLE__", html.escape(title)).replace("__SEED_JSON__", data)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"{out} {out.stat().st_size} bytes, {len(seed.get('items', []))} items")


if __name__ == "__main__":
    main()
