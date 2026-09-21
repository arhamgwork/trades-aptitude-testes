# -*- coding: utf-8 -*-
"""Builds the 36 Reading Comprehension items (4 original passages) for IBEW 701 Form A.

Passages are original prose written for this project. Keys here cannot be
computed, so every item carries verify="blind-solve" and is checked by an
independent solver that never sees the key (see VERIFICATION_REPORT.md).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import Item

S = "read"
items = []
passages = []

def P(pid, title, text):
    passages.append({"id": pid, "title": title, "text": text.strip()})

def Q(n, pid, skills, stem, correct, distractors, explanation, difficulty="medium"):
    items.append(Item(f"e701a-read-{n:03d}", S, skills, stem, correct, distractors,
                      explanation, "blind-solve", difficulty,
                      passage_id=pid, formatter=str))

# ---------------------------------------------------------------- passage 1
P("p1", "Why Water Towers Stand So Tall", """
A municipal water tower is not a storage tank that happens to sit on legs. Its
height is the entire point. Water pressure in a distribution system comes from
elevation, and every foot of height adds roughly 0.43 pounds per square inch at
the ground below. A tank standing 150 feet above the neighborhood it serves
therefore delivers about 65 pounds per square inch at street level, which is
close to the range most household fixtures are designed to accept.

This arrangement lets a utility size its pumps for average demand rather than
peak demand. Pumps run steadily through the night, when electricity is cheaper
and consumption is low, filling the tank. During the morning rush, when
thousands of households draw water at once, the tank empties faster than the
pumps refill it, and gravity covers the difference. Without the tower, the
utility would need pumps large enough to meet the highest demand of the year,
and those pumps would sit idle most of the time.

The stored volume matters for a second reason that has nothing to do with daily
demand. Fire flow can require several thousand gallons per minute for hours at a
stretch, far beyond what distribution pumps supply. A full tower is a reserve
that begins delivering the instant a hydrant opens, with no startup delay and no
dependence on the electrical grid. During a power failure, a water tower keeps
supplying pressure until it drains, which is why many utilities treat tank level
as a measure of how long they can operate blind.

