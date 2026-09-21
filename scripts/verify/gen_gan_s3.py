# -*- coding: utf-8 -*-
"""GAN battery Form B — Section 3, Problem Solving (25 items).

Word problems in job-site language: ratios, rates, unit conversions and
multi-step arithmetic. Every key is computed from the item's own parameters.
"""
import sys, os
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(__file__))
from common import Item

S = "s3"
items = []

def num(x):
    if isinstance(x, F):
        if x.denominator == 1:
            return str(x.numerator)
        whole, rem = divmod(abs(x.numerator), x.denominator)
        sign = "-" if x < 0 else ""
        return f"{sign}{whole} {rem}/{x.denominator}" if whole else f"{sign}{rem}/{x.denominator}"
    return str(x)

def add(n, skills, stem, key, distractors, explanation, difficulty="medium", fmt=num):
    vals = [fmt(key)] + [fmt(d[0]) for d in distractors]
    assert len(set(vals)) == len(vals), f"s3-{n}: duplicate choices {vals}"
    items.append(Item(f"ganb-s3-{n:03d}", S, skills, stem, key, distractors,
                      explanation, "python:fractions", difficulty, formatter=fmt))

# ---- unit conversion --------------------------------------------------------
v = 3 * 12 + 6; assert v == 42
add(1, ["convert.units"], "How many inches are in 3 feet 6 inches?", v,
    [(3 * 12, "converted the feet but dropped the extra inches"),
     (3 + 6, "added the numbers without converting feet to inches"),
     (3 * 6 + 12, "multiplied the wrong pair of numbers")],
    "Each foot is 12 inches, so 3 feet is 36 inches, plus the 6 inches gives 42.", "easy")

v = F(90, 12); assert v == F(15, 2)
add(2, ["convert.units"], "A run of duct is 90 inches long. How many feet is that?", v,
    [(F(90, 10), "divided by 10 instead of 12"),
     (90 * 12, "multiplied by 12 instead of dividing"),
     (F(90, 36), "divided by the number of inches in a yard")],
    "Dividing inches by 12 converts to feet: 90 ÷ 12 = 7 1/2 feet.", "easy")

v = 2 * 3 + 1; assert v == 7
add(3, ["convert.units"], "How many feet of material is 2 yards 1 foot?", v,
    [(2 * 3, "converted the yards but dropped the extra foot"),
     (2 + 1, "added without converting yards to feet"),
     (2 * 12 + 1, "used 12 feet per yard instead of 3")],
    "A yard is 3 feet, so 2 yards is 6 feet, plus 1 foot gives 7.", "easy")

# ---- rate -------------------------------------------------------------------
v = F(240, 15); assert v == 16
add(4, ["rate.work"], "A tank holds 240 gallons and fills at 15 gallons per minute. "
    "How long does it take to fill?", v,
    [(F(240, 12), "used 12 gallons per minute instead of 15"),
     (240 * 15, "multiplied instead of divided"),
     (240 - 15, "subtracted the rate from the volume")],
    "Dividing the volume by the rate gives the time: 240 ÷ 15 = 16 minutes.", "easy")

v = F(165, 55); assert v == 3
add(5, ["rate.distance"], "A truck covers 165 miles at an average of 55 miles per hour. "
    "How many hours does the trip take?", v,
    [(F(165, 50), "rounded the speed to 50 before dividing"),
     (165 * 55, "multiplied instead of divided"),
     (165 - 55, "subtracted the speed from the distance")],
    "Time is distance divided by speed: 165 ÷ 55 = 3 hours.", "easy")

v = F(1, F(1, 6) + F(1, 3)); assert v == 2
add(6, ["rate.work"], "One crew can finish a job in 6 hours and another in 3 hours. "
    "Working together at those rates, how long does the job take?", v,
    [(F(6 + 3, 2), "averaged the two times instead of adding the rates"),
     (6 - 3, "subtracted the two times"),
     (F(1, 6) + F(1, 3), "added the two rates correctly but did not take the reciprocal at the end")],
    "Their rates add: 1/6 + 1/3 = 1/2 of the job per hour. The time is the "
    "reciprocal of that rate, so 2 hours.", "hard")

# ---- ratio / proportion ------------------------------------------------------
v = F(3 * 56, 8); assert v == 21
add(7, ["ratio.proportion"], "On a drawing, 3 inches represents 8 feet. "
    "How many inches represent 56 feet?", v,
    [(F(8 * 56, 3), "set the proportion up the wrong way round"),
     (F(56, 8), "divided but forgot to multiply by the 3"),
     (56 - 8 + 3, "treated the scale as a difference instead of a ratio")],
    "Set up the proportion 3/8 = x/56. Cross-multiplying gives 8x = 168, so x = 21 inches.")

