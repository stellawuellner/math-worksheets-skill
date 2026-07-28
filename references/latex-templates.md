# LaTeX Templates Reference

> **Source of truth:** the preamble, header/title macros, study-guide boxes,
> and figure macros ship as `\input`-able files in `templates/`
> (`worksheet-preamble.tex`, `figure-macros.tex`). This page documents how to
> USE them — never re-transcribe macro bodies from a markdown code block;
> transcription drift is exactly the error class the pipeline exists to
> catch. `compile.sh` stages the template files beside your `.tex`
> automatically, so `/tmp` compiles just work.

## Document Shell

```latex
\documentclass[12pt]{article}
\usepackage[margin=1in, top=0.75in, bottom=0.75in]{geometry}
\input{worksheet-preamble}
\input{figure-macros}       % when using the shipped figure macros
\wsheader{TOPIC Practice}

\begin{document}
\wstitleblock{TOPIC Practice Worksheet}{COURSE}{DATE}

% [problems here]

\end{document}
```

Macro reference (defined in `templates/worksheet-preamble.tex`):

| Macro | Purpose |
|---|---|
| `\problem{...}` | numbered problem stem (steps the `prob` counter) |
| `\fittedtitle{...}` | shrink-to-fit title: `\LARGE` when it fits on one line, otherwise scaled to the text width — never enlarges, never wraps mid-phrase |
| `\wsheader{Short Title}` | worksheet running header: title left, Name/Date blanks right. Keep the title SHORT (under ~28 chars, e.g. "Triangle Trig Practice") — it shares the line with the blanks and a long title overlaps them |
| `\akheader{Topic}` | answer-key header ("Topic --- Answer Key" / "For instructor/parent use") |
| `\ssheader{Topic}` | study-guide header ("Skills Summary: Topic" / "Study Guide \& Reference") |
| `\wstitleblock{Title}{Course}{Date}` | worksheet title block + horizontal rule |
| `\aktitleblock{Topic}{Course}{Date}` | topic on its own line, **"Answer Key" as a subtitle beneath it** — never appended to the big title, or a long topic wraps mid-phrase |
| `\sstitleblock{Topic}` | study-guide title block |
| `formulabox` / `examplebox` / `watchoutbox` | study-guide box environments (blue formula / green worked example / orange watch-out) |
| `\skillheading{...}` | study-guide skill-section heading |

## Problem Patterns

### Simple algebraic problem
```latex
\problem{Solve for $x$: \quad $2x^2 - 5x - 3 = 0$}
\vspace{6cm}
```

### Two-column layout (shorter problems)
```latex
\begin{multicols}{2}
\begin{enumerate}[label=\textbf{\arabic*.}, itemsep=4cm]
  \item $3x + 7 = 22$
  \item $-2(x - 5) = 14$
  \item $\dfrac{x}{4} + 3 = 9$
  \item $5x - 3 = 2x + 9$
\end{enumerate}
\end{multicols}
```

### Multi-part problem
```latex
\problem{Given $f(x) = 3x^2 - 2x + 1$, find:}
\begin{enumerate}[label=(\alph*), itemsep=3cm, leftmargin=1.5cm]
  \item $f(0)$
  \item $f(-2)$
  \item $f(x+1)$ --- expand and simplify
  \vspace{2cm}
\end{enumerate}
```

### Function table
```latex
\problem{Complete the table for $y = 3x - 2$.}
\vspace{0.3cm}
\begin{center}
\begin{tabular}{|>{\centering\arraybackslash}m{1.5cm}|>{\centering\arraybackslash}m{1.5cm}|}
\hline
\textbf{$x$} & \textbf{$y$} \\
\hline
$-2$ & \rule{1.2cm}{0pt} \\[0.5cm]\hline
$0$  & \\[0.5cm]\hline
$1$  & \\[0.5cm]\hline
$3$  & \\[0.5cm]\hline
\end{tabular}
\end{center}
\vspace{1cm}
```

## Coordinate Planes

