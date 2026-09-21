# -*- coding: utf-8 -*-
"""Builds the variable-relationship drill set: 60 items, 15 per sub-type.

No key is typed by hand. Inequality and if-then keys come from enumeration,
sufficiency keys from a search over both statements, symbolic keys from direct
evaluation, and every distractor is reproduced from the mistake it names.
"""
import sys, os
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(__file__))
from varrel_lib import (models, classify, truth_models, sufficiency,
                        SUFF_CHOICES, SUFF_INDEX, SUFF_NOTES)
from common import Item

items = []

# ============================================================ 1. inequality chains
def ineq(n, intro, varnames, constraints, asked, candidates, difficulty="medium"):
    """candidates: list of (text, lambda, note). Exactly one must match `asked`."""
    ms = models(varnames, constraints)
    cls = [(t, classify(ms, f), note) for t, f, note in candidates]
    keyed = [c for c in cls if c[1] == asked]
    assert len(keyed) == 1, f"varrel-ineq-{n}: {len(keyed)} choices classify as {asked}: {[(c[0], c[1]) for c in cls]}"
    key = keyed[0]
    others = [c for c in cls if c is not key]
    word = {"MUST": "MUST be true", "CANNOT": "CANNOT be true", "MIGHT": "MIGHT be true but is not guaranteed"}[asked]
    items.append(Item(
        f"varrel-ineq-{n:03d}", "varrel", ["varrel.inequality"],
        f"{intro}\nWhich statement {word}?",
        key[0], [(t, f"this one {('is only sometimes true' if c == 'MIGHT' else 'is never true')} under the stated relationships — {note}") for t, c, note in others],
        f"Checked against every assignment satisfying the constraints ({len(ms)} of them): "
        f"the stated relationship holds in {'all' if asked == 'MUST' else 'none' if asked == 'CANNOT' else 'some but not all'} of them.",
        f"python:exhaustive ({len(ms)} models)", difficulty, formatter=str))

gt = lambda a, b: (lambda e: e[a] > e[b])
ge = lambda a, b: (lambda e: e[a] >= e[b])
pos = lambda a: (lambda e: e[a] > 0)
neg = lambda a: (lambda e: e[a] < 0)
ne = lambda a, b: (lambda e: e[a] != e[b])

ineq(1, "Three gauge readings satisfy x > y, y > z, and z > 0.", ['x','y','z'],
     [gt('x','y'), gt('y','z'), pos('z')], "MUST",
     [("x > z", lambda e: e['x'] > e['z'], "the chain carries through"),
      ("x > 2z", lambda e: e['x'] > 2*e['z'], "doubling z is not supported by the chain"),
      ("x is negative", lambda e: e['x'] < 0, "everything above a positive z is positive"),
      ("y = z", lambda e: e['y'] == e['z'], "y is strictly greater than z")])

ineq(2, "Two lengths satisfy a ≤ b and b ≤ c.", ['a','b','c'],
     [lambda e: e['a'] <= e['b'], lambda e: e['b'] <= e['c']], "MUST",
     [("a ≤ c", lambda e: e['a'] <= e['c'], "≤ chains the same way > does"),
      ("a < c", lambda e: e['a'] < e['c'], "all three can be equal"),
      ("a ≠ c", lambda e: e['a'] != e['c'], "all three can be equal"),
      ("b is the largest of the three", lambda e: e['b'] >= e['a'] and e['b'] >= e['c'], "c can exceed b")])

ineq(3, "Readings satisfy p > q and q > 0.", ['p','q'],
     [gt('p','q'), pos('q')], "CANNOT",
     [("p ≤ 0", lambda e: e['p'] <= 0, "p exceeds a positive number, so it is positive"),
      ("p > 1", lambda e: e['p'] > 1, "this is sometimes true"),
      ("q < p", lambda e: e['q'] < e['p'], "this is always true, not never"),
      ("p − q > 0", lambda e: e['p'] - e['q'] > 0, "this is always true, not never")])

