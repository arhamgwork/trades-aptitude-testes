# -*- coding: utf-8 -*-
"""GAN battery Form B — Section 5, Mechanical Aptitude (25 items).

Gears, pulleys, levers, hydraulics and simple circuits. Every value is computed
numerically and the diagram is built from the same numbers the stem quotes, so
the drawing cannot disagree with the question.
"""
import sys, os
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(__file__))
from common import Item
import mech_svg as M

S = "s5"
items = []

def num(x):
    if isinstance(x, F):
        if x.denominator == 1:
            return str(x.numerator)
        whole, rem = divmod(abs(x.numerator), x.denominator)
        sign = "-" if x < 0 else ""
        return f"{sign}{whole} {rem}/{x.denominator}" if whole else f"{sign}{rem}/{x.denominator}"
    return str(x)

def add(n, skills, stem, key, distractors, explanation, verify, fig=None,
        difficulty="medium", fmt=num):
    vals = [fmt(key)] + [fmt(d[0]) for d in distractors]
    assert len(set(vals)) == len(vals), f"s5-{n}: duplicate choices {vals}"
    items.append(Item(f"ganb-s5-{n:03d}", S, skills, stem, key, distractors,
                      explanation, verify, difficulty, figure=fig, formatter=fmt))

# ---------------------------------------------------------------- gears
GEARS = [(12, 36, 120), (15, 45, 90), (20, 40, 100), (24, 12, 60)]
for n, (t1, t2, rpm1) in enumerate(GEARS, start=1):
    rpm2 = F(t1 * rpm1, t2)
    assert rpm2 * t2 == rpm1 * t1, "gear relation must hold"
    add(n, ["mech.gears"],
        f"Gear A has {t1} teeth and gear B has {t2} teeth. They are meshed together. "
        f"If gear A turns at {rpm1} rpm, how fast does gear B turn?",
        rpm2,
        [(F(t2 * rpm1, t1), "inverted the ratio, so the answer moves the wrong way"),
         (rpm1, "assumed meshed gears always turn at the same speed"),
         (F(rpm1 * (t1 + t2), t2), "added the tooth counts instead of taking their ratio")],
        f"Teeth times speed is the same on both gears: {t1} × {rpm1} = {t2} × speed, "
        f"so gear B turns at {num(rpm2)} rpm. The gear with fewer teeth always turns faster.",
        "python:gear-ratio", M.gear_pair(t1, t2),
        fmt=lambda v: f"{num(v)} rpm")

add(5, ["mech.gears"],
    "Two gears are meshed directly together. Gear A turns clockwise. Which way does gear B turn?",
    "Counter-clockwise",
    [("Clockwise", "meshed gears drive each other in opposite directions, not the same one"),
     ("It depends on which gear has more teeth", "tooth count changes the speed, not the direction"),
     ("It does not turn at all", "meshed gears do drive one another")],
    "Two gears meshed directly turn in opposite directions. Tooth count sets the "
    "speed; only an idler gear between them would restore the original direction.",
    "conceptual:blind-solve", M.gear_pair(18, 30), "easy", fmt=str)

add(6, ["mech.gears"],
    "A small gear drives a large gear. Compared with the small gear, the large gear turns",
    "more slowly, with more turning force",
    [("more slowly, with less turning force", "speed and turning force trade in opposite directions, not the same one"),
     ("faster, with more turning force", "the larger gear cannot turn faster than the smaller one driving it"),
     ("at the same speed and force", "a change in tooth count must change the speed")],
    "Driving a larger gear from a smaller one trades speed for turning force: the "
    "large gear turns more slowly and delivers more torque.",
    "conceptual:blind-solve", M.gear_pair(14, 42), fmt=str)

