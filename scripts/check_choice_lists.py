#!/usr/bin/env python3
"""Checks that ServiceNow choice lists match the categories and severities the AI service returns.

The service defines them once (Category and Severity in ai-service/app/schemas.py); the HR case and
routing rule tables in servicenow-app/src/fluent/tables.now.ts must offer exactly those values
(routing rules may add "any"). Standard library only. Exits 1 on a mismatch.

Usage: python3 scripts/check_choice_lists.py
"""

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "ai-service/app/schemas.py"
TABLES = ROOT / "servicenow-app/src/fluent/tables.now.ts"


def literal_values(name: str) -> set[str]:
    for node in ast.parse(SCHEMAS.read_text()).body:
        if isinstance(node, ast.Assign) and any(
            getattr(t, "id", None) == name for t in node.targets
        ):
            return {e.value for e in node.value.slice.elts}
    raise SystemExit(f"{name} not found in {SCHEMAS}")


def table_choices(table: str, column: str) -> set[str]:
    source = TABLES.read_text()
    start = source.index(f"name: '{table}'")
    end = source.find("\nexport const", start)
    block = source[start : end if end != -1 else None]
    match = re.search(rf"\b{column}: ChoiceColumn\(\{{.*?choices: \{{(.*?)\}}", block, re.S)
    if not match:
        raise SystemExit(f"{table}.{column} has no choices in {TABLES}")
    return set(re.findall(r"(\w+):", match.group(1)))


def main() -> int:
    expected = {"category": literal_values("Category"), "severity": literal_values("Severity")}
    failures = []
    for table, extra in (
        ("x_2312287_hrorch_hr_case", set()),
        ("x_2312287_hrorch_routing_rule", {"any"}),
    ):
        for column, values in expected.items():
            actual = table_choices(table, column)
            if actual != values | extra:
                failures.append(f"{table}.{column}: {sorted(actual)} != {sorted(values | extra)}")
    for line in failures:
        print("MISMATCH", line)
    print("choice lists match" if not failures else f"{len(failures)} mismatch(es)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
