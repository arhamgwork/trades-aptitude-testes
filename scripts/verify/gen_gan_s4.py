# -*- coding: utf-8 -*-
"""GAN battery Form B — Section 4, Reading Comprehension (25 items).

Five original technical passages, five questions each. Keys here cannot be
computed, so every item carries verify="blind-solve" and is checked by an
independent solver that never sees the key.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import Item

S = "s4"
items = []
passages = []

def P(pid, title, text):
    passages.append({"id": pid, "title": title, "text": text.strip()})

def Q(n, pid, skills, stem, correct, distractors, explanation, difficulty="medium"):
    items.append(Item(f"ganb-s4-{n:03d}", S, skills, stem, correct, distractors,
                      explanation, "blind-solve", difficulty,
                      passage_id=pid, formatter=str))

# ------------------------------------------------------------------ passage 1
P("gb1", "Gauge numbers run backwards", """
Sheet metal thickness is given as a gauge number, and the scale runs opposite to
the way most people expect: the larger the gauge number, the thinner the metal.
Sixteen gauge is thicker than twenty gauge, and twenty-four gauge is thinner
still. The convention survives from a time when sheet was produced by drawing it
through successive dies, and the number recorded how many passes the metal had
been through. More passes meant thinner stock, so a higher count came to mean a
lighter sheet.

The practical consequence is that gauge numbers cannot be compared across
materials. A gauge number refers to a weight per unit area, not a distance, and
because steel, aluminum and copper differ in density, the same gauge number
corresponds to a different thickness in each. Sixteen gauge aluminum is
noticeably thicker than sixteen gauge steel, because it takes more aluminum by
volume to reach the same weight. Anyone ordering by gauge alone, without naming
the material, has not specified the job.

For that reason many specifications now give a decimal thickness alongside the
gauge, or in place of it. A drawing that calls for 0.0598 inch steel leaves
nothing to interpret, while one that calls for sixteen gauge relies on the
reader knowing which gauge table applies. Where both appear and they disagree,
the decimal governs, because it is the measurement that can be checked directly
with a micrometer on the material in hand.

The habit of checking rather than assuming matters most on repair work, where
the existing material was ordered under a table that may no longer be the one in
use. Measuring the old sheet takes a moment and settles the question. Ordering
from the gauge number stamped on a decades-old drawing, without measuring, is
how a job ends up with stock that looks right on paper and is wrong on the
bench.
""")

Q(1, "gb1", ["reading.detail"],
  "According to the passage, a higher gauge number means the metal is",
  "thinner",
  [("thicker", "reverses the relationship the passage states in its first sentence"),
   ("heavier per square foot", "weight per area falls as the sheet gets thinner"),
   ("denser", "gauge describes weight per area, not the density of the material")],
  "The passage states directly that the larger the gauge number, the thinner the "
  "metal.", "easy")

Q(2, "gb1", ["reading.detail"],
  "The passage explains that the gauge convention originally recorded",
  "how many passes through dies the metal had been through",
  [("the weight of a standard sheet in pounds", "weight per area is what a gauge refers to now, not what the number originally counted"),
   ("the number of sheets in a standard bundle", "the passage never mentions bundling"),
   ("the thickness in thousandths of an inch", "the passage contrasts gauge numbers with decimal thickness")],
  "The passage says the number recorded how many passes the metal had been "
  "drawn through, and that more passes meant thinner stock.")

Q(3, "gb1", ["reading.inference"],
  "Based on the passage, ordering “sixteen gauge” without naming the material is a problem because",
  "the same gauge number means a different thickness in different metals",
  [("sixteen gauge is too thin for most work", "the passage makes no claim about what thickness is suitable"),
   ("gauge numbers are no longer used by any supplier", "the passage says specifications often give gauge alongside a decimal"),
   ("aluminum cannot be ordered by gauge at all", "the passage gives sixteen gauge aluminum as an example")],
  "The passage says a gauge number refers to weight per unit area, and because "
  "metals differ in density the same number is a different thickness in each.")

Q(4, "gb1", ["reading.detail"],
  "Where a drawing gives both a gauge number and a decimal thickness that disagree, the passage says",
  "the decimal thickness governs",
  [("the gauge number governs", "reverses what the passage states"),
   ("the job must stop until the drawing is reissued", "the passage gives a rule for resolving it, not a reason to stop"),
   ("either may be used, at the fabricator's discretion", "the passage names one of them as governing")],
  "The passage says the decimal governs, because it is the measurement that can "
  "be checked directly with a micrometer.")

Q(5, "gb1", ["reading.purpose"],
  "The final paragraph is included mainly to",
  "warn that repair work may involve an older gauge table, so the material should be measured",
  [("argue that old drawings should be destroyed", "the passage recommends measuring, not discarding drawings"),
   ("explain how a micrometer works", "the tool is mentioned but not explained"),
   ("show that repair work is more profitable than new work", "the passage makes no comparison of that kind")],
  "The paragraph says existing material may have been ordered under a table no "
  "longer in use, and that measuring the old sheet settles the question.")

# ------------------------------------------------------------------ passage 2
P("gb2", "Why torque is specified", """
A bolted joint does not hold because the bolt is strong. It holds because the
bolt has been stretched, and the tension in that stretched bolt clamps the parts
together. Tightening a nut is a way of stretching the bolt, and the torque
figure in a specification is an indirect way of aiming at a particular stretch.
It is indirect because most of the effort applied at the wrench never reaches
the bolt as tension at all.

