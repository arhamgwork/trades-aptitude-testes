# -*- coding: utf-8 -*-
"""GAN battery Form B — Section 6, Spatial Relations / paper folding (20 items).

Every key is produced by the fold model and confirmed by a reverse check:
each hole in the answer is re-folded and must land back on the punch. Each
distractor is produced by a named mistake, not by moving dots at random.
"""
import sys, os
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(__file__))
from common import Item
from fold_model import unfold, verify, holes_svg, sequence_svg, mirror_point

S = "s6"
items = []
H = F(1, 2)
Q, T = F(1, 4), F(3, 4)

def err_one_fold_short(punches, folds):
    """Opened every crease but the first."""
    return unfold(punches, folds[1:]) if len(folds) > 1 else list(punches)

def err_wrong_axis(punches, folds):
    """Mirrored across a crease running the other way."""
    flipped = [('y' if a == 'x' else 'x', c, k) for a, c, k in folds]
    return unfold(punches, flipped)

def err_no_mirror(punches, folds):
    """Opened the sheet but never mirrored the holes."""
    return sorted(set(punches))

def build(n, folds, punches, difficulty="medium"):
    key = verify(punches, folds)                     # reverse-checked
    candidates = [
        (err_one_fold_short(punches, folds), "opened one crease too few, so half the holes are missing"),
        (err_wrong_axis(punches, folds), "mirrored the holes across creases running the other way"),
        (err_no_mirror(punches, folds), "opened the sheet but never mirrored the punch across the creases"),
    ]
    keyset = {tuple(h) for h in key}
    picked, seen = [], {tuple(sorted(keyset))}
    for holes, note in candidates:
        sig = tuple(sorted(tuple(h) for h in holes))
        if sig in seen:
            continue
        seen.add(sig)
        picked.append((holes_svg(holes), note))
    # Fallbacks, tried in order, when two named errors happen to coincide.
    fallbacks = [
        (sorted(key)[:-1], "missed one of the mirrored holes"),
        ([(h[1], h[0]) for h in key], "swapped the two directions when mirroring"),
        ([(1 - h[0], h[1]) for h in key], "mirrored the finished pattern across the vertical centre"),
        ([(h[0], 1 - h[1]) for h in key], "mirrored the finished pattern across the horizontal centre"),
        (sorted(key)[:1], "mirrored nothing and kept a single hole"),
    ]
    for holes, note in fallbacks:
        if len(picked) >= 3:
            break
        if not holes:
            continue
        sig = tuple(sorted(tuple(h) for h in holes))
        if sig in seen:
            continue
        seen.add(sig)
        picked.append((holes_svg(holes), note))
    assert len(picked) >= 3, f"s6-{n}: only {len(picked)} distinct distractors"
    fig = sequence_svg(folds, punches)
    items.append(Item(
        f"ganb-s6-{n:03d}", S, ["spatial.folding"],
        "The square is folded as shown, then punched through every layer. "
        "Which choice shows the sheet unfolded?",
        holes_svg(key), picked[:3],
        f"Work backwards one crease at a time. Each unfold mirrors every existing hole "
        f"across the crease being opened, so {len(folds)} fold"
        f"{'s' if len(folds) != 1 else ''} turn{'' if len(folds) != 1 else 's'} "
        f"{len(punches)} punch{'es' if len(punches) != 1 else ''} into {len(key)} holes.",
        "python:fold-model+reverse-check", difficulty,
        figure=fig, formatter=str))
    items[-1].d["choicesAreFigures"] = True

# one fold
build(1,  [('x', H, 'right')], [(T, T)], "easy")
build(2,  [('y', H, 'top')],   [(Q, T)], "easy")
build(3,  [('x', H, 'left')],  [(Q, Q)], "easy")
build(4,  [('y', H, 'bottom')],[(T, Q)], "easy")
build(5,  [('x', H, 'right')], [(T, Q)], "easy")
# two folds
build(6,  [('x', H, 'right'), ('y', H, 'top')], [(T, T)])
build(7,  [('x', H, 'right'), ('y', H, 'top')], [(F(5, 8), F(5, 8))])
build(8,  [('y', H, 'top'), ('x', H, 'right')], [(T, F(7, 8))])
build(9,  [('x', H, 'left'), ('y', H, 'bottom')], [(Q, Q)])
build(10, [('x', H, 'right'), ('y', H, 'bottom')], [(T, Q)])
build(11, [('y', H, 'top'), ('x', H, 'left')], [(Q, T)])
build(12, [('x', H, 'right'), ('y', H, 'top')], [(F(7, 8), F(5, 8))])
# three folds
build(13, [('x', H, 'right'), ('y', H, 'top'), ('x', T, 'right')], [(F(7, 8), T)], "hard")
build(14, [('x', H, 'right'), ('y', H, 'top'), ('y', T, 'top')], [(T, F(7, 8))], "hard")
build(15, [('y', H, 'top'), ('x', H, 'right'), ('x', T, 'right')], [(F(7, 8), F(5, 8))], "hard")
build(16, [('x', H, 'left'), ('y', H, 'top'), ('x', Q, 'left')], [(F(1, 8), T)], "hard")
# two punches
build(17, [('x', H, 'right')], [(F(5, 8), T), (F(7, 8), Q)])
build(18, [('y', H, 'top')], [(Q, F(5, 8)), (T, F(7, 8))])
build(19, [('x', H, 'right'), ('y', H, 'top')], [(F(5, 8), F(7, 8))])
build(20, [('x', H, 'right'), ('y', H, 'top')], [(F(7, 8), F(7, 8))])

if __name__ == "__main__":
    assert len(items) == 20, f"expected 20, got {len(items)}"
    counts = {}
    for it in items:
        d = it.as_dict()
        assert d["choicesAreFigures"], d["id"]
        assert len(d["choices"]) == 4, (d["id"], len(d["choices"]))
        n = d["choices"][d["correctIndex"]].count("<circle")
        counts[n] = counts.get(n, 0) + 1
    print(f"GAN Form B section 6 (Spatial Relations): {len(items)} items verified")
    print("  holes in the correct answer:", dict(sorted(counts.items())))
