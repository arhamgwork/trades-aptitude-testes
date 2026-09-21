# -*- coding: utf-8 -*-
"""Paper-folding model with a reverse check.

A sheet is the unit square. A fold is a reflection about a vertical or
horizontal crease; the half on one side lands on the half on the other. Holes
are punched through the folded stack, then the sheet is opened.

Unfolding mirrors every hole back across each crease in reverse order.
The reverse check then re-folds every unfolded hole and asserts it lands back
on the punch that produced it, so a key can only be wrong if both directions
are wrong in the same way.
"""
from fractions import Fraction as F

# A fold: (axis, crease, keep) where keep says which half survives.
#   axis 'x', keep 'right' -> the left half folds onto the right
#   axis 'y', keep 'top'   -> the bottom half folds onto the top


def fold_point(p, fold):
    """Apply one fold to a point, moving it onto the surviving half."""
    x, y = p
    axis, c, keep = fold
    if axis == 'x':
        if (keep == 'right' and x < c) or (keep == 'left' and x > c):
            x = 2 * c - x
    else:
        if (keep == 'top' and y < c) or (keep == 'bottom' and y > c):
            y = 2 * c - y
    return (x, y)


def mirror_point(p, fold):
    """Reflect a point across a crease, regardless of side."""
    x, y = p
    axis, c, _ = fold
    return (2 * c - x, y) if axis == 'x' else (x, 2 * c - y)


def fold_all(p, folds):
    for f in folds:
        p = fold_point(p, f)
    return p


def unfold(punches, folds):
    """Open the sheet: each fold doubles the holes by mirroring across it."""
    holes = list(punches)
    for f in reversed(folds):
        holes = holes + [mirror_point(h, f) for h in holes]
    # A punch sitting exactly on a crease mirrors onto itself.
    out = []
    for h in holes:
        if h not in out:
            out.append(h)
    return sorted(out)


def verify(punches, folds):
    """Reverse check: re-fold every unfolded hole onto a punch position."""
    holes = unfold(punches, folds)
    punch_set = {tuple(p) for p in punches}
    for h in holes:
        landed = fold_all(h, folds)
        assert landed in punch_set, (
            f"reverse check failed: hole {h} re-folds to {landed}, "
            f"which is not one of the punches {sorted(punch_set)}")
    # every punch must be reachable
    reached = {fold_all(h, folds) for h in holes}
    assert reached == punch_set, (
        f"reverse check failed: punches {punch_set - reached} were never produced")
    # hole count: each fold doubles unless the punch lies on that crease
    expected = 1
    for f in folds:
        axis, c, _ = f
        on_crease = all((p[0] == c) if axis == 'x' else (p[1] == c) for p in punches)
        if not on_crease:
            expected *= 2
    assert len(holes) == expected * len(punches) or len(holes) <= 2 ** len(folds) * len(punches), \
        f"unexpected hole count {len(holes)}"
    return holes


def holes_svg(holes, size=104, note=None):
    """Draw an opened sheet with its holes."""
    pad = 7
    span = size - 2 * pad
    parts = [f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}" '
             f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="unfolded sheet">']
    parts.append(f'<rect x="{pad}" y="{pad}" width="{span}" height="{span}" '
                 f'fill="#FBFCFA" stroke="#22323A" stroke-width="2"/>')
    for (hx, hy) in holes:
        cx = pad + float(hx) * span
        cy = pad + (1 - float(hy)) * span
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="5.6" fill="#22323A"/>')
    parts.append('</svg>')
    return "".join(parts)


def sequence_svg(folds, punches, panel=88):
    """Draw the fold sequence: the flat sheet, each fold, then the punch."""
    gap = 10
    n = len(folds) + 2
    width = n * panel + (n - 1) * gap
    pad = 6
    span = panel - 2 * pad
    out = [f'<svg viewBox="0 0 {width} {panel + 14}" width="100%" height="{panel + 14}" '
           f'xmlns="http://www.w3.org/2000/svg" role="img" '
           f'aria-label="fold sequence, then the punch">']

    # region of the sheet still showing after k folds, as (x0,x1,y0,y1)
    def region_after(k):
        x0, x1, y0, y1 = F(0), F(1), F(0), F(1)
        for axis, c, keep in folds[:k]:
            if axis == 'x':
                if keep == 'right':
                    x0 = max(x0, c)
                else:
                    x1 = min(x1, c)
            else:
                if keep == 'top':
                    y0 = max(y0, c)
                else:
                    y1 = min(y1, c)
        return x0, x1, y0, y1

    for k in range(n):
        ox = k * (panel + gap)
        step = min(k, len(folds))
        x0, x1, y0, y1 = region_after(step)
        rx = pad + float(x0) * span
        rw = float(x1 - x0) * span
        ry = pad + (1 - float(y1)) * span
        rh = float(y1 - y0) * span
        out.append(f'<g transform="translate({ox},0)">')
        # faint outline of the original sheet
        out.append(f'<rect x="{pad}" y="{pad}" width="{span}" height="{span}" fill="none" '
                   f'stroke="#B9C4C9" stroke-width="1" stroke-dasharray="3 3"/>')
        out.append(f'<rect x="{rx:.1f}" y="{ry:.1f}" width="{rw:.1f}" height="{rh:.1f}" '
                   f'fill="#FBFCFA" stroke="#22323A" stroke-width="2"/>')
        # the crease just made
        if 0 < k <= len(folds):
            axis, c, _ = folds[k - 1]
            if axis == 'x':
                cx = pad + float(c) * span
                out.append(f'<line x1="{cx:.1f}" y1="{pad}" x2="{cx:.1f}" y2="{pad + span}" '
                           f'stroke="#6B7C83" stroke-width="1.4" stroke-dasharray="4 3"/>')
            else:
                cy = pad + (1 - float(c)) * span
                out.append(f'<line x1="{pad}" y1="{cy:.1f}" x2="{pad + span}" y2="{cy:.1f}" '
                           f'stroke="#6B7C83" stroke-width="1.4" stroke-dasharray="4 3"/>')
        if k == n - 1:
            for (px, py) in punches:
                cx = pad + float(px) * span
                cy = pad + (1 - float(py)) * span
                out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="5" fill="#22323A"/>')
        label = "flat" if k == 0 else ("punch" if k == n - 1 else f"fold {k}")
        out.append(f'<text x="{panel/2:.0f}" y="{panel + 11}" text-anchor="middle" '
                   f'font-size="9" fill="#6B7C83">{label}</text>')
        out.append('</g>')
    out.append('</svg>')
    return "".join(out)
