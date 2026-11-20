"""Build the standalone offline decision page: embedded data, embedded (subset) fonts, no network.

Usage: python -I -X utf8 build_offline.py <page from build_page.py> <font dir | -> <output .html>
                                          [--lang tr] [--test-hook]

<font dir> is a folder holding Inter-Regular.ttf, Inter-Medium.ttf, Inter-SemiBold.ttf and
JetBrainsMono-Regular.ttf (both families SIL OFL 1.1), typically the font folder of the product's
UI kit. The fonts are subset to Latin + Turkish + the punctuation the page uses and inlined as data
URIs (about 150 KB). Pass "-" to skip fonts; the page then uses system fonts and still works
offline. If a folder is given but none of the four files is found, the build stops. Needs fontTools
(pip install fonttools; brotli optional for woff2).

--test-hook exposes window.__sdpTest.attach(handle, mode) so a test can attach an OPFS file handle
instead of the native file picker. Never ship a page built with --test-hook.
"""
import argparse
import base64
import io
import re
import sys
from pathlib import Path

UNICODES = (
    list(range(0x20, 0x7F)) + list(range(0xA0, 0x180)) + list(range(0x2010, 0x2028)) + list(range(0x2030, 0x203B))
    + list(range(0x2190, 0x21A0)) + [0x2026, 0x2122, 0x2212, 0x00D7, 0x2264, 0x2265, 0x2248, 0x2260, 0x00B1, 0x2022, 0x25CF, 0x25BE]
)
FACES = [
    ("Inter", 400, "Inter-Regular.ttf"),
    ("Inter", 500, "Inter-Medium.ttf"),
    ("Inter", 600, "Inter-SemiBold.ttf"),
    ("JetBrains Mono", 400, "JetBrainsMono-Regular.ttf"),
]
WEB_FONT_LINK = re.compile(r'<link rel="(?:preconnect|stylesheet)" href="https://fonts\.(?:googleapis|gstatic)\.com[^>]*>\n?')
HEAD_PART = re.compile(r'^\s*((?:<title>.*?</title>\s*|<meta [^>]*>\s*|<style>.*?</style>\s*)+)', re.S)


def subset_font(path):
    from fontTools import subset
    from fontTools.ttLib import TTFont
    try:
        import brotli  # noqa: F401
        flavor, mime = "woff2", "font/woff2"
    except ImportError:
        flavor, mime = "woff", "font/woff"
    font = TTFont(str(path))
    opts = subset.Options()
    opts.flavor = flavor
    opts.layout_features = ["kern", "liga", "calt", "tnum", "case"]
    opts.name_IDs = ["*"]
    opts.notdef_outline = True
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=UNICODES)
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = flavor
    font.save(buf)
    return mime, flavor, buf.getvalue()


def font_block(font_dir):
    if str(font_dir) == "-":
        return "", 0
    faces, total = [], 0
    for family, weight, name in FACES:
        path = font_dir / name
        if not path.exists():
            print(f"warning: {path} not found; this face falls back to system fonts")
            continue
        mime, flavor, data = subset_font(path)
        total += len(data)
        uri = f"data:{mime};base64,{base64.b64encode(data).decode('ascii')}"
        faces.append(f'@font-face {{ font-family: "{family}"; font-weight: {weight}; font-style: normal; font-display: swap; src: url("{uri}") format("{flavor}"); }}')
    if not faces:
        sys.exit(f"error: none of {[f[2] for f in FACES]} found in {font_dir}; pass '-' to build without fonts")
    style = (
        "<style>\n/* Inter (c) The Inter Project Authors, JetBrains Mono (c) The JetBrains Mono Project Authors;"
        " both SIL Open Font License 1.1, subset and embedded so the page needs no network. */\n"
        + "\n".join(faces) + "\n</style>\n"
    )
    return style, total


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page")
    ap.add_argument("font_dir")
    ap.add_argument("out")
    ap.add_argument("--lang", default="tr")
    ap.add_argument("--test-hook", action="store_true")
    args = ap.parse_args()
    page = WEB_FONT_LINK.sub("", Path(args.page).read_text(encoding="utf-8"))
    head_extra = ""
    m = HEAD_PART.match(page)
    if m:  # title, metas and the page's own style block belong in <head>
        head_extra, page = m.group(1), page[m.end():]
    style, total = font_block(Path(args.font_dir))
    if args.test_hook:
        page = page.replace('"meta":{', '"meta":{"testHook":true,', 1)
    doc = (
        f'<!doctype html>\n<html lang="{args.lang}">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + style + head_extra + "</head>\n<body>\n" + page + "\n</body>\n</html>\n"
    )
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    print({"fonts_bytes": total, "html_bytes": len(doc.encode("utf-8")), "network_refs": "fonts.googleapis" in doc,
           "head_moved": bool(head_extra), "test_hook": args.test_hook})


if __name__ == "__main__":
    main()