### Blank grid (student fills in — algebraic range)
```latex
\begin{center}
\begin{tikzpicture}
\begin{axis}[
    axis lines=center, xmin=-6, xmax=6, ymin=-6, ymax=6,
    xtick={-6,-4,...,6}, ytick={-6,-4,...,6},
    grid=both,
    grid style={line width=0.15pt, draw=gray!30},
    major grid style={line width=0.3pt, draw=gray!50},
    tick label style={font=\small},
    xlabel={$x$}, ylabel={$y$},
    width=9cm, height=9cm, enlargelimits=false
]
\end{axis}
\end{tikzpicture}
\end{center}
```

### Blank grid (full −10 to 10, Pre-Algebra style)
```latex
\begin{axis}[
    axis lines=center, xmin=-10, xmax=10, ymin=-10, ymax=10,
    xtick={-10,-8,...,10}, ytick={-10,-8,...,10},
    minor tick num=1, grid=both,
    grid style={line width=0.12pt, draw=gray!20},
    major grid style={line width=0.3pt, draw=gray!50},
    tick label style={font=\scriptsize},
    xlabel={$x$}, ylabel={$y$}, width=9cm, height=9cm
]
\end{axis}
```

### Completed graph (answer key — plot a function)
```latex
\addplot[blue, thick, domain=-1:5, samples=100] {x^2 - 4*x + 3};
\addplot[only marks, mark=*, mark size=2.5pt, red] coordinates {(1,0)(3,0)};   % x-intercepts
\addplot[only marks, mark=diamond*, mark size=3pt, green!60!black] coordinates {(2,-1)};  % vertex
\draw[dashed, gray] (axis cs:2,-6) -- (axis cs:2,8) node[above] {$x=2$};
```

## Geometric Figures

**Figure conventions** (apply to every figure):
- **Draw to scale from the problem's actual values** whenever possible — a to-scale figure is a free visual sanity check on the answer. Only distort deliberately (e.g. to make a cramped angle readable), and then add *"(not to scale)"* below the figure.
- Label triangle vertices $A, B, C$ with sides $a, b, c$ opposite them — the same convention the `triangle` verification type uses.
- **Every number printed in a figure must come from the problem statement / verify JSON.** Never invent display values; a verified answer key with a mismatched figure is still a wrong worksheet.
- Wrap each figure in `\begin{center}...\end{center}`.

**Avoiding label collisions** (the most common figure defect — check every figure against these):
- Put side labels on the *outside* of the triangle: choose the `above/below/left/right` anchor by edge orientation — `below` for the bottom edge, `above left`/`above right` for the two upper edges of an upward-pointing triangle, mirrored for other orientations. Never leave the default anchor on a midpoint node.
- When an angle-arc label would crowd a vertex label, push it inward with a larger `angle eccentricity` (1.6–2.2) **or** shrink `angle radius` — don't move the vertex label instead, or it will detach from its vertex.
- In thin or small triangles (any angle < 25° or any side rendered < 2cm), move that side's label fully outside with an explicit shift, e.g. `\node[below=2pt] at ...`, and prefer `font=\small` for all labels in the figure.
- Vertex labels take anchors pointing *away* from the triangle interior (e.g. `below left` for a bottom-left vertex).
- After composing a figure, mentally trace each label's bounding box against every drawn line; if in doubt, add a 2pt shift. A worksheet with an unreadable figure fails the student even when the math is right.
- **Keep a problem and its figure on the same page**: wrap the statement + figure in `\noindent\begin{minipage}{\linewidth} \problem{...} \begin{center}\begin{tikzpicture}...\end{tikzpicture}\end{center} \end{minipage}` — LaTeX won't break inside a minipage, so a figure can never be orphaned from its problem across a page break. Leave the work-space `\vspace` *outside* the minipage so pages can still fill naturally.
- **ASCII only in templates**: pdflatex (the fallback engine) cannot typeset literal Unicode symbols like ⚠ or →. Use LaTeX macros or ASCII markers — `(!)`, `$\rightarrow$`, `$^\circ$` — so documents compile identically under both engines.

### Shipped figure macros — use these before hand-writing TikZ

