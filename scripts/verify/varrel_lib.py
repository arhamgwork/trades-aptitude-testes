# -*- coding: utf-8 -*-
"""Classification helpers for variable-relationship items.

Every item's key is decided by enumeration, not by hand, so a stated
relationship is MUST / MIGHT / CANNOT because the search says so.
"""
import itertools
from fractions import Fraction as F

# A discrete universe wide enough to expose counterexamples, including
# negatives, zero and halves (so "double it" style traps are caught).
UNIVERSE = [F(n, 2) for n in range(-12, 25)]


def models(varnames, constraints, universe=None):
    """All assignments over `varnames` satisfying every constraint."""
    uni = universe or UNIVERSE
    out = []
    for combo in itertools.product(uni, repeat=len(varnames)):
        env = dict(zip(varnames, combo))
        if all(c(env) for c in constraints):
            out.append(env)
    return out


def classify(ms, statement):
    """MUST / CANNOT / MIGHT for `statement` across the models `ms`."""
    assert ms, "constraints are unsatisfiable"
    t = sum(1 for env in ms if statement(env))
    if t == len(ms):
        return "MUST"
    if t == 0:
        return "CANNOT"
    return "MIGHT"


def truth_models(varnames, premises):
    """All boolean assignments satisfying the premises."""
    out = []
    for combo in itertools.product([False, True], repeat=len(varnames)):
        env = dict(zip(varnames, combo))
        if all(p(env) for p in premises):
            out.append(env)
    return out


def sufficiency(target, s1, s2, varnames, universe=None):
    """Classify which statements pin `target` to a single value.

    Returns one of 'S1', 'S2', 'BOTH', 'NEITHER', matching the four standard
    sufficiency choices.
    """
    uni = universe or UNIVERSE

    def values(constraints):
        vals = {target(env) for env in models(varnames, constraints, uni)}
        return vals

    v1 = values([s1])
    v2 = values([s2])
    v12 = values([s1, s2])
    assert v12, "the two statements together are contradictory"
    a = len(v1) == 1
    b = len(v2) == 1
    if a and b:
        return "EITHER"
    if a:
        return "S1"
    if b:
        return "S2"
    if len(v12) == 1:
        return "BOTH"
    return "NEITHER"


SUFF_CHOICES = [
    "Statement (1) alone is enough, but statement (2) alone is not",
    "Statement (2) alone is enough, but statement (1) alone is not",
    "Neither statement alone is enough, but together they are enough",
    "Each statement alone is enough",
    "Even together, the two statements are not enough",
]
SUFF_INDEX = {"S1": 0, "S2": 1, "BOTH": 2, "EITHER": 3, "NEITHER": 4}

SUFF_NOTES = {
    0: "credits the first statement with pinning a value it does not pin on its own",
    1: "credits the second statement with pinning a value it does not pin on its own",
    2: "assumes the two must be combined when that is not what the statements do here",
    3: "assumes each statement settles the value by itself",
    4: "concludes nothing is determined when the statements do determine it",
}
