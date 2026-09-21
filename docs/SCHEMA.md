# Data schema

Source of truth is `data/<trade>/<exam>.json`. The build refuses to produce
`dist/` if any file fails `scripts/validate.js`.

## Exam file

| Field | Type | Notes |
|---|---|---|
| `id` | string | unique, kebab-case, matches filename |
| `trade` | string | trade slug, matches folder |
| `title` | string | shown on the trade page |
| `testName` | string | real test name, text only, no logos |
| `provider` | string | test publisher |
| `locals` | string[] | which locals use it |
| `confidence` | `CONFIRMED`\|`PARTIAL`\|`UNKNOWN` | shown as a badge |
| `confidenceNote` | string | what exactly is unverified; required unless CONFIRMED |
| `blueprint` | string | path to the blueprint doc |
| `dateChecked` | `YYYY-MM-DD` | |
| `calculatorAllowed` | boolean | per-exam flag; false = no calculator |
| `selfPaced` | boolean | true only if the real test has no per-section clock |
| `sections` | Section[] | in real administered order |
| `passages` | Passage[] | optional, referenced by questions |
| `questions` | Question[] | |

## Section

`id`, `name`, `questionCount`, `timeLimitSec`, optional `timeConfirmed`
(boolean — false means the time is derived, not official, and the UI says so).

## Question

| Field | Type | Notes |
|---|---|---|
| `id` | string | unique across the exam |
| `section` | string | must match a section id |
| `skills` | string[] | skill tags, drive drills and weak-spot detection |
| `type` | `mc` \| `cloze` | |
| `stem` | string | |
| `figure` | string\|null | inline SVG markup |
| `passageId` | string\|null | |
| `choices` | string[] | 4 or 5; exactly one correct |
| `correctIndex` | integer | 0-based, in range |
| `explanation` | string | **must not name a choice by letter** |
| `distractorNotes` | (string\|null)[] | same length as `choices`; the specific error each wrong choice represents; null at `correctIndex` |
| `difficulty` | `easy`\|`medium`\|`hard` | |
| `verify` | string | how the key was checked, e.g. `python:fractions`, `python:geometry`, `blind-solve`, `unchecked` |

## Build gates

The build fails if any of these break:

1. Question, section and option counts match the blueprint's section table.
2. `correctIndex` is within range of `choices`.
3. No duplicate stems within an exam.
4. No two identical options within a question.
5. `node --check` passes on every JS file.
6. No third-party script or tracking URLs anywhere in the output.
7. Every SVG figure parses.
8. Explanations contain no letter references (`option A`, `choice B`, ...).
9. `distractorNotes` length matches `choices`, null exactly at the key.
10. Answer-key balance (new exams): no letter more than 8 points from uniform
    across the exam; no more than 12 points within any section of 30+ items;
    no more than 3 identical correct letters in a row.