ineq(4, "Three values satisfy m > n and n < k.", ['m','n','k'],
     [gt('m','n'), lambda e: e['n'] < e['k']], "MIGHT",
     [("m > k", lambda e: e['m'] > e['k'], "m and k are only both above n, so either can be larger"),
      ("m > n", lambda e: e['m'] > e['n'], "this is stated outright, so it is guaranteed"),
      ("n < k", lambda e: e['n'] < e['k'], "this is stated outright, so it is guaranteed"),
      ("n > m", lambda e: e['n'] > e['m'], "this contradicts the first relationship")])

ineq(5, "Two readings satisfy r ≥ s and s ≥ r.", ['r','s'],
     [ge('r','s'), ge('s','r')], "MUST",
     [("r = s", lambda e: e['r'] == e['s'], "each is at least the other, so they are equal"),
      ("r > s", lambda e: e['r'] > e['s'], "the two constraints force equality, not strict order"),
      ("r and s are both positive", lambda e: e['r'] > 0 and e['s'] > 0, "both could be zero or negative"),
      ("r ≠ s", lambda e: e['r'] != e['s'], "the constraints force them equal")], "easy")

ineq(6, "Pressures satisfy a > 0, b < 0, and a > b.", ['a','b'],
     [pos('a'), neg('b'), gt('a','b')], "MUST",
     [("a − b > 0", lambda e: e['a'] - e['b'] > 0, "subtracting a negative increases the value"),
      ("a + b > 0", lambda e: e['a'] + e['b'] > 0, "the negative b can outweigh a"),
      ("a × b > 0", lambda e: e['a'] * e['b'] > 0, "a positive times a negative is negative"),
      ("a + b < 0", lambda e: e['a'] + e['b'] < 0, "a can outweigh b")])

ineq(7, "Values satisfy x > y and y > 0 and x < 4.", ['x','y'],
     [gt('x','y'), pos('y'), lambda e: e['x'] < 4], "CANNOT",
     [("y ≥ 4", lambda e: e['y'] >= 4, "y sits below x, which is below 4"),
      ("y < 2", lambda e: e['y'] < 2, "this is sometimes true"),
      ("x > 3", lambda e: e['x'] > 3, "this is sometimes true"),
      ("x − y > 0", lambda e: e['x'] - e['y'] > 0, "this is always true, not never")])

ineq(8, "Three values satisfy u > v, v > w, and u < 5.", ['u','v','w'],
     [gt('u','v'), gt('v','w'), lambda e: e['u'] < 5], "MUST",
     [("w < 5", lambda e: e['w'] < 5, "w sits below v, which sits below u, which is below 5"),
      ("w > 0", lambda e: e['w'] > 0, "nothing puts a floor under w"),
      ("u − w < 1", lambda e: e['u'] - e['w'] < 1, "the gap can be large"),
      ("v = 3", lambda e: e['v'] == 3, "v is not pinned to any single value")])

ineq(9, "Two readings satisfy c ≠ d and c > 0 and d > 0.", ['c','d'],
     [ne('c','d'), pos('c'), pos('d')], "MIGHT",
     [("c > d", lambda e: e['c'] > e['d'], "they differ, but which is larger is not stated"),
      ("c = d", lambda e: e['c'] == e['d'], "this contradicts the stated inequality"),
      ("c + d > 0", lambda e: e['c'] + e['d'] > 0, "two positives always sum to a positive"),
      ("c × d < 0", lambda e: e['c'] * e['d'] < 0, "two positives never multiply to a negative")])

ineq(10, "Values satisfy g ≥ h, h ≥ j, and g = j.", ['g','h','j'],
      [ge('g','h'), ge('h','j'), lambda e: e['g'] == e['j']], "MUST",
      [("h = g", lambda e: e['h'] == e['g'], "h is squeezed between two equal values"),
       ("h > g", lambda e: e['h'] > e['g'], "h cannot exceed g"),
       ("h < j", lambda e: e['h'] < e['j'], "h cannot fall below j"),
       ("g > j", lambda e: e['g'] > e['j'], "they are stated equal")], "hard")

