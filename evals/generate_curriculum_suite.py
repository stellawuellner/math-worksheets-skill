#!/usr/bin/env python3
"""Generate the deterministic 500-prompt curriculum acceptance suite.

The catalog is intentionally authored as curriculum data rather than 500 hand-
copied JSON objects. Ten bands contain ten topic families each; every family has
five distinct instructional focuses. The checked-in JSON is the executable eval
manifest, while this script is its compact, reviewable source of truth.
"""

import json
import os
import sys
from collections import Counter, defaultdict


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUTPUT = os.path.join(ROOT, "evals", "curriculum-suite-500.json")

VERIFY_TYPES = {
    "solve", "zeros", "factor", "expand", "eval", "diff", "integrate",
    "limit", "equiv", "solve_interval", "approx", "distance", "midpoint",
    "slope", "polygon_area", "triangle", "system", "series", "inequality",
    "stats", "probability", "read_data", "definite_integral", "estimate",
    "compare", "manual",
}

VARIANTS = (
    {
        "key": "concept-models",
        "format": "guided concept practice",
        "instruction": (
            "Use age-appropriate concrete, visual, tabular, or graphical models "
            "where they clarify the idea; connect each model to mathematical notation."
        ),
    },
    {
        "key": "procedural-fluency",
        "format": "procedural fluency practice",
        "instruction": (
            "Build a clean difficulty ramp from a worked pattern to independent "
            "fluency, without repeating an identical problem skeleton."
        ),
    },
    {
        "key": "representations-applications",
        "format": "representations and applications workshop",
        "instruction": (
            "Use meaningful representations or realistic applications, state units "
            "and givens explicitly, and avoid irrelevant story detail."
        ),
    },
    {
        "key": "misconception-analysis",
        "format": "misconception and error-analysis practice",
        "instruction": (
            "Include at least two age-appropriate find-and-fix items. Declare any "
            "planted wrong results as machine-checked misconception traps."
        ),
    },
    {
        "key": "interleaved-synthesis",
        "format": "interleaved synthesis review",
        "instruction": (
            "Interleave the named subskills after a short warm-up so method choice is "
            "required, and finish with one synthesis challenge appropriate to the level."
        ),
    },
)


def topic(domain, name, standard, verify, focuses):
    assert len(focuses) == 5
    return {
        "domain": domain,
        "topic": name,
        "standard_refs": standard if isinstance(standard, list) else [standard],
        "verification_targets": verify,
        "focuses": focuses,
    }


