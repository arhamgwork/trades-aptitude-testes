# -*- coding: utf-8 -*-
"""Independently re-derives migrated answer keys where the item is computable.

Migration fidelity is already proven (the migrated key matches the source key).
This is the separate question the brief asks: is that key actually *right*?
Nothing here reads the key before computing; the computed value is compared
with the keyed choice afterwards, and disagreements are reported, never
silently corrected.
"""
import json, os, re, sys
from fractions import Fraction as F

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
FILES = [
    "data/pipefitting/ua-597-formA.json",
    "data/plumbing/ua-130-formA.json",
    "data/elevator/eiat-formA.json",
    "data/drills/sign-analysis.json",
]

NUM = r"(?:\d+\s+\d+/\d+|\d+/\d+|\d+(?:\.\d+)?)"

def parse_num(t):
    """Parse '2 1/2', '5/8', '0.375' or '42' as an exact Fraction."""
    t = t.strip().replace(",", "")
    m = re.fullmatch(r"(\d+)\s+(\d+)/(\d+)", t)
    if m:
        w, n, d = map(int, m.groups())
        return F(w) + F(n, d)
    m = re.fullmatch(r"(\d+)/(\d+)", t)
    if m:
        return F(int(m.group(1)), int(m.group(2)))
    m = re.fullmatch(r"(\d+)(?:\.(\d+))?", t)
    if m:
        return F(t)
    return None

def choice_values(choices):
    """Every choice parsed as a number where possible, else None."""
    out = []
    for c in choices:
        c = re.sub(r"[^0-9/.\s]", "", str(c)).strip()
        c = re.sub(r"\s+", " ", c)
        out.append(parse_num(c))
    return out

OPS = {"+": lambda a, b: a + b, "−": lambda a, b: a - b, "-": lambda a, b: a - b,
       "×": lambda a, b: a * b, "*": lambda a, b: a * b,
       "÷": lambda a, b: (a / b if b else None), "/": None}

def derive(stem):
    """Return the computed answer for a stem we recognise, else None."""
    s = " ".join(str(stem).split())

    # A op B = ?
    m = re.fullmatch(rf"({NUM})\s*([+−×÷])\s*({NUM})\s*=\s*\??", s)
    if m:
        a, op, b = parse_num(m.group(1)), m.group(2), parse_num(m.group(3))
        if a is not None and b is not None and OPS.get(op):
            return OPS[op](a, b)

    # What is P% of N?
    m = re.fullmatch(rf"What is ({NUM})\s*% of ({NUM})\s*\?", s, re.I)
    if m:
        p, n = parse_num(m.group(1)), parse_num(m.group(2))
        if p is not None and n is not None:
            return p / 100 * n

    # N is what percent of M?
    m = re.fullmatch(rf"({NUM}) is what percent of ({NUM})\s*\?", s, re.I)
    if m:
        a, b = parse_num(m.group(1)), parse_num(m.group(2))
        if a is not None and b is not None and b:
            return a / b * 100

    # Next number in an arithmetic or geometric series
    m = re.search(r"([\d,]+(?:\s*,\s*[\d,]+){2,})\s*,\s*(?:\?|__|_)", s)
    if m:
        try:
            terms = [int(x.strip()) for x in m.group(1).split(",") if x.strip()]
        except ValueError:
            terms = []
        if len(terms) >= 3:
            d = [terms[i + 1] - terms[i] for i in range(len(terms) - 1)]
            if len(set(d)) == 1:
                return F(terms[-1] + d[0])
            if all(terms[i] and terms[i + 1] % terms[i] == 0 for i in range(len(terms) - 1)):
                r = {terms[i + 1] // terms[i] for i in range(len(terms) - 1)}
                if len(r) == 1:
                    return F(terms[-1] * r.pop())
    return None

def main():
    total = checked = agreed = 0
    mismatches = []
    per_file = {}
    for rel in FILES:
        path = os.path.join(ROOT, rel)
        exam = json.load(open(path, encoding="utf-8"))
        n_checked = n_agreed = 0
        for q in exam["questions"]:
            total += 1
            if q.get("choicesAreFigures"):
                continue
            want = derive(q["stem"])
            if want is None:
                continue
            vals = choice_values(q["choices"])
            if vals[q["correctIndex"]] is None:
                continue
            # The computed value must match exactly one choice, and it must be the key.
            hits = [i for i, v in enumerate(vals) if v is not None and v == want]
            if len(hits) != 1:
                continue
            checked += 1
            n_checked += 1
            if hits[0] == q["correctIndex"]:
                agreed += 1
                n_agreed += 1
                q["verify"] = "python:recomputed"
            else:
                mismatches.append((exam["id"], q["id"], q["stem"],
                                   q["choices"][q["correctIndex"]], q["choices"][hits[0]]))
        per_file[exam["id"]] = (n_checked, n_agreed, len(exam["questions"]))
        if "--write" in sys.argv and not mismatches:
            json.dump(exam, open(path, "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)
    print(f"migrated items scanned: {total}")
    print(f"independently recomputed: {checked}")
    print(f"agreed with the migrated key: {agreed}")
    for k, (c, a, n) in per_file.items():
        print(f"  {k}: {a}/{c} agreed, of {n} items ({100*c/n:.0f}% computable)")
    if mismatches:
        print(f"\nMISMATCHES ({len(mismatches)}) — key NOT corrected automatically:")
        for eid, qid, stem, keyed, computed in mismatches:
            print(f"  {eid} {qid}: {stem[:70]}")
            print(f"      keyed: {keyed}   computed: {computed}")
        return 1
    print("\nno disagreements")
    return 0

if __name__ == "__main__":
    sys.exit(main())