The shape of the tank follows from these demands. Engineers prefer a design in
which most of the stored water sits near the top, because pressure at the ground
depends on the height of the water surface, not on the total volume held. A tank
that drains from a tall, narrow column would see its pressure fall steadily as
the level dropped. A tank with a wide bowl high on a single pedestal keeps the
water surface within a narrow band of elevation through most of its useful
range, so pressure at the customer's tap stays nearly constant as the tank
empties.
""")

Q(1, "p1", ["reading.main-idea"],
  "Which statement best expresses the main idea of the passage?",
  "A water tower's height and shape are both driven by the need to deliver steady pressure and reserve capacity.",
  [("Water towers are an outdated technology that modern pumps have largely replaced.",
    "contradicts the passage, which presents towers as actively useful"),
   ("Municipal utilities use water towers mainly to reduce their nighttime electricity costs.",
    "takes one supporting detail and treats it as the whole point"),
   ("The chief purpose of a water tower is to guarantee water during a fire.",
    "names one of several purposes as though it were the only one")],
  "The passage moves through pressure from elevation, pump sizing, fire reserve "
  "and finally tank shape, and each of those is tied back to delivering steady "
  "pressure and holding a reserve.")

Q(2, "p1", ["reading.detail"],
  "According to the passage, about how much pressure does each foot of height add?",
  "About 0.43 pounds per square inch",
  [("About 0.65 pounds per square inch", "borrows a digit from the 65 psi figure, which is a total, not a per-foot rate"),
   ("About 1.5 pounds per square inch", "derives from the 150-foot height rather than the stated rate"),
   ("About 4.3 pounds per square inch", "misplaces the decimal point in the stated rate")],
  "The passage states directly that every foot of height adds roughly 0.43 "
  "pounds per square inch.", "easy")

Q(3, "p1", ["reading.inference"],
  "The passage suggests that without a water tower, a utility would most likely have to",
  "buy larger pumps that would run below capacity much of the time",
  [("raise the price of water to cover higher nighttime electricity costs",
    "reverses the passage, which says nighttime electricity is the cheaper period"),
   ("reduce the pressure available at household fixtures",
    "assumes a consequence the passage never draws"),
   ("build a second tower at a different elevation",
    "offers an outside solution the passage does not mention")],
  "The passage says the tower lets a utility size pumps for average rather than "
  "peak demand, and that without it the pumps would have to meet the year's "
  "highest demand and would sit idle most of the time.")

Q(4, "p1", ["reading.vocabulary"],
  "As used in the final paragraph, the phrase \"useful range\" most nearly means",
  "the span of tank levels over which the tower still does its job",
  [("the distance the water can travel through the distribution system",
    "reads 'range' as horizontal distance rather than a span of levels"),
   ("the variety of purposes the tower can serve",
    "reads 'range' as variety, which the sentence's focus on level does not support"),
   ("the maximum volume the tank was designed to hold",
    "substitutes total volume, which the paragraph explicitly sets aside")],
  "The sentence contrasts water surface elevation with total volume and "
  "describes pressure staying nearly constant as the tank empties, so the "
  "phrase refers to the span of levels over which the tower still performs.")

Q(5, "p1", ["reading.detail"],
  "The passage says fire flow can demand",
  "several thousand gallons per minute for hours",
  [("several hundred gallons per minute for hours", "understates the figure given"),
   ("several thousand gallons per hour for minutes", "swaps the units of rate and duration"),
   ("more water than the tower itself can hold", "states a comparison the passage does not make")],
  "The passage gives fire flow as several thousand gallons per minute for hours "
  "at a stretch.", "easy")

Q(6, "p1", ["reading.purpose"],
  "The author mentions power failures chiefly in order to",
  "show that the tower supplies pressure without depending on the electrical grid",
  [("warn that water service is fragile during storms",
    "adopts an alarmed tone the passage does not take"),
   ("argue that utilities should invest in backup generators",
    "recommends an action the passage never proposes"),
   ("explain why pumps are sized for average demand",
    "attaches the example to the wrong argument in the passage")],
  "The power-failure sentence follows the claim that a full tower delivers with "
  "no startup delay and no dependence on the grid, and it illustrates that "
  "independence.")

Q(7, "p1", ["reading.inference"],
  "Based on the passage, a tall narrow tank would be a poor design mainly because",
  "its pressure would drop noticeably as the water level fell",
  [("it would hold too little water to be useful during a fire",
    "raises a volume objection the passage does not make about this shape"),
   ("it would cost more to build than a bowl on a pedestal",
    "introduces cost, which the passage never discusses"),
   ("it would freeze more readily in cold weather",
    "brings in an outside concern absent from the passage")],
  "The passage says pressure depends on the height of the water surface, and "
  "that a tank draining from a tall narrow column would see pressure fall "
  "steadily as the level dropped.")

Q(8, "p1", ["reading.organization"],
  "Which best describes how the passage is organized?",
  "A central principle is stated, then several consequences of it are developed in turn",
  [("A common belief is introduced and then refuted with evidence",
    "no belief is set up and knocked down in the passage"),
   ("Two competing designs are compared point by point throughout",
    "the comparison of shapes appears only at the end, not throughout"),
   ("A chronological account traces the development of a technology",
    "the passage is not organized by time at all")],
  "The passage opens with the principle that pressure comes from elevation and "
  "then works out what follows from it for pump sizing, fire reserve and shape.")

Q(9, "p1", ["reading.detail"],
  "A tank 150 feet above the neighborhood delivers roughly what pressure at street level?",
  "65 pounds per square inch",
  [("43 pounds per square inch", "uses the per-foot rate as though it were the total"),
   ("150 pounds per square inch", "reports the height in place of the pressure"),
   ("100 pounds per square inch", "rounds to a figure the passage does not give")],
  "The passage states that a tank standing 150 feet up delivers about 65 pounds "
  "per square inch at street level.", "easy")

# ---------------------------------------------------------------- passage 2
P("p2", "Keeping the Grid at Sixty Cycles", """
An alternating-current power grid has a heartbeat, and in North America that
heartbeat is sixty cycles per second. The figure is not a target the operators
aim at so much as a reading they watch. Frequency on a grid is a direct
consequence of the balance between how much power generators are producing and
how much load is drawing. When generation exceeds demand, the spinning machines
speed up and frequency rises. When demand exceeds generation, the machines are
dragged down and frequency falls. Nobody sets the number; the physics reports
it.