`templates/figure-macros.tex` (staged beside your `.tex` by `compile.sh`)
covers the two most common figures plus the mandatory reference figure. The
mandatory arguments take flat braces only (no nested `{}`); scale/styling
goes in the optional `[..]` argument — that contract is what lets
`check_layout.py` and `check_prose_consistency.py` see macro figures.

```latex
% right triangle (right angle at B); args = bottom-leg, right-leg, hypotenuse labels
\rtfig{$8$}{$6$}{$x$}
\rtfig[0.9]{$a = 8$}{$b = 6$}{$c$}

% general triangle, TO SCALE by construction (SAS): numeric args are the
% ACTUAL givens c, b, A(deg); label args are what gets printed
\trifig{7}{5}{34}{$c = 7$}{$b = 5$}{$a = ?$}{$34^\circ$}

% the value-free reference figure (SKILL.md figure-scope rule): vertices
% A/B/C, sides a/b/c opposite, caption baked in, zero numerals by construction
\refrt
```

The raw TikZ patterns below remain the documented path for figure kinds the
macros do not cover (parallel lines, circles, solids, charts) and show what
the macros do internally.

### Right triangle
```latex
\begin{center}
\begin{tikzpicture}[scale=1.2]
  \coordinate (A) at (0,0);
  \coordinate (B) at (4,0);
  \coordinate (C) at (4,3);
  \draw[thick] (A) -- (B) -- (C) -- cycle;
  \draw (B) ++(-.25,0) -- ++(0,.25) -- ++(.25,0);  % right angle mark
  \node[below left] at (A) {$A$};
  \node[below right] at (B) {$B$};
  \node[above right] at (C) {$C$};
  \node[below] at (2,0) {$8$};
  \node[right] at (4,1.5) {$6$};
  \node[above left] at (2,1.5) {$x$};
\end{tikzpicture}
\end{center}
```

### General triangle, to scale (SAS setup)
Place $A$ at the origin, $B$ on the x-axis at distance $c$, and compute $C$ from side $b$ and angle $A$ — the figure is automatically to scale. TikZ trig functions take degrees.
```latex
\begin{center}
\begin{tikzpicture}[scale=0.6]
  \coordinate (A) at (0,0);
  \coordinate (B) at (7,0);                        % c = AB = 7
  \coordinate (C) at ({5*cos(34)},{5*sin(34)});    % b = AC = 5, angle A = 34$^\circ$
  \draw[thick] (A) -- (B) -- (C) -- cycle;
  \node[below left]  at (A) {$A$};
  \node[below right] at (B) {$B$};
  \node[above]       at (C) {$C$};
  \node[below]       at ($(A)!0.5!(B)$) {$c = 7$};
  \node[above left]  at ($(A)!0.5!(C)$) {$b = 5$};
  \node[above right] at ($(B)!0.5!(C)$) {$a = ?$};
  \pic [draw, angle radius=7mm, angle eccentricity=1.6, "$34^\circ$"] {angle = B--A--C};
\end{tikzpicture}
\end{center}
```

### Parallel lines cut by a transversal
Intersections at $(1,1)$ and $(-1,-1)$; angle numbers sit in the four quadrants around each.
```latex
\begin{center}
\begin{tikzpicture}[scale=1.1]
  \draw[thick, <->] (-3,1) -- (3,1) node[right] {$\ell_1$};
  \draw[thick, <->] (-3,-1) -- (3,-1) node[right] {$\ell_2$};
  \draw[thick, <->] (-2.2,-2.2) -- (2.2,2.2) node[above right] {$t$};
  % arrowhead-style parallel marks
  \draw (1.9,0.9) -- (2.1,1.1);  \draw (2.1,0.9) -- (2.3,1.1);
  \draw (1.9,-1.1) -- (2.1,-0.9);  \draw (2.1,-1.1) -- (2.3,-0.9);
  \node[font=\small] at (1.55,1.3)   {$1$};
  \node[font=\small] at (0.7,1.3)    {$2$};
  \node[font=\small] at (0.45,0.7)   {$3$};
  \node[font=\small] at (1.3,0.7)    {$4$};
  \node[font=\small] at (-0.45,-0.7) {$5$};
  \node[font=\small] at (-1.3,-0.7)  {$6$};
  \node[font=\small] at (-1.55,-1.3) {$7$};
  \node[font=\small] at (-0.7,-1.3)  {$8$};
\end{tikzpicture}
\end{center}
```

