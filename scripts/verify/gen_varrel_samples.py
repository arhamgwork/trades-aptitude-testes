# -*- coding: utf-8 -*-
"""Four sample variable-relationship items, one per sub-type, each verified
exhaustively by substitution before it is shown."""
import itertools
from fractions import Fraction as F

samples = []

# ---------------------------------------------------------------- 1. inequality chain
# x > y, y > z, z > 0.  What must be true about x and z?
def check_ineq():
    universe = [F(n, 2) for n in range(-10, 21)]
    ok_must, ok_cannot = True, True
    saw = 0
    for x, y, z in itertools.product(universe, repeat=3):
        if not (x > y and y > z and z > 0):
            continue
        saw += 1
        if not (x > z):          # candidate key: x > z must be true
            ok_must = False
        if x <= 0:               # "x could be negative" must never happen
            ok_cannot = False
    assert saw > 100, saw
    assert ok_must and ok_cannot
    # "x > 2z" is only sometimes true -> a correct MIGHT-be-true, wrong as MUST
    sometimes_true = any(x > 2 * z for x, y, z in itertools.product(universe, repeat=3)
                         if x > y and y > z and z > 0)
    sometimes_false = any(not (x > 2 * z) for x, y, z in itertools.product(universe, repeat=3)
                          if x > y and y > z and z > 0)
    assert sometimes_true and sometimes_false
    return saw

n1 = check_ineq()
samples.append(dict(
    subtype="Inequality chains", skill="varrel.inequality",
    stem="On a job, three readings satisfy x > y, y > z, and z > 0.\n"
         "Which statement MUST be true?",
    choices=["x > z",
             "x > 2z",
             "y is positive but x could be negative",
             "z > y"],
    correct=0,
    notes=[None,
           "true for some values and false for others, so it is a 'might be true', not a 'must'",
           "reverses the chain: everything above z is greater than z, so x is positive too",
           "states the chain backwards"],
    explanation="The chain runs x > y > z, and the greater-than relation carries "
                "through, so x is greater than z. Doubling z is not supported: "
                "x > 2z happens for some values and fails for others.",
    verify=f"python:exhaustive ({n1} satisfying triples checked)"))

# ---------------------------------------------------------------- 2. two-statement sufficiency
# Question: what is a?  (1) a + b = 10   (2) b = 4
def check_suff():
    # statement 1 alone: many a -> insufficient
    a1 = {a for a in range(-20, 21) for b in range(-20, 21) if a + b == 10}
    assert len(a1) > 1
    # statement 2 alone: a unconstrained -> insufficient
    a2 = {a for a in range(-20, 21) for b in range(-20, 21) if b == 4}
    assert len(a2) > 1
    # together: unique
    both = {a for a in range(-20, 21) for b in range(-20, 21) if a + b == 10 and b == 4}
    assert both == {6}, both
    return sorted(both)[0]

v2 = check_suff()
samples.append(dict(
    subtype="Two-statement sufficiency", skill="varrel.sufficiency",
    stem="What is the value of a?\n"
         "  (1) a + b = 10\n"
         "  (2) b = 4",
    choices=["Statement (1) alone is enough, but statement (2) alone is not",
             "Statement (2) alone is enough, but statement (1) alone is not",
             "Neither statement alone is enough, but together they are enough",
             "Even together, the two statements are not enough"],
    correct=2,
    notes=["one equation in two unknowns fixes neither value on its own",
           "knowing b says nothing about a without a relationship between them",
           None,
           "together they give a single value, so they are sufficient"],
    explanation=f"Alone, a + b = 10 allows many pairs and b = 4 says nothing about a. "
                f"Together they force a = {v2}, so both are needed and both together suffice.",
    verify="python:exhaustive (all integer pairs in [-20,20] enumerated)"))

# ---------------------------------------------------------------- 3. symbolic substitution
# a ▲ b  means  2a − b.   Evaluate (5 ▲ 3) ▲ 4
def tri(a, b): return 2 * a - b
inner = tri(5, 3); outer = tri(inner, 4)
assert inner == 7 and outer == 10
wrong_order = tri(5, tri(3, 4))          # right-to-left: 2*5 - 2 = 8
assert wrong_order == 8
swapped = 2 * 3 - 5                      # operands reversed in the inner step
assert swapped == 1
samples.append(dict(
    subtype="Symbolic / functional substitution", skill="varrel.symbolic",
    stem="The operation a ▲ b means 2a − b.\n"
         "What is the value of (5 ▲ 3) ▲ 4?",
    choices=[str(outer), str(wrong_order), str(swapped), str(2 * 5 - 3 - 4)],
    correct=0,
    notes=[None,
           "worked the operation from right to left instead of evaluating the bracket first",
           "reversed the two operands inside the bracket",
           "subtracted both numbers from 2a in one step instead of applying the operation twice"],
    explanation="Work the bracket first: 5 ▲ 3 doubles the 5 and subtracts the 3, "
                "giving 7. Then 7 ▲ 4 doubles the 7 and subtracts the 4, giving 10.",
    verify="python:substitution (both steps evaluated; each distractor reproduced from its named error)"))
assert len(set([str(outer), str(wrong_order), str(swapped), str(2*5-3-4)])) == 4

# ---------------------------------------------------------------- 4. if-then chain
# If P then Q. If Q then not R. R is true. What follows?
def check_ifthen():
    results = []
    for P, Q, R in itertools.product([False, True], repeat=3):
        if (not P or Q) and (not Q or not R) and R:
            results.append((P, Q, R))
    assert results, "premises unsatisfiable"
    assert all(not P for P, Q, R in results), "P must be false"
    assert all(not Q for P, Q, R in results), "Q must be false"
    return results

rows = check_ifthen()
samples.append(dict(
    subtype="If-then chains", skill="varrel.ifthen",
    stem="Take these three facts as given:\n"
         "  If the pump is running, the tank is filling.\n"
         "  If the tank is filling, the alarm is off.\n"
         "  The alarm is on.\n"
         "What follows?",
    choices=["The pump is not running",
             "The pump is running",
             "The tank is filling",
             "Nothing can be concluded about the pump"],
    correct=0,
    notes=[None,
           "reads the conditional forwards from a false conclusion, which does not follow",
           "contradicts the second fact, since the alarm being on rules out filling",
           "the chain does settle it: an alarm that is on works backwards to a pump that is not running"],
    explanation="The alarm being on means the tank is not filling, by the second "
                "fact. If the tank is not filling, the pump cannot be running, by "
                "the first. Working a conditional backwards from a false "
                "conclusion is valid; working it forwards from one is not.",
    verify=f"python:truth-table (all 8 assignments enumerated; {len(rows)} satisfy the premises, all with pump false)"))

if __name__ == "__main__":
    for i, s in enumerate(samples, 1):
        print(f"\n{'='*72}\nSAMPLE {i} — {s['subtype']}   [{s['skill']}]\n{'='*72}")
        print(s['stem'])
        for j, c in enumerate(s['choices']):
            mark = "  <- correct" if j == s['correct'] else ""
            print(f"   {'ABCD'[j]}. {c}{mark}")
        print(f"\n   Why: {s['explanation']}")
        print(f"   Verified: {s['verify']}")
        for j, n in enumerate(s['notes']):
            if n: print(f"     {'ABCD'[j]} represents: {n}")
    print(f"\nAll {len(samples)} samples verified.")