ineq(11, "Values satisfy a > b, b > c, and a = 4.", ['a','b','c'],
      [gt('a','b'), gt('b','c'), lambda e: e['a'] == 4], "MUST",
      [("c < 4", lambda e: e['c'] < 4, "c sits two steps below a fixed 4"),
       ("c > 0", lambda e: e['c'] > 0, "nothing stops c being negative"),
       ("b = 3", lambda e: e['b'] == 3, "b is not pinned to one value"),
       ("c ≥ b", lambda e: e['c'] >= e['b'], "this reverses the stated order")])

ineq(12, "Readings satisfy x < 0 and y < 0.", ['x','y'],
      [neg('x'), neg('y')], "MUST",
      [("x × y > 0", lambda e: e['x']*e['y'] > 0, "a negative times a negative is positive"),
       ("x + y > 0", lambda e: e['x']+e['y'] > 0, "two negatives always sum to a negative"),
       ("x > y", lambda e: e['x'] > e['y'], "their order is not stated"),
       ("x × y < 0", lambda e: e['x']*e['y'] < 0, "two negatives multiply to a positive")], "easy")

ineq(13, "Values satisfy p ≥ 0, q > p, and q < 2.", ['p','q'],
      [lambda e: e['p'] >= 0, gt('q','p'), lambda e: e['q'] < 2], "CANNOT",
      [("p ≥ 2", lambda e: e['p'] >= 2, "p sits below q, which is below 2"),
       ("p = 0", lambda e: e['p'] == 0, "this is sometimes true"),
       ("q > 1", lambda e: e['q'] > 1, "this is sometimes true"),
       ("q − p > 0", lambda e: e['q']-e['p'] > 0, "this is always true, not never")])

ineq(14, "Three values satisfy k > m, m > n, and k − n = 1.", ['k','m','n'],
      [gt('k','m'), gt('m','n'), lambda e: e['k']-e['n'] == 1], "MUST",
      [("k − m < 1", lambda e: e['k']-e['m'] < 1, "m sits strictly inside a gap of exactly 1"),
       ("k − m = 1", lambda e: e['k']-e['m'] == 1, "that would put m at n, but m is above n"),
       ("m − n > 1", lambda e: e['m']-e['n'] > 1, "the whole span is only 1"),
       ("k = n", lambda e: e['k'] == e['n'], "they differ by exactly 1")], "hard")

ineq(15, "Values satisfy w > 0 and w > z.", ['w','z'],
      [pos('w'), gt('w','z')], "MIGHT",
      [("z is negative", lambda e: e['z'] < 0, "z sits below a positive w, but can still be positive itself"),
       ("z > w", lambda e: e['z'] > e['w'], "this contradicts the stated order"),
       ("w > z", lambda e: e['w'] > e['z'], "this is stated outright, so it is guaranteed"),
       ("w ≤ 0", lambda e: e['w'] <= 0, "w is stated positive")])

# ============================================================ 2. sufficiency
def suff(n, question, t1, t2, target, varnames, difficulty="medium"):
    """t1/t2 are (text, lambda). The key comes from the enumeration."""
    verdict = sufficiency(target, t1[1], t2[1], varnames)
    assert verdict in SUFF_INDEX, f"varrel-suff-{n}: ambiguous verdict {verdict}"
    ki = SUFF_INDEX[verdict]
    key = SUFF_CHOICES[ki]
    others = [(c, SUFF_NOTES[i]) for i, c in enumerate(SUFF_CHOICES) if i != ki]
    items.append(Item(
        f"varrel-suff-{n:03d}", "varrel", ["varrel.sufficiency"],
        f"{question}\n  (1) {t1[0]}\n  (2) {t2[0]}",
        key, others,
        "Decided by working out which values survive each statement alone and then both "
        "together. A statement is sufficient only when exactly one value of the quantity "
        "asked about remains.",
        "python:exhaustive (all assignments over the search range enumerated)",
        difficulty, formatter=str))