### Circle: central and inscribed angle on the same arc
Keep the geometry honest: the inscribed angle must be half the central angle (here $120^\circ$ and $60^\circ$).
```latex
\begin{center}
\begin{tikzpicture}[scale=0.9]
  \draw[thick] (0,0) circle (2);
  \coordinate (O) at (0,0);
  \coordinate (P) at (150:2);
  \coordinate (Q) at (30:2);
  \coordinate (R) at (270:2);
  \draw[thick] (P) -- (O) -- (Q);
  \draw[thick] (P) -- (R) -- (Q);
  \fill (O) circle (1.2pt);
  \node[below]      at (O) {$O$};
  \node[above left] at (P) {$P$};
  \node[above right] at (Q) {$Q$};
  \node[below]      at (R) {$R$};
  \pic [draw, angle radius=5mm, angle eccentricity=1.9, "$120^\circ$"] {angle = Q--O--P};
  \pic [draw, angle radius=7mm, angle eccentricity=1.6, "$60^\circ$"]  {angle = Q--R--P};
\end{tikzpicture}
\end{center}
```

### Circle: shaded sector
```latex
\begin{center}
\begin{tikzpicture}[scale=0.8]
  \coordinate (O) at (0,0);
  \coordinate (A) at (0:2);
  \coordinate (B) at (115:2);
  \draw[thick] (O) circle (2);
  \draw[thick, fill=blue!12] (O) -- (A) arc (0:115:2) -- cycle;
  \fill (O) circle (1.2pt);
  \node[below left] at (O) {$O$};
  \node[below] at (1,0) {$r = 6$};
  \pic [draw, angle radius=5mm, angle eccentricity=1.9, "$115^\circ$"] {angle = A--O--B};
\end{tikzpicture}
\end{center}
```

### Ambiguous SSA case — two-triangle "swing" figure
Both possible triangles from the same SSA data (here $a=6$, $b=8$, $A=40^\circ$): the swinging side $a$ is drawn solid to $C_1$ (acute $B_1$) and dashed to $C_2$ (obtuse $B_2$). Compute both apex points from the actual solutions so the figure is to scale; keep the shared-side label below and each swing label on its own side of the apex to avoid collisions.
```latex
\begin{center}
\begin{tikzpicture}[scale=0.55]
  \coordinate (A) at (0,0);
  % B1 = 58.99$^\circ$, B2 = 121.01$^\circ$, C = 180 - 40 - B. Place base along x-axis:
  % c1 = a·sin(C1)/sin(A) ≈ 9.24, c2 = a·sin(C2)/sin(A) ≈ 3.05
  \coordinate (B1) at (9.24,0);
  \coordinate (B2) at (3.05,0);
  \coordinate (C)  at ({8*cos(40)},{8*sin(40)});   % b = 8 from A at 40$^\circ$
  \draw[thick] (A) -- (B1) -- (C) -- cycle;
  \draw[thick, dashed] (C) -- (B2);
  \node[below left]  at (A)  {$A$};
  \node[below right] at (B1) {$B_1$};
  \node[below=2pt]   at (B2) {$B_2$};
  \node[above]       at (C)  {$C$};
  \node[above left]  at ($(A)!0.35!(C)$)  {$b = 8$};
  \node[above right] at ($(B1)!0.45!(C)$) {$a = 6$};
  \node[right=3pt]   at ($(B2)!0.3!(C)$)  {$a = 6$};
  \pic [draw, angle radius=8mm, angle eccentricity=1.5, "$40^\circ$"] {angle = B1--A--C};
\end{tikzpicture}
\end{center}
```