total, a, b = 200, 3, 2
v = F(total * a, a + b); assert v == 120
add(8, ["ratio.proportion"], "Two workers split 200 feet of pipe in the ratio 3 to 2. "
    "How many feet does the larger share come to?", v,
    [(F(total * b, a + b), "reported the smaller share"),
     (F(total, a), "divided the total by 3 instead of by the 5 total parts"),
     (F(total, 2), "split the total evenly instead of by the ratio")],
    "The ratio makes 5 parts in all, so one part is 200 ÷ 5 = 40 feet. "
    "The larger share is 3 parts, or 120 feet.")

# ---- percent in context ------------------------------------------------------
v = F(46 - 40, 40) * 100; assert v == 15
add(9, ["arith.percent"], "A crew's output rises from 40 units per shift to 46. "
    "What is the percent increase?", v,
    [(F(46 - 40, 46) * 100, "divided the change by the new figure instead of the original"),
     (F(46, 40) * 100, "found the new output as a percent of the old rather than the increase"),
     (46 - 40, "reported the raw change as if it were a percent")],
    "Percent increase divides the change by the original: 6 ÷ 40 = 0.15, or 15%.",
    fmt=lambda x: f"{num(x)}%")

price = 180; disc = F(25, 100)
v = price * (1 - disc); assert v == 135
add(10, ["arith.percent"], "A tool listed at $180 is discounted 25%. What is the price after the discount?", v,
    [(price * disc, "gave the size of the discount instead of the new price"),
     (price - 25, "subtracted 25 dollars instead of 25 percent"),
     (price * (1 + disc), "added the discount instead of subtracting it")],
    "A 25% discount leaves 75% of the price: 0.75 × 180 = $135.",
    fmt=lambda x: f"${num(x)}")

# ---- area / volume -----------------------------------------------------------
v = 14 * 9; assert v == 126
add(11, ["geom.area"], "A rectangular sheet measures 14 inches by 9 inches. "
    "What is its area in square inches?", v,
    [(2 * (14 + 9), "found the perimeter instead of the area"),
     (14 + 9, "added the sides"), (14 - 9, "subtracted the sides")],
    "Area of a rectangle is length times width: 14 × 9 = 126 square inches.", "easy")

L, W, H = 6, 4, 3
v = L * W * H; assert v == 72
add(12, ["geom.volume"], "A rectangular duct section measures 6 feet by 4 feet by 3 feet. "
    "What is its volume in cubic feet?", v,
    [(2 * (L * W + L * H + W * H), "found the surface area instead of the volume"),
     (L + W + H, "added the three dimensions"),
     (L * W, "multiplied only two of the three dimensions")],
    "Volume is length times width times height: 6 × 4 × 3 = 72 cubic feet.")

b, h = 12, 7
v = F(b * h, 2); assert v == 42
add(13, ["geom.area"], "A triangular gusset has a base of 12 inches and a height of 7 inches. "
    "What is its area in square inches?", v,
    [(b * h, "used the rectangle formula and forgot to halve it"),
     (F(b + h, 2), "averaged the base and height"),
     (b + h, "added the base and height")],
    "Area of a triangle is half the base times the height: (12 × 7) ÷ 2 = 42.")

# ---- multi-step --------------------------------------------------------------
v = (8 * 12 + 4) - (3 * 12 + 7); assert v == 57
add(14, ["convert.units", "algebra.word"],
    "A length of 8 feet 4 inches has 3 feet 7 inches cut from it. "
    "How many inches are left?", v,
    [((8 * 12 + 4) - (3 * 12 - 7), "subtracted the 7 inches in the wrong direction"),
     (8 * 12 - 3 * 12, "worked in whole feet and dropped both inch amounts"),
     ((8 - 3) * 12 + (7 - 4), "subtracted the inch amounts in the wrong order")],
    "Convert both to inches: 100 inches minus 43 inches leaves 57 inches.", "hard")

sheets, per = 17, 8
v = sheets * per; assert v == 136
add(15, ["algebra.word"], "Each sheet takes 8 fasteners and there are 17 sheets. "
    "How many fasteners are needed?", v,
    [(sheets + per, "added instead of multiplied"),
     (sheets * per - per, "left one sheet out"),
     (sheets * (per + 1), "used one fastener too many per sheet")],
    "Multiply the number of sheets by the fasteners each: 17 × 8 = 136.", "easy")

total_cost, hours = 1092, 12
v = F(total_cost, hours); assert v == 91
add(16, ["algebra.word"], "A job costs $1,092 in labour for 12 hours of work. "
    "What is the cost per hour?", v,
    [(total_cost * hours, "multiplied instead of divided"),
     (F(total_cost, 10), "divided by 10 instead of 12"),
     (total_cost - hours, "subtracted the hours from the cost")],
    "Divide the total by the hours: 1,092 ÷ 12 = $91 per hour.",
    fmt=lambda x: f"${num(x)}")

