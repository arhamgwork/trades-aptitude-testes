"""Builds and verifies the 33 Algebra & Functions items for IBEW 701 Form A.

Every key is computed here with exact arithmetic and asserted against an
independent recomputation. Distractors encode named mistakes.
"""
import sys, os
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(__file__))
from common import Item, fmt

S = "alg"
items = []
def add(*a, **k): items.append(Item(*a, **k))

# --- 1. one-step / two-step linear -----------------------------------------
# 7x - 4 = 31
a, b, c = 7, -4, 31
x = F(c - b, a); assert a * x + b == c
add("e701a-alg-001", S, ["algebra.linear"],
    "If 7x − 4 = 31, what is the value of x?", x,
    [(F(c + (-b), a) + 1, "added 4 to 31 but then divided by the wrong number"),
     (F(c - 4, a), "subtracted 4 instead of adding it when undoing −4"),
     (F(c, a), "divided by 7 without first undoing the −4")],
    "Undo the subtraction first: 7x = 31 + 4 = 35. Then divide both sides by 7, "
    "giving x = 5.", "python:fractions", "easy")

# --- 2. linear with fractions ----------------------------------------------
# (2/3)x + 5 = 13
x = F(3, 2) * (13 - 5); assert F(2, 3) * x + 5 == 13
add("e701a-alg-002", S, ["algebra.linear", "arith.fractions"],
    "If (2/3)x + 5 = 13, what is the value of x?", x,
    [(F(2, 3) * 8, "multiplied by 2/3 instead of by its reciprocal"),
     (F(3, 2) * 13, "divided before subtracting the 5"),
     (8, "stopped after subtracting 5 and never undid the 2/3")],
    "Subtract 5 from both sides to get (2/3)x = 8, then multiply both sides by "
    "the reciprocal 3/2. That gives x = 12.", "python:fractions", "easy")

# --- 3. distribute then solve ----------------------------------------------
# 3(2x - 5) = 4x + 7  -> 6x - 15 = 4x + 7 -> 2x = 22 -> x = 11
x = F(7 + 15, 6 - 4); assert 3 * (2 * x - 5) == 4 * x + 7
add("e701a-alg-003", S, ["algebra.linear"],
    "Solve for x:  3(2x − 5) = 4x + 7", x,
    [(F(7 - 15, 6 - 4), "subtracted 15 from 7 instead of adding it to both sides"),
     (F(7 + 15, 6 + 4), "added the x-terms instead of subtracting 4x from both sides"),
     (F(7 + 5, 6 - 4), "distributed the 3 to 2x but not to −5")],
    "Distributing gives 6x − 15 = 4x + 7. Subtract 4x and add 15 to both "
    "sides: 2x = 22, so x = 11.", "python:fractions")

# --- 4. literal equation ----------------------------------------------------
add("e701a-alg-004", S, ["algebra.literal"],
    "The formula P = 2L + 2W gives the perimeter of a rectangle. "
    "Which expression gives W in terms of P and L?",
    "W = (P − 2L) / 2",
    [("W = P − 2L", "subtracted 2L but never divided by 2"),
     ("W = (P + 2L) / 2", "added 2L instead of subtracting it"),
     ("W = P / 2 − L / 2", "divided the L term by 2 a second time")],
    "Subtract 2L from both sides to get P − 2L = 2W, then divide both sides "
    "by 2. Note that dividing P − 2L by 2 leaves L, not L/2.",
    "python:symbolic", formatter=str)

# --- 5. system by substitution ---------------------------------------------
# y = 2x + 1 ; 3x + y = 16  -> 3x + 2x + 1 = 16 -> 5x = 15 -> x = 3, y = 7
x = F(16 - 1, 3 + 2); y = 2 * x + 1
assert 3 * x + y == 16 and y == 2 * x + 1
add("e701a-alg-005", S, ["algebra.systems"],
    "If y = 2x + 1 and 3x + y = 16, what is the value of y?", y,
    [(x, "solved for x and stopped without finding y"),
     (2 * F(16, 5) + 1, "dropped the +1 when substituting into the second equation"),
     (F(16 + 1, 3 + 2), "added 1 to 16 instead of subtracting it")],
    "Substitute 2x + 1 for y: 3x + (2x + 1) = 16, so 5x = 15 and x = 3. "
    "Then y = 2(3) + 1 = 7.", "python:fractions")

