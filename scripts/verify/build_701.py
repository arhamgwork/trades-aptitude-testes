# -*- coding: utf-8 -*-
"""Assembles data/electrical/ibew-701-formA.json from the verified item sets."""
import sys, os, json, collections
sys.path.insert(0, os.path.dirname(__file__))
from common import balance_keys
import gen_701_algebra as alg
import gen_701_reading as rd

SEED = "ibew-701-formA-v1"
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")

questions = [i.as_dict() for i in alg.items] + [i.as_dict() for i in rd.items]
balance_keys(questions, SEED)

exam = {
    "id": "ibew-701-formA",
    "trade": "electrical",
    "title": "IBEW Local 701 (DuPage) — Practice Exam, Form A",
    "testName": "Electrical Training Alliance Aptitude Test",
    "provider": "Electrical Training Alliance",
    "locals": ["IBEW Local 701 / DuPage County JATC"],
    "confidence": "CONFIRMED",
    "confidenceNote": "",
    "blueprint": "docs/blueprints/electrical-ibew-701.md",
    "dateChecked": "2026-09-21",
    "calculatorAllowed": False,
    "selfPaced": False,
    "sections": [
        {"id": "alg", "name": "Algebra and Functions",
         "questionCount": 33, "timeLimitSec": 46 * 60, "timeConfirmed": True},
        {"id": "read", "name": "Reading Comprehension",
         "questionCount": 36, "timeLimitSec": 51 * 60, "timeConfirmed": True},
    ],
    "passages": rd.passages,
    "questions": questions,
}

def balance_report(exam):
    width = max(len(q["choices"]) for q in exam["questions"])
    uniform = 100 / width
    out = {"width": width, "uniform_pct": uniform, "overall": {}, "sections": {}}
    c = collections.Counter(chr(65 + q["correctIndex"]) for q in exam["questions"])
    n = len(exam["questions"])
    out["overall"] = {k: {"n": c[k], "pct": round(100 * c[k] / n, 1)}
                      for k in sorted(c)}
    for s in exam["sections"]:
        qs = [q for q in exam["questions"] if q["section"] == s["id"]]
        cc = collections.Counter(chr(65 + q["correctIndex"]) for q in qs)
        out["sections"][s["id"]] = {
            k: {"n": cc[k], "pct": round(100 * cc[k] / len(qs), 1)} for k in sorted(cc)}
    return out

if __name__ == "__main__":
    rep = balance_report(exam)
    print(f"total questions: {len(exam['questions'])}")
    print(f"uniform target: {rep['uniform_pct']:.1f}%")
    print("overall:", {k: v["pct"] for k, v in rep["overall"].items()})
    for sid, d in rep["sections"].items():
        print(f"  {sid}:", {k: v["pct"] for k, v in d.items()})
    worst = max(abs(v["pct"] - rep["uniform_pct"]) for v in rep["overall"].values())
    print(f"worst overall deviation: {worst:.1f} points (limit 8)")
    for sid, d in rep["sections"].items():
        w = max(abs(v["pct"] - rep["uniform_pct"]) for v in d.values())
        print(f"worst deviation in {sid}: {w:.1f} points (limit 12)")
    out = os.path.join(ROOT, "data", "electrical", "ibew-701-formA.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(exam, f, ensure_ascii=False, indent=1)
    print("wrote", os.path.relpath(out, ROOT))
    with open(os.path.join(ROOT, "scripts", "verify", "_701_balance.json"), "w") as f:
        json.dump(rep, f, indent=1)
