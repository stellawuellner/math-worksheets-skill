# Two-Step Measurement Stories (Grade 3) — what you received

Three PDFs:

- **Student worksheet** (`ws_twostep_curr090.pdf`) — 12 two-step word problems
  across time (minutes), money (cents and dollars), mass (g, kg), and liquid
  volume (L). After the warm-up the four subskills are interleaved, so every
  problem forces a fresh decision about which operations the story hides, and
  the sheet ends with a three-part challenge (the lemonade problem). Every
  answer line names the required unit.
- **Step-by-step answer key** (`ak_twostep_curr090.pdf`) — each solution names
  the hidden first step, shows both steps of arithmetic, and boxes the final
  answer with its unit, plus a quick-answers bank for fast grading.
- **Study guide** (`ss_twostep_curr090.pdf`) — one section per subskill (time,
  money, mass, liquid volume), each teaching the "find the hidden number
  first" pattern with a rule box, a worked example, and a fresh try-it with
  the answer printed upside down.

**What is verified:** all 12 worksheet answers are machine-checked — SymPy
recomputed every two-step chain from the printed givens, and the unit gate
confirmed each answer line and boxed answer carries the declared unit
(money answers are stated in cents/dollars in the stems; currency has no unit
line by design). Nothing needs manual review: there are no open-response
items, and the key's "What is verified" note is silent because every problem
is covered. The 8 study-guide examples and try-its are machine-verified too.