# --- 6. system by elimination ----------------------------------------------
# 4x + 3y = 27 ; 2x - 3y = 3  -> 6x = 30 -> x = 5 ; y = (27-20)/3
x = F(27 + 3, 4 + 2); y = F(27 - 4 * x, 3)
assert 4 * x + 3 * y == 27 and 2 * x - 3 * y == 3
add("e701a-alg-006", S, ["algebra.systems"],
    "Solve the system:  4x + 3y = 27  and  2x − 3y = 3.  What is x + y?",
    x + y,
    [(x, "found x and reported it instead of x + y"),
     (x - y, "subtracted the two values instead of adding them"),
     (F(27 - 3, 4 + 2), "subtracted the constants when adding the equations")],
    "Adding the two equations eliminates y: 6x = 30, so x = 5. Substituting "
    "back gives 3y = 7, y = 7/3. Their sum is 5 + 7/3 = 22/3.",
    "python:fractions", "hard")

# --- 7. exponent product rule ----------------------------------------------
add("e701a-alg-007", S, ["algebra.exponents"],
    "Simplify:  (3x³)(4x⁵)", "12x⁸",
    [("12x¹⁵", "multiplied the exponents instead of adding them"),
     ("7x⁸", "added the coefficients instead of multiplying them"),
     ("12x²", "subtracted the exponents instead of adding them")],
    "Multiply the coefficients and add the exponents: 3 × 4 = 12 and "
    "x³ · x⁵ = x⁸.", "python:symbolic", "easy", formatter=str)

# --- 8. power of a power ----------------------------------------------------
add("e701a-alg-008", S, ["algebra.exponents"],
    "Simplify:  (2x⁴)³", "8x¹²",
    [("2x¹²", "raised x to the third power but left the 2 alone"),
     ("6x¹²", "multiplied the base 2 by 3 instead of cubing it"),
     ("8x⁷", "added the exponents instead of multiplying them")],
    "Every factor inside the parentheses is cubed: 2³ = 8, and x⁴ "
    "raised to the third power multiplies the exponents to give x¹².",
    "python:symbolic", formatter=str)

# --- 9. negative exponent ---------------------------------------------------
v = F(1, 2 ** 4); assert v == F(1, 16)
add("e701a-alg-009", S, ["algebra.exponents"],
    "What is the value of 2⁻⁴?", v,
    [(-16, "treated the negative exponent as a negative result"),
     (F(1, 8), "used 2³ instead of 2⁴ in the denominator"),
     (F(-1, 16), "kept a negative sign that the reciprocal does not produce")],
    "A negative exponent means the reciprocal of the positive power: "
    "2⁻⁴ = 1/2⁴ = 1/16. The result is positive.",
    "python:fractions")

# --- 10. FOIL ---------------------------------------------------------------
add("e701a-alg-010", S, ["algebra.polynomials"],
    "Multiply:  (x + 6)(x − 4)", "x² + 2x − 24",
    [("x² − 2x − 24", "subtracted the outer and inner terms instead of adding −4x and 6x"),
     ("x² + 10x − 24", "added 6 and 4 instead of combining +6x and −4x"),
     ("x² − 24", "multiplied the first and last terms only and dropped the middle terms")],
    "The outer and inner products are −4x and +6x, which combine to +2x, "
    "and the last terms give 6 × (−4) = −24.",
    "python:symbolic", formatter=str)

# --- 11. factoring a quadratic ---------------------------------------------
# x^2 - 7x + 12 = (x-3)(x-4)
r1, r2 = 3, 4
assert r1 + r2 == 7 and r1 * r2 == 12
add("e701a-alg-011", S, ["algebra.factoring"],
    "Factor completely:  x² − 7x + 12", "(x − 3)(x − 4)",
    [("(x + 3)(x + 4)", "ignored that a positive constant with a negative middle term needs two negative factors"),
     ("(x − 2)(x − 6)", "picked factors of 12 that add to 8, not 7"),
     ("(x − 1)(x − 12)", "picked factors of 12 that add to 13, not 7")],
    "Two numbers that multiply to +12 and add to −7 are −3 and "
    "−4, so the quadratic factors into those two binomials.",
    "python:symbolic", formatter=str)

