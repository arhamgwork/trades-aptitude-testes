# -*- coding: utf-8 -*-
"""Assembles data/drills/variable-relationships.json."""
import sys, os, json, collections
sys.path.insert(0, os.path.dirname(__file__))
from common import balance_keys
import gen_varrel as g

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
questions = [i.as_dict() for i in g.items]
# keep sub-types grouped for the section table, ordered by sub-type
order = ["varrel.inequality", "varrel.sufficiency", "varrel.symbolic", "varrel.ifthen"]
questions.sort(key=lambda q: (order.index(q["skills"][0]), q["id"]))
for q in questions:
    q["section"] = q["skills"][0].split(".")[1]

balance_keys(questions, "varrel-v1")

sections = []
for key in order:
    sid = key.split(".")[1]
    n = sum(1 for q in questions if q["section"] == sid)
    name = {"inequality": "Inequality chains",
            "sufficiency": "Two-statement sufficiency",
            "symbolic": "Symbolic and functional substitution",
            "ifthen": "If-then chains"}[sid]
    sections.append({"id": sid, "name": name, "questionCount": n, "timeLimitSec": None})

exam = {
    "id": "variable-relationships", "trade": "drills",
    "title": "Variable relationships — all four sub-types",
    "testName": "Skill drill", "provider": "This site",
    "locals": [], "confidence": "CONFIRMED", "confidenceNote": "",
    "blueprint": "docs/blueprints/_gan-battery.md", "dateChecked": "2026-09-21",
    "calculatorAllowed": False, "selfPaced": True,
    "sections": sections, "passages": [], "questions": questions,
}

if __name__ == "__main__":
    out = os.path.join(ROOT, "data", "drills", "variable-relationships.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(exam, f, ensure_ascii=False, indent=1)
    print(f"wrote data/drills/variable-relationships.json: {len(questions)} items")
    for s in sections:
        qs = [q for q in questions if q["section"] == s["id"]]
        c = collections.Counter(chr(65 + q["correctIndex"]) for q in qs)
        w = max(len(q["choices"]) for q in qs)
        print(f"  {s['name']}: {s['questionCount']} items, width {w}, keys "
              + " ".join(f"{k}={c[k]}" for k in sorted(c)))