### Unit circle (skills summary)
Compact version with degree labels; swap the labels for radians ($\frac{\pi}{6}$, …) or exact coordinate pairs depending on the unit being taught.
```latex
\begin{center}
\begin{tikzpicture}[scale=1.8]
  \draw[->] (-1.3,0) -- (1.3,0) node[right] {$x$};
  \draw[->] (0,-1.3) -- (0,1.3) node[above] {$y$};
  \draw[thick] (0,0) circle (1);
  % cardinal angles use offset anchors so labels clear the axes
  \foreach \ang/\lab/\pos in {
      0/{0^\circ}/below right, 30/{30^\circ}/above right, 45/{45^\circ}/above right,
      60/{60^\circ}/above right, 90/{90^\circ}/above right, 120/{120^\circ}/above left,
      135/{135^\circ}/above left, 150/{150^\circ}/above left, 180/{180^\circ}/below left,
      210/{210^\circ}/below left, 225/{225^\circ}/below left, 240/{240^\circ}/below left,
      270/{270^\circ}/below right, 300/{300^\circ}/below right, 315/{315^\circ}/below right,
      330/{330^\circ}/below right}{
    \fill (\ang:1) circle (0.6pt);
    \node[\pos, font=\tiny] at (\ang:1) {$\lab$};
  }
\end{tikzpicture}
\end{center}
```

### Trig function graph (radian axis)
```latex
\begin{center}
\begin{tikzpicture}
\begin{axis}[width=12cm, height=5cm,
  xmin=-0.3, xmax=6.6, ymin=-1.5, ymax=1.5,
  xtick={0, 1.5708, 3.1416, 4.7124, 6.2832},
  xticklabels={$0$, $\frac{\pi}{2}$, $\pi$, $\frac{3\pi}{2}$, $2\pi$},
  ytick={-1, 0, 1}, axis lines=middle, samples=200, domain=0:6.2832]
  \addplot[thick, blue] {sin(deg(x))};
\end{axis}
\end{tikzpicture}
\end{center}
```
For a degree axis (Geometry level): `domain=0:360`, `xtick={0,90,...,360}`, and plot `{sin(x)}` (pgfplots trig defaults to degrees).

### Data charts (bar / line) — data-driven, matches `read_data`
Source the plotted values from the SAME array the `read_data` verify check uses, so the chart and the answer can't disagree.
```latex
% Bar chart of category counts (Mon..Thu = 12,8,15,6)
\begin{center}
\begin{tikzpicture}
\begin{axis}[ybar, width=10cm, height=5cm, bar width=18pt,
  ymin=0, enlarge x limits=0.15, ylabel={Count},
  symbolic x coords={Mon,Tue,Wed,Thu}, xtick=data,
  nodes near coords, axis lines=left]
  \addplot coordinates {(Mon,12) (Tue,8) (Wed,15) (Thu,6)};
\end{axis}
\end{tikzpicture}
\end{center}
```
For a line plot swap `ybar`→(remove) and use `\addplot[mark=*] coordinates {(1,3)(2,7)(3,2)(4,8)}`. For a pictogram, print a row of repeated symbols per category (e.g. `\faStar`×count) instead of an axis.