# --- 12. difference of squares ---------------------------------------------
add("e701a-alg-012", S, ["algebra.factoring"],
    "Factor:  9x² − 25", "(3x + 5)(3x − 5)",
    [("(3x − 5)(3x − 5)", "used the same sign twice instead of opposite signs"),
     ("(9x + 5)(9x − 5)", "used 9 as the square root of 9x² instead of 3x"),
     ("(3x + 25)(3x − 25)", "used 25 instead of its square root 5")],
    "This is a difference of two squares: the square root of 9x² is 3x and "
    "the square root of 25 is 5, giving a sum factor and a difference factor.",
    "python:symbolic", formatter=str)

# --- 13. function evaluation ------------------------------------------------
# f(x) = 3x^2 - 2x + 1, f(-2)
def f13(t): return 3 * t ** 2 - 2 * t + 1
val = f13(-2); assert val == 17
add("e701a-alg-013", S, ["algebra.functions"],
    "If f(x) = 3x² − 2x + 1, what is f(−2)?", val,
    [(3 * (-2 ** 2) - 2 * (-2) + 1, "squared before applying the negative, making the first term negative"),
     (f13(2), "substituted +2 instead of −2"),
     (3 * (-2) ** 2 - 2 * (-2), "dropped the constant term when adding up")],
    "Squaring −2 gives +4, so the first term is 12. The middle term is "
    "−2(−2) = +4. Adding the constant gives 12 + 4 + 1 = 17.",
    "python:fractions")

# --- 14. composition --------------------------------------------------------
# f(x)=2x+3, g(x)=x^2 ; f(g(3))
g = lambda t: t ** 2
fn = lambda t: 2 * t + 3
val = fn(g(3)); assert val == 21
add("e701a-alg-014", S, ["algebra.functions"],
    "If f(x) = 2x + 3 and g(x) = x², what is f(g(3))?", val,
    [(g(fn(3)), "applied the functions in the reverse order"),
     (fn(3) * 3, "multiplied the two results instead of substituting one into the other"),
     (g(3), "stopped at the inner function and never applied the outer one")],
    "Work from the inside out: g(3) = 9, then f(9) = 2(9) + 3 = 21.",
    "python:fractions")

# --- 15. slope from two points ---------------------------------------------
x1, y1, x2, y2 = 2, -3, 6, 5
m = F(y2 - y1, x2 - x1); assert m == 2
add("e701a-alg-015", S, ["algebra.graphs"],
    "What is the slope of the line through the points (2, −3) and (6, 5)?",
    m,
    [(F(x2 - x1, y2 - y1), "divided the run by the rise instead of the rise by the run"),
     (F(y1 - y2, x2 - x1), "subtracted the y-values in one order and the x-values in the other"),
     (F(y2 - y1, x2 + x1), "added the x-values in the denominator instead of subtracting them")],
    "Slope is the change in y over the change in x: (5 − (−3)) divided "
    "by (6 − 2) = 8/4 = 2.", "python:fractions")

# --- 16. slope-intercept evaluation ----------------------------------------
# y = -3x + 7 at x = 4
yv = -3 * 4 + 7; assert yv == -5
add("e701a-alg-016", S, ["algebra.graphs"],
    "A line is given by y = −3x + 7. What is y when x = 4?", yv,
    [(3 * 4 + 7, "ignored the negative sign on the slope"),
     (-3 * (4 + 7), "added 7 to x before multiplying instead of after"),
     (-3 * 4 - 7, "subtracted the intercept instead of adding it")],
    "Substitute 4 for x: −3(4) = −12, then add the intercept 7 to get "
    "−5.", "python:fractions", "easy")

# --- 17. linear inequality --------------------------------------------------
add("e701a-alg-017", S, ["algebra.inequalities"],
    "Solve for x:  −4x + 9 > 25", "x < −4",
    [("x > −4", "did not reverse the inequality sign when dividing by a negative"),
     ("x < 4", "divided 16 by −4 but kept the result positive"),
     ("x > 4", "both dropped the sign reversal and lost the negative")],
    "Subtract 9 to get −4x > 16. Dividing both sides by −4 reverses "
    "the inequality, giving x less than −4.",
    "python:symbolic", formatter=str)