That relationship makes frequency the most convenient signal in the whole
system. A control room thousands of miles from a failed generator learns of the
failure almost instantly, because the deviation appears everywhere at once on an
interconnected grid. Operators do not need to know which machine tripped in
order to begin responding. They need only see that the balance has moved, and in
which direction.

The response happens in layers, distinguished by how quickly each acts. The
first layer is not a decision at all but inertia: the rotating mass of every
turbine and generator still connected resists any change in speed, and in doing
so donates kinetic energy to the grid during the first seconds of a shortfall.
This buys time and nothing else, but the time is essential. The second layer,
governor response, arrives within seconds as individual units sense the
frequency drop and open their valves slightly. The third, automatic generation
control, works over minutes to return frequency exactly to sixty and to restore
the reserves that the first two layers spent.

The growth of generation that connects through power electronics rather than
through a spinning shaft has complicated the first layer in particular. Solar
arrays and battery installations have no rotating mass to contribute, so a grid
with a large share of such resources has less natural inertia and its frequency
falls faster after a loss. Engineers have responded by programming inverters to
imitate the behavior they displaced, detecting a frequency change and injecting
power within milliseconds. The imitation is deliberate, and in some respects it
outperforms the original, since a programmed response can be tuned while the
physics of a spinning mass cannot.
""")

Q(10, "p2", ["reading.main-idea"],
  "Which best states the main idea of the passage?",
  "Grid frequency reflects the balance of generation and load, and the system defends it in layers that new technology has had to reproduce.",
  [("North American grids run at sixty cycles per second because regulators chose that standard.",
    "contradicts the passage, which says the number is read rather than set"),
   ("Solar and battery resources have made grid frequency impossible to control.",
    "overstates a difficulty the passage says engineers have addressed"),
   ("Grid operators must identify which generator has failed before they can respond.",
    "reverses an explicit statement in the passage")],
  "The passage establishes frequency as a consequence of balance, describes the "
  "three layers of response, and then explains how inverter-based resources "
  "have had to imitate the first layer.")

Q(11, "p2", ["reading.detail"],
  "According to the passage, frequency rises when",
  "generation exceeds demand",
  [("demand exceeds generation", "reverses the stated relationship"),
   ("operators increase the frequency setting", "assumes a setting the passage denies exists"),
   ("inertia is added to the system", "attributes the rise to a stabilizing factor rather than an imbalance")],
  "The passage states that when generation exceeds demand the spinning machines "
  "speed up and frequency rises.", "easy")

Q(12, "p2", ["reading.detail"],
  "Which layer of response is described as acting first?",
  "Inertia from rotating mass",
  [("Governor response", "acts within seconds, after inertia"),
   ("Automatic generation control", "works over minutes and is described as third"),
   ("Inverter injection", "is a later engineering addition, not the original first layer")],
  "The passage names inertia as the first layer and explicitly says it is not a "
  "decision at all.", "easy")

Q(13, "p2", ["reading.vocabulary"],
  "As used in the passage, \"donates\" most nearly means",
  "contributes automatically, without being commanded",
  [("transfers on the condition that it be repaid",
    "reads a repayment condition into the word; restoring reserves later is a separate control action, not a condition attached to the inertial contribution"),
   ("contributes only after a deliberate decision",
    "conflicts with the passage calling this layer not a decision at all"),
   ("wastes through unavoidable loss",
    "treats the energy as lost rather than usefully supplied to the grid")],
  "The sentence describes rotating mass resisting a speed change and supplying "
  "kinetic energy automatically, which the passage contrasts with a decision.")

Q(14, "p2", ["reading.inference"],
  "The passage implies that a grid with a very large share of inverter-based generation would",
  "experience a faster frequency drop after losing a generator unless inverters are programmed to respond",
  [("be unable to detect a generator failure at all",
    "contradicts the passage's account of frequency as an instant signal"),
   ("require operators to abandon the sixty-cycle standard",
    "proposes a change the passage never suggests"),
   ("have more inertia than a conventional grid",
    "reverses the passage's statement about rotating mass")],
  "The passage says such resources have no rotating mass, so the grid has less "
  "natural inertia and frequency falls faster, and that engineers program "
  "inverters to imitate the missing response.")

Q(15, "p2", ["reading.purpose"],
  "The author says \"the physics reports it\" mainly to emphasize that frequency is",
  "a measured result of conditions rather than a value anyone chooses",
  [("too complex for operators to influence", "overstates it; the passage describes deliberate responses"),
   ("measured by instruments that can drift out of calibration", "raises an accuracy issue the passage never mentions"),
   ("identical at every point on every grid in the world", "extends the claim beyond the interconnected grid discussed")],
  "The sentence closes a paragraph arguing that nobody sets the number and that "
  "it follows from the balance of generation and load.")

Q(16, "p2", ["reading.detail"],
  "Automatic generation control is described as working over",
  "minutes",
  [("milliseconds", "belongs to the programmed inverter response"),
   ("seconds", "belongs to governor response"),
   ("hours", "is longer than any interval the passage gives")],
  "The passage says the third layer works over minutes to return frequency "
  "exactly to sixty and restore reserves.", "easy")

Q(17, "p2", ["reading.inference"],
  "The final sentence suggests that a programmed inverter response can be superior because it",
  "can be adjusted, whereas the behavior of a spinning mass cannot",
  [("responds more slowly, giving operators time to think", "reverses the speed advantage the passage describes"),
   ("eliminates the need for governor response entirely", "claims a replacement the passage does not assert"),
   ("produces more total energy than a turbine of the same size", "compares energy output, which the passage does not discuss")],
  "The passage closes by noting that a programmed response can be tuned while "
  "the physics of a spinning mass cannot.")

Q(18, "p2", ["reading.organization"],
  "The third paragraph is organized primarily by",
  "the speed at which each response acts",
  [("the cost of each response", "cost is not mentioned in the paragraph"),
   ("the geographic location of each resource", "location plays no part in that paragraph"),
   ("the age of each technology", "the paragraph does not order the layers historically")],
  "The paragraph introduces the layers as distinguished by how quickly each "
  "acts and then moves from seconds to minutes.")

# ---------------------------------------------------------------- passage 3
P("p3", "The Box That Rearranged the World", """
Before the shipping container, loading a cargo ship was a craft. Longshoremen
moved barrels, sacks and crates one lot at a time, fitting irregular goods into
an irregular hold in an order that had to be worked out on the spot. A ship
might spend as long in port as it spent at sea. Cargo handling, not the voyage,
was the expensive part of shipping, and it was expensive chiefly because it
consumed labor and time in roughly equal measure.