### 3D solids (volume & surface area problems)
Cylinder:
```latex
\begin{center}
\begin{tikzpicture}[scale=0.8]
  \draw[thick] (0,3) ellipse (1.4 and 0.4);
  \draw[thick] (-1.4,3) -- (-1.4,0);
  \draw[thick] (1.4,3) -- (1.4,0);
  \draw[thick] (-1.4,0) arc (180:360:1.4 and 0.4);
  \draw[dashed] (1.4,0) arc (0:180:1.4 and 0.4);
  \draw[dashed] (0,0) -- (0,3);
  \node[right] at (0.05,1.5) {$h = 8$};
  \draw (0,3) -- (1.4,3);
  \node[above] at (0.7,3.05) {$r = 3$};
\end{tikzpicture}
\end{center}
```
Cone:
```latex
\begin{center}
\begin{tikzpicture}[scale=0.8]
  \draw[thick] (-1.4,0) arc (180:360:1.4 and 0.4);
  \draw[dashed] (1.4,0) arc (0:180:1.4 and 0.4);
  \draw[thick] (-1.4,0) -- (0,3) -- (1.4,0);
  \draw[dashed] (0,0) -- (0,3);
  \node[left] at (0,1.5) {$h$};
  \draw (0,0) -- (1.4,0);
  \node[below] at (0.7,-0.1) {$r$};
  \node[right] at (0.78,1.5) {$\ell$};
\end{tikzpicture}
\end{center}
```
Rectangular prism:
```latex
\begin{center}
\begin{tikzpicture}[scale=0.7]
  \draw[thick] (0,0) -- (4,0) -- (4,2.5) -- (0,2.5) -- cycle;
  \draw[thick] (4,0) -- (5.2,0.8) -- (5.2,3.3) -- (4,2.5);
  \draw[thick] (0,2.5) -- (1.2,3.3) -- (5.2,3.3);
  \draw[dashed] (0,0) -- (1.2,0.8) -- (5.2,0.8);
  \draw[dashed] (1.2,0.8) -- (1.2,3.3);
  \node[below] at (2,0) {$\ell = 8$};
  \node[right] at (4.65,0.3) {$w = 3$};
  \node[left] at (0,1.25) {$h = 5$};
\end{tikzpicture}
\end{center}
```
Sphere:
```latex
\begin{center}
\begin{tikzpicture}[scale=0.8]
  \draw[thick] (0,0) circle (1.5);
  \draw[thick] (-1.5,0) arc (180:360:1.5 and 0.45);
  \draw[dashed] (1.5,0) arc (0:180:1.5 and 0.45);
  \fill (0,0) circle (1.2pt);
  \draw (0,0) -- (40:1.5) node[midway, above left] {$r$};
\end{tikzpicture}
\end{center}
```

## Answer Key Patterns

### Answer key header and title block
Use the shipped macros (defined in `templates/worksheet-preamble.tex`):
```latex
\akheader{TOPIC}                       % keep TOPIC short (under ~28 chars)
...
\aktitleblock{TOPIC}{COURSE}{DATE}
```
`\aktitleblock` puts the topic on its own line (shrink-to-fit) and **"Answer
Key" as a subtitle beneath it** — never append "--- Answer Key" to the big
title, or a long topic wraps mid-phrase. The skills summary uses
`\ssheader`/`\sstitleblock` the same way.

### Step-by-step solution
```latex
\problem{[Repeat full problem statement]}

\textbf{Solution:}
\begin{align*}
  2x^2 - 5x - 3 &= 0 \\
  \intertext{Factor --- find factors of $2(-3)=-6$ summing to $-5$: use $-6,+1$:}
  2x^2 - 6x + x - 3 &= 0 \\
  2x(x - 3) + 1(x - 3) &= 0 \\
  (2x + 1)(x - 3) &= 0 \\
  \intertext{Zero product property:}
  2x + 1 = 0 \quad &\text{or} \quad x - 3 = 0 \\
\end{align*}
\[ \boxed{x = -\tfrac{1}{2} \quad \text{or} \quad x = 3} \]

\vspace{0.3cm}\noindent\rule{\linewidth}{0.2pt}\vspace{0.3cm}
```

### Sign chart (for polynomial graphing)
```latex
\[
\underbrace{+}_{x<-2}\ \Bigl|_{-2}\ \underbrace{-}_{-2<x<0}\ \Bigl|_{0}\ \underbrace{-}_{0<x<2}\ \Bigl|_{2}\ \underbrace{+}_{x>2}
\]
```

### Two-column proof (geometry answer keys)
Proofs are always `manual` in the verify JSON, but the answer key should still show a complete model proof for the student to compare against.
```latex
{\renewcommand{\arraystretch}{1.5}
\noindent
\begin{tabular}{|p{0.47\textwidth}|p{0.43\textwidth}|}
\hline
\multicolumn{1}{|c|}{\textbf{Statements}} & \multicolumn{1}{c|}{\textbf{Reasons}} \\ \hline
1.\ $\overline{AB} \cong \overline{DE}$;\ $\angle A \cong \angle D$ & 1.\ Given \\
2.\ $\angle ABC \cong \angle DEF$ & 2.\ Vertical angles are congruent \\
3.\ $\triangle ABC \cong \triangle DEF$ & 3.\ ASA \\
4.\ $\overline{BC} \cong \overline{EF}$ & 4.\ CPCTC \\ \hline
\end{tabular}}
```
On the student worksheet, print the same table with empty rows (use `\rule{0pt}{1.1cm}` in the first cell of each blank row for writing space).