Of the torque applied, a large share is consumed by friction under the nut face
and in the threads. Only the remainder does the useful work of stretching the
fastener. The exact split depends on the condition of the parts, which is why
the same torque figure produces different clamping forces on a dry joint, an
oiled joint and a joint with a plated fastener. A specification that names a
torque without naming the lubrication condition has left out something that
changes the result substantially.

Under-tightening and over-tightening fail in different ways, and the difference
matters when a joint is being diagnosed. A joint that is too loose allows the
parts to move against each other under load, and that movement, repeated, works
the fastener loose or fatigues it until it breaks. A joint that is too tight may
yield the bolt on assembly, so that it no longer springs back and the clamping
force falls away. The loose joint usually announces itself gradually; the
over-tightened one may have already lost its clamp before the assembly leaves
the bench.

This is why a torque wrench is checked against a standard periodically rather
than trusted indefinitely, and why a fastener that has been tightened past yield
is replaced rather than re-used. Neither precaution is about the strength of the
bolt. Both are about preserving the stretch that does the actual holding.
""")

Q(6, "gb2", ["reading.main-idea"],
  "Which best states the main idea of the passage?",
  "A bolted joint holds by the tension in a stretched bolt, and torque is only an indirect way of producing it",
  [("Torque wrenches are unreliable and should not be used", "the passage recommends checking them, not abandoning them"),
   ("Stronger bolts make for better joints", "the passage opens by denying that strength is what makes the joint hold"),
   ("Over-tightening is always worse than under-tightening", "the passage describes two different failure modes without ranking them")],
  "The passage argues that clamping comes from bolt stretch, that torque aims at "
  "that stretch indirectly, and that both practices at the end exist to preserve it.")

Q(7, "gb2", ["reading.detail"],
  "According to the passage, much of the torque applied at the wrench is consumed by",
  "friction under the nut face and in the threads",
  [("stretching the bolt", "that is the remainder, after friction takes its share"),
   ("bending the parts being clamped", "the passage does not mention bending"),
   ("heat in the wrench itself", "the passage does not mention the wrench absorbing effort")],
  "The passage states that a large share is consumed by friction under the nut "
  "face and in the threads, with only the remainder stretching the fastener.")

Q(8, "gb2", ["reading.inference"],
  "The passage implies that applying the same torque figure to a dry joint and an oiled joint will",
  "produce different clamping forces",
  [("produce the same clamping force either way", "contradicts the passage's point about lubrication condition"),
   ("strip the threads on the oiled joint", "the passage does not describe this outcome"),
   ("make no practical difference", "the passage calls the difference substantial")],
  "The passage says the split between friction and stretch depends on the "
  "condition of the parts, so the same torque gives different clamping forces.")

Q(9, "gb2", ["reading.detail"],
  "The passage says a joint that is too loose fails because",
  "repeated movement between the parts works the fastener loose or fatigues it",
  [("the bolt yields on assembly and loses its spring", "that is how the over-tightened joint fails"),
   ("the threads corrode more quickly", "corrosion is not mentioned"),
   ("the clamping force was never applied at all", "the passage describes a joint under some clamp, just too little")],
  "The passage says a loose joint lets the parts move under load, and that "
  "repeated movement works the fastener loose or fatigues it until it breaks.")

Q(10, "gb2", ["reading.inference"],
  "Why does the passage say an over-tightened joint is harder to catch than a loose one?",
  "It may already have lost its clamp before the assembly leaves the bench",
  [("It makes no noise when it fails", "the passage does not discuss noise"),
   ("It always fails later than a loose joint", "the passage suggests the opposite timing"),
   ("It cannot be detected with any instrument", "the passage does not claim this")],
  "The passage contrasts the loose joint, which announces itself gradually, with "
  "the over-tightened one, which may have already lost its clamp on the bench.")

# ------------------------------------------------------------------ passage 3
P("gb3", "Balancing an air system", """
A duct system that has been installed exactly to drawing will still not deliver
the airflow the drawing intended. Fittings, joints and bends each add resistance
that the design accounted for only approximately, and the fan responds to the
total resistance it actually meets rather than the one that was calculated.
Balancing is the work of correcting that difference after the fact, by measuring
what each outlet actually delivers and adjusting dampers until the distribution
matches the design.