BANDS = [
    {
        "key": "foundations-k1",
        "label": "Kindergarten–Grade 1 foundations",
        "learner": "a kindergarten or first-grade learner",
        "counts": [8, 10, 8, 6, 10],
        "topics": [
            topic("Counting and cardinality", "Counting sequences and cardinality", "K.CC.A.1–K.CC.C.7", ["eval", "compare"], [
                "counting forward from varied starting numbers within 100",
                "one-to-one counting and stating how many objects are in a set",
                "matching numerals, number words, and represented quantities",
                "finding missing or misplaced numbers in a counting sequence",
                "counting on to compare the sizes of two represented sets",
            ]),
            topic("Counting and cardinality", "Subitizing and quantity representation", "K.CC.B.4–K.CC.B.5", ["eval", "compare"], [
                "recognizing quantities to 5 without counting one by one",
                "recognizing structured quantities to 10 on ten-frames",
                "building a requested quantity with dots, counters, or tally marks",
                "checking and correcting a mismatched numeral-and-set representation",
                "combining two small visual groups and naming the total",
            ]),
            topic("Number comparison", "Comparing numbers and quantities", "K.CC.C.6–K.CC.C.7", ["compare", "eval"], [
                "using more, fewer, and the same with object sets",
                "comparing written numerals from 1 through 10",
                "ordering three quantities from least to greatest",
                "diagnosing a reversed greater-than or less-than comparison",
                "choosing and justifying the greatest quantity across mixed representations",
            ]),
            topic("Operations and algebraic thinking", "Composing and decomposing numbers to 10", "K.OA.A", ["solve", "eval"], [
                "making number bonds for totals through 5",
                "finding a missing part when the whole is at most 10",
                "showing one total as two different pairs of addends",
                "correcting an incomplete or duplicated number-bond family",
                "using composition and decomposition to make 10",
            ]),
            topic("Operations and algebraic thinking", "Addition within 10", "K.OA.A / 1.OA.C.6", ["eval", "solve"], [
                "joining pictured groups and writing an addition equation",
                "using doubles and near-doubles facts within 10",
                "solving add-to result-unknown stories within 10",
                "finding and fixing an addition count-on error",
                "selecting an efficient strategy for mixed addition facts within 10",
            ]),
            topic("Operations and algebraic thinking", "Subtraction within 10", "K.OA.A / 1.OA.C.6", ["eval", "solve"], [
                "taking away objects and writing a subtraction equation",
                "using a number path to subtract within 10",
                "solving take-from and comparison stories within 10",
                "finding and fixing a subtraction direction error",
                "connecting subtraction facts to related addition facts",
            ]),
            topic("Number and operations in base ten", "Teen numbers and place value", "1.NBT", ["eval", "compare"], [
                "representing teen numbers as one ten and some ones",
                "reading and writing teen numerals and number words",
                "comparing teen numbers using tens and ones",
                "correcting a swapped tens-and-ones representation",
                "ordering mixed teen-number representations on a number line",
            ]),
            topic("Operations and algebraic thinking", "Addition and subtraction within 20", "1.OA.C.6", ["eval", "solve"], [
                "making ten to add within 20",
                "using related facts to subtract within 20",
                "solving missing-addend equations within 20",
                "analyzing a student strategy that misuses a teen-number digit",
                "interleaving add, subtract, and missing-number facts within 20",
            ]),
            topic("Measurement and data", "Direct measurement comparisons and picture data", "1.MD", ["compare", "read_data", "manual"], [
                "ordering objects by directly compared length",
                "measuring length with equal-size nonstandard units",
                "reading a simple picture graph with one-to-one symbols",
                "correcting gaps or overlaps in a unit-measurement example",
                "using measurement and picture-graph evidence in one-step questions",
            ]),
            topic("Geometry", "Shapes, attributes, position, and equal shares", "K.G / 1.G", ["compare", "manual"], [
                "identifying two-dimensional shapes regardless of orientation",
                "sorting shapes by defining attributes rather than color or size",
                "using positional words to locate shapes in a scene",
                "correcting unequal shares labeled as halves or fourths",
                "composing larger shapes from smaller two-dimensional shapes",
            ]),
        ],
    },
    {
        "key": "elementary-2-3",
        "label": "Grades 2–3 elementary arithmetic",
        "learner": "a second- or third-grade learner",
        "counts": [8, 10, 10, 8, 12],
        "topics": [
            topic("Number and operations in base ten", "Place value through 1,000", "2.NBT.A", ["eval", "compare"], [
                "reading hundreds, tens, and ones from base-ten models",
                "writing numbers in standard, word, and expanded form",
                "comparing three-digit numbers using place value",
                "correcting a zero-placeholder error in expanded form",
                "rounding and ordering numbers using a number-line model",
            ]),
            topic("Number and operations in base ten", "Multi-digit addition", "2.NBT.B.5 / 3.NBT.A.2", ["eval", "estimate"], [
                "adding two-digit numbers with place-value strategies",
                "adding three-digit numbers with regrouping",
                "estimating sums before calculating exactly",
                "diagnosing a regrouping or alignment error",
                "choosing mental, partial-sums, or standard-algorithm methods",
            ]),
            topic("Number and operations in base ten", "Multi-digit subtraction", "2.NBT.B.5 / 3.NBT.A.2", ["eval", "estimate"], [
                "subtracting two-digit numbers with place-value models",
                "subtracting across a zero with regrouping",
                "estimating differences and checking reasonableness",
                "diagnosing an add-instead-of-regroup subtraction error",
                "solving mixed comparison and take-away subtraction situations",
            ]),
            topic("Operations and algebraic thinking", "Foundations of multiplication", "3.OA.A.1–3.OA.A.3", ["eval", "solve"], [
                "interpreting equal groups as multiplication",
                "connecting arrays to multiplication equations",
                "solving equal-group and array word problems",
                "correcting a rows-versus-total interpretation error",
                "moving among repeated addition, arrays, and products",
            ]),
            topic("Operations and algebraic thinking", "Foundations of division", "3.OA.A.2–3.OA.A.4", ["eval", "solve"], [
                "interpreting division as sharing equally",
                "interpreting division as finding the number of groups",
                "finding unknown factors with related multiplication facts",
                "diagnosing confusion between group size and group count",
                "matching division stories, drawings, and equations",
            ]),
            topic("Operations and algebraic thinking", "Multiplication and division fact fluency", "3.OA.C.7", ["eval", "solve"], [
                "using twos, fives, and tens as anchor facts",
                "using commutative and distributive fact strategies",
                "solving missing-factor equations within 100",
                "finding and fixing a multiplication fact-pattern error",
                "interleaving multiplication and related division facts",
            ]),
            topic("Number and operations—fractions", "Fractions as numbers", "3.NF.A", ["compare", "eval", "manual"], [
                "identifying unit fractions in area models",
                "placing fractions with denominators 2, 3, 4, 6, and 8 on number lines",
                "matching fraction notation to equal-part visual models",
                "correcting a model whose parts are not equal-sized",
                "comparing simple fractions using benchmarks and models",
            ]),
            topic("Measurement and data", "Time, money, mass, and liquid volume", "2.MD / 3.MD", ["eval", "approx"], [
                "telling and writing time to five-minute intervals",
                "counting mixed coin collections and making change",
                "solving one-step mass and liquid-volume problems",
                "diagnosing an elapsed-time or coin-value error",
                "solving two-step measurement stories with appropriate units",
            ]),
            topic("Measurement and data", "Area and perimeter", "3.MD.C.7 / 3.MD.D.8", ["eval", "approx"], [
                "counting square units to find rectangle area",
                "using multiplication to find rectangle area",
                "finding perimeter when side lengths are given or missing",
                "correcting confusion between area and perimeter",
                "solving composite rectilinear area-and-perimeter challenges",
            ]),
            topic("Data and geometry", "Graphs, line plots, and shape classification", "3.MD / 3.G.A", ["read_data", "stats", "manual"], [
                "reading scaled picture and bar graphs",
                "creating and interpreting whole-number line plots",
                "classifying quadrilaterals by shared attributes",
                "diagnosing a graph-scale or shape-attribute error",
                "using data displays and shape properties in mixed reasoning tasks",
            ]),
        ],
    },
    {
        "key": "upper-elementary-4-5",
        "label": "Grades 4–5 upper elementary",
        "learner": "a fourth- or fifth-grade learner",
        "counts": [10, 12, 10, 8, 12],
        "topics": [
            topic("Number and operations in base ten", "Multi-digit place value and rounding", "4.NBT.A / 5.NBT.A", ["eval", "compare", "estimate"], [
                "reading and comparing multi-digit whole numbers",
                "using powers-of-ten place-value relationships",
                "rounding multi-digit numbers to named places",
                "diagnosing a rounding-boundary or placeholder error",
                "combining expanded form, comparison, and rounding decisions",
            ]),
            topic("Number and operations in base ten", "Multi-digit multiplication", "4.NBT.B.5", ["eval", "estimate"], [
                "using area models for two-digit multiplication",
                "multiplying up to four digits by one digit",
                "multiplying two two-digit numbers in applications",
                "diagnosing a missing partial product or place-value shift",
                "selecting estimation, area-model, or standard-algorithm strategies",
            ]),
            topic("Number and operations in base ten", "Whole-number division", "4.NBT.B.6", ["eval", "estimate", "solve"], [
                "interpreting quotients and remainders with visual models",
                "dividing up to four digits by one-digit divisors",
                "interpreting remainders in real contexts",
                "diagnosing an omitted-zero or partial-quotient error",
                "solving multistep division problems and checking by multiplication",
            ]),
            topic("Operations and algebraic thinking", "Factors, multiples, primes, and patterns", "4.OA.B / 4.OA.C", ["eval", "compare", "manual"], [
                "listing factor pairs and identifying multiples",
                "classifying numbers as prime or composite",
                "finding common factors and common multiples",
                "diagnosing an overgeneralized number-pattern rule",
                "using factor structure to solve pattern and divisibility puzzles",
            ]),
            topic("Number and operations—fractions", "Fraction equivalence and comparison", "4.NF.A", ["equiv", "compare"], [
                "generating equivalent fractions with visual models",
                "simplifying fractions to equivalent lowest terms",
                "comparing unlike fractions with benchmarks or common denominators",
                "diagnosing numerator-only or denominator-only comparison errors",
                "ordering fractions and mixed numbers across representations",
            ]),
            topic("Number and operations—fractions", "Adding and subtracting fractions", "4.NF.B.3 / 5.NF.A.1", ["eval", "solve"], [
                "adding and subtracting fractions with like denominators",
                "finding common denominators for unlike fractions",
                "adding and subtracting mixed numbers in contexts",
                "diagnosing the add-numerators-and-denominators misconception",
                "interleaving fraction sums, differences, and missing addends",
            ]),
            topic("Number and operations—fractions", "Multiplying and dividing fractions", "5.NF.B / 6.NS.A.1", ["eval", "solve", "approx"], [
                "interpreting a fraction of a whole number or set",
                "multiplying fractions and mixed numbers",
                "dividing unit fractions and whole numbers conceptually",
                "diagnosing reciprocal or cross-cancellation misuse",
                "solving multistep fraction-operation applications",
            ]),
            topic("Number and operations in base ten", "Decimal place value and operations", "5.NBT.A / 5.NBT.B.7", ["eval", "compare", "estimate"], [
                "reading, writing, and comparing decimals to thousandths",
                "adding and subtracting decimals with aligned place values",
                "multiplying and dividing decimals using place-value reasoning",
                "diagnosing a decimal-point alignment or shift error",
                "estimating and exactly solving mixed decimal applications",
            ]),
            topic("Measurement and geometry", "Measurement conversion, volume, and angle measure", "4.MD / 5.MD", ["eval", "approx", "manual"], [
                "converting within one customary or metric measurement system",
                "finding volume of rectangular prisms with unit cubes and formulas",
                "measuring and calculating missing angles",
                "diagnosing a squared-versus-cubed unit error",
                "solving multistep volume, conversion, and angle problems",
            ]),
            topic("Coordinates, data, and patterns", "Coordinate plane, line plots, and numerical patterns", "5.G / 5.MD.B.2 / 5.OA.B", ["read_data", "eval", "stats", "manual"], [
                "plotting and reading first-quadrant coordinate points",
                "interpreting fractional line-plot data",
                "generating and comparing two numerical patterns",
                "diagnosing a coordinate-order or graph-scale error",
                "using coordinate, data, and pattern information in combined tasks",
            ]),
        ],
    },
    {
        "key": "middle-grades-6-7",
        "label": "Grades 6–7 middle school",
        "learner": "a sixth- or seventh-grade learner",
        "counts": [10, 12, 10, 8, 12],
        "topics": [
            topic("Ratios and proportional relationships", "Ratios and equivalent ratio tables", "6.RP.A.2, 6.RP.A.3", ["eval", "compare", "solve"], [
                "writing and interpreting ratios in multiple forms",
                "building equivalent ratio tables",
                "using tape diagrams and double number lines for ratios",
                "diagnosing reversed or non-equivalent ratios",
                "selecting ratio representations to solve multistep comparisons",
            ]),
            topic("Ratios and proportional relationships", "Unit rates and unit conversion", "6.RP.A.2, 6.RP.A.3", ["approx", "eval", "solve"], [
                "finding unit rates with whole-number quantities",
                "finding unit rates involving fractions",
                "converting units through ratio reasoning",
                "diagnosing inverted units in a rate calculation",
                "comparing rates and converting units in applications",
            ]),
            topic("Ratios and proportional relationships", "Percent applications", "6.RP.A.3.c / 7.RP.A.3", ["eval", "approx", "solve"], [
                "finding a percent of a quantity",
                "finding the whole or percent rate from part-whole data",
                "solving tax, tip, discount, and markup contexts",
                "diagnosing use of the wrong percent base",
                "solving successive percent-change and percent-error problems",
            ]),
            topic("The number system", "Signed rational-number operations", "7.NS.A.1, 7.NS.A.2", ["eval", "compare"], [
                "adding and subtracting integers on a number line",
                "multiplying and dividing signed numbers",
                "operating with signed fractions and decimals",
                "diagnosing subtraction and negative-sign errors",
                "evaluating mixed rational-number expressions with method choice",
            ]),
            topic("Expressions and equations", "Numerical and algebraic expressions", "6.EE.A / 7.EE.A", ["eval", "expand", "factor", "equiv"], [
                "translating verbal phrases into algebraic expressions",
                "evaluating expressions with substitution",
                "using distributive properties and combining like terms",
                "diagnosing invalid distribution or unlike-term combination",
                "rewriting expressions in equivalent expanded and factored forms",
            ]),
            topic("Expressions and equations", "One- and two-step equations", "6.EE.B.7 / 7.EE.B.4", ["solve", "eval"], [
                "solving one-step equations with rational coefficients",
                "solving two-step equations and checking solutions",
                "writing equations from word situations",
                "diagnosing an inverse-operation or balance error",
                "interleaving equations with variables on either side in context",
            ]),
            topic("Expressions and equations", "One-variable inequalities", "7.EE.B.4", ["inequality", "solve", "manual"], [
                "writing inequalities from verbal constraints",
                "solving and graphing one-step inequalities",
                "solving multi-step inequalities with rational numbers",
                "diagnosing failure to reverse an inequality after multiplying by a negative",
                "interpreting inequality solution sets in real constraints",
            ]),
            topic("Ratios and proportional relationships", "Proportional relationships", "7.RP.A.2", ["slope", "eval", "solve", "read_data"], [
                "recognizing proportional relationships in tables",
                "finding constants of proportionality",
                "graphing proportional relationships through the origin",
                "diagnosing additive reasoning used on proportional data",
                "moving among table, graph, equation, and context representations",
            ]),
            topic("Geometry", "Scale drawings, area, circles, and surface area", "6.G / 7.G", ["approx", "polygon_area", "manual"], [
                "using scale factors in drawings and maps",
                "finding area of triangles, quadrilaterals, and composite figures",
                "finding circumference and area of circles",
                "diagnosing radius-versus-diameter or area-versus-perimeter errors",
                "solving multistep surface-area and scale-design problems",
            ]),
            topic("Statistics and probability", "Distributions, sampling, and chance", "6.SP.A / 6.SP.B.5 / 7.SP", ["stats", "probability", "read_data", "manual"], [
                "distinguishing statistical questions and describing variability",
                "computing and interpreting center and spread",
                "using random samples and simple probability models",
                "diagnosing biased samples or mismatched probability denominators",
                "comparing distributions and compound-event probabilities",
            ]),
        ],
    },
    {
        "key": "grade8-prealgebra",
        "label": "Grade 8 and pre-algebra",
        "learner": "an eighth-grade or pre-algebra learner",
        "counts": [10, 12, 10, 8, 12],
        "topics": [
            topic("The number system", "Irrational numbers and roots", "8.NS.A", ["eval", "approx", "compare"], [
                "classifying rational and irrational numbers",
                "evaluating perfect square and cube roots",
                "approximating irrational roots on a number line",
                "diagnosing invalid simplification of sums of radicals",
                "ordering mixed rational and irrational quantities",
            ]),
            topic("Expressions and equations", "Exponent laws and scientific notation", "8.EE.A.1, 8.EE.A.4", ["eval", "equiv", "compare"], [
                "applying integer exponent product and quotient laws",
                "using zero and negative exponents",
                "operating with scientific notation in applications",
                "diagnosing exponent addition or power-of-a-power errors",
                "choosing among exponent laws in mixed expressions",
            ]),
            topic("Expressions and equations", "Linear equations in one variable", "8.EE.C.7", ["solve", "equiv"], [
                "solving equations with variables on both sides",
                "solving equations with distributive properties and fractions",
                "classifying equations with one, no, or infinitely many solutions",
                "diagnosing a lost solution or invalid distribution step",
                "writing and solving multistep linear models",
            ]),
            topic("Expressions and equations", "Slope and rate of change", "8.EE.B.5, 8.EE.B.6", ["slope", "eval", "read_data"], [
                "finding slope from graphs and rise-over-run triangles",
                "finding slope from two coordinate points",
                "interpreting slope as a unit rate in context",
                "diagnosing inverted or sign-reversed slope calculations",
                "comparing rates of change across tables, graphs, and equations",
            ]),
            topic("Functions", "Linear representations and equations", "8.EE.B.6 / 8.F.B.4", ["slope", "solve", "eval", "read_data"], [
                "writing slope-intercept equations from slope and intercept",
                "writing equations from two points or a table",
                "converting standard form and slope-intercept form",
                "diagnosing confusion between slope and y-intercept",
                "matching linear contexts, tables, equations, and graphs",
            ]),
            topic("Expressions and equations", "Systems of two linear equations", "8.EE.C.8a–c", ["system", "manual"], [
                "understanding intersections as solutions to systems",
                "solving systems by graphing",
                "solving systems algebraically by substitution or elimination",
                "diagnosing a substitution or equation-scaling error",
                "modeling and interpreting systems in word problems",
            ]),
            topic("Functions", "Function concepts and comparisons", "8.F.A.1–8.F.B.5", ["eval", "read_data", "compare", "manual"], [
                "determining whether a relation is a function",
                "evaluating functions from rules, tables, and graphs",
                "comparing two functions represented differently",
                "diagnosing swapped input-output or function-notation errors",
                "describing qualitative function behavior across intervals",
            ]),
            topic("Geometry", "Transformations, congruence, and similarity", "8.G.A", ["distance", "slope", "manual"], [
                "performing translations, reflections, and rotations on coordinates",
                "describing transformation sequences",
                "using dilations to reason about similarity",
                "diagnosing a sign, center, or scale-factor transformation error",
                "establishing congruence or similarity through transformation evidence",
            ]),
            topic("Geometry", "Pythagorean theorem and coordinate distance", "8.G.B.7, 8.G.B.8", ["approx", "distance", "solve"], [
                "finding a missing right-triangle side",
                "using the converse to classify triangles",
                "finding coordinate distance with the Pythagorean theorem",
                "diagnosing leg-versus-hypotenuse substitution errors",
                "solving multistep spatial and coordinate applications",
            ]),
            topic("Statistics", "Scatter plots and bivariate association", "8.SP.A.1", ["read_data", "stats", "manual"], [
                "describing direction, form, and strength in scatter plots",
                "drawing and interpreting informal lines of fit",
                "using two-way tables to compare categorical frequencies",
                "diagnosing correlation-versus-causation claims",
                "using bivariate evidence to make and qualify predictions",
            ]),
        ],
    },
    {
        "key": "algebra-1",
        "label": "Algebra 1",
        "learner": "an Algebra 1 student",
        "counts": [10, 12, 10, 8, 12],
        "topics": [
            topic("Algebraic structure", "Expressions and polynomial operations", "HSA-APR.A.1", ["expand", "factor", "equiv", "eval"], [
                "interpreting terms, factors, coefficients, and degree",
                "adding, subtracting, and multiplying polynomials",
                "rewriting expressions with distributive structure",
                "diagnosing sign and like-term errors in polynomial operations",
                "choosing expanded or factored forms to expose useful structure",
            ]),
            topic("Equations and inequalities", "Linear equations and inequalities", "HSA-REI.A / HSA-REI.B", ["solve", "inequality", "equiv"], [
                "explaining legal equation transformations",
                "solving multistep linear equations with rational coefficients",
                "solving compound linear inequalities",
                "diagnosing extraneous steps or inequality-direction errors",
                "modeling constraints with equations and inequalities together",
            ]),
            topic("Systems", "Linear systems and modeling", "HSA-REI.C.6", ["system", "manual"], [
                "interpreting system solutions graphically",
                "solving systems by substitution",
                "solving systems by elimination with scaling",
                "diagnosing inconsistent algebra in a system solution",
                "building and interpreting systems for mixture, rate, or cost contexts",
            ]),
            topic("Functions", "Function notation, domain, and range", "HSF-IF.A", ["eval", "solve", "manual"], [
                "interpreting function notation and input-output statements",
                "evaluating functions and solving for inputs",
                "finding domain and range from rules or contexts",
                "diagnosing notation that confuses f(x) with multiplication",
                "connecting function rules, tables, graphs, and contextual restrictions",
            ]),
            topic("Sequences", "Arithmetic sequences as linear functions", "HSF-BF.A / HSF-LE.A", ["eval", "solve", "series"], [
                "recognizing arithmetic sequences and common differences",
                "writing explicit arithmetic sequence formulas",
                "writing recursive arithmetic sequence formulas",
                "diagnosing off-by-one errors in sequence indexing",
                "modeling discrete linear change and finite arithmetic sums",
            ]),
            topic("Exponential functions", "Exponential growth and decay", "HSF-LE.A", ["eval", "solve", "approx"], [
                "distinguishing exponential from linear change",
                "evaluating and graphing exponential functions",
                "writing growth and decay models from data",
                "diagnosing percent-factor and repeated-addition errors",
                "comparing exponential models and solving contextual predictions",
            ]),
            topic("Quadratic functions", "Parabola features and transformations", "HSF-IF.C / HSA-SSE.B.3", ["eval", "zeros", "manual"], [
                "identifying vertex, axis, intercepts, and opening direction",
                "graphing quadratics from vertex or standard form",
                "rewriting quadratics to reveal vertex or intercept structure",
                "diagnosing sign errors in parabola transformations",
                "connecting graph features to multiple algebraic forms",
            ]),
            topic("Polynomials", "Factoring quadratic and special-form expressions", "HSA-SSE.B.3 / HSA-APR.A.1", ["factor", "equiv"], [
                "factoring out greatest common factors",
                "factoring monic and nonmonic trinomials",
                "factoring differences of squares and perfect-square trinomials",
                "diagnosing sign-pair and forgotten-GCF errors",
                "selecting and combining factoring techniques in mixed expressions",
            ]),
            topic("Quadratic equations", "Solving quadratic equations", "HSA-REI.B.4", ["solve", "zeros", "approx"], [
                "solving quadratics by the zero-product property",
                "solving by square roots and completing the square",
                "using the quadratic formula and discriminant",
                "diagnosing incomplete root sets or formula sign errors",
                "selecting efficient solution methods and interpreting roots in context",
            ]),
            topic("Modeling and functions", "Absolute-value, piecewise, and linear-quadratic models", "HSF-IF / HSA-CED", ["eval", "solve", "system", "manual"], [
                "evaluating piecewise and absolute-value functions",
                "graphing transformations of absolute-value functions",
                "writing piecewise rules for rates or fees",
                "diagnosing boundary-condition and open-closed endpoint errors",
                "choosing linear, quadratic, or piecewise models from contextual evidence",
            ]),
        ],
    },
    {
        "key": "geometry",
        "label": "High-school geometry",
        "learner": "a high-school geometry student",
        "counts": [8, 10, 8, 6, 10],
        "topics": [
            topic("Geometric reasoning", "Definitions, postulates, and proof logic", "HSG-CO.A / HSG-CO.C", ["manual", "solve"], [
                "using precise definitions and counterexamples",
                "distinguishing postulates, theorems, converses, and biconditionals",
                "completing short algebraic and segment proofs",
                "diagnosing circular reasoning or an unsupported proof statement",
                "constructing coherent multi-step arguments from stated givens",
            ]),
            topic("Lines and angles", "Parallel lines, transversals, and angle relationships", "HSG-CO.C.9", ["solve", "eval", "manual"], [
                "identifying angle pairs formed by transversals",
                "solving for angle measures when lines are parallel",
                "using converses to establish parallel lines",
                "diagnosing misuse of corresponding or alternate-interior relationships",
                "combining angle algebra and parallel-line proof reasoning",
            ]),
            topic("Congruence", "Triangle congruence", "HSG-CO.B / HSG-CO.C", ["manual", "solve"], [
                "identifying SSS, SAS, ASA, AAS, and HL evidence",
                "completing two-column triangle-congruence proofs",
                "using congruence to solve for corresponding parts",
                "diagnosing invalid AAA or SSA congruence claims",
                "planning proofs with overlapping or auxiliary triangles",
            ]),
            topic("Similarity", "Triangle similarity and proportional reasoning", "HSG-SRT.A / HSG-SRT.B", ["solve", "approx", "manual"], [
                "identifying AA, SAS, and SSS similarity evidence",
                "solving proportions for corresponding sides",
                "using similarity in indirect measurement applications",
                "diagnosing reversed correspondence or scale-factor errors",
                "combining similarity, perimeter, and area scale relationships",
            ]),
            topic("Right triangles", "Pythagorean theorem, special triangles, and right-triangle trigonometry", "HSG-SRT.C.6–C.8", ["approx", "triangle", "eval"], [
                "using Pythagorean and special-right-triangle relationships",
                "writing and evaluating sine, cosine, and tangent ratios",
                "solving right triangles in elevation and depression contexts",
                "diagnosing wrong-ratio, inverse, or degree-mode errors",
                "choosing among Pythagorean, special-triangle, and trig methods",
            ]),
            topic("Coordinate geometry", "Distance, midpoint, slope, and coordinate proof", "HSG-GPE.B.4–B.7", ["distance", "midpoint", "slope", "polygon_area", "manual"], [
                "computing distance and midpoint from coordinates",
                "using slopes to establish parallel or perpendicular lines",
                "finding coordinate polygon perimeter and area",
                "diagnosing coordinate-order or slope-reciprocal errors",
                "proving coordinate figures are special quadrilaterals",
            ]),
            topic("Polygons", "Quadrilaterals and polygon angle relationships", "HSG-CO.C / HSG-SRT.B", ["solve", "manual"], [
                "classifying quadrilaterals from defining properties",
                "using interior and exterior polygon angle sums",
                "applying parallelogram and trapezoid theorems",
                "diagnosing one-way property implications between quadrilaterals",
                "combining classification, angle algebra, and proof",
            ]),
            topic("Circles", "Circle theorems, arcs, sectors, and equations", "HSG-C.B.5", ["approx", "solve", "manual"], [
                "using central, inscribed, and tangent-chord angle relationships",
                "finding arc length and sector area",
                "writing and interpreting circle equations",
                "diagnosing radius-diameter and arc-angle errors",
                "solving multi-theorem circle configurations",
            ]),
            topic("Measurement", "Area, surface area, and volume", "HSG-GMD / HSG-MG", ["approx", "solve", "manual"], [
                "finding areas of triangles, quadrilaterals, and regular polygons",
                "finding surface area of prisms, pyramids, cylinders, and cones",
                "finding volumes of solids including spheres",
                "diagnosing linear, square, and cubic scale-factor confusion",
                "solving composite-solid and density-design applications",
            ]),
            topic("Transformations and construction", "Rigid motions, dilations, symmetry, and constructions", "HSG-CO.A / HSG-CO.D", ["distance", "manual"], [
                "performing coordinate rigid transformations",
                "describing composition of transformations and symmetry",
                "using dilations to create similar figures",
                "diagnosing an incorrect center, vector, or scale factor",
                "planning classical compass-straightedge constructions and justifications",
            ]),
        ],
    },
    {
        "key": "algebra-2",
        "label": "Algebra 2",
        "learner": "an Algebra 2 student",
        "counts": [10, 12, 10, 8, 12],
        "topics": [
            topic("Complex numbers", "Complex-number arithmetic and equations", "HSN-CN", ["eval", "solve", "zeros"], [
                "interpreting powers of i and the complex plane",
                "adding, subtracting, and multiplying complex numbers",
                "dividing complex numbers with conjugates",
                "diagnosing sign and conjugate errors",
                "solving equations and reporting complete complex solution sets",
            ]),
            topic("Polynomials", "Polynomial arithmetic and division", "HSA-APR.A.1", ["expand", "factor", "eval", "equiv"], [
                "adding, subtracting, and multiplying higher-degree polynomials",
                "dividing polynomials by long division",
                "using synthetic division and the remainder theorem",
                "diagnosing quotient alignment and missing-term errors",
                "selecting efficient arithmetic or division representations",
            ]),
            topic("Polynomials", "Polynomial factoring, roots, and graphs", "HSA-APR.B.3", ["factor", "zeros", "solve", "manual"], [
                "factoring cubes and higher-degree expressions",
                "using the rational root theorem to find zeros",
                "connecting zeros, multiplicity, and graph behavior",
                "diagnosing incomplete real or complex zero sets",
                "synthesizing factorization, end behavior, and sign analysis",
            ]),
            topic("Rational functions", "Rational expressions and functions", "HSA-APR.D / HSF-IF.C", ["factor", "equiv", "solve", "limit", "manual"], [
                "simplifying rational expressions with domain restrictions",
                "adding, subtracting, multiplying, and dividing rational expressions",
                "solving rational equations and checking extraneous roots",
                "diagnosing canceled-factor holes versus vertical asymptotes",
                "analyzing rational graphs with intercepts, holes, and asymptotes",
            ]),
            topic("Radicals", "Radical expressions and rational exponents", "HSN-RN / HSA-REI.A", ["eval", "equiv", "solve", "approx"], [
                "rewriting between radicals and rational exponents",
                "simplifying and operating on radical expressions",
                "solving radical equations and checking extraneous roots",
                "diagnosing invalid distribution across sums under radicals",
                "combining radical equations, domains, and approximate solutions",
            ]),
            topic("Exponential and logarithmic functions", "Exponential equations and logarithms", "HSF-LE.A.4, HSF-BF.B.5", ["eval", "solve", "equiv", "approx"], [
                "converting between exponential and logarithmic forms",
                "applying product, quotient, and power log properties",
                "solving exponential and logarithmic equations",
                "diagnosing log-of-a-sum and exponent-factor errors",
                "modeling growth, decay, interest, and half-life",
            ]),
            topic("Functions", "Function composition, inverses, and transformations", "HSF-BF.A.1c, HSF-BF.B.4", ["eval", "solve", "equiv", "manual"], [
                "composing functions from symbolic rules",
                "finding and verifying inverse functions",
                "transforming parent functions with parameter changes",
                "diagnosing reversed composition or unverified inverse domains",
                "connecting compositions, inverses, graphs, and restricted domains",
            ]),
            topic("Systems and matrices", "Nonlinear systems and matrix methods", "HSA-REI.C.7", ["system", "solve", "manual"], [
                "solving linear-quadratic systems graphically",
                "solving nonlinear systems algebraically",
                "performing basic matrix operations",
                "diagnosing extraneous intersections or row-operation errors",
                "using matrices or systems in multivariable modeling",
            ]),
            topic("Sequences and combinatorics", "Sequences, series, and the binomial theorem", "HSF-BF / HSA-APR.C", ["series", "eval", "expand", "solve"], [
                "writing explicit and recursive geometric sequences",
                "finding finite arithmetic and geometric sums",
                "evaluating infinite geometric series when convergent",
                "diagnosing index, common-ratio, or convergence errors",
                "using binomial coefficients and sequence structure in expansions",
            ]),
            topic("Conics and modeling", "Conic sections and nonlinear models", "HSG-GPE.A / HSF-IF", ["solve", "eval", "system", "manual"], [
                "identifying conics from equations and key features",
                "rewriting circle and parabola equations in standard form",
                "analyzing ellipse and hyperbola vertices, foci, and asymptotes",
                "diagnosing sign and denominator errors in conic equations",
                "modeling loci and intersections with conic sections",
            ]),
        ],
    },
    {
        "key": "precalculus-statistics",
        "label": "Precalculus and advanced statistics",
        "learner": "a precalculus or advanced high-school mathematics student",
        "counts": [10, 12, 10, 8, 12],
        "topics": [
            topic("Functions", "Advanced function transformations and composition", "HSF-BF / HSF-IF", ["eval", "equiv", "solve", "manual"], [
                "analyzing transformations with multiple parameters",
                "composing piecewise and nonlinear functions",
                "finding inverses with domain restrictions",
                "diagnosing transformation-order and inverse-domain errors",
                "synthesizing transformations, compositions, and inverse relationships",
            ]),
            topic("Functions", "Polynomial and rational function analysis", "HSA-APR.B.3 / HSF-IF.C", ["zeros", "factor", "limit", "manual"], [
                "using end behavior and multiplicity to sketch polynomials",
                "locating zeros and turning-point constraints",
                "analyzing rational holes, asymptotes, and intercepts",
                "diagnosing false cancellation or asymptote claims",
                "building functions from prescribed graphical and algebraic features",
            ]),
            topic("Exponential and logarithmic modeling", "Advanced exponential and logarithmic models", "HSF-LE.A.4, HSF-BF.B.5", ["solve", "eval", "approx", "equiv"], [
                "solving exponential equations with common bases",
                "solving logarithmic equations with domain checks",
                "fitting and interpreting exponential models",
                "diagnosing model-parameter and logarithm-property errors",
                "comparing compound interest, continuous growth, and logistic contexts",
            ]),
            topic("Trigonometry", "Unit circle and trigonometric graphs", "HSF-TF.A.2, HSF-TF.B.5", ["eval", "solve_interval", "manual"], [
                "finding exact unit-circle values",
                "graphing sine, cosine, and tangent transformations",
                "determining period, amplitude, phase, and vertical shifts",
                "diagnosing degree-radian and quadrant-sign errors",
                "modeling periodic behavior and recovering parameters from graphs",
            ]),
            topic("Trigonometry", "Trigonometric identities and equations", "HSF-TF.C.8", ["equiv", "solve_interval", "eval"], [
                "using reciprocal, quotient, and Pythagorean identities",
                "verifying identities with algebraic transformations",
                "solving trigonometric equations on restricted intervals",
                "diagnosing illegal cancellation and lost-solution errors",
                "combining identities, multiple angles, and exact solution sets",
            ]),
            topic("Trigonometry and vectors", "Oblique triangles, vectors, and bearings", "HSG-SRT.D.10, HSG-SRT.D.11", ["triangle", "approx", "eval", "manual"], [
                "solving AAS and ASA triangles with the law of sines",
                "solving SAS and SSS triangles with the law of cosines",
                "handling ambiguous SSA cases completely",
                "diagnosing wrong-law, bearing, or component errors",
                "combining vector components and triangle laws in navigation problems",
            ]),
            topic("Coordinate systems", "Polar and parametric representations", "HSF-TF / HSN-VM", ["eval", "solve_interval", "manual"], [
                "converting between rectangular and polar coordinates",
                "graphing basic polar curves from equations",
                "evaluating and eliminating parameters from parametric equations",
                "diagnosing quadrant and parameter-orientation errors",
                "analyzing intersections and multiple representations of curves",
            ]),
            topic("Discrete mathematics", "Matrices, counting, probability, and binomial models", "HSN-VM / HSS-CP", ["eval", "probability", "expand", "manual"], [
                "performing matrix operations and transformations",
                "using permutations and combinations",
                "calculating conditional and independent-event probabilities",
                "diagnosing order-sensitive counting and conditional-base errors",
                "using binomial coefficients in probability and algebraic expansion",
            ]),
            topic("Sequences and limits", "Sequences, series, sigma notation, and introductory limits", "HSF-BF / LIM-1", ["series", "limit", "eval", "manual"], [
                "writing sequence rules and sigma notation",
                "evaluating finite arithmetic and geometric series",
                "determining convergence of infinite geometric series",
                "diagnosing index-shift and convergence-condition errors",
                "connecting numerical, graphical, and algebraic ideas of a limit",
            ]),
            topic("Statistics", "Distributions, regression, and inference foundations", "HSS-ID / HSS-IC", ["stats", "read_data", "probability", "manual"], [
                "summarizing distributions with center, spread, and shape",
                "using normal-model z-scores and percentiles",
                "interpreting correlation and least-squares regression",
                "diagnosing causation claims and biased study designs",
                "comparing models and making qualified data-based inferences",
            ]),
        ],
    },
    {
        "key": "calculus-ab-bc",
        "label": "AP Calculus AB and BC",
        "learner": "an AP Calculus AB or BC student",
        "counts": [8, 10, 8, 8, 10],
        "topics": [
            topic("Limits and continuity", "Limits and continuity", "LIM-1, LIM-2", ["limit", "solve", "manual"], [
                "evaluating algebraic limits by factoring and rationalizing",
                "analyzing one-sided, infinite, and end-behavior limits",
                "finding parameters that make piecewise functions continuous",
                "diagnosing direct-substitution and one-sided-sign errors",
                "synthesizing graphical, numerical, and symbolic limit evidence",
            ]),
            topic("Differentiation", "Derivative definition and core rules", "FUN-3.A–FUN-3.C", ["diff", "limit", "eval"], [
                "interpreting derivative as a limit and instantaneous rate",
                "using power, product, and quotient rules",
                "using chain rules for nested functions",
                "diagnosing omitted product or inner-derivative factors",
                "selecting and combining derivative rules efficiently",
            ]),
            topic("Differentiation", "Implicit, inverse, and higher-order differentiation", "FUN-3.D–FUN-3.E", ["diff", "solve", "eval"], [
                "differentiating implicit relations",
                "differentiating inverse and inverse-trigonometric functions",
                "finding second and higher derivatives",
                "diagnosing missing dy/dx and inverse-rule errors",
                "combining implicit, inverse, and higher-order derivative reasoning",
            ]),
            topic("Applications of derivatives", "Derivative applications and modeling", "CHA-3.D / FUN-4.B–FUN-4.C", ["diff", "solve", "approx", "manual"], [
                "writing tangent lines and linearizations",
                "finding extrema with critical-point and endpoint analysis",
                "analyzing motion, monotonicity, and concavity",
                "diagnosing related-rates and optimization setup errors",
                "solving related-rates, optimization, and curve-analysis syntheses",
            ]),
            topic("Integration", "Definite integrals and the Fundamental Theorem", "LIM-5, FUN-6", ["definite_integral", "integrate", "eval", "manual"], [
                "interpreting accumulation and signed area",
                "evaluating definite integrals with antiderivatives",
                "differentiating accumulation functions using the FTC",
                "diagnosing bounds, sign, and variable-of-integration errors",
                "connecting Riemann sums, accumulation, and FTC conclusions",
            ]),
            topic("Integration techniques", "Substitution, parts, partial fractions, and improper integrals", "FUN-6.D–FUN-6.E", ["integrate", "definite_integral", "limit"], [
                "using u-substitution in indefinite and definite integrals",
                "using integration by parts strategically",
                "integrating rational functions with partial fractions",
                "diagnosing unchanged bounds and divergent-improper-integral errors",
                "selecting techniques for mixed BC-level integrals",
            ]),
            topic("Differential equations", "Differential equations and numerical solution", "FUN-7", ["solve", "integrate", "approx", "manual"], [
                "reading and sketching slope fields",
                "solving separable differential equations with initial conditions",
                "using Euler's method from a table of steps",
                "diagnosing separation and initial-condition errors",
                "modeling exponential and logistic growth with differential equations",
            ]),
            topic("Applications of integration", "Area, volume, average value, and motion", "FUN-6", ["definite_integral", "approx", "solve", "manual"], [
                "finding area between curves",
                "finding volumes by disks and washers",
                "finding volumes with known cross sections and shells",
                "diagnosing top-minus-bottom and radius-versus-diameter setup errors",
                "combining average value, accumulated change, and motion applications",
            ]),
            topic("BC parametric and polar calculus", "Parametric, polar, and vector-valued calculus", "FUN-3 / FUN-6", ["diff", "definite_integral", "approx", "manual"], [
                "finding parametric velocity and dy/dx",
                "finding second derivatives and arc length parametrically",
                "finding polar slope and area",
                "diagnosing parameter, polar-bound, and speed-versus-velocity errors",
                "synthesizing vector motion, polar intersections, and accumulated quantities",
            ]),
            topic("BC sequences and series", "Convergence and Taylor series", "LIM-7, LIM-8", ["series", "limit", "eval", "manual"], [
                "classifying geometric and p-series and applying the nth-term test",
                "using comparison, integral, ratio, and alternating-series tests",
                "finding intervals of convergence with endpoint checks",
                "diagnosing inconclusive-test and omitted-endpoint errors",
                "constructing Taylor polynomials and using remainder bounds",
            ]),
        ],
    },
]