suff(1, "What is the value of a?", ("a + b = 10", lambda e: e['a']+e['b'] == 10),
     ("b = 4", lambda e: e['b'] == 4), lambda e: e['a'], ['a','b'])
suff(2, "What is the value of x?", ("x = 7", lambda e: e['x'] == 7),
     ("x + y > 0", lambda e: e['x']+e['y'] > 0), lambda e: e['x'], ['x','y'])
suff(3, "What is the value of m?", ("m > 3", lambda e: e['m'] > 3),
     ("m < 6", lambda e: e['m'] < 6), lambda e: e['m'], ['m'])
suff(4, "What is the value of p?", ("2p = 9", lambda e: 2*e['p'] == 9),
     ("p is positive", lambda e: e['p'] > 0), lambda e: e['p'], ['p'])
suff(5, "What is the value of c?", ("c − d = 2", lambda e: e['c']-e['d'] == 2),
     ("d = 5", lambda e: e['d'] == 5), lambda e: e['c'], ['c','d'])
suff(6, "What is the value of r?", ("r + s = 8", lambda e: e['r']+e['s'] == 8),
     ("r − s = 2", lambda e: e['r']-e['s'] == 2), lambda e: e['r'], ['r','s'])
suff(7, "What is the value of k?", ("k > 0", lambda e: e['k'] > 0),
     ("k < 10", lambda e: e['k'] < 10), lambda e: e['k'], ['k'])
suff(8, "What is the value of y?", ("3y = 12", lambda e: 3*e['y'] == 12),
     ("y + 1 = 5", lambda e: e['y']+1 == 5), lambda e: e['y'], ['y'])
suff(9, "What is the value of t?", ("t = u", lambda e: e['t'] == e['u']),
     ("u = 6", lambda e: e['u'] == 6), lambda e: e['t'], ['t','u'])
suff(10, "What is the value of g?", ("g + h = 7", lambda e: e['g']+e['h'] == 7),
      ("2g + 2h = 14", lambda e: 2*e['g']+2*e['h'] == 14), lambda e: e['g'], ['g','h'], "hard")
suff(11, "What is the value of n?", ("n is greater than 2 and less than 4", lambda e: 2 < e['n'] < 4),
      ("n is a whole number", lambda e: e['n'].denominator == 1), lambda e: e['n'], ['n'], "hard")
suff(12, "What is the value of v?", ("v × 2 = 11", lambda e: e['v']*2 == 11),
      ("v − 1 = 4.5", lambda e: e['v']-1 == F(9,2)), lambda e: e['v'], ['v'])
suff(13, "What is the value of a?", ("a = b + 3", lambda e: e['a'] == e['b']+3),
      ("b > 0", lambda e: e['b'] > 0), lambda e: e['a'], ['a','b'])
suff(14, "What is the value of w?", ("w + 2 = 9", lambda e: e['w']+2 == 9),
      ("w > 5", lambda e: e['w'] > 5), lambda e: e['w'], ['w'])
suff(15, "What is the value of z?", ("z + q = 4", lambda e: e['z']+e['q'] == 4),
      ("q + z = 4", lambda e: e['q']+e['z'] == 4), lambda e: e['z'], ['z','q'], "hard")

# ============================================================ 3. symbolic substitution
def sym(n, defn, expr_text, fn, distractors, explanation, difficulty="medium"):
    """distractors: list of (value, note). Key computed by fn()."""
    key = fn()
    vals = [key] + [d[0] for d in distractors]
    assert len(set(map(str, vals))) == len(vals), f"varrel-sym-{n}: duplicate values {vals}"
    items.append(Item(
        f"varrel-sym-{n:03d}", "varrel", ["varrel.symbolic"],
        f"{defn}\n{expr_text}",
        key, distractors, explanation,
        "python:substitution (evaluated directly; each distractor reproduced from its named error)",
        difficulty, formatter=str))

