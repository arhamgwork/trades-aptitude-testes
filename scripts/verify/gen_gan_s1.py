# -*- coding: utf-8 -*-
"""GAN battery Form B — Section 1, Numerical Computation (25 items).

Fractions, decimals, percents and signed numbers, worked by hand. Every key is
computed with exact rational arithmetic and asserted.
"""
import sys, os
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(__file__))
from common import Item

S = "s1"
items = []
def add(*a, **k): items.append(Item(*a, **k))

def mixed(fr):
    """Format a Fraction the way a test booklet writes it."""
    if fr.denominator == 1:
        return str(fr.numerator)
    whole, rem = divmod(abs(fr.numerator), fr.denominator)
    sign = "-" if fr < 0 else ""
    if whole:
        return f"{sign}{whole} {rem}/{fr.denominator}"
    return f"{sign}{rem}/{fr.denominator}"

# ---- fraction addition / subtraction ---------------------------------------
for n, (a, b, op) in enumerate([
    (F(5, 8), F(3, 16), '+'), (F(7, 12), F(1, 4), '-'),
    (F(2, 3), F(3, 5), '+'), (F(15, 16), F(5, 8), '-'),
], start=1):
    key = a + b if op == '+' else a - b
    assert key == (a + b if op == '+' else a - b)
    wrong_den = F(a.numerator + b.numerator, a.denominator + b.denominator) if op == '+' \
        else F(abs(a.numerator - b.numerator), abs(a.denominator - b.denominator) or 1)
    flipped = b - a if op == '-' else None
    cands = [(wrong_den, "added the numerators and the denominators straight across instead of finding a common denominator")]
    if op == '-':
        cands.append((flipped, "subtracted in the wrong order"))
        cands.append((a + b, "added instead of subtracted"))
    else:
        cands.append((a - b, "subtracted instead of added"))
        cands.append((a * b, "multiplied instead of added"))
    seen = {mixed(key)}
    picked = []
    for v, note in cands:
        if mixed(v) in seen:
            continue
        seen.add(mixed(v))
        picked.append((v, note))
    while len(picked) < 3:
        cand = key + F(1, a.denominator * 2 * len(picked) + 2)
        if mixed(cand) not in seen:
            seen.add(mixed(cand))
            picked.append((cand, "used a common denominator but converted one of the fractions wrongly"))
    add(f"ganb-s1-{n:03d}", S, ["arith.fractions"],
        f"{mixed(a)} {op} {mixed(b)} = ?", key, picked[:3],
        f"The common denominator is {(a.denominator * b.denominator) // __import__('math').gcd(a.denominator, b.denominator)}. "
        f"Converting both fractions and {'adding' if op == '+' else 'subtracting'} the numerators gives {mixed(key)}.",
        "python:fractions", "medium", formatter=mixed)

# ---- multiply / divide fractions -------------------------------------------
for n, (a, b, op) in enumerate([
    (F(5, 2), F(16, 5), '*'), (F(5, 8), F(1, 4), '/'),
    (F(3, 4), F(2, 9), '*'), (F(7, 8), F(7, 16), '/'),
], start=5):
    key = a * b if op == '*' else a / b
    if op == '*':
        # The classic mixed-number error: multiply the whole parts and the
        # fraction parts separately instead of converting to improper first.
        w1, f1 = divmod(a, 1)
        w2, f2 = divmod(b, 1)
        separate = w1 * w2 + f1 * f2
        others = [(a / b, "inverted the second fraction and divided instead of multiplying"),
                  (a + b, "added instead of multiplied"),
                  (separate, "multiplied the whole parts and the fraction parts separately instead of converting to improper fractions first")]
        expl = (f"Convert to improper fractions, then multiply numerators and "
                f"denominators straight across and cancel: the result is {mixed(key)}.")
    else:
        others = [(a * b, "multiplied without inverting the divisor"),
                  (b / a, "inverted the wrong fraction"),
                  (a - b, "subtracted instead of divided")]
        expl = (f"Invert the divisor and multiply: {mixed(a)} × {mixed(1/b)} = {mixed(key)}. "
                f"Dividing by a fraction smaller than one makes the result larger.")
    seen = {mixed(key)}
    picked = []
    for v, note in others:
        if mixed(v) in seen: continue
        seen.add(mixed(v)); picked.append((v, note))
    step = 1
    while len(picked) < 3:
        cand = key + F(step, max(a.denominator, b.denominator) * 2)
        step += 1
        if mixed(cand) in seen: continue
        seen.add(mixed(cand))
        picked.append((cand, "cancelled one factor too few before multiplying out"))
    add(f"ganb-s1-{n:03d}", S, ["arith.fractions"],
        f"{mixed(a)} {'×' if op == '*' else '÷'} {mixed(b)} = ?", key, picked[:3],
        expl, "python:fractions", "medium", formatter=mixed)

# ---- decimal <-> fraction ---------------------------------------------------
dec_pairs = [(F(3, 8), "0.375"), (F(5, 16), "0.3125"), (F(7, 8), "0.875"), (F(9, 16), "0.5625")]
for n, (fr, dec) in enumerate(dec_pairs, start=9):
    assert abs(float(fr) - float(dec)) < 1e-12
    wrong = [F(3, 4), F(1, 3), F(5, 8), F(1, 2), F(11, 16), F(7, 16), F(1, 4)]
    others = []
    for w in wrong:
        if w == fr or len(others) == 3: continue
        note = ("read the decimal as a more familiar fraction without checking the division"
                if w.denominator <= 4 else
                "picked a neighbouring sixteenth, which differs in the third decimal place")
        others.append((w, note))
    add(f"ganb-s1-{n:03d}", S, ["arith.decimals", "arith.fractions"],
        f"Which fraction is equal to {dec}?", fr, others,
        f"Dividing the numerator by the denominator gives {dec} exactly. "
        f"The eighths and sixteenths are worth memorising, since they come up constantly on layout work.",
        "python:fractions", "medium", formatter=mixed)