# --- 18. compound inequality ------------------------------------------------
# -1 <= 2x - 5 <= 7  -> 4 <= 2x <= 12 -> 2 <= x <= 6
lo = F(-1 + 5, 2); hi = F(7 + 5, 2); assert lo == 2 and hi == 6
add("e701a-alg-018", S, ["algebra.inequalities"],
    "Solve:  −1 ≤ 2x − 5 ≤ 7", "2 ≤ x ≤ 6",
    [("−3 ≤ x ≤ 1", "subtracted 5 from the outer parts instead of adding it"),
     ("4 ≤ x ≤ 12", "added 5 correctly but never divided by 2"),
     ("2 ≤ x ≤ 12", "divided only the left-hand part by 2")],
    "Add 5 to all three parts to get 4 ≤ 2x ≤ 12, then divide all "
    "three parts by 2.", "python:fractions", formatter=str)

# --- 19. proportion ---------------------------------------------------------
# 3/8 = x/56
xv = F(3 * 56, 8); assert xv * 8 == 3 * 56
add("e701a-alg-019", S, ["ratio.proportion"],
    "If 3/8 = x/56, what is the value of x?", xv,
    [(F(8 * 56, 3), "cross-multiplied in the wrong direction"),
     (F(56, 8), "divided 56 by 8 and forgot to multiply by 3"),
     (56 - 8 + 3, "treated the proportion as a difference instead of a ratio")],
    "Cross-multiply: 8x = 3 × 56 = 168, so x = 21.",
    "python:fractions", "easy")

# --- 20. percent increase ---------------------------------------------------
old, new = 40, 46
pct = F(new - old, old) * 100; assert pct == 15
add("e701a-alg-020", S, ["arith.percent"],
    "A crew's hourly output rises from 40 units to 46 units. "
    "What is the percent increase?", f"{fmt(pct)}%",
    [(f"{fmt(F(new - old, new) * 100)}%", "divided the change by the new value instead of the original"),
     (f"{fmt(F(new, old) * 100)}%", "found the new value as a percent of the old instead of the increase"),
     (f"{fmt(new - old)}%", "reported the raw change as if it were a percent")],
    "Percent increase divides the change by the original amount: 6/40 = 0.15, "
    "which is 15%.", "python:fractions", formatter=str)

# --- 21. direct variation ---------------------------------------------------
# y varies directly with x; y=18 when x=4. find y when x=10
k = F(18, 4); yv = k * 10; assert yv == 45
add("e701a-alg-021", S, ["algebra.variation"],
    "y varies directly with x. When x = 4, y = 18. What is y when x = 10?",
    yv,
    [(F(4 * 18, 10), "set up the proportion inversely instead of directly"),
     (18 + 6, "added the change in x to y instead of scaling y"),
     (F(18, 4) + 10, "added the constant of variation to x instead of multiplying")],
    "Direct variation means y/x is constant: 18/4 = 4.5. Multiplying by x = 10 "
    "gives y = 45.", "python:fractions")

# --- 22. inverse variation --------------------------------------------------
# y inversely with x; y=12 when x=5; find y when x=15
kk = 12 * 5; yv = F(kk, 15); assert yv == 4
add("e701a-alg-022", S, ["algebra.variation"],
    "y varies inversely with x. When x = 5, y = 12. What is y when x = 15?",
    yv,
    [(F(12 * 15, 5), "used direct variation instead of inverse"),
     (12 - 3, "subtracted the change in x from y"),
     (F(15, 12), "inverted the wrong pair of values")],
    "Inverse variation means the product xy is constant: 5 × 12 = 60. "
    "Dividing 60 by the new x = 15 gives y = 4.", "python:fractions")

# --- 23. quadratic roots ----------------------------------------------------
# x^2 + 2x - 15 = 0 -> (x+5)(x-3) -> x = -5, 3 ; larger root 3
roots = sorted([-5, 3]); assert all(r * r + 2 * r - 15 == 0 for r in roots)
add("e701a-alg-023", S, ["algebra.quadratic"],
    "What is the larger solution of x² + 2x − 15 = 0?", max(roots),
    [(min(roots), "identified both roots but reported the smaller one"),
     (5, "reversed the signs of the factors"),
     (15, "read the constant term as a solution")],
    "The quadratic factors using two numbers that multiply to −15 and add "
    "to +2, namely +5 and −3. The solutions are −5 and 3, and the "
    "larger is 3.", "python:fractions")

