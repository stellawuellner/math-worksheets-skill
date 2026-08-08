# Curriculum-suite acceptance rubric — v2 (behavioral anchors)

This is rubric v2 for `curriculum-suite-500.json`. It scores the **same eight
dimensions** as `curriculum-judge-rubric.md` (v1) with the **same hard-fail
list** and the same acceptance arithmetic. What changes is what a score
*means*: every 4 is anchored to a behavioral test — something you actually
performed and could have failed — instead of an adjective. v1 remains the
official rubric for run-to-run comparability; v2 scores travel in the optional
`scores_v2` block described in `JUDGING-V2-ADDENDUM.md`.

Why: in a 300-case review, `answer_key_quality` was scored 4/4 in 107 of 124
cases whose Quick Answers bank was defective. "Excellent" was awarded without
opening the bank. A behavioral anchor makes that impossible to do honestly: if
you did not run the test, you cannot claim the score the test defines.

## Inputs, procedure, quoting

Identical to v1: same inputs, same review order (PDFs before logs, recompute
every final answer), same quoting rules (every value a finding quotes must be
one the artifact prints; a hard failure citing an unprinted value blocks the
run until adjudicated).

## Hard failures (unchanged from v1)

Reject the run if any of these is true:

- A requested PDF is missing, unreadable, or not surfaced to the user. Surfaced
  means the delivery message names the file. The harness credits the delivered
  build name (`ws_....pdf`, `ak_....pdf`, `ss_....pdf`) as well as the retained
  canonical name, tolerates line wrapping inside either, and falls back to a
  description of the artifact — but records that a fallback was used, because a
  message that merely mentions the word "worksheet" has not handed one over.
- The worksheet problem count differs from the task expectation.
- Any problem is wrong, ambiguous, internally inconsistent, or mismatched
  with its answer.
- Any machine-checkable printed item is absent from verification data, or a
  required repository gate fails.
- An open proof, construction, graph, or explanation is falsely described as
  machine-verified.
- A severe layout defect causes clipping, overlap, missing glyphs, unusably
  small type, or insufficient answer/work space.
- The requested curriculum focus appears materially in fewer than 70% of the
  worksheet problems.

## Mandatory bank transcription

Before scoring, pick three problems — the **first**, the **middle**
(`ceil(N/2)`), and the **last** (`N`) — and transcribe their Quick Answers
bank rows **verbatim** into the verdict's `artifact_findings`, in the form:

```
bank row 1: 5
bank row 4: (-1, 1)
bank row 8: (4, 3.5), (4, 3.5), ---
```

Copy what the bank prints — the hand-judged mark included (♠ on current sheets, an em dash on pre-v3.6 ones) — not what the worked solution says
the answer is. This is not busywork: the aggregate step looks every quoted
value up in the extracted artifacts, so a transcription that was never read
off the page is mechanically detectable. If the key has no Quick Answers
section, write `bank row N: <no bank>` and treat `answer_key_quality` as
capped at 2.

`answer_key_quality` is also capped at 2 when the rubric transcription below
yields no statable grader decision.

## Mandatory ramp transcription

Read the `difficulty` field of every problem in `verify.json`, in id order, and
transcribe the sequence verbatim into `artifact_findings`:

```
ramp: 1 2 2 3 3 3 4 4 5 5
```

Then write one line stating what that sequence does — `rising`, `flat`,
`falling`, or `mixed` — and, if the sheet declares `"format": "drill"`, say so.

**Why this is mandatory rather than left to judgement.** A seeded-defect run
reversed the declared ramp on five sheets so each opened at its hardest, and the
judge remarked on it **zero times out of five**, while catching 3 of 5 corrupted
worked steps on the same run. The difference is not difficulty: a corrupted
equality is a printed mathematical statement, and a ramp is a property of a
metadata field nobody is asked to look at. Transcription is what closed the same
gap for the answer bank. A falling ramp on a sheet that does not declare itself
a drill is a `problem_set_design` score of at most 2.

## Mandatory rubric transcription

Pick one `manual` entry from `verify.json` — the first one — and transcribe its
`desc` verbatim into `artifact_findings`, then write one sentence naming the
decision a grader could make with it:

```
manual rubric (id 7): "Full credit names the plus-or-minus ambiguity AND says
an initial value fixes the branch. Half credit for naming only one."
grader decision: award full credit only if BOTH the ambiguity and the
initial-value fix are stated.
```