sym(1, "The operation a ▲ b means 2a − b.", "What is the value of (5 ▲ 3) ▲ 4?",
    lambda: 2*(2*5-3)-4,
    [(2*5-(2*3-4), "worked the operation from right to left instead of evaluating the bracket first"),
     (2*3-5, "reversed the two operands inside the bracket"),
     (2*5-3-4, "subtracted both numbers in one step instead of applying the operation twice")],
    "Evaluate the bracket first: doubling 5 and subtracting 3 gives 7. Then doubling 7 and subtracting 4 gives 10.")

sym(2, "The operation x ★ y means x + 2y.", "What is the value of 3 ★ 5?",
    lambda: 3+2*5,
    [(2*3+5, "doubled the wrong operand"), (3+5, "ignored the factor of 2"),
     ((3+5)*2, "doubled the whole sum instead of only the second operand")],
    "The first operand is used as is and the second is doubled, so 3 + 10 = 13.", "easy")

sym(3, "The operation a ◆ b means (a − b) × 2.", "What is the value of 9 ◆ 4?",
    lambda: (9-4)*2,
    [((4-9)*2, "subtracted in the wrong order"), (9-4*2, "doubled only the second operand"),
     (9-4, "forgot to double the difference")],
    "Take the difference first, 9 − 4 = 5, then double it to get 10.", "easy")

sym(4, "For any number n, f(n) = 3n − 1.", "What is f(f(2))?",
    lambda: 3*(3*2-1)-1,
    [(3*2-1, "applied the function once instead of twice"),
     ((3*2-1)*2, "doubled the inner result instead of putting it back through the function"),
     (3*3*2-1, "multiplied by 3 twice but subtracted only once")],
    "Work outward: f(2) = 5, then f(5) = 3(5) − 1 = 14.")

sym(5, "The operation p △ q means p² − q.", "What is the value of 4 △ 7?",
    lambda: 4**2-7,
    [(7**2-4, "squared the wrong operand"), (4**2+7, "added the second operand instead of subtracting it"),
     (2*4-7, "doubled the first operand instead of squaring it")],
    "Square the first operand and subtract the second: 16 − 7 = 9.")

sym(6, "The operation a ⊙ b means a × b + a.", "What is the value of 6 ⊙ 2?",
    lambda: 6*2+6,
    [(6*2+2, "added the second operand instead of the first"), (6*2, "dropped the added term"),
     (6*2-6, "subtracted the first operand instead of adding it")],
    "Multiply the two operands to get 12, then add the first operand to get 18.")

sym(7, "For any number n, g(n) = n/2 + 4.", "What is g(10)?",
    lambda: F(10,2)+4,
    [(F(10+4,2), "added before dividing instead of after"), (F(10,2), "left off the added 4"),
     (10*2+4, "multiplied by 2 instead of dividing")],
    "Halve the input first to get 5, then add 4, giving 9.", "easy")

sym(8, "The operation x ⊞ y means 2(x + y).", "What is the value of 3 ⊞ 4?",
    lambda: 2*(3+4),
    [(2*3+4, "doubled only the first operand"), (3+4, "forgot to double the sum"),
     (2*3*4, "multiplied the operands instead of adding them")],
    "Add the operands first to get 7, then double the sum to get 14.", "easy")

sym(9, "The operation a ⊖ b means a − 2b.", "Which is larger, 8 ⊖ 1 or 5 ⊖ (−1)?",
    lambda: "5 ⊖ (−1), because it equals 7 while 8 ⊖ 1 equals 6",
    [("8 ⊖ 1, because 8 is the larger starting number", "compared the first operands instead of evaluating both expressions"),
     ("They are equal", "did not carry the double negative through"),
     ("8 ⊖ 1, because subtracting a negative makes it smaller", "reversed the effect of subtracting a negative")],
    "The first gives 8 − 2 = 6. The second subtracts twice a negative, which adds: 5 + 2 = 7.", "hard")
assert 8-2*1 == 6 and 5-2*(-1) == 7