# ---------------------------------------------------------------- pulleys
PULLEY = [(4, 400), (2, 300), (5, 250), (3, 180)]
for n, (lines, load) in enumerate(PULLEY, start=7):
    effort = F(load, lines)
    assert effort * lines == load
    add(n, ["mech.pulleys"],
        f"A block and tackle supports a {load} lb load on {lines} supporting lines. "
        f"Ignoring friction, how much effort is needed to hold the load?",
        effort,
        [(load * lines, "multiplied by the number of lines instead of dividing"),
         (load, "ignored the mechanical advantage entirely"),
         (F(load, lines + 1), "counted one supporting line too many")],
        f"The supporting lines share the load, so the effort is {load} ÷ {lines} = "
        f"{num(effort)} lb. The rope must be pulled {lines} feet to raise the load one foot — "
        f"what is gained in force is paid for in distance.",
        "python:mechanical-advantage", M.pulley_block(lines, load),
        fmt=lambda v: f"{num(v)} lb")

add(11, ["mech.pulleys"],
    "A single fixed pulley bolted to a beam is used to raise a load. Its main purpose is to",
    "change the direction of the pull without changing the force needed",
    [("halve the force needed to lift the load", "a single fixed pulley gives no mechanical advantage"),
     ("double the speed at which the load rises", "a fixed pulley does not change speed"),
     ("hold the load without any effort at all", "the full load must still be supported")],
    "A fixed pulley redirects the rope so the load can be raised by pulling down, "
    "but only one line supports the load, so the effort still equals the load.",
    "conceptual:blind-solve", M.pulley_block(1, 200), fmt=str)

# ---------------------------------------------------------------- levers
LEVERS = [(6, 2, 90), (8, 2, 60), (5, 1, 40), (9, 3, 120)]
for n, (d_e, d_l, load) in enumerate(LEVERS, start=12):
    effort = F(load * d_l, d_e)
    assert effort * d_e == load * d_l, "torque must balance"
    add(n, ["mech.levers"],
        f"A lever balances on a fulcrum. The load of {load} lb sits {d_l} ft from the fulcrum "
        f"and the effort is applied {d_e} ft from it on the other side. "
        f"How much effort is needed to balance the load?",
        effort,
        [(F(load * d_e, d_l), "used the distances the wrong way round"),
         (load, "ignored the difference in distances"),
         (F(load, d_e + d_l), "divided by the total length instead of balancing the two turning effects")],
        f"Turning effect is force times distance, and the two sides must match: "
        f"effort × {d_e} = {load} × {d_l}, so the effort is {num(effort)} lb. "
        f"The longer the effort arm, the less force is needed.",
        "python:torque-balance", M.lever(d_e, d_l, load),
        fmt=lambda v: f"{num(v)} lb")

add(16, ["mech.levers"],
    "On a lever, moving the fulcrum closer to the load while the effort stays where it is",
    "reduces the effort needed",
    [("increases the effort needed", "this shortens the load arm and lengthens the effort arm, which helps rather than hurts"),
     ("makes no difference to the effort", "the ratio of the two arms is exactly what sets the effort"),
     ("prevents the lever from balancing at all", "the lever still balances, just at a different effort")],
    "Moving the fulcrum toward the load shortens the load arm and lengthens the "
    "effort arm, so less force balances the same load.",
    "conceptual:blind-solve", M.lever(8, 2, 100), fmt=str)

# ---------------------------------------------------------------- hydraulics
HYD = [(2, 10, 50), (3, 12, 60), (4, 20, 30)]
for n, (a_small, a_big, f_in) in enumerate(HYD, start=17):
    pressure = F(f_in, a_small)
    f_out = pressure * a_big
    assert f_out * a_small == f_in * a_big
    add(n, ["mech.hydraulics"],
        f"Two pistons are connected by a closed fluid line. A force of {f_in} lb is applied to "
        f"the small piston, which has an area of {a_small} square inches. The large piston has "
        f"an area of {a_big} square inches. What force does the large piston deliver?",
        f_out,
        [(F(f_in * a_small, a_big), "inverted the area ratio"),
         (f_in, "assumed the force passes through unchanged"),
         (f_in + a_big - a_small, "added the areas instead of taking their ratio")],
        f"Pressure is the same throughout the fluid: {f_in} ÷ {a_small} = {num(pressure)} psi. "
        f"Acting on {a_big} square inches, that pressure gives {num(f_out)} lb. "
        f"The large piston moves a shorter distance in exchange.",
        "python:pressure", M.pistons(a_small, a_big, f_in),
        fmt=lambda v: f"{num(v)} lb")