The order in which the work is done matters more than the individual
adjustments. Closing a damper at one outlet does not simply reduce the air at
that outlet; it raises the resistance of that branch, which sends more air to
every other outlet on the system. Balancing one outlet at a time and moving on
therefore undoes earlier work continuously. The usual method is to find the
outlet that is furthest below its target, treat it as the reference, and set the
others relative to it, accepting that several passes will be needed before the
readings settle.

Measurement introduces its own difficulty. Air leaving a diffuser is turbulent,
and a reading taken too close to the face or off to one side will not represent
the flow. Readings are taken at a consistent distance and position, and repeated,
because a single reading in a turbulent stream says very little. Where readings
disagree from one pass to the next by more than a small margin, the usual cause
is the measurement position rather than a change in the system.

None of this is a sign that the design was wrong. A design predicts; a system
behaves. Balancing is the step that reconciles the two, and a system that has
never been balanced is delivering some distribution of air that nobody has
confirmed, however carefully the ductwork was installed.
""")

Q(11, "gb3", ["reading.main-idea"],
  "The passage is mainly about",
  "why an installed duct system must be measured and adjusted rather than trusted to the drawing",
  [("how to design a duct system from scratch", "design is discussed only as the thing balancing reconciles"),
   ("why duct drawings are usually wrong", "the passage explicitly denies the design was wrong"),
   ("how to choose the right fan for a building", "fan selection is not the subject")],
  "The passage explains why actual resistance differs from the calculation and "
  "presents balancing as the step that reconciles design with behaviour.")

Q(12, "gb3", ["reading.detail"],
  "According to the passage, closing a damper at one outlet",
  "sends more air to the other outlets on the system",
  [("reduces the air at that outlet and leaves the others unchanged", "the passage says the effect is not confined to that outlet"),
   ("reduces the total air the fan delivers to zero", "the passage does not describe this"),
   ("has no effect until every damper is closed", "the passage describes an immediate redistribution")],
  "The passage says closing a damper raises that branch's resistance, which "
  "sends more air to every other outlet.")

Q(13, "gb3", ["reading.inference"],
  "The passage suggests that balancing one outlet at a time and moving on is ineffective because",
  "each adjustment changes the outlets already set",
  [("dampers wear out if adjusted repeatedly", "wear is not mentioned"),
   ("the fan cannot respond quickly enough", "fan response time is not discussed"),
   ("only one outlet can be measured per visit", "the passage does not describe such a limit")],
  "Because closing one damper redistributes air to the others, working outlet by "
  "outlet undoes earlier work continuously.")

Q(14, "gb3", ["reading.detail"],
  "When readings disagree between passes by more than a small margin, the passage says the usual cause is",
  "the position the measurement was taken from",
  [("a real change in the system", "the passage names this as the less likely explanation"),
   ("a faulty instrument", "instrument faults are not mentioned"),
   ("a damper that has slipped", "the passage does not offer this explanation")],
  "The passage states that where readings disagree from pass to pass, the usual "
  "cause is the measurement position rather than a change in the system.")

Q(15, "gb3", ["reading.vocabulary"],
  "As used in the final paragraph, “reconciles” most nearly means",
  "brings into agreement",
  [("apologises for", "the word is used of two things being matched, not of regret"),
   ("replaces with something better", "balancing adjusts the system, it does not replace the design"),
   ("keeps separate records of", "the sentence is about closing a gap, not recording one")],
  "The sentence contrasts what a design predicts with how a system behaves, and "
  "names balancing as the step that brings the two together.")

# ------------------------------------------------------------------ passage 4
P("gb4", "The permit before the work", """
A confined space is not defined by how tight it is. It is defined by three
conditions taken together: the space is large enough to enter and work in, it
has limited means of entry or exit, and it is not designed for continuous
occupancy. A tank, a pit and a section of large duct can all meet that
definition, and so can places that do not look hazardous at all. The definition
turns on the difficulty of getting out, not on the discomfort of being in.