sym(10, "For any numbers a and b, h(a, b) = a² + b.", "What is h(3, h(1, 2))?",
     lambda: 3**2+(1**2+2),
     [(3+(1**2+2), "added the first operand instead of squaring it"),
      (3**2+2, "used the inner second operand directly instead of the inner result"),
      ((3+1)**2+2, "combined the two first operands before squaring")],
     "The inner call gives 1 + 2 = 3. The outer call then squares 3 and adds that 3, giving 12.", "hard")

sym(11, "The operation m ▷ n means the larger of m and n, minus the smaller.",
     "What is the value of (−3) ▷ 5?",
     lambda: 5-(-3),
     [(-3-5, "subtracted in the order written instead of larger minus smaller"),
      (5+(-3), "added the two values"), (5*(-3), "multiplied instead of subtracting")],
     "The larger value is 5 and the smaller is −3, and subtracting a negative adds, so the result is 8.")

sym(12, "For any number n, f(n) = 2n and g(n) = n + 3.", "What is f(g(4))?",
     lambda: 2*(4+3),
     [(2*4+3, "applied the functions in the reverse order"), (4+3, "never applied the doubling"),
      (2*4*3, "multiplied by 3 instead of adding it")],
     "Apply g first: 4 + 3 = 7. Then f doubles that to 14.")

sym(13, "The operation a ⊕ b means (a + b) ÷ 2.", "What is the value of 7 ⊕ 2?",
     lambda: F(7+2,2),
     [(F(7,2)+2, "halved only the first operand"), (7+2, "forgot to halve the sum"),
      (F(7-2,2), "subtracted instead of adding")],
     "Add the operands to get 9, then halve it, giving 4.5.")

sym(14, "The operation x ⊙ y means x × y − (x + y).", "What is the value of 5 ⊙ 3?",
     lambda: 5*3-(5+3),
     [(5*3-5+3, "subtracted only the first operand instead of the whole sum"),
      (5*3+(5+3), "added the sum instead of subtracting it"), (5*3, "dropped the subtracted term")],
     "The product is 15 and the sum is 8, so the result is 7.")

sym(15, "For any number n, f(n) = n − 4.", "For which value of n does f(f(n)) equal 0?",
     lambda: 8,
     [(4, "solved f(n) = 0 instead of applying the function twice"),
      (0, "assumed the input equals the output"), (-8, "applied the subtraction in the wrong direction")],
     "Applying the function twice subtracts 4 twice, so the input must be 8 for the result to be 0.", "hard")
assert (8-4)-4 == 0

# ============================================================ 4. if-then chains
def ifthen(n, intro, varnames, premises, candidates, difficulty="medium"):
    """Exactly one candidate must be entailed by the premises."""
    ms = truth_models(varnames, premises)
    assert ms, f"varrel-if-{n}: premises unsatisfiable"
    cls = [(t, all(f(env) for env in ms), any(f(env) for env in ms), note) for t, f, note in candidates]
    keyed = [c for c in cls if c[1]]
    assert len(keyed) == 1, f"varrel-if-{n}: {len(keyed)} entailed candidates: {[(c[0], c[1]) for c in cls]}"
    key = keyed[0]
    others = [(t, f"this does not follow — {note}") for t, always, ever, note in cls if t != key[0]]
    items.append(Item(
        f"varrel-if-{n:03d}", "varrel", ["varrel.ifthen"],
        f"{intro}\nWhat follows?",
        key[0], others,
        f"Checked against all {2**len(varnames)} truth assignments: {len(ms)} satisfy the premises, "
        f"and the stated conclusion holds in every one of them.",
        f"python:truth-table ({2**len(varnames)} assignments, {len(ms)} satisfying)",
        difficulty, formatter=str))

IMP = lambda a, b: (lambda e: (not e[a]) or e[b])
IMPN = lambda a, b: (lambda e: (not e[a]) or (not e[b]))
TRUE = lambda a: (lambda e: e[a])
FALSE = lambda a: (lambda e: not e[a])

