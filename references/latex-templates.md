# LaTeX Templates Reference

## Document Shell

```latex
\documentclass[12pt]{article}
\usepackage[margin=1in, top=0.75in, bottom=0.75in]{geometry}
\usepackage{amsmath, amssymb, tikz, pgfplots, enumitem, fancyhdr, multicol, array, booktabs}
\pgfplotsset{compat=1.18}
\usetikzlibrary{calc, angles, quotes}   % needed by the geometric figure templates

\pagestyle{fancy}
\fancyhf{}
% Keep the left title SHORT (≤ ~28 chars, e.g. "Triangle Trig Practice", not the
% full course name) — it shares the header line with the Name/Date blanks and a
% long title overlaps them. \small buys extra margin.
\fancyhead[L]{\textbf{\small TOPIC Practice}}
\fancyhead[R]{\small Name: \underline{\hspace{4.5cm}}~Date: \underline{\hspace{1.8cm}}}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}

\newcounter{prob}
\newcommand{\problem}[1]{\stepcounter{prob}\vspace{0.4cm}\noindent\textbf{\large\theprob.}\quad #1\vspace{0.3cm}}

\begin{document}
\begin{center}
  {\LARGE\textbf{TOPIC Practice Worksheet}}\\[0.3cm]
  {\large COURSE \quad $\bullet$ \quad DATE}
\end{center}
\noindent\rule{\linewidth}{0.4pt}\vspace{0.2cm}

% [problems here]

\end{document}
```

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
  \item $f(x+1)$ — expand and simplify
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
  \coordinate (C) at ({5*cos(34)},{5*sin(34)});    % b = AC = 5, angle A = 34°
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
  % B1 = 58.99°, B2 = 121.01°, C = 180 − 40 − B. Place base along x-axis:
  % c1 = a·sin(C1)/sin(A) ≈ 9.24, c2 = a·sin(C2)/sin(A) ≈ 3.05
  \coordinate (B1) at (9.24,0);
  \coordinate (B2) at (3.05,0);
  \coordinate (C)  at ({8*cos(40)},{8*sin(40)});   % b = 8 from A at 40°
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

### Answer key document header
```latex
\fancyhead[L]{\textbf{TOPIC — Answer Key}}
\fancyhead[R]{\textit{For instructor/parent use}}
```

### Step-by-step solution
```latex
\problem{[Repeat full problem statement]}

\textbf{Solution:}
\begin{align*}
  2x^2 - 5x - 3 &= 0 \\
  \intertext{Factor — find factors of $2(-3)=-6$ summing to $-5$: use $-6,+1$:}
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

```latex
\documentclass[12pt]{article}
\usepackage[margin=0.85in, top=0.7in, bottom=0.7in]{geometry}
\usepackage{amsmath, amssymb, tikz, enumitem, fancyhdr, multicol, mdframed, xcolor}

% Color palette
\definecolor{skillblue}{RGB}{30,100,180}
\definecolor{skillbluebg}{RGB}{235,244,255}
\definecolor{warnorange}{RGB}{200,90,0}
\definecolor{warnbg}{RGB}{255,243,230}
\definecolor{exgreen}{RGB}{20,120,60}
\definecolor{exgreenbg}{RGB}{230,248,238}

% Formula/rule box
\newmdenv[
  backgroundcolor=skillbluebg,
  linecolor=skillblue, linewidth=1.5pt,
  innertopmargin=6pt, innerbottommargin=6pt,
  innerleftmargin=10pt, innerrightmargin=10pt,
  skipabove=6pt, skipbelow=4pt
]{formulabox}

% Mini example box
\newmdenv[
  backgroundcolor=exgreenbg,
  linecolor=exgreen, linewidth=1pt,
  innertopmargin=5pt, innerbottommargin=5pt,
  innerleftmargin=10pt, innerrightmargin=10pt,
  skipabove=4pt, skipbelow=4pt
]{examplebox}

% Watch-out box
\newmdenv[
  backgroundcolor=warnbg,
  linecolor=warnorange, linewidth=1pt,
  innertopmargin=5pt, innerbottommargin=5pt,
  innerleftmargin=10pt, innerrightmargin=10pt,
  skipabove=4pt, skipbelow=4pt
]{watchoutbox}

% Skill section heading
\newcommand{\skillheading}[1]{%
  \vspace{0.4cm}
  {\large\textbf{\textcolor{skillblue}{#1}}}
  \vspace{0.1cm}
  \hrule height 1pt
  \vspace{0.2cm}
}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\textbf{Skills Summary: TOPIC}}
\fancyhead[R]{\small\textit{Study Guide \& Reference}}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}

\begin{document}

\begin{center}
  {\LARGE\textbf{Skills Summary}}\\[0.2cm]
  {\large\textbf{TOPIC}}\\[0.1cm]
  {\small\textit{Use this reference while completing your worksheet or when studying.}}
\end{center}
\vspace{0.1cm}
\noindent\rule{\linewidth}{1.5pt}
\vspace{0.3cm}

% =================== SKILL 1 ===================
\skillheading{Skill 1 Name — e.g. Factoring Trinomials (a = 1)}

\begin{formulabox}
\textbf{Rule / Formula:}\\[4pt]
$x^2 + bx + c = (x + p)(x + q)$ \quad where $p + q = b$ and $p \cdot q = c$
\end{formulabox}

\vspace{0.2cm}

\begin{examplebox}
\textbf{Example:} \quad Factor $x^2 - 7x + 12$\\[4pt]
Find two numbers that \textit{add to} $-7$ and \textit{multiply to} $12$: \quad $-3$ and $-4$ ✓\\[2pt]
$\Rightarrow\quad x^2 - 7x + 12 = \boldsymbol{(x-3)(x-4)}$
\end{examplebox}

\vspace{0.2cm}

\begin{watchoutbox}
\textbf{⚠ Watch out:} Signs matter! If $c > 0$, both factors have the \textit{same sign} as $b$.\par
If $c < 0$, the factors have \textit{opposite signs}.
\end{watchoutbox}

% =================== SKILL 2 ===================
\skillheading{Skill 2 Name — e.g. Quadratic Formula}

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