The container did not solve this problem by being a better box. Boxes were not
the difficulty. What the container did was standardize the unit of cargo so that
every step of the journey could be mechanized around the same dimensions. A
crane that could lift one container could lift them all. A chassis that fit one
would fit any. The gain came not from the steel but from the agreement, and the
agreement took longer to reach than the engineering did.

The consequences reached well beyond the docks. When moving goods became cheap
and predictable, the calculation that had tied factories to their customers
loosened. A manufacturer could put a plant where labor or materials were
advantageous rather than where the market happened to be, because the cost of
bridging the distance had fallen to a rounding error in the price of the
finished product. Whole industries relocated over the following decades, and
economists still argue about how much of that shift to attribute to the
container and how much to trade policy that arrived alongside it.

The costs fell unevenly, as such changes usually do. Ports that could not
accommodate the cranes and the land area the new system demanded declined
quickly, sometimes within a decade, while ports with deep water and room to
expand grew into the hubs the system required. The workforce contracted sharply.
A job that had rewarded experience in stowing an awkward hold became a job
operating a machine to a fixed procedure. Historians of the period generally
treat the container as a case in which a change framed as a simple efficiency
turned out to redistribute work and wealth on a scale nobody had forecast.
""")

Q(19, "p3", ["reading.main-idea"],
  "The passage is primarily concerned with",
  "how standardizing cargo reshaped shipping, industry and port communities",
  [("how engineers designed a stronger and lighter cargo box",
    "focuses on the steel, which the passage says was not the source of the gain"),
   ("why longshoremen resisted the introduction of new technology",
    "treats a consequence mentioned briefly as the central subject"),
   ("how trade policy rather than technology drove industrial relocation",
    "picks one side of a debate the passage leaves open")],
  "The passage moves from the old loading process to standardization and then "
  "to effects on factory location, ports and the workforce.")

Q(20, "p3", ["reading.detail"],
  "Before containers, a ship might spend",
  "as long in port as it spent at sea",
  [("more time at sea than in port", "reverses the comparison given"),
   ("a few hours in port between voyages", "understates the delay the passage describes"),
   ("most of the year laid up awaiting repair", "introduces a circumstance the passage never mentions")],
  "The passage states that a ship might spend as long in port as it spent at "
  "sea.", "easy")

Q(21, "p3", ["reading.inference"],
  "The statement that \"the gain came not from the steel but from the agreement\" most nearly means that",
  "the value lay in everyone adopting common dimensions, not in the box itself",
  [("the container was poorly built and needed frequent repair",
    "reads a quality complaint into a sentence about standardization"),
   ("labor agreements with dockworkers were the decisive factor",
    "reads 'agreement' as a labor contract rather than a shared standard"),
   ("steel prices were the main obstacle to adoption",
    "raises a cost issue the passage does not discuss")],
  "The sentence follows the observation that one crane could lift them all and "
  "one chassis would fit any, which depends on shared dimensions.")

Q(22, "p3", ["reading.detail"],
  "According to the passage, cargo handling was expensive chiefly because it consumed",
  "labor and time in roughly equal measure",
  [("fuel and labor in roughly equal measure", "substitutes fuel for time"),
   ("more money than the voyage itself ever did", "overstates a comparison the passage frames differently"),
   ("specialized equipment that wore out quickly", "names a cause the passage does not give")],
  "The passage says it was expensive chiefly because it consumed labor and time "
  "in roughly equal measure.", "easy")

Q(23, "p3", ["reading.inference"],
  "The passage suggests that a port with shallow water and little surrounding land would most likely have",
  "declined as the container system spread",
  [("specialized in handling containers for smaller vessels",
    "invents an adaptation the passage does not describe"),
   ("retained its workforce longer than deep-water ports",
    "conflicts with the account of rapid decline"),
   ("become a hub because it faced less competition",
    "reverses the outcome the passage reports")],
  "The passage says ports that could not accommodate the cranes and land area "
  "declined quickly, sometimes within a decade.")

Q(24, "p3", ["reading.vocabulary"],
  "As used in the third paragraph, \"loosened\" most nearly means",
  "became less binding",
  [("came apart entirely", "overstates it; the passage describes weakening, not elimination"),
   ("grew more complicated", "substitutes complexity for reduced constraint"),
   ("was deliberately relaxed by regulators", "attributes the change to policy rather than falling costs")],
  "The sentence says the calculation that had tied factories to their customers "
  "loosened because the cost of distance fell, which is a weakening of a "
  "constraint.")

Q(25, "p3", ["reading.purpose"],
  "The author notes that economists still argue about attribution in order to",
  "acknowledge that the container's exact share of the change is uncertain",
  [("dismiss economists as unable to agree on anything",
    "adopts a dismissive tone the passage does not take"),
   ("argue that trade policy mattered more than the container",
    "takes a side the passage explicitly leaves open"),
   ("show that the relocation of industry has been exaggerated",
    "denies a shift the passage treats as real")],
  "The passage reports that industries relocated and then notes the open "
  "question of how much to attribute to the container versus trade policy.")

Q(26, "p3", ["reading.detail"],
  "The passage says the dock workforce",
  "contracted sharply",
  [("grew as ports expanded", "contradicts the passage"),
   ("stayed level but earned less", "describes a change in pay the passage does not report"),
   ("moved inland to work at new factories", "invents a destination the passage never mentions")],
  "The passage states plainly that the workforce contracted sharply.", "easy")

Q(27, "p3", ["reading.inference"],
  "The final sentence implies that the container's effects were",
  "larger and less predictable than the efficiency argument for it suggested",
  [("smaller than historians originally believed", "reverses the sentence's emphasis"),
   ("confined mostly to the shipping industry itself", "contradicts the passage's account of wider effects"),
   ("fully anticipated by the people who promoted it", "contradicts 'nobody had forecast'")],
  "The sentence describes a change framed as a simple efficiency that "
  "redistributed work and wealth on a scale nobody had forecast.")

# ---------------------------------------------------------------- passage 4
P("p4", "Room to Move", """
Nearly every solid expands when heated, and the amount is small enough to ignore
in casual life and far too large to ignore in construction. A steel beam a
hundred feet long grows roughly three quarters of an inch over a temperature
swing of a hundred degrees Fahrenheit. That figure sounds modest until one
considers what happens if the beam is not permitted to grow. The expansion does
not simply fail to occur. The material develops internal stress instead, and the
stress a restrained member generates is set by the stiffness of the material
rather than by the size of the movement prevented. For steel the resulting
forces are large enough to buckle a member or to crack whatever is holding it.