ifthen(1, "If the pump is running, the tank is filling.\nIf the tank is filling, the alarm is off.\nThe alarm is on.",
       ['pump','fill','alarmoff'],
       [IMP('pump','fill'), IMP('fill','alarmoff'), lambda e: not e['alarmoff']],
       [("The pump is not running", FALSE('pump'), "the chain runs backwards from a false conclusion, which does settle it"),
        ("The pump is running", TRUE('pump'), "this is the opposite of what the chain gives"),
        ("The tank is filling", TRUE('fill'), "an alarm that is on rules filling out"),
        ("Nothing can be concluded about the pump", lambda e: False, "the chain does settle the pump")])

ifthen(2, "If the breaker trips, the light goes out.\nThe breaker trips.", ['trip','out'],
       [IMP('trip','out'), TRUE('trip')],
       [("The light goes out", TRUE('out'), "reading the conditional forwards from a true premise is valid"),
        ("The light stays on", FALSE('out'), "this contradicts the conditional"),
        ("The breaker does not trip", FALSE('trip'), "the premise states that it does"),
        ("Nothing follows about the light", lambda e: False, "the conditional settles it")], "easy")

ifthen(3, "If the valve is open, flow is present.\nFlow is not present.", ['open','flow'],
       [IMP('open','flow'), FALSE('flow')],
       [("The valve is not open", FALSE('open'), "denying the consequent denies the antecedent"),
        ("The valve is open", TRUE('open'), "an open valve would produce flow"),
        ("Flow is present", TRUE('flow'), "the premise says it is not"),
        ("Nothing follows about the valve", lambda e: False, "denying the consequent does settle it")], "easy")

ifthen(4, "If the switch is on, the motor runs.\nThe motor runs.", ['sw','motor'],
       [IMP('sw','motor'), TRUE('motor')],
       [("Nothing follows about the switch", lambda e: True, "a running motor does not prove the switch is what started it"),
        ("The switch is on", TRUE('sw'), "this affirms the consequent, which is not valid"),
        ("The switch is off", FALSE('sw'), "nothing rules the switch out either"),
        ("The motor does not run", FALSE('motor'), "the premise states that it does")], "hard")

ifthen(5, "If A then B.\nIf B then C.\nA is true.", ['A','B','C'],
       [IMP('A','B'), IMP('B','C'), TRUE('A')],
       [("C is true", TRUE('C'), "the chain carries forward from a true antecedent"),
        ("C is false", FALSE('C'), "this contradicts the chain"),
        ("B is false", FALSE('B'), "A being true forces B"),
        ("Nothing follows about C", lambda e: False, "the chain reaches C")])

ifthen(6, "If A then B.\nIf B then C.\nC is false.", ['A','B','C'],
       [IMP('A','B'), IMP('B','C'), FALSE('C')],
       [("A is false", FALSE('A'), "a false end of the chain forces the start false"),
        ("A is true", TRUE('A'), "a true A would force C true"),
        ("B is true", TRUE('B'), "a true B would force C true"),
        ("Nothing follows about A", lambda e: False, "the chain does settle A")])

ifthen(7, "If the guard is fitted, the machine can start.\nIf the machine can start, the light is green.\nThe light is not green.",
       ['guard','start','green'],
       [IMP('guard','start'), IMP('start','green'), FALSE('green')],
       [("The guard is not fitted", FALSE('guard'), "working backwards down the chain settles it"),
        ("The guard is fitted", TRUE('guard'), "a fitted guard would make the light green"),
        ("The machine can start", TRUE('start'), "that would make the light green"),
        ("Nothing follows about the guard", lambda e: False, "the chain settles the guard")])

ifthen(8, "If P then not Q.\nQ is true.", ['P','Q'],
       [IMPN('P','Q'), TRUE('Q')],
       [("P is false", FALSE('P'), "a true P would rule Q out"),
        ("P is true", TRUE('P'), "that would make Q false"),
        ("Q is false", FALSE('Q'), "the premise states Q is true"),
        ("Nothing follows about P", lambda e: False, "the premise settles P")])