A space that meets the definition is treated as permit-required when it also
holds, or could hold, a hazardous atmosphere, or contains material that could
engulf an entrant, or has a shape that could trap someone, or presents any other
recognised serious hazard. The permit itself is not paperwork for its own sake.
It records the specific hazards identified, the steps taken to control each one,
the testing that was done and when, and the names of the people filling each
role. It is the evidence that the assessment actually happened.

Atmospheric testing follows a fixed order that reflects how quickly each hazard
kills. Oxygen is tested first, because a meter reading for anything else cannot
be trusted in an atmosphere that is oxygen-deficient or oxygen-enriched.
Flammable gases are tested next, then toxic contaminants. Testing is done from
outside the space, working downward through it, because gases stratify and a
reading at the opening says nothing about conditions at the bottom.

The role that is most often misunderstood is the attendant's. The attendant does
not enter. That is the whole point of the position: someone outside must remain
outside, maintaining contact with the entrants and able to summon rescue. An
attendant who enters to help a collapsed entrant becomes a second casualty, and
the majority of deaths in confined spaces are among would-be rescuers rather
than the original entrant.
""")

Q(16, "gb4", ["reading.detail"],
  "According to the passage, a confined space is defined by",
  "three conditions: it can be entered and worked in, entry or exit is limited, and it is not meant for continuous occupancy",
  [("how physically tight the space is", "the passage opens by denying this"),
   ("whether it contains a hazardous atmosphere", "that is what makes a confined space permit-required, not what defines one"),
   ("whether a permit has been issued for it", "the permit follows from the definition, it does not create it")],
  "The passage lists exactly those three conditions taken together, and says the "
  "definition turns on the difficulty of getting out.")

Q(17, "gb4", ["reading.detail"],
  "The passage says oxygen is tested first because",
  "readings for other hazards cannot be trusted when oxygen is out of range",
  [("oxygen deficiency is the most common hazard", "the passage gives a different reason"),
   ("oxygen meters take the longest to stabilise", "timing of the instrument is not mentioned"),
   ("the permit requires it in that order for record-keeping", "the passage gives a technical reason, not a clerical one")],
  "The passage states that a meter reading for anything else cannot be trusted in "
  "an atmosphere that is oxygen-deficient or oxygen-enriched.")

Q(18, "gb4", ["reading.inference"],
  "Testing is done working downward through the space because",
  "gases settle at different levels, so a reading at the opening does not describe the bottom",
  [("the meter is more accurate when lowered slowly", "meter accuracy is not the stated reason"),
   ("the entrant will be working at the bottom", "the passage gives stratification as the reason"),
   ("the space must be tested after entry begins", "the passage says testing is done from outside")],
  "The passage says gases stratify and a reading at the opening says nothing "
  "about conditions at the bottom.")

Q(19, "gb4", ["reading.detail"],
  "The passage says the attendant's defining responsibility is to",
  "remain outside the space while staying in contact and able to summon rescue",
  [("enter first to check conditions", "the passage states the attendant does not enter"),
   ("complete the permit paperwork", "the permit records the assessment but is not named as the attendant's role"),
   ("perform the atmospheric testing", "testing is described separately from the attendant's role")],
  "The passage says the attendant does not enter, and that the whole point of the "
  "position is that someone outside stays outside.")

Q(20, "gb4", ["reading.inference"],
  "The last sentence is included to show that",
  "an attendant who enters to help usually adds a casualty rather than preventing one",
  [("rescue teams are poorly trained", "the passage makes no claim about training"),
   ("confined space work should be avoided entirely", "the passage describes how to do it safely"),
   ("the original entrant is rarely in real danger", "the passage does not minimise the entrant's risk")],
  "The sentence follows the statement that an attendant who enters becomes a "
  "second casualty, and reports that most deaths are among would-be rescuers.")

# ------------------------------------------------------------------ passage 5
P("gb5", "Reading a material list", """
A material list is not simply an inventory of what the job needs. It is a
statement of what has been counted, in a particular order, and the order carries
information that a reader who skips to the quantities will miss. Items are
grouped by system and then by size, largest first, because that is the sequence
in which material is normally set out and installed. A line that appears out of
that order is usually an addition made after the original takeoff, and is worth
a second look for exactly that reason.