Designers therefore spend a surprising amount of effort providing somewhere for
movement to go. A bridge deck rides on bearings that permit it to slide, and the
familiar toothed joint at each end exists to let the deck lengthen without
pressing against the abutment. Long runs of pipe are routed with deliberate
bends, or fitted with loops, so that thermal growth is absorbed by flexing
rather than by thrust against the anchors. Masonry walls receive soft joints at
intervals for the same reason. In each case the design accepts the movement as
inevitable and directs it, rather than attempting to prevent it.

Trouble arises most often where two materials meet. Aluminum expands about twice
as much as steel for the same temperature change, and concrete falls between
them. A joint that fastens dissimilar materials rigidly will work itself loose
over many cycles, or will concentrate stress at the fastener until something
yields, even though neither material alone would have been overstressed. The
failure belongs to the connection rather than to either component.

The same principle appears wherever temperature varies and materials differ, and
the remedy is nearly always the same. Slotted holes, flexible connectors and
deliberate gaps are not concessions to sloppy work. They are the acknowledgment
that a structure exposed to weather is never quite the same size twice, and that
a design which assumes otherwise will find its own way to relieve the stress.
""")

Q(28, "p4", ["reading.main-idea"],
  "The main point of the passage is that",
  "structures must be designed to accommodate thermal movement rather than to resist it",
  [("thermal expansion is too small to matter in most buildings",
    "contradicts the passage's central claim"),
   ("aluminum should be avoided in structures exposed to weather",
    "draws a recommendation the passage never makes"),
   ("modern fasteners have eliminated problems caused by expansion",
    "claims a solution the passage does not offer")],
  "The passage argues that expansion will occur or else generate stress, and "
  "that good design directs the movement instead of preventing it.")

Q(29, "p4", ["reading.detail"],
  "A hundred-foot steel beam is said to grow about how much over a hundred-degree swing?",
  "Three quarters of an inch",
  [("Three quarters of a foot", "misreads the unit, overstating the movement twelvefold"),
   ("Three inches", "reports a figure the passage does not give"),
   ("A hundredth of an inch", "understates the stated figure")],
  "The passage gives roughly three quarters of an inch for that beam and that "
  "temperature change.", "easy")

Q(30, "p4", ["reading.detail"],
  "According to the passage, the stress in a restrained member is set mainly by",
  "the stiffness of the material",
  [("the length of the member", "is ruled out; the passage separates stress from the size of the movement"),
   ("the size of the movement that was prevented", "is explicitly contrasted with the correct factor"),
   ("the type of fastener used at the connection", "belongs to the later discussion of joints")],
  "The passage states that the stress a restrained member generates is set by "
  "the stiffness of the material rather than by the size of the movement "
  "prevented.")

Q(31, "p4", ["reading.detail"],
  "Compared with steel, aluminum is said to expand",
  "about twice as much",
  [("about half as much", "reverses the comparison"),
   ("about the same amount", "denies the difference the paragraph is built on"),
   ("about ten times as much", "overstates the stated ratio")],
  "The passage says aluminum expands about twice as much as steel for the same "
  "temperature change.", "easy")

Q(32, "p4", ["reading.inference"],
  "The passage implies that a rigid joint between aluminum and steel is likely to fail because",
  "the two materials move by different amounts, concentrating stress at the connection",
  [("aluminum is inherently weaker than steel",
    "attributes failure to material strength, which the passage sets aside"),
   ("the joint is exposed to more weather than the members are",
    "invents an exposure difference the passage does not mention"),
   ("neither material is strong enough for the load applied",
    "contradicts the statement that neither alone would be overstressed")],
  "The passage says such a joint concentrates stress at the fastener until "
  "something yields even though neither material alone would have been "
  "overstressed, and that the failure belongs to the connection.")

Q(33, "p4", ["reading.purpose"],
  "The author mentions bridge bearings, pipe loops and soft joints in masonry chiefly to",
  "give varied examples of designs that give movement somewhere to go",
  [("show that bridges require more care than buildings",
    "draws a comparison the passage does not make"),
   ("argue that older construction methods were superior",
    "introduces a judgment absent from the passage"),
   ("explain how each of those components is manufactured",
    "describes a purpose the passage does not pursue")],
  "The three examples follow the claim that designers provide somewhere for "
  "movement to go, and each illustrates directing movement rather than "
  "preventing it.")

Q(34, "p4", ["reading.vocabulary"],
  "As used in the final paragraph, \"concessions\" most nearly means",
  "allowances made to make up for a shortcoming",
  [("formal agreements between contracting parties", "uses a legal sense the sentence does not support"),
   ("rights granted to operate a business", "uses an unrelated commercial sense"),
   ("reductions in the price of materials", "reads the word as a discount")],
  "The sentence denies that these features are concessions to sloppy work, "
  "meaning they are not allowances compensating for a deficiency.")

Q(35, "p4", ["reading.inference"],
  "The closing phrase about a structure finding \"its own way to relieve the stress\" suggests that",
  "if movement is not planned for, the structure will crack or deform instead",
  [("structures gradually become more flexible as they age",
    "describes an adaptation the passage does not claim"),
   ("stress in a structure dissipates harmlessly over time",
    "contradicts the passage's warnings about buckling and cracking"),
   ("repairs will always restore a structure to its original condition",
    "addresses repair, which the passage does not discuss")],
  "The passage has already described buckling, cracking and fasteners yielding "
  "as what happens when movement is restrained, so an unplanned release is a "
  "failure.")

Q(36, "p4", ["reading.organization"],
  "Which best describes the structure of the passage?",
  "A physical effect is described, then its design consequences, then a case where it is worst, then a general conclusion",
  [("A problem is posed and two competing solutions are weighed",
    "no competing solutions are set against each other"),
   ("A historical development is traced from early practice to the present",
    "the passage is not organized chronologically"),
   ("A general rule is stated and then shown to have many exceptions",
    "the passage presents no exceptions to its rule")],
  "The passage opens with expansion and restraint, moves to accommodations in "
  "design, then to dissimilar materials as the worst case, and ends with a "
  "general statement.")

if __name__ == "__main__":
    assert len(items) == 36, f"expected 36 reading items, got {len(items)}"
    assert len(passages) == 4, f"expected 4 passages, got {len(passages)}"
    per = {}
    for it in items:
        per[it.d["passageId"]] = per.get(it.d["passageId"], 0) + 1
    print(f"reading: {len(items)} items across {len(passages)} passages — {per}")