# ---- averages ----------------------------------------------------------------
vals = [72, 85, 79, 92]
v = F(sum(vals), len(vals)); assert v == 82
add(17, ["arith.average"], "Four readings are 72, 85, 79 and 92. What is their average?", v,
    [(F(sum(vals), 3), "divided by one fewer reading than there are"),
     (sum(vals), "reported the total instead of the average"),
     (F(sum(vals), len(vals) + 1), "divided by one more reading than there are")],
    "Add the four readings to get 328 and divide by 4, giving 82.")

# ---- proportional scaling ----------------------------------------------------
v = F(45 * 14, 6); assert v == 105
add(18, ["ratio.proportion"], "If 6 fittings cost $45, what do 14 fittings cost at the same rate?", v,
    [(F(45, 6) * 6, "scaled back to the original quantity instead of the new one"),
     (45 + 14, "added the quantity to the price"),
     (F(45 * 6, 14), "set the proportion up the wrong way round")],
    "One fitting costs 45 ÷ 6 = $7.50, so 14 cost 7.50 × 14 = $105.",
    fmt=lambda x: f"${num(x)}")

# ---- remaining assorted -------------------------------------------------------
v = F(3, 4) * 96; assert v == 72
add(19, ["arith.fractions"], "Three quarters of a 96-foot run has been installed. "
    "How many feet is that?", v,
    [(F(1, 4) * 96, "found the part still remaining instead of the part installed"),
     (96 - 3, "subtracted 3 from the total"),
     (F(96, 3), "divided by 3 instead of taking three quarters")],
    "Three quarters of 96 is (96 ÷ 4) × 3 = 72 feet.", "easy")

v = 5 * 60 + 45; assert v == 345
add(20, ["convert.units"], "How many minutes are in 5 hours 45 minutes?", v,
    [(5 * 60, "converted the hours but dropped the extra minutes"),
     (5 + 45, "added without converting hours to minutes"),
     (5 * 45 + 60, "multiplied the wrong pair of numbers")],
    "Each hour is 60 minutes, so 5 hours is 300 minutes, plus 45 gives 345.", "easy")

v = F(1, 2) + F(3, 8) + F(1, 4); assert v == F(9, 8)
add(21, ["arith.fractions"], "Three pieces measure 1/2 inch, 3/8 inch and 1/4 inch. "
    "What is their combined length in inches?", v,
    [(F(5, 14), "added the numerators and the denominators straight across"),
     (F(1, 2) + F(3, 8) - F(1, 4), "subtracted the last piece instead of adding it"),
     (F(1, 2) + F(3, 8), "dropped the smallest piece when adding")],
    "Using eighths: 4/8 + 3/8 + 2/8 = 9/8, which is 1 1/8 inches.")

pieces = F(100, F(5, 2)); assert pieces == 40
add(22, ["algebra.word"], "How many 2 1/2-foot pieces can be cut from a 100-foot length, "
    "ignoring waste?", pieces,
    [(F(100, 2), "rounded the piece length down to 2 feet"),
     (100 * F(5, 2), "multiplied instead of divided"),
     (F(100, 3), "rounded the piece length up to 3 feet")],
    "Divide the total by the piece length: 100 ÷ 2.5 = 40 pieces.")

v = 12 * 8 - 3 * 8; assert v == 72
add(23, ["algebra.word"], "A crew of 12 works an 8-hour shift, but 3 of them leave for the whole shift. "
    "How many worker-hours are actually put in?", v,
    [(12 * 8, "counted the full crew"),
     (3 * 8, "counted only the workers who left"),
     ((12 - 3) * 8 + 8, "added an extra worker's shift")],
    "Nine workers each put in 8 hours, giving 72 worker-hours.")

markup = F(20, 100); cost = 85
v = cost * (1 + markup); assert v == 102
add(24, ["arith.percent"], "A part costing $85 is sold with a 20% markup. What is the selling price?", v,
    [(cost * markup, "gave the markup amount instead of the selling price"),
     (cost - cost * markup, "subtracted the markup instead of adding it"),
     (cost + 20, "added 20 dollars instead of 20 percent")],
    "A 20% markup adds 0.20 × 85 = $17 to the cost, giving $102.",
    fmt=lambda x: f"${num(x)}")

v = F(3 * 60, 45); assert v == 4
add(25, ["rate.work"], "A machine produces a part every 45 seconds. "
    "How many parts does it produce in 3 minutes?", v,
    [(F(3, 45), "divided the minutes by the seconds without converting"),
     (3 * 45, "multiplied instead of dividing"),
     (F(3 * 60, 30), "used 30 seconds per part instead of 45")],
    "Three minutes is 180 seconds, and 180 ÷ 45 = 4 parts.")

if __name__ == "__main__":
    assert len(items) == 25, f"expected 25, got {len(items)}"
    print(f"GAN Form B section 3 (Problem Solving): {len(items)} items verified")