ifthen(9, "If the tank is full, the pump stops.\nThe pump has not stopped.", ['full','stop'],
       [IMP('full','stop'), FALSE('stop')],
       [("The tank is not full", FALSE('full'), "a full tank would have stopped the pump"),
        ("The tank is full", TRUE('full'), "that would have stopped the pump"),
        ("The pump has stopped", TRUE('stop'), "the premise says it has not"),
        ("Nothing follows about the tank", lambda e: False, "it does follow")], "easy")

ifthen(10, "If A then B.\nA is false.", ['A','B'],
       [IMP('A','B'), FALSE('A')],
       [("Nothing follows about B", lambda e: True, "denying the antecedent says nothing about the consequent"),
        ("B is false", FALSE('B'), "this denies the antecedent, which proves nothing"),
        ("B is true", TRUE('B'), "nothing forces B either way"),
        ("A is true", TRUE('A'), "the premise states A is false")], "hard")

ifthen(11, "If the feed is jammed, the sensor trips.\nIf the sensor trips, the line halts.\nThe feed is jammed.",
       ['jam','sensor','halt'],
       [IMP('jam','sensor'), IMP('sensor','halt'), TRUE('jam')],
       [("The line halts", TRUE('halt'), "the chain carries all the way through"),
        ("The line keeps running", FALSE('halt'), "this contradicts the chain"),
        ("The sensor does not trip", FALSE('sensor'), "a jam forces the sensor to trip"),
        ("Nothing follows about the line", lambda e: False, "the chain reaches the line")])

ifthen(12, "If X then Y.\nIf Y then not Z.\nZ is true.", ['X','Y','Z'],
       [IMP('X','Y'), IMPN('Y','Z'), TRUE('Z')],
       [("X is false", FALSE('X'), "a true X would force Y, which would rule Z out"),
        ("X is true", TRUE('X'), "that would rule Z out"),
        ("Y is true", TRUE('Y'), "a true Y would rule Z out"),
        ("Nothing follows about X", lambda e: False, "the chain settles X")])

ifthen(13, "If the permit is signed, work may begin.\nWork may not begin.", ['permit','work'],
       [IMP('permit','work'), FALSE('work')],
       [("The permit is not signed", FALSE('permit'), "a signed permit would allow work"),
        ("The permit is signed", TRUE('permit'), "that would allow work to begin"),
        ("Work may begin", TRUE('work'), "the premise says it may not"),
        ("Nothing follows about the permit", lambda e: False, "it does follow")], "easy")

ifthen(14, "If A then B.\nIf not A then B.", ['A','B'],
       [IMP('A','B'), lambda e: e['A'] or e['B']],
       [("B is true", TRUE('B'), "B follows whether A holds or not"),
        ("A is true", TRUE('A'), "A is not settled by these premises"),
        ("A is false", FALSE('A'), "A is not settled by these premises"),
        ("Nothing follows about B", lambda e: False, "both branches lead to B")], "hard")

ifthen(15, "If the line is pressurised, the gauge reads above zero.\nThe gauge reads above zero.",
       ['pres','gauge'],
       [IMP('pres','gauge'), TRUE('gauge')],
       [("Nothing follows about whether the line is pressurised", lambda e: True,
         "a gauge above zero can have another cause, so this affirms the consequent"),
        ("The line is pressurised", TRUE('pres'), "this affirms the consequent, which is not valid"),
        ("The line is not pressurised", FALSE('pres'), "nothing rules it out either"),
        ("The gauge reads zero", FALSE('gauge'), "the premise says it reads above zero")], "hard")

if __name__ == "__main__":
    from collections import Counter
    by = Counter(i.d["skills"][0] for i in items)
    assert len(items) == 60, f"expected 60 items, got {len(items)}"
    print(f"variable-relationship: {len(items)} items built and verified")
    for k, v in sorted(by.items()):
        print(f"  {k}: {v}")