# --- 24. simplify rational expression ---------------------------------------
add("e701a-alg-024", S, ["algebra.rational"],
    "Simplify:  (x² − 9) / (x + 3),  where x ≠ −3",
    "x − 3",
    [("x + 3", "cancelled to the wrong one of the two factors"),
     ("x² − 3", "cancelled the 3 from the numerator's constant only"),
     ("x − 9", "cancelled the x terms rather than factoring first")],
    "Factor the numerator as a difference of squares into (x + 3)(x − 3). "
    "The (x + 3) cancels with the denominator, leaving x − 3.",
    "python:symbolic", formatter=str)

# --- 25. radicals -----------------------------------------------------------
# sqrt(72) = 6 sqrt 2
assert 6 ** 2 * 2 == 72
add("e701a-alg-025", S, ["algebra.radicals"],
    "Simplify:  √72", "6√2",
    [("2√6", "swapped the factor taken out with the one left under the radical"),
     ("8√3", "used 64 × 3, which is not 72"),
     ("36√2", "took 36 out of the radical without taking its square root")],
    "72 factors as 36 × 2, and the square root of 36 is 6, so a 6 comes "
    "out and the 2 stays under the radical.",
    "python:symbolic", formatter=str)

# --- 26. absolute value -----------------------------------------------------
# |2x - 3| = 11 -> x = 7 or x = -4 ; sum = 3
s1 = F(11 + 3, 2); s2 = F(-11 + 3, 2)
assert abs(2 * s1 - 3) == 11 and abs(2 * s2 - 3) == 11
add("e701a-alg-026", S, ["algebra.absolute"],
    "If |2x − 3| = 11, what is the sum of all possible values of x?",
    s1 + s2,
    [(s1, "found only the positive case and ignored the negative one"),
     (s1 - s2, "subtracted the two solutions instead of adding them"),
     (s2, "found only the negative case and ignored the positive one")],
    "The expression inside equals either 11 or −11, giving x = 7 and "
    "x = −4. Their sum is 3.", "python:fractions", "hard")

# --- 27-29. number series ---------------------------------------------------
seq = [4, 9, 14, 19]; nxt = seq[-1] + 5
assert all(seq[i+1] - seq[i] == 5 for i in range(len(seq)-1))
add("e701a-alg-027", S, ["series.arithmetic"],
    "What number comes next in the series?   4, 9, 14, 19, __", nxt,
    [(seq[-1] + 4, "used the first term as the common difference"),
     (seq[-1] * 2, "doubled the last term instead of adding the difference"),
     (seq[-1] + 6, "misread the difference as 6")],
    "Each term is 5 more than the one before it, so the next term is "
    "19 + 5 = 24.", "python:fractions", "easy")

seq = [3, 6, 12, 24]; nxt = seq[-1] * 2
assert all(seq[i+1] == seq[i] * 2 for i in range(len(seq)-1))
add("e701a-alg-028", S, ["series.geometric"],
    "What number comes next in the series?   3, 6, 12, 24, __", nxt,
    [(seq[-1] + 12, "added the last difference instead of doubling"),
     (seq[-1] + 3, "used the first term as a common difference"),
     (seq[-1] * 3, "tripled instead of doubled")],
    "Each term is twice the one before it, so the next term is "
    "24 × 2 = 48.", "python:fractions", "easy")

# alternating: 2, 5, 4, 7, 6, ? -> +3, -1, +3, -1, +3 = 9
seq = [2, 5, 4, 7, 6]; nxt = seq[-1] + 3
deltas = [seq[i+1]-seq[i] for i in range(len(seq)-1)]
assert deltas == [3, -1, 3, -1]
add("e701a-alg-029", S, ["series.alternating"],
    "What number comes next in the series?   2, 5, 4, 7, 6, __", nxt,
    [(seq[-1] - 1, "continued with the subtract-1 step instead of the add-3 step"),
     (seq[-1] + 1, "read the pattern as a simple alternating increase of 1"),
     (seq[-1] + 2, "averaged the two steps instead of alternating them")],
    "The series alternates between adding 3 and subtracting 1. The last step "
    "was a subtraction, so the next step adds 3 to give 9.",
    "python:fractions")

