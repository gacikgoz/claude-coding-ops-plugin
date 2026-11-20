"""Validate a decision-page seed before building it.

Usage: python -I -X utf8 validate_seed.py <seed.json>
Exit code 1 when an error is found, 2 on wrong usage. Checks: schema values, unique ids, known
groups, the "only what exists / Yok." rule for the implementation column, and banned wording.
"""
import json
import re
import sys
from pathlib import Path

KINDS = {"kept", "changed", "replaced", "removed", "partial", "incompatible", "new", "doc-drift", "pattern"}
POINT_STATUS = {"kept", "changed", "replaced", "removed", "partial", "incompatible", "new"}
ACTIONS = {"keep", "adopt", "adapt", "defer", "drop"}
IMPACTS = {"high", "medium", "low"}
PRIORITIES = {"P1", "P2", "P3", ""}
WHY_SOURCES = {"documented", "commit", "inferred", "none", ""}
# User preference: the term "invariant" (Turkish noun "değişmez") is not used; say rule/principle.
# Noun forms are errors; a bare "değişmez" may be a verb ("does not change") and is only a warning.
BANNED = re.compile(r"değişmezler|değişmezlik|degismezler|\binvariants?\b", re.IGNORECASE)
BARE = re.compile(r"değişmez|degismez", re.IGNORECASE)
# Signals of commentary in the implementation column instead of a plain statement of what exists.
COMMENTARY = re.compile(r"planlan|ertelen|yerine geç", re.IGNORECASE)


def main():
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(2)
    seed = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errors, warnings = [], []
    groups = {g["id"] for g in seed.get("groups", [])}
    seen = set()
    for it in seed.get("items", []):
        iid = it.get("id", "?")
        if iid in seen:
            errors.append(f"{iid}: duplicate id")
        seen.add(iid)
        if it.get("group") not in groups:
            errors.append(f"{iid}: unknown group {it.get('group')}")
        if it.get("kind") not in KINDS:
            errors.append(f"{iid}: kind {it.get('kind')}")
        if it.get("impact") not in IMPACTS:
            errors.append(f"{iid}: impact {it.get('impact')}")
        if it.get("priority", "") not in PRIORITIES:
            errors.append(f"{iid}: priority {it.get('priority')}")
        if it.get("recommended", "") not in ("spec", "current", "proposal", ""):
            errors.append(f"{iid}: recommended {it.get('recommended')}")
        for side in ("spec", "current", "proposal"):
            if not isinstance(it.get(side), dict) or not it[side].get("summary"):
                errors.append(f"{iid}: {side}.summary missing")
        cur = it.get("current") if isinstance(it.get("current"), dict) else {}
        if cur.get("whySource", "") not in WHY_SOURCES:
            errors.append(f"{iid}: current.whySource {cur.get('whySource')}")
        if it.get("kind") == "removed" and cur.get("summary", "").strip() != "Yok.":
            warnings.append(f"{iid}: kind removed but current.summary is not 'Yok.'")
        if COMMENTARY.search(cur.get("summary", "")):
            warnings.append(f"{iid}.current.summary reads like commentary")
        for i, p in enumerate(it.get("points", [])):
            status, current = p.get("status"), (p.get("current") or "").strip()
            if status not in POINT_STATUS:
                errors.append(f"{iid}.points[{i}]: status {status}")
            if p.get("action") not in ACTIONS:
                errors.append(f"{iid}.points[{i}]: action {p.get('action')}")
            if status == "removed" and current != "Yok.":
                errors.append(f"{iid}.points[{i}]: status removed but current is not 'Yok.'")
            if current == "Yok." and status not in ("removed", None):
                errors.append(f"{iid}.points[{i}]: current is 'Yok.' but status is {status}")
            if not current:
                errors.append(f"{iid}.points[{i}]: current is empty (write what exists or 'Yok.')")
            if COMMENTARY.search(current):
                warnings.append(f"{iid}.points[{i}].current reads like commentary: {current[:100]}")

    def walk(o, path):
        if isinstance(o, str):
            if BANNED.search(o):
                errors.append(f"{path}: banned term")
            elif BARE.search(o):
                warnings.append(f"{path}: 'değişmez' — reword as 'değiştirilmez' if it is a verb")
        elif isinstance(o, dict):
            for k, v in o.items():
                walk(v, f"{path}.{k}")
        elif isinstance(o, list):
            for j, v in enumerate(o):
                walk(v, f"{path}[{j}]")

    walk(seed, "seed")
    points = sum(len(it.get("points", [])) for it in seed.get("items", []))
    print(f"items {len(seed.get('items', []))}, points {points}, groups {len(groups)}")
    for w in warnings[:30]:
        print("warning:", w)
    if len(warnings) > 30:
        print(f"warning: {len(warnings) - 30} more")
    for e in errors[:60]:
        print("error:", e)
    if errors:
        print(f"{len(errors)} errors")
        sys.exit(1)
    print("ok")


if __name__ == "__main__":
    main()
