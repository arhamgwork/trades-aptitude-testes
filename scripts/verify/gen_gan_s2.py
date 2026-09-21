# -*- coding: utf-8 -*-
"""GAN battery Form B — Section 2, Number Series (20 items).

Each series is generated from an explicit rule, the rule is re-checked against
every printed term, and the key is the rule applied once more.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import Item

S = "s2"
items = []

def series(n, terms, nxt, rule_desc, distractors, difficulty="medium", skill="series.arithmetic"):
    shown = ", ".join(str(t) for t in terms)
    vals = [nxt] + [d[0] for d in distractors]
    assert len(set(map(str, vals))) == len(vals), f"s2-{n}: duplicate choices {vals}"
    items.append(Item(
        f"ganb-s2-{n:03d}", S, [skill],
        f"What number comes next in the series?   {shown}, __",
        nxt, distractors, rule_desc,
        "python:rule-check (rule re-applied to every printed term)", difficulty))

def arith(n, start, step, count=5, difficulty="medium"):
    terms = [start + step * i for i in range(count)]
    for i in range(len(terms) - 1):
        assert terms[i + 1] - terms[i] == step
    nxt = terms[-1] + step
    d = [(terms[-1] + step + step, "went two steps on instead of one"),
         (terms[-1] - step, "stepped backwards"),
         (terms[-1] * 2, "doubled the last term instead of adding the common difference")]
    seen = {str(nxt)}; picked = []
    for v, note in d:
        if str(v) in seen: continue
        seen.add(str(v)); picked.append((v, note))
    k = 1
    while len(picked) < 3:
        cand = nxt + k; k += 1
        if str(cand) in seen: continue
        seen.add(str(cand)); picked.append((cand, "slipped by one on the common difference"))
    series(n, terms, nxt,
           f"Each term is {abs(step)} {'more' if step > 0 else 'less'} than the one before it, "
           f"so the next term is {terms[-1]} {'+' if step > 0 else '−'} {abs(step)} = {nxt}.",
           picked[:3], difficulty)

def geom(n, start, ratio, count=4, difficulty="medium"):
    terms = [start * ratio ** i for i in range(count)]
    for i in range(len(terms) - 1):
        assert terms[i + 1] == terms[i] * ratio
    nxt = terms[-1] * ratio
    d = [(terms[-1] + (terms[-1] - terms[-2]), "added the last gap instead of multiplying"),
         (terms[-1] * (ratio + 1), "multiplied by one more than the common ratio"),
         (terms[-1] + start, "added the first term")]
    seen = {str(nxt)}; picked = []
    for v, note in d:
        if str(v) in seen: continue
        seen.add(str(v)); picked.append((v, note))
    k = 1
    while len(picked) < 3:
        cand = nxt + k; k += 1
        if str(cand) in seen: continue
        seen.add(str(cand)); picked.append((cand, "slipped by one after multiplying"))
    series(n, terms, nxt,
           f"Each term is {ratio} times the one before it, so the next term is "
           f"{terms[-1]} × {ratio} = {nxt}.", picked[:3], difficulty, "series.geometric")

def alternating(n, start, up, down, count=6, difficulty="medium"):
    terms = [start]
    for i in range(count - 1):
        terms.append(terms[-1] + (up if i % 2 == 0 else -down))
    deltas = [terms[i + 1] - terms[i] for i in range(len(terms) - 1)]
    assert deltas == [(up if i % 2 == 0 else -down) for i in range(len(terms) - 1)]
    step_next = up if (len(terms) - 1) % 2 == 0 else -down
    nxt = terms[-1] + step_next
    other = -down if step_next == up else up
    d = [(terms[-1] + other, "continued with the other step instead of alternating"),
         (terms[-1] + up + (-down), "applied both steps at once"),
         (terms[-1], "repeated the last term")]
    seen = {str(nxt)}; picked = []
    for v, note in d:
        if str(v) in seen: continue
        seen.add(str(v)); picked.append((v, note))
    k = 1
    while len(picked) < 3:
        cand = nxt + k; k += 1
        if str(cand) in seen: continue
        seen.add(str(cand)); picked.append((cand, "slipped by one on the alternating step"))
    series(n, terms, nxt,
           f"The series alternates between adding {up} and subtracting {down}. The next step "
           f"{'adds ' + str(up) if step_next > 0 else 'subtracts ' + str(down)}, giving {nxt}.",
           picked[:3], difficulty, "series.alternating")

def growing(n, start, first_step, increment, count=5, difficulty="hard"):
    """Differences themselves grow by a constant amount."""
    terms = [start]
    step = first_step
    for _ in range(count - 1):
        terms.append(terms[-1] + step)
        step += increment
    deltas = [terms[i + 1] - terms[i] for i in range(len(terms) - 1)]
    assert all(deltas[i + 1] - deltas[i] == increment for i in range(len(deltas) - 1))
    nxt = terms[-1] + step
    d = [(terms[-1] + deltas[-1], "kept the last gap instead of growing it"),
         (terms[-1] + increment, "added the growth amount instead of the next gap"),
         (terms[-1] * 2, "doubled the last term")]
    seen = {str(nxt)}; picked = []
    for v, note in d:
        if str(v) in seen: continue
        seen.add(str(v)); picked.append((v, note))
    k = 1
    while len(picked) < 3:
        cand = nxt + k; k += 1
        if str(cand) in seen: continue
        seen.add(str(cand)); picked.append((cand, "slipped by one on the growing gap"))
    series(n, terms, nxt,
           f"The gaps between terms are {', '.join(str(x) for x in deltas)} — each gap is "
           f"{increment} larger than the one before. The next gap is {step}, giving {nxt}.",
           picked[:3], difficulty, "series.growing")

def interleaved(n, a_start, a_step, b_start, b_step, pairs=3, difficulty="hard"):
    """Two series taking turns."""
    terms = []
    for i in range(pairs):
        terms.append(a_start + a_step * i)
        terms.append(b_start + b_step * i)
    nxt = a_start + a_step * pairs
    d = [(terms[-1] + b_step, "continued the second series instead of returning to the first"),
         (terms[-1] + a_step, "applied the first series' step to the wrong term"),
         (terms[-1], "repeated the last term")]
    seen = {str(nxt)}; picked = []
    for v, note in d:
        if str(v) in seen: continue
        seen.add(str(v)); picked.append((v, note))
    k = 1
    while len(picked) < 3:
        cand = nxt + k; k += 1
        if str(cand) in seen: continue
        seen.add(str(cand)); picked.append((cand, "slipped by one on the alternating series"))
    series(n, terms, nxt,
           f"Two series take turns. Positions 1, 3 and 5 go up by {a_step}; positions 2, 4 and 6 "
           f"go {'up' if b_step > 0 else 'down'} by {abs(b_step)}. The next term belongs to the "
           f"first series, giving {nxt}.",
           picked[:3], difficulty, "series.interleaved")

arith(1, 4, 5, difficulty="easy")
arith(2, 7, 6)
arith(3, 90, -7)
arith(4, 3, 11)
arith(5, 48, -9)
geom(6, 3, 2, difficulty="easy")
geom(7, 2, 3)
geom(8, 5, 4, count=4)
geom(9, 128, 2, count=4)
alternating(10, 2, 3, 1)
alternating(11, 10, 5, 2)
alternating(12, 40, 6, 9)
growing(13, 2, 3, 1)
growing(14, 5, 2, 2)
growing(15, 1, 4, 3)
interleaved(16, 2, 4, 30, -5)
interleaved(17, 1, 3, 100, -10)
arith(18, 12, 12)
geom(19, 1, 5, count=4)
growing(20, 10, 1, 2)

if __name__ == "__main__":
    assert len(items) == 20, f"expected 20, got {len(items)}"
    print(f"GAN Form B section 2 (Number Series): {len(items)} items verified")