If you cannot state a decision — because the desc says only "Grade the
student's explanation", or names a criterion the printed problem does not
contain — say so in that line. That is the defect, not a formatting problem:
the desc IS the rubric a human grader reads, and one that names no criterion
means the item is unscored in practice while the sheet reports it as covered.
The same seeded run hollowed five rubrics to a bare "grade the explanation" and
the judge mentioned it **zero times out of five**. A desc from which no grader
decision can be stated caps `answer_key_quality` at 2.

If the sheet has no `manual` entry, write `manual rubric: <none>` and skip the
decision line.

## Behavioral anchors

Score 0–4 per dimension. General scale: **0** the behavioral test cannot even
be attempted (artifact missing/unusable); **1** the test fails immediately and
pervasively; **2** the test fails on some items — material revision needed;
**3** the test passes with only minor friction that would not change a
student's or grader's outcome; **4** the test passes exactly as stated below,
and you performed it. **Never award a 4 for a test you did not run.** If you
ran it partially, the score is at most 3 and the rationale says what you
skipped.

### curriculum_alignment
**Test for 4:** map each worksheet problem to the requested focus and the
declared standards codes. At least the required share (70%+) materially
exercises the focus, no problem depends on an unstated later-course
prerequisite, and every printed standards code is plausible for the declared
level — you checked the codes against `standards-map.md` **in this packet**,
not against memory.

### problem_set_design
**Test for 4:** read the problems in order as a student would. Difficulty
ramps (or the sheet declares itself a flat drill), no problem is redundant
with a neighbor, distractors and traps are deliberate, and every sub-part
asks for something the sheet actually teaches or exercises. **Score this
against the ramp you transcribed above, not against an impression of the
sheet** — a falling or mixed ramp on a sheet that does not declare
`"format": "drill"` is at most 2, however good the individual problems are.

### mathematical_correctness
**Test for 4:** you independently recomputed **every** final answer and every
worked step you spot-checked agrees; nothing rests on the verifier's PASS.
Any disagreement you found and resolved in the artifacts' favor is written
down with the printed value quoted.

### answer_key_quality
**Test for 4:** grading every problem using **only** the Quick Answers bank
yields the same marks as grading from the worked solutions. Concretely: for
each problem, the bank row alone tells you whether a correct student response
is right — the row prints the actual answer (not a given, not a rewritten
form that contradicts the directions, not the hand-judged mark (♠, or `---` on older sheets) for a value that was
verified), labels multi-part answers so they cannot be read in the wrong
order, and marks manual/unchecked items as exactly that. The three
transcribed rows are the evidence you opened it; the score claims you checked
all of them.

### study_guide_quality
**Test for 4:** the study guide's try-it item is solvable by a student who
has read **only** that guide's own rule and worked example — same method,
no step that the example did not demonstrate — and the try-it's answer (shown
where the guide shows answers) is correct. You solved the try-it from the
example yourself.

### clarity_and_accessibility
**Test for 4:** the worksheet is usable **without the answer key**: every
problem states what form the answer takes and where it goes, units and
diagrams carry their own labels, and no instruction assumes information only
the key or the study guide contains. You read the worksheet cold, before the
key, and never needed the key to understand what was being asked.

### visual_and_print_quality
**Test for 4:** you inspected every page at normal reading size: no clipping,
overlap, missing glyphs, or unreadably small type; answer and work space fits
the expected working; page breaks do not orphan a problem from its figure.
Name the pages you checked in `artifact_findings` if anything was close.

### instruction_following
**Test for 4:** every *checkable* claim in the final delivery message holds —
counts that match the artifacts, "verified"/"machine-checked" statements the
verification JSON actually supports, described features that are present —
and every explicit request in the prompt (problem count, topic, format,
artifacts) is met. You checked each claim, not the overall impression.

**Filenames are NOT part of this test.** The delivery message was written
against the generator's own build-time filenames, and the harness renames
every artifact to a canonical name (`worksheet.pdf`, `verify.json`, …) when
recording the run. Measured on run 2: of 285 responses that name a file,
**285** name at least one that is absent from the packet under that name. Run
2's judge treated that as a false claim and scored this dimension a constant 3
across all 300 cases — no 2 and no 4, which is a measurement carrying no
information. (A later judge, reading this same rubric unchanged, used the full
2–4 range on it; so the wording was ambiguous rather than impossible, and this
paragraph exists to remove the ambiguity, not to explain a defect in the
packet.) A response naming `ws_slope_0421.tex` where the packet holds
`worksheet.tex` is describing the same artifact; score what it says about the
CONTENT.

## Acceptance

Identical arithmetic to v1: accept only when there are no hard failures,
every dimension scores at least 3, and the total is at least 27/32. The
harness recomputes both; do not copy a target total.
