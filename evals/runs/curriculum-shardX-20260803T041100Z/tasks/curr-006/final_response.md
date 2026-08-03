# Seeing How Many Without Counting — subitizing quantities to 5 (K–1)

Three PDFs are ready: the student worksheet, a full step-by-step answer key, and
a two-page study guide.

## What the worksheet asks (8 problems)

Every problem is a *look-and-say* task, so the picture is the model and the
number sentence beside it is the notation:

- **Problems 1–2** — dot cards in the familiar dice arrangements (slant of
  three, four-corners-plus-middle). The child names the pattern; there is
  nothing to count.
- **Problems 3–4** — five-frames. A full frame is five, so the child reads the
  *empty* boxes and subtracts: $5-1=4$, $5-3=2$. This is the bridge from picture
  to notation.
- **Problems 5–6** — two small groups on one page (conceptual subitizing):
  see 2 and 2, know 4; see 3 and 2, know 5.
- **Problems 7–8** — compare two cards with $>$ or $<$. Problem 8 is the
  deliberate trap: the left card is physically wider (two separate boxes holding
  $2+2=4$) but the narrow full five-frame holds more, so a child who judges by
  area rather than by quantity gets it backwards.

Difficulty ramps 1, 1, 2, 2, 2, 3, 3, 4. Each problem carries about 3 cm of
answer space, which is what a kindergartener needs to write one digit
comfortably.

## Verification

All 8 problems are machine-checked by SymPy — 8 verified, 0 manual. The dot
cards themselves carry no printed numbers, so the figures cannot contradict the
key; the quantity each card shows is stated in the JSON and re-derived by the
checker (`eval` for the six counting problems, `compare` for the two symbol
problems). The answer key's boxed answers are bound problem-by-problem to those
verified values, and the study guide's four worked examples and four try-its are
verified the same way. `BUILD PASSED — all gates green`.

## Study guide (2 pages)

One section per worksheet skill, each with a rule, a worked example with a
strategy line, and a distinct try-it whose answer is printed upside down inside
the box: knowing a dot pattern at a glance, reading a five-frame by its empty
boxes, putting two small groups together, and deciding which picture shows more.

## Notes for the teacher or parent

- The answer key opens with a usage note: a child who counts one-by-one and
  still gets the right number has the *answer* but not the *skill*. Flash the
  card for about two seconds and ask again.
- **Standards code.** `references/standards-map.md` carries counting and
  cardinality as the single row `K.CC.A.1–K.CC.C.7`; the curriculum task named
  `K.CC.B.4–K.CC.B.5`, which sits inside that row. Every problem is tagged with
  the map's code verbatim rather than a narrower code the map does not contain.