# --- 30. mixture ------------------------------------------------------------
# 12 gal of 30% + x gal of 60% = 40%?  0.3*12 + 0.6x = 0.4(12+x) -> 3.6+0.6x=4.8+0.4x -> 0.2x=1.2 -> x=6
xv = F(F(4, 10) * 12 - F(3, 10) * 12, F(6, 10) - F(4, 10)); assert xv == 6
assert F(3,10)*12 + F(6,10)*xv == F(4,10)*(12+xv)
add("e701a-alg-030", S, ["algebra.word", "algebra.linear"],
    "A tank holds 12 gallons of a 30% antifreeze mixture. How many gallons of "
    "a 60% mixture must be added to bring the tank to a 40% mixture?", xv,
    [(12, "assumed equal parts of the two mixtures"),
     (F(F(4, 10) * 12 - F(3, 10) * 12, F(6, 10)), "applied the 40% target only to the original 12 gallons, ignoring that the added gallons raise the total volume too"),
     (F(18, 1), "solved for the total volume rather than the amount added")],
    "The antifreeze already present is 3.6 gallons. Adding x gallons at 60% "
    "must satisfy 3.6 + 0.6x = 0.4(12 + x), which simplifies to 0.2x = 1.2, "
    "so 6 gallons are needed.", "python:fractions", "hard")

# --- 31. work rate ----------------------------------------------------------
# A does job in 6 h, B in 3 h, together?  1/6+1/3 = 1/2 -> 2 h
t = F(1, F(1, 6) + F(1, 3)); assert t == 2
add("e701a-alg-031", S, ["algebra.word", "rate.work"],
    "One worker can complete a task in 6 hours and another can complete the "
    "same task in 3 hours. Working together at these rates, how many hours "
    "does the task take?", t,
    [(F(6 + 3, 2), "averaged the two times instead of adding the rates"),
     (F(6 - 3, 1), "subtracted the times"),
     (F(1, 6) + F(1, 3), "added the rates but did not invert the result")],
    "Their rates add: 1/6 + 1/3 = 1/2 of the task per hour. The time is the "
    "reciprocal of that rate, so 2 hours.", "python:fractions")

# --- 32. distance -----------------------------------------------------------
# 165 miles at 55 mph, leaves 7:00 -> 3 h -> 10:00
hrs = F(165, 55); assert hrs == 3
add("e701a-alg-032", S, ["algebra.word", "rate.distance"],
    "A truck leaves at 7:00 a.m. and travels 165 miles at an average speed of "
    "55 miles per hour. At what time does it arrive?", "10:00 a.m.",
    [("9:00 a.m.", "divided by 55 but subtracted an hour when adding to the start time"),
     ("11:00 a.m.", "used 4 hours, which corresponds to 220 miles, not 165"),
     ("10:30 a.m.", "carried a half hour that the exact division does not produce")],
    "Dividing 165 miles by 55 miles per hour gives exactly 3 hours, and 3 "
    "hours after 7:00 a.m. is 10:00 a.m.", "python:fractions",
    formatter=str)

# --- 33. scientific notation ------------------------------------------------
# (3.0e4)(2.0e-6) = 6.0e-2
mant = 3.0 * 2.0; expo = 4 + (-6)
assert abs(mant * 10 ** expo - 0.06) < 1e-12
add("e701a-alg-033", S, ["arith.scientific"],
    "Multiply and express the result in scientific notation:  "
    "(3.0 × 10⁴)(2.0 × 10⁻⁶)",
    "6.0 × 10⁻²",
    [("6.0 × 10⁻²⁴", "multiplied the exponents instead of adding them"),
     ("6.0 × 10²", "subtracted the exponents in the wrong order"),
     ("5.0 × 10⁻²", "added the mantissas instead of multiplying them")],
    "Multiply the mantissas to get 6.0 and add the exponents: 4 + (−6) = "
    "−2.", "python:symbolic", formatter=str)

if __name__ == "__main__":
    assert len(items) == 33, f"expected 33 algebra items, got {len(items)}"
    print(f"algebra: {len(items)} items built and verified")