---

## Skills Summary / Study Guide Template

This is the **third document** generated alongside every worksheet. It's a one-to-two page reference card the student can use while working or studying.

### Document shell

The colors, box environments (`formulabox`/`examplebox`/`watchoutbox`), and
`\skillheading` all live in `templates/worksheet-preamble.tex` — the same
file the worksheet inputs. Only the geometry margins differ:

```latex
\documentclass[12pt]{article}
\usepackage[margin=0.85in, top=0.7in, bottom=0.7in]{geometry}
\input{worksheet-preamble}
\ssheader{TOPIC}

\begin{document}

\sstitleblock{TOPIC}

% =================== SKILL 1 ===================
\skillheading{Skill 1 Name --- e.g. Factoring Trinomials (a = 1)}

\begin{formulabox}
\textbf{Rule / Formula:}\\[4pt]
$x^2 + bx + c = (x + p)(x + q)$ \quad where $p + q = b$ and $p \cdot q = c$
\end{formulabox}

\vspace{0.2cm}

\begin{examplebox}
\textbf{Example:} \quad Factor $x^2 - 7x + 12$\\[4pt]
Find two numbers that \textit{add to} $-7$ and \textit{multiply to} $12$: \quad $-3$ and $-4$ $\checkmark$\\[2pt]
$\Rightarrow\quad x^2 - 7x + 12 = \boldsymbol{(x-3)(x-4)}$
\end{examplebox}

\vspace{0.2cm}

\begin{watchoutbox}
% Engine-neutral warning marker: pdflatex cannot typeset a literal Unicode (!),
% so use a bold exclamation badge that works under both tectonic and pdflatex.
\textbf{(!) Watch out:} Signs matter! If $c > 0$, both factors have the \textit{same sign} as $b$.\par
If $c < 0$, the factors have \textit{opposite signs}.
\end{watchoutbox}

% =================== SKILL 2 ===================
\skillheading{Skill 2 Name --- e.g. Quadratic Formula}

\begin{formulabox}
\textbf{Formula:}\\[4pt]
\[
  x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
\]
\textbf{Discriminant:}\quad $\Delta = b^2 - 4ac$\par
\begin{itemize}[leftmargin=1.5cm, itemsep=1pt, topsep=2pt]
  \item $\Delta > 0$: two real solutions
  \item $\Delta = 0$: one real solution (double root)
  \item $\Delta < 0$: no real solutions (complex roots)
\end{itemize}
\end{formulabox}

\vspace{0.2cm}

\begin{examplebox}
\textbf{Example:} \quad Solve $2x^2 - 3x - 5 = 0$\\[4pt]
$a = 2,\ b = -3,\ c = -5$\quad $\Delta = 9 + 40 = 49$\\[2pt]
$x = \dfrac{3 \pm 7}{4}$\quad $\Rightarrow\quad\boldsymbol{x = \tfrac{10}{4} = \tfrac{5}{2}}$ \quad or \quad $\boldsymbol{x = \tfrac{-4}{4} = -1}$
\end{examplebox}

% =================== KEY VOCABULARY ===================
\vspace{0.3cm}
\skillheading{Key Vocabulary}

\begin{multicols}{2}
\begin{description}[leftmargin=0.5cm, itemsep=2pt, font=\normalfont\bfseries]
  \item[Term 1:] Definition here
  \item[Term 2:] Definition here
  \item[Term 3:] Definition here
  \item[Term 4:] Definition here
\end{description}
\end{multicols}

\end{document}
```

### Usage guidance

- Generate **one skill section per distinct skill** tested in the worksheet (typically 2–5 sections)
- Each section should have: a formula/rule box + 1 mini example + optional watch-out
- Keep the whole document to **1–2 pages max** — it's a reference card, not a lesson
- Vocabulary section is optional — include only when there are ≥3 important terms
- The mini examples should be **shorter and simpler** than the worksheet problems, to illustrate the pattern without being distracting
- The watch-out box is optional per skill — only add if there's a genuinely common mistake worth flagging