Quantities appear in the unit the material is purchased in, not the unit it is
measured in on the drawing. Pipe measured in feet on a drawing may be listed in
lengths, because that is how it arrives. Fittings counted individually may be
listed by the box. A reader who treats every number as though it were the
drawing measurement will over-order in some places and under-order in others,
and the error will not be consistent enough to notice from the totals.

Allowances are the part most often misread. A list that shows a waste allowance
has already added it, and adding a further allowance on top duplicates it. A
list that shows no allowance has not, and ordering the bare figure leaves nothing
for offcuts. The only way to tell which convention is in use is to read the
heading, which is why the heading is not decoration.

None of this makes a material list difficult. It makes it a document with
conventions, like a drawing. The reader who learns the conventions can check a
list against a drawing quickly and find the discrepancies that matter. The
reader who treats it as a shopping list will order confidently and be wrong.
""")

Q(21, "gb5", ["reading.main-idea"],
  "The passage is chiefly concerned with",
  "the conventions a material list follows and what a reader misses by ignoring them",
  [("how to calculate a waste allowance", "allowances are one example, not the subject"),
   ("why material lists should be replaced by drawings", "the passage compares the two without recommending replacement"),
   ("how material is delivered to a job site", "delivery units are mentioned only as one convention")],
  "The passage works through ordering, units and allowances as conventions, and "
  "closes by contrasting a reader who learns them with one who does not.")

Q(22, "gb5", ["reading.detail"],
  "According to the passage, items on a material list are grouped",
  "by system, then by size with the largest first",
  [("alphabetically by material name", "the passage names system and size as the grouping"),
   ("in the order the items were priced", "pricing order is not mentioned"),
   ("by supplier", "suppliers are not discussed")],
  "The passage states that items are grouped by system and then by size, largest "
  "first, matching the sequence material is set out and installed in.", "easy")

Q(23, "gb5", ["reading.inference"],
  "The passage suggests that a line appearing out of the usual order deserves attention because",
  "it was probably added after the original count",
  [("it is probably priced incorrectly", "the passage does not connect ordering to price"),
   ("it indicates the list is a forgery", "the passage suggests nothing of the kind"),
   ("it always means the quantity is wrong", "the passage recommends a second look, not a conclusion")],
  "The passage says a line out of that order is usually an addition made after "
  "the original takeoff, and is worth a second look for that reason.")

Q(24, "gb5", ["reading.detail"],
  "The passage says quantities are given in",
  "the unit the material is purchased in",
  [("the unit used on the drawing", "the passage explicitly contrasts the two"),
   ("whichever unit is shortest to write", "the passage gives a purchasing reason"),
   ("metric units throughout", "units of measurement systems are not discussed")],
  "The passage states that quantities appear in the unit the material is "
  "purchased in, not the unit it is measured in on the drawing.")

Q(25, "gb5", ["reading.inference"],
  "Based on the passage, adding a waste allowance to a list that already shows one will",
  "order more material than the job needs",
  [("leave nothing for offcuts", "that is the result of ordering the bare figure from a list with no allowance"),
   ("have no effect on the total", "the passage says it duplicates the allowance"),
   ("correct an error in the original takeoff", "the passage treats it as an error, not a correction")],
  "The passage says a list showing an allowance has already added it, and adding "
  "a further allowance duplicates it.")

if __name__ == "__main__":
    assert len(items) == 25, f"expected 25, got {len(items)}"
    assert len(passages) == 5, f"expected 5 passages, got {len(passages)}"
    per = {}
    for it in items:
        per[it.d["passageId"]] = per.get(it.d["passageId"], 0) + 1
    print(f"GAN Form B section 4 (Reading Comprehension): {len(items)} items across {len(passages)} passages")
    print("  per passage:", per)
