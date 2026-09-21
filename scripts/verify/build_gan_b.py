# -*- coding: utf-8 -*-
"""Assembles the GAN Battery Form B exam from the six verified sections."""
import sys, os, json, collections
sys.path.insert(0, os.path.dirname(__file__))
from common import balance_keys
import gen_gan_s1 as s1, gen_gan_s2 as s2, gen_gan_s3 as s3
import gen_gan_s4 as s4, gen_gan_s5 as s5, gen_gan_s6 as s6

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
SEED = "gan-form-b-v1"

SECTIONS = [
    ("s1", "Numerical Computation", 25, 15),
    ("s2", "Number Series",         20, 12),
    ("s3", "Problem Solving",       25, 25),
    ("s4", "Reading Comprehension", 25, 30),
    ("s5", "Mechanical Aptitude",   25, 18),
    ("s6", "Spatial Relations",     20, 12),
]

questions = []
for mod in (s1, s2, s3, s4, s5, s6):
    questions.extend(i.as_dict() for i in mod.items)

balance_keys(questions, SEED)

sections = [{"id": sid, "name": name, "questionCount": n,
             "timeLimitSec": mins * 60, "timeConfirmed": False}
            for sid, name, n, mins in SECTIONS]

for sid, name, n, _ in SECTIONS:
    got = sum(1 for q in questions if q["section"] == sid)
    assert got == n, f"section {sid}: expected {n}, got {got}"

exam = {
    "id": "gan-battery-formB", "trade": "sheetmetal",
    "title": "GAN Aptitude Battery — Practice Exam, Form B",
    "testName": "GAN Aptitude Battery", "provider": "GAN Human Resources",
    "locals": ["Sheet Metal Workers' Local 73", "Iron Workers Local 1",
               "UA Locals 597 and 130", "other Chicago-area GAN programs"],
    "confidence": "PARTIAL",
    "confidenceNote": (
        "GAN is confirmed as the testing company for several Chicago-area locals, and the "
        "section names come from those locals' own sites. GAN publishes no per-section "
        "question counts or time limits, so the 25/20/25/25/25/20 split and the timings here "
        "follow the structure Local 597 uses and are derived, not official. Sheet Metal Local "
        "73 publishes no format at all, so its use of this battery is inferred from GAN "
        "listing sheet metal among the trades it tests."),
    "blueprint": "docs/blueprints/_gan-battery.md",
    "dateChecked": "2026-09-21",
    "calculatorAllowed": False, "selfPaced": False,
    "sections": sections,
    "passages": s4.passages,
    "questions": questions,
}

if __name__ == "__main__":
    out = os.path.join(ROOT, "data", "sheetmetal", "gan-battery-formB.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(exam, f, ensure_ascii=False, indent=1)
    print(f"wrote data/sheetmetal/gan-battery-formB.json: {len(questions)} items")
    for sid, name, n, mins in SECTIONS:
        qs = [q for q in questions if q["section"] == sid]
        c = collections.Counter(chr(65 + q["correctIndex"]) for q in qs)
        comp = sum(1 for q in qs if q["verify"].startswith("python:"))
        print(f"  {name:<24} {len(qs):>3} items, {mins:>2} min, "
              f"computational {comp:>2}/{len(qs):<3} keys " + " ".join(f"{k}={c[k]}" for k in sorted(c)))
