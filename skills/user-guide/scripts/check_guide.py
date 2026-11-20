"""Check an interactive user guide that follows the user-guide skill's content model.

Usage: python -I -X utf8 check_guide.py --src <guide src dir> --dist <guide dist dir>
                                        --base <base-language content file, e.g. content.tr.js or content.js>
                                        [--icons <dist>/assets/icons.js]

Content files: the base-language file given by --base and every other content.<lang>.js in --src.
The checks are heuristic (regular expressions over the JS data):
  1. section/subsection ids are unique; a translation may miss ids (warning: it falls back to the
     base language) but may not add ids the base language does not have (error);
  2. every in-guide link href="#id" points to an existing id (or to a known page anchor);
  3. every picture('name', ...) and every name inside pictures([...]) exists as
     assets/img[/<lang>]/<name>-dark.png, <name>-light.png, <name>.png, .svg or .jpg;
  4. every icon: 'name' exists in icons.js (window.ICONS keys).
Exit code 1 when an error is found; 2 on wrong usage.
"""
import argparse
import re
import sys
from pathlib import Path

ID_RE = re.compile(r"""\bid\s*:\s*['"]([A-Za-z0-9_-]+)['"]""")
LINK_RE = re.compile(r"""href=\\?["']#([A-Za-z0-9_-]+)""")
PIC_RE = re.compile(r"""\bpicture\(\s*['"]([A-Za-z0-9_.-]+)['"]""")
PICS_START_RE = re.compile(r"""\bpictures\(""")
PICS_NAME_RE = re.compile(r"""\[\s*['"]([A-Za-z0-9_.-]+)['"]""")
ICON_RE = re.compile(r"""\bicon\s*:\s*['"]([A-Za-z0-9_-]+)['"]""")
ICONS_KEY_RE = re.compile(r"""["']([a-z0-9-]+)["']\s*:""")
PAGE_ANCHORS = {"top", "chapters", "toc", "search"}
HELPER_PARAMS = {"ad", "name", "img", "src"}


def pictures_blocks(text):
    """Yield the argument text of every pictures( ... ) call, balancing parentheses."""
    for m in PICS_START_RE.finditer(text):
        depth, i = 1, m.end()
        while i < len(text) and depth:
            depth += {"(": 1, ")": -1}.get(text[i], 0)
            i += 1
        yield text[m.end():i - 1]


def lang_of(name, base):
    if name == base:
        return ""
    m = re.match(r"content\.([a-z]{2}(?:-[A-Za-z]{2})?)\.js$", name)
    return m.group(1) if m else None


def image_exists(img_dir, name):
    return any((img_dir / f"{name}{s}").exists() for s in ("-dark.png", "-light.png", ".png", ".svg", ".jpg"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--dist", required=True)
    ap.add_argument("--base", required=True, help="base-language content file name, e.g. content.tr.js")
    ap.add_argument("--icons")
    args = ap.parse_args()
    src, dist = Path(args.src), Path(args.dist)
    if not (src / args.base).exists():
        print(f"error: base content file {src / args.base} not found")
        sys.exit(2)
    errors, warnings, ids_by_lang, texts = [], [], {}, {}
    for f in sorted(src.glob("content*.js")):
        lang = lang_of(f.name, args.base)
        if lang is None:
            continue
        text = f.read_text(encoding="utf-8")
        texts[lang] = text
        ids = ID_RE.findall(text)
        dup = sorted({i for i in ids if ids.count(i) > 1})
        if dup:
            errors.append(f"{f.name}: duplicate ids {dup}")
        ids_by_lang[lang] = set(ids)
    base_ids = ids_by_lang.get("", set())
    for lang, ids in ids_by_lang.items():
        if not lang:
            continue
        missing, extra = sorted(base_ids - ids), sorted(ids - base_ids)
        if missing:
            warnings.append(f"[{lang}] ids missing in translation (falls back to base language): {missing[:20]}")
        if extra:
            errors.append(f"[{lang}] ids not in base language: {extra[:20]}")
    all_ids = set().union(*ids_by_lang.values()) | PAGE_ANCHORS
    for lang, text in texts.items():
        tag = lang or "base"
        for target in sorted(set(LINK_RE.findall(text))):
            if target not in all_ids:
                errors.append(f"[{tag}] link #{target} has no target id")
        names = set(PIC_RE.findall(text))
        for block in pictures_blocks(text):
            names |= set(PICS_NAME_RE.findall(block))
        img_dir = dist / "assets" / "img" / lang if lang else dist / "assets" / "img"
        for name in sorted(names - HELPER_PARAMS):
            if not image_exists(img_dir, name):
                errors.append(f"[{tag}] image '{name}' not found in {img_dir}")
    icons_file = Path(args.icons) if args.icons else dist / "assets" / "icons.js"
    if icons_file.exists():
        keys = set(ICONS_KEY_RE.findall(icons_file.read_text(encoding="utf-8")))
        for lang, text in texts.items():
            for icon in sorted(set(ICON_RE.findall(text))):
                if icon not in keys:
                    errors.append(f"[{lang or 'base'}] icon '{icon}' not in {icons_file.name}")
    else:
        warnings.append(f"icons file not found: {icons_file}")
    print(f"languages: {', '.join(sorted(l or 'base' for l in ids_by_lang))}; ids in base: {len(base_ids)}")
    for w in warnings:
        print("warning:", w)
    for e in errors:
        print("error:", e)
    if errors:
        sys.exit(1)
    print("ok")


if __name__ == "__main__":
    main()