def slug(text):
    chars = [c.lower() if c.isalnum() else "-" for c in text]
    return "-".join(part for part in "".join(chars).split("-") if part)


def build_suite():
    tasks = []
    coverage = defaultdict(list)
    index = 0
    for band in BANDS:
        assert len(band["topics"]) == 10
        for topic_index, item in enumerate(band["topics"], 1):
            assert set(item["verification_targets"]) <= VERIFY_TYPES
            for focus_index, focus in enumerate(item["focuses"]):
                index += 1
                variant = VARIANTS[focus_index]
                count = band["counts"][focus_index]
                task_id = f"curr-{index:03d}"
                curriculum_key = (
                    f"{band['key']}/{slug(item['domain'])}/{slug(item['topic'])}/"
                    f"{slug(focus)}"
                )
                review_mode = (
                    "manual_allowed" if "manual" in item["verification_targets"]
                    else "machine_first"
                )
                prompt_text = (
                    f"Create a worksheet containing {count} problems in a "
                    f"{variant['format']} format for "
                    f"{band['learner']} on {item['topic']}, focused specifically on "
                    f"{focus}. {variant['instruction']} Generate and deliver all three "
                    f"PDFs: the student worksheet, a full step-by-step answer key, and "
                    f"a useful 1–2 page study guide. Verify every machine-checkable "
                    f"answer and clearly label any genuinely open response for manual review."
                )
                task = {
                    "id": task_id,
                    "curriculum_key": curriculum_key,
                    "band": band["key"],
                    "band_label": band["label"],
                    "domain": item["domain"],
                    "topic": item["topic"],
                    "focus": focus,
                    "instructional_mode": variant["key"],
                    "standard_refs": item["standard_refs"],
                    "verification_targets": item["verification_targets"],
                    "review_mode": review_mode,
                    "profile": "artifact_trio_acceptance",
                    "prompt": prompt_text,
                    "expected": {
                        "worksheet_problem_count": count,
                        "required_pdf_artifacts": [
                            "student_worksheet", "step_by_step_answer_key", "study_guide"
                        ],
                        "assertions": [
                            f"At least 70% of worksheet problems materially exercise: {focus}.",
                            f"Content is appropriate for {band['label']} and does not depend on unstated later-course prerequisites.",
                            "The answer key shows reasoning, not answer-only output, and every final answer agrees with the worksheet and verification data.",
                            "The study guide directly teaches the requested focus with a rule or model, a worked example, and a distinct try-it item.",
                        ],
                    },
                }
                tasks.append(task)
                for verify_type in item["verification_targets"]:
                    coverage[verify_type].append(task_id)

    assert index == 500
    band_counts = Counter(task["band"] for task in tasks)
    topic_counts = Counter((task["band"], task["topic"]) for task in tasks)
    return {
        "schema_version": "1.0",
        "suite": {
            "name": "math-worksheets 500-prompt curriculum acceptance suite",
            "target_repository": "stellawuellner/math-worksheets-skill",
            "purpose": (
                "Evaluate worksheet, answer-key, and study-guide quality across the "
                "claimed curriculum range from counting through AP Calculus BC."
            ),
            "task_count": len(tasks),
            "curriculum_design": (
                "10 bands × 10 topic families × 5 distinct instructional focuses"
            ),
            "primary_metric": "acceptance_rate",
            "secondary_metrics": [
                "hard_gate_pass_rate", "mean_quality_score_among_hard_gate_passes",
                "acceptance_rate_by_band", "acceptance_rate_by_domain",
                "manual_review_rate", "median_latency_seconds", "median_cost",
            ],
        },
        "execution": {
            "condition": "skill_on",
            "clean_workspace_per_task": True,
            "default_trials_per_task": 1,
            "recommended_shard_size": 25,
            "do_not_expose_judge_rubric_to_generator": True,
            "judge_blind_to_model_and_generation_transcript": True,
            "retain": [
                "prompt", "final_response", "all_pdf_artifacts", "latex_sources",
                "verification_json", "gate_logs", "latency", "token_usage", "cost",
            ],
        },
        "scoring_harness": {
            "script": "scripts/score_eval_run.py",
            "documentation": "evals/scoring-harness.md",
            "stages": ["prepare", "independent_judgment", "aggregate"],
            "machine_outputs": [
                "machine findings", "rendered PDF pages", "judge packets",
                "validated task scores", "run summary", "issue ledger",
            ],
            "trust_boundary": (
                "Deterministic checks collect structural evidence and enforce score "
                "arithmetic; a trained human or independent vision agent judges math, "
                "pedagogy, curriculum alignment, and rendered-page quality."
            ),
        },
        "author_review": {
            "script": "scripts/review_eval_run.py",
            "documentation": "evals/author-review.md",
            "stages": ["prepare", "author_system_diagnosis", "aggregate"],
            "response_per_task": True,
            "official_score_is_immutable": True,
            "github_workflow": ".github/workflows/eval-results.yml",
            "outputs": [
                "validated case reviews", "root-cause category counts",
                "deduplicated improvement backlog", "GitHub issue ledger",
            ],
        },
        "distribution": {
            "tasks_per_band": dict(sorted(band_counts.items())),
            "tasks_per_topic_family": 5,
            "topic_family_count": len(topic_counts),
            "instructional_modes": [variant["key"] for variant in VARIANTS],
        },
        "judge_protocol": {
            "eligible_judges": [
                "trained human reviewer", "independent second agent with PDF vision"
            ],
            "judge_inputs": [
                "the original eval prompt",
                "the three rendered PDFs",
                "worksheet and study-guide verification JSON",
                "gate-chain logs and final delivery response",
            ],
            "review_order": [
                "Read the prompt and inspect PDFs before reading gate logs.",
                "Count worksheet problems and confirm all requested artifacts and focus constraints.",
                "Independently solve or recompute every final answer; do not accept a verifier PASS as the sole correctness oracle.",
                "Check each worked solution, study-guide rule/example/try-it, and any manual item for mathematical and pedagogical validity.",
                "Inspect every rendered page at normal reading size for print and accessibility defects.",
                "Apply hard-fail rules, then score all quality dimensions and emit the structured verdict.",
            ],
            "hard_fail_conditions": [
                "Any requested PDF is missing, unreadable, or not surfaced to the user.",
                "The worksheet problem count differs from the task expectation.",
                "Any problem is mathematically wrong, ambiguous, internally inconsistent, or mismatched with its answer.",
                "Any machine-checkable printed item is absent from verification data or any required repository gate fails.",
                "A genuinely open proof, construction, graph, or explanation is falsely described as machine-verified.",
                "A severe layout defect causes clipping, overlap, missing glyphs, unusably small type, or insufficient answer/work space.",
                "The requested curriculum focus is superficial or appears in fewer than 70% of worksheet problems.",
            ],
            "score_scale": {
                "0": "missing or unusable",
                "1": "major defects",
                "2": "partially acceptable; material revision needed",
                "3": "good and acceptance-ready with only minor issues",
                "4": "excellent",
            },
            "quality_dimensions": {
                "curriculum_alignment": "Accuracy, depth, and fidelity to the named focus and level.",
                "problem_set_design": "Variety, progression, independence of items, and appropriate challenge.",
                "mathematical_correctness": "Correct statements, answers, units, diagrams, and reasoning throughout.",
                "answer_key_quality": "Complete, readable steps that use valid methods and match every problem.",
                "study_guide_quality": "Useful rules/models, strategy-first example, distinct try-it, and direct focus coverage.",
                "clarity_and_accessibility": "Unambiguous language, age fit, notation, accommodations, and cognitive load.",
                "visual_and_print_quality": "Legibility, spacing, page flow, figure quality, and absence of rendering defects.",
                "instruction_following": "Artifact completeness, count, requested format, and honest trust-boundary disclosure.",
            },
            "acceptance_rule": (
                "ACCEPT only when no hard-fail condition applies, every quality dimension "
                "scores at least 3, and the total score is at least 27 of 32."
            ),
            "verdict_schema": {
                "task_id": "curr-NNN",
                "verdict": "ACCEPT or REJECT",
                "hard_failures": ["string"],
                "dimension_scores": {"dimension_name": "integer 0..4"},
                "total_score": "integer 0..32",
                "manual_items_reviewed": "integer",
                "incorrect_or_ambiguous_items": ["problem identifier and explanation"],
                "errors": [
                    {
                        "description": "objective defect with evidence",
                        "severity": "critical, major, or minor",
                        "artifact": "artifact role",
                        "location": "page, problem, or section",
                    }
                ],
                "critical_observations": [
                    {
                        "description": "important evidence-backed observation",
                        "category": "math, pedagogy, layout, accessibility, or instruction",
                    }
                ],
                "artifact_findings": ["concise evidence-backed note"],
                "rationale": "concise acceptance rationale",
            },
        },
        "verifier_type_coverage": {
            verify_type: coverage[verify_type] for verify_type in sorted(VERIFY_TYPES)
        },
        "tasks": tasks,
    }


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) > 1:
        print("Usage: generate_curriculum_suite.py [output.json]", file=sys.stderr)
        return 2
    output = os.path.abspath(argv[0]) if argv else DEFAULT_OUTPUT
    suite = build_suite()
    with open(output, "w", encoding="utf-8") as handle:
        json.dump(suite, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    print(f"Wrote {output}: {len(suite['tasks'])} unique curriculum prompts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