add(20, ["mech.hydraulics"],
    "Fluid flows at a steady rate through a pipe that narrows partway along its length. "
    "In the narrower section, the speed of the fluid",
    "increases",
    [("decreases in proportion to the smaller area", "the same volume per second through a smaller opening must move faster, not slower"),
     ("stays the same as in the wider section", "the cross-section changed, so the speed must change"),
     ("depends only on the pressure, not the pipe size", "the flow rate and the cross-section together fix the speed")],
    "The same volume passes every point each second, so a smaller cross-section "
    "forces the fluid to move faster.",
    "conceptual:blind-solve", fmt=str)

# ---------------------------------------------------------------- circuits
add(21, ["mech.circuits"],
    "Two resistors of 4 Ω and 6 Ω are wired in series across a 12 V supply. "
    "What is the total resistance?",
    10,
    [(F(4 * 6, 4 + 6), "used the parallel rule instead of the series rule"),
     (24, "multiplied the two resistances"), (2, "subtracted the two resistances")],
    "Resistances in series add: 4 + 6 = 10 Ω.",
    "python:circuit", M.circuit([4, 6], 12, "series"), "easy",
    fmt=lambda v: f"{num(v)} Ω")

add(22, ["mech.circuits"],
    "Two resistors of 4 Ω and 12 Ω are wired in parallel. What is the total resistance?",
    F(4 * 12, 4 + 12),
    [(16, "added them as though they were in series"),
     (48, "multiplied without dividing by the sum"),
     (8, "averaged the two resistances")],
    "For two resistors in parallel the total is the product over the sum: "
    "(4 × 12) ÷ 16 = 3 Ω. The total is always less than the smaller resistor.",
    "python:circuit", M.circuit([4, 12], 12, "parallel"),
    fmt=lambda v: f"{num(v)} Ω")

add(23, ["mech.circuits"],
    "A 24 V supply drives a circuit whose total resistance is 6 Ω. What current flows?",
    F(24, 6),
    [(24 * 6, "multiplied volts by ohms instead of dividing"),
     (F(6, 24), "divided ohms by volts"), (24 - 6, "subtracted the resistance from the voltage")],
    "Current is voltage divided by resistance: 24 ÷ 6 = 4 amps.",
    "python:circuit", M.circuit([6], 24, "series"), "easy",
    fmt=lambda v: f"{num(v)} A")

add(24, ["mech.circuits"],
    "Three lamps are wired in series. If one lamp burns out, the others",
    "go out as well, because the circuit is broken",
    [("stay lit at the same brightness", "a series circuit has only one path, so a break stops everything"),
     ("stay lit but get brighter", "no current flows once the single path is broken"),
     ("stay lit but get dimmer", "no current flows at all, so they cannot stay lit")],
    "A series circuit offers a single path. Breaking it anywhere stops the current "
    "everywhere, so all the lamps go out.",
    "conceptual:blind-solve", None, "easy", fmt=str)

add(25, ["mech.levers"],
    "A ramp is used to raise a heavy crate to a loading dock. Compared with lifting the crate "
    "straight up, using a longer ramp means",
    "less force is needed, but it must be applied over a greater distance",
    [("less force is needed, over the same distance", "the work done cannot fall, so a shorter distance is impossible"),
     ("more force is needed over a greater distance", "a ramp reduces the force needed, it does not increase it"),
     ("the same force is needed, over a greater distance", "a longer ramp does reduce the force")],
    "A ramp trades force for distance. The work done is the same either way, so a "
    "gentler slope needs less push but a longer push.",
    "conceptual:blind-solve", None, fmt=str)

if __name__ == "__main__":
    assert len(items) == 25, f"expected 25, got {len(items)}"
    figs = sum(1 for i in items if i.d["figure"])
    comp = sum(1 for i in items if i.d["verify"].startswith("python:"))
    print(f"GAN Form B section 5 (Mechanical Aptitude): {len(items)} items verified")
    print(f"  with a diagram: {figs}, computationally checked: {comp}, conceptual: {len(items)-comp}")