# ---- percents ---------------------------------------------------------------
pct_items = [
    (F(15, 100), 340, "15% of 340"),
    (F(8, 100), 250, "8% of 250"),
    (F(125, 1000), 96, "12.5% of 96"),
    (F(6, 100), 450, "6% of 450"),
]
for n, (p, base, label) in enumerate(pct_items, start=13):
    key = p * base
    others = [(p * base * 10, "moved the decimal point one place the wrong way"),
              (F(base, 1) * p / 10, "took a tenth of the correct percentage"),
              (base - p * base, "found what is left after taking the percentage instead of the percentage itself")]
    seen = {mixed(key)}; picked = []
    for v, note in others:
        if mixed(v) in seen: continue
        seen.add(mixed(v)); picked.append((v, note))
    add(f"ganb-s1-{n:03d}", S, ["arith.percent"],
        f"What is {label}?", key, picked[:3],
        f"A percent is a count out of 100, so {label} is {float(p)} × {base} = {mixed(key)}.",
        "python:fractions", "medium", formatter=mixed)

# ---- percent of / what percent ----------------------------------------------
for n, (part, whole) in enumerate([(18, 45), (21, 84), (36, 144), (27, 60)], start=17):
    key = F(part, whole) * 100
    others = [(F(whole, part) * 100, "divided the larger number by the smaller instead of part by whole"),
              (F(part, whole) * 10, "lost a factor of ten when converting to a percentage"),
              (whole - part, "reported the difference instead of a percentage")]
    seen = {mixed(key)}; picked = []
    for v, note in others:
        if mixed(v) in seen: continue
        seen.add(mixed(v)); picked.append((v, note))
    add(f"ganb-s1-{n:03d}", S, ["arith.percent"],
        f"{part} is what percent of {whole}?", key, picked[:3],
        f"Divide the part by the whole and multiply by 100: {part} ÷ {whole} = "
        f"{F(part, whole)}, which is {mixed(key)}%.",
        "python:fractions", "medium", formatter=lambda v: f"{mixed(v)}%")

# ---- signed numbers ----------------------------------------------------------
signed = [
    (-8, 3, '+', "Adding a positive to a negative moves toward zero"),
    (-12, -5, '-', "Subtracting a negative is the same as adding its opposite"),
    (-6, -7, '*', "A negative times a negative is positive"),
    (-45, 9, '/', "A negative divided by a positive is negative"),
]
for n, (a, b, op, hint) in enumerate(signed, start=21):
    key = {'+': a + b, '-': a - b, '*': a * b, '/': F(a, b)}[op]
    wrongs = {
        '+': [(a - b, "subtracted instead of added"), (abs(a) + b, "dropped the sign on the first number"),
              (abs(a) - b, "worked with sizes only and then lost the sign")],
        '-': [(a + b, "added the negative instead of subtracting it"),
              (-(abs(a) + abs(b)), "treated the double negative as a single negative"),
              (b - a, "subtracted in the wrong order")],
        '*': [(-(abs(a) * abs(b)), "kept a negative sign that two negatives cancel"),
              (a + b, "added instead of multiplied"), (abs(a) - abs(b), "subtracted the sizes")],
        '/': [(abs(F(a, b)), "dropped the negative sign"), (F(b, a), "divided in the wrong order"),
              (a * b, "multiplied instead of divided")],
    }[op]
    symbol = {'+': '+', '-': '−', '*': '×', '/': '÷'}[op]
    bstr = f"({b})" if b < 0 else str(b)
    seen = {mixed(F(key))}; picked = []
    for v, note in wrongs:
        vf = F(v)
        if mixed(vf) in seen: continue
        seen.add(mixed(vf)); picked.append((vf, note))
    step = 1
    while len(picked) < 3:
        cand = F(key) + step
        step += 1
        if mixed(cand) in seen: continue
        seen.add(mixed(cand)); picked.append((cand, "carried the sign correctly but slipped by one on the arithmetic"))
    add(f"ganb-s1-{n:03d}", S, ["arith.signed"],
        f"{a} {symbol} {bstr} = ?", F(key), picked[:3],
        f"{hint}, so the result is {mixed(F(key))}.",
        "python:fractions", "medium", formatter=mixed)

# ---- one order-of-operations item --------------------------------------------
val = 4 + 3 * (10 - 6)
assert val == 16
add("ganb-s1-025", S, ["arith.order"],
    "4 + 3 × (10 − 6) = ?", val,
    [((4 + 3) * (10 - 6), "worked left to right instead of doing the multiplication first"),
     (4 + 3 * (10 + 6), "added inside the brackets instead of subtracting"),
     (4 + 3 + (10 - 6), "added instead of multiplying")],
    "Brackets first: 10 − 6 = 4. Then multiplication before addition: "
    "3 × 4 = 12, and 4 + 12 = 16.", "python:fractions", "easy")

if __name__ == "__main__":
    assert len(items) == 25, f"expected 25, got {len(items)}"
    print(f"GAN Form B section 1 (Numerical Computation): {len(items)} items verified")
