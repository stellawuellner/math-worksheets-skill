#!/usr/bin/env python3
r"""test_unit_binding.py — direct unit tests of tests/_units.py, the shared
matcher both unit gates (check_answer_key.py, check_answer_line.py) build on.

The fixture suite proves the gates end to end; these tests pin the matcher's
edge semantics — token-sequence (never substring) matching, the wrapper
drops, the deg/degrees ≡ ^\circ alias, longest-match lexicon scanning, and
the declared/expected-string filters — so a refactor cannot quietly loosen
what counts as a printed unit. Mirrors test_answer_key_binding.py's role.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from _units import tokenize, unit_in, same_unit, undeclared_units  # noqa: E402
import verify  # noqa: E402

FAILS = []


def check(name, cond):
    print(f"  {'✅' if cond else '❌'} {name}")
    if not cond:
        FAILS.append(name)


print("tokenize:")
check("macro + word + caret + digit split",
      tokenize(r"\text{cm^2}") == ["\\text", "{", "cm", "^", "2", "}"])
check("math wrapper split", tokenize("cm$^2$") == ["cm", "$", "^", "2", "$"])

print("unit_in (forward matching):")
check("plain \\text{ft}", unit_in(r"6.30\ \text{ft}", "ft"))
check("thin-space \\,", unit_in(r"6.30\,\text{ft}", "ft"))
check("split \\text{cm}^2 satisfies cm^2", unit_in(r"17\ \text{cm}^2", "cm^2"))
check("math-wrapped cm$^2$ satisfies cm^2", unit_in(r"cm$^2$", "cm^2"))
check("two-word square units", unit_in(r"6\ \text{square units}", "square units"))
check("km/h token run", unit_in(r"\text{km/h}", "km/h"))
check("degrees satisfied by ^\\circ alias", unit_in(r"48.19^\circ", "degrees"))
check("deg satisfied by ^\\circ alias", unit_in(r"48.19^\circ", "deg"))
check("wrong unit does not match", not unit_in(r"6.30\ \text{m}", "ft"))
check("substring never matches: undefined vs in",
      not unit_in(r"\text{undefined}", "in"))
check("bare number does not match", not unit_in("6.30", "ft"))

print("same_unit:")
check("deg alias", same_unit("deg", "degrees") and same_unit("degrees", "deg"))
check("distinct units differ", not same_unit("m", "mm"))

print("undeclared_units (reverse gate):")
check("undeclared \\text{ft} is found",
      undeclared_units(r"7\ \text{ft}", []) == ["ft"])
check("declared unit is filtered",
      undeclared_units(r"7\ \text{ft}", [], declared=["ft"]) == [])
check("split \\text{cm}^2 with declared cm^2 is clean (sub-sequence filter)",
      undeclared_units(r"17\ \text{cm}^2", [], declared=["cm^2"]) == [])
check("longest match wins: square units is ONE unit",
      undeclared_units(r"\text{square units}", []) == ["square units"])
check("connective \\text{ or } is clean by construction",
      undeclared_units(r"x = 2 \text{ or } x = 3", []) == [])
check("\\text{undefined} with expected 'undefined' is clean",
      undeclared_units(r"\text{undefined}", ["undefined"]) == [])
check("expected-string filter: '3 ft' keeps \\text{ft} clean",
      undeclared_units(r"\text{ft}", ["3 ft"]) == [])
check("\\mathrm is scanned too",
      undeclared_units(r"5\ \mathrm{kg}", []) == ["kg"])
check("degrees printed vs declared deg is clean (alias)",
      undeclared_units(r"\text{degrees}", [], declared=["deg"]) == [])

print("verify.py answer_unit schema (the field the gates bind to):")


def schema_rejects(name, problem):
    try:
        verify.check_schema(problem)
        check(name, False)
    except verify.VerifyInputError:
        check(name, True)


schema_rejects("empty answer_unit rejected",
               {"id": 1, "type": "approx", "expr": "1", "expected": 1,
                "answer_unit": "  "})
schema_rejects("non-string answer_unit rejected",
               {"id": 1, "type": "approx", "expr": "1", "expected": 1,
                "answer_unit": 3})
try:
    verify.check_schema({"id": 1, "type": "approx", "expr": "1", "expected": 1,
                         "answer_unit": "ft"})
    check("answer_unit 'ft' accepted on any type (universal field)", True)
except verify.VerifyInputError:
    check("answer_unit 'ft' accepted on any type (universal field)", False)

print()
if FAILS:
    print(f"❌ {len(FAILS)} unit-binding test(s) failed")
    sys.exit(1)
print("✅ All unit-binding tests passed")
