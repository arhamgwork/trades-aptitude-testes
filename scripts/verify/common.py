"""Shared helpers for building and verifying exam items.

Every item is built by computing the correct answer from the item's own
parameters and asserting it, then building distractors that each encode a
specific, named mistake. Nothing is hand-typed as a bare answer string.
"""
from fractions import Fraction


def fmt(x):
    """Format a number the way a test booklet would."""
    if isinstance(x, Fraction):
        if x.denominator == 1:
            return str(x.numerator)
        return f"{x.numerator}/{x.denominator}"
    if isinstance(x, float):
        s = f"{x:.4f}".rstrip("0").rstrip(".")
        return s
    return str(x)


class Item:
    """One question. Choices are (value, error_note); the key has note None."""

    def __init__(self, qid, section, skills, stem, correct, distractors,
                 explanation, verify, difficulty="medium", figure=None,
                 passage_id=None, qtype="mc", formatter=fmt, extra_choice=None):
        vals = [correct] + [d[0] for d in distractors]
        rendered = [formatter(v) for v in vals]
        if extra_choice is not None:
            rendered.append(extra_choice[0])
        # A distractor that renders identically to the key is a bug, not a choice.
        if len(set(rendered)) != len(rendered):
            raise AssertionError(f"{qid}: duplicate rendered choices {rendered}")
        notes = [None] + [d[1] for d in distractors]
        if extra_choice is not None:
            notes.append(extra_choice[1])
        self.d = dict(
            id=qid, section=section, skills=skills, type=qtype, stem=stem,
            figure=figure, passageId=passage_id,
            choices=rendered, correctIndex=0, explanation=explanation,
            distractorNotes=notes, difficulty=difficulty, verify=verify,
        )

    def as_dict(self):
        return dict(self.d)


def _seeded_rand(seed, n):
    """Deterministic pseudo-random ints in [0, n) from a seed string."""
    import hashlib
    h = hashlib.sha256(seed.encode()).digest()
    i = 0
    while True:
        if i >= len(h):
            h = hashlib.sha256(h).digest()
            i = 0
        yield h[i] % n
        i += 1


def _shuffled(seq, seed):
    """Deterministic Fisher-Yates using a seeded byte stream."""
    import hashlib
    out = list(seq)
    h = hashlib.sha256(seed.encode()).digest()
    pool, i = list(h), 0
    for k in range(len(out) - 1, 0, -1):
        if i + 4 > len(pool):
            h = hashlib.sha256(bytes(pool[-32:])).digest()
            pool += list(h)
        val = int.from_bytes(bytes(pool[i:i + 4]), "big")
        i += 4
        j = val % (k + 1)
        out[k], out[j] = out[j], out[k]
    return out


def _break_runs_in_targets(targets, max_run=3):
    """Repair runs of identical targets by swapping within the list.

    Swapping preserves the multiset, so the letter distribution is unchanged.
    """
    n = len(targets)
    for i in range(max_run, n):
        window = targets[i - max_run:i + 1]
        if len(set(window)) != 1:
            continue
        for j in range(i + 1, n):
            if targets[j] != targets[i] and (
                    j + 1 >= n or targets[j + 1] != targets[i]):
                targets[i], targets[j] = targets[j], targets[i]
                break
        else:
            for j in range(i - max_run - 1, -1, -1):
                if targets[j] != targets[i]:
                    targets[i], targets[j] = targets[j], targets[i]
                    break
    return targets


def balance_keys(items, seed, section_key="section"):
    """Deterministically place each item's key so letters are near-uniform.

    Builds a balanced multiset of target positions per (section, choice-width)
    group, shuffles it with the seed, repairs runs without changing counts,
    then permutes each item's choices so the key lands on its target.
    """
    groups = {}
    for idx, q in enumerate(items):
        groups.setdefault((q[section_key], len(q["choices"])), []).append(idx)

    for (sec, width), idxs in sorted(groups.items()):
        targets = [i % width for i in range(len(idxs))]
        targets = _shuffled(targets, f"{seed}:{sec}:{width}")
        targets = _break_runs_in_targets(targets, 3)
        for pos, qi in enumerate(idxs):
            q = items[qi]
            target = targets[pos]
            cur = q["correctIndex"]
            if cur == target:
                continue
            order = list(range(width))
            order[cur], order[target] = order[target], order[cur]
            # order[k] says which OLD index now sits at NEW index k
            q["choices"] = [q["choices"][order[k]] for k in range(width)]
            q["distractorNotes"] = [q["distractorNotes"][order[k]] for k in range(width)]
            q["correctIndex"] = target
    return items


def fix_runs(items, max_run=3):
    """Break runs of >max_run identical correct letters by rotating an item."""
    for i in range(len(items)):
        run = 1
        j = i
        while j > 0 and items[j]["correctIndex"] == items[j - 1]["correctIndex"]:
            run += 1
            j -= 1
        if run > max_run:
            q = items[i]
            n = len(q["choices"])
            target = (q["correctIndex"] + 1) % n
            q["choices"][q["correctIndex"]], q["choices"][target] = (
                q["choices"][target], q["choices"][q["correctIndex"]])
            q["distractorNotes"][q["correctIndex"]], q["distractorNotes"][target] = (
                q["distractorNotes"][target], q["distractorNotes"][q["correctIndex"]])
            q["correctIndex"] = target
    return items


def report(items, label):
    from collections import Counter
    c = Counter(chr(65 + q["correctIndex"]) for q in items)
    total = len(items)
    parts = ", ".join(f"{k}={c[k]} ({100*c[k]/total:.0f}%)" for k in sorted(c))
    print(f"  {label}: {total} items — {parts}")
    return c
