#!/usr/bin/env python3
"""Build crosswalk artifacts from mappings.yaml."""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

DEFAULT_OUT_MD = Path("crosswalk.md")
DEFAULT_OUT_JSON = Path("crosswalk.json")
DEFAULT_OUT_CSV = Path("crosswalk.csv")

VALID_CONFIDENCE = frozenset({"Strong", "Partial", "Contextual"})
SOC2_CC_PATTERN = re.compile(r"^CC\d+\.\d+$")
NIST_PATTERN = re.compile(r"^[A-Z]{2}-\d+(?:\(\d+\))?$")
ISO_PATTERN = re.compile(r"^A\.[5-8]\.\d+$")
FIELDNAMES = [
    "soc2_cc",
    "nist_800_53",
    "iso_27001_2022",
    "confidence",
    "rationale",
]


def load_mappings(path: Path) -> dict[str, Any]:
    """Read and parse mappings.yaml with yaml.safe_load."""
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if data is None:
        raise ValueError(f"{path}: file is empty")
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be a mapping")
    return data


def validate_mappings(data: dict[str, Any]) -> list[str]:
    """Return a list of validation error messages (empty if valid)."""
    errors: list[str] = []

    mappings = data.get("mappings")
    if not isinstance(mappings, list):
        errors.append("mappings must be a list")
        return errors

    if len(mappings) != 9:
        errors.append(f"mappings must contain exactly 9 rows (found {len(mappings)})")

    for index, row in enumerate(mappings, start=1):
        prefix = f"row {index}"

        if not isinstance(row, dict):
            errors.append(f"{prefix}: must be a mapping")
            continue

        for field in FIELDNAMES:
            if field not in row:
                errors.append(f"{prefix}: missing required field '{field}'")

        soc2_cc = row.get("soc2_cc")
        if not isinstance(soc2_cc, str) or not SOC2_CC_PATTERN.match(soc2_cc):
            errors.append(f"{prefix}: soc2_cc must match CC#.# (got {soc2_cc!r})")

        nist = row.get("nist_800_53")
        if not isinstance(nist, list) or not nist:
            errors.append(f"{prefix}: nist_800_53 must be a non-empty list")
        else:
            for control in nist:
                if not isinstance(control, str) or not NIST_PATTERN.match(control):
                    errors.append(
                        f"{prefix}: invalid nist_800_53 control {control!r}"
                    )

        iso = row.get("iso_27001_2022")
        if not isinstance(iso, list) or not iso:
            errors.append(f"{prefix}: iso_27001_2022 must be a non-empty list")
        else:
            for control in iso:
                if not isinstance(control, str) or not ISO_PATTERN.match(control):
                    errors.append(
                        f"{prefix}: invalid iso_27001_2022 control {control!r}"
                    )

        confidence = row.get("confidence")
        if confidence not in VALID_CONFIDENCE:
            errors.append(
                f"{prefix}: confidence must be one of "
                f"{sorted(VALID_CONFIDENCE)} (got {confidence!r})"
            )

        rationale = row.get("rationale")
        if not isinstance(rationale, str) or not rationale.strip():
            errors.append(f"{prefix}: rationale must be a non-empty string")

    return errors


def _join_controls(controls: list[str]) -> str:
    return " / ".join(controls)


def _md_cell(value: str) -> str:
    return value.replace("|", "\\|")


def _sort_key(row: dict[str, Any]) -> tuple[str, str]:
    nist = row.get("nist_800_53", [])
    primary_nist = nist[0] if isinstance(nist, list) and nist else ""
    return (str(row.get("soc2_cc", "")), primary_nist)


def normalize_rows(mappings: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Sort rows deterministically and flatten control lists to display strings."""
    sorted_rows = sorted(mappings, key=_sort_key)
    normalized: list[dict[str, str]] = []

    for row in sorted_rows:
        normalized.append(
            {
                "soc2_cc": row["soc2_cc"],
                "nist_800_53": _join_controls(row["nist_800_53"]),
                "iso_27001_2022": _join_controls(row["iso_27001_2022"]),
                "confidence": row["confidence"],
                "rationale": " ".join(row["rationale"].split()),
            }
        )

    return normalized


def render_markdown(rows: list[dict[str, str]]) -> str:
    """Return a human-readable Markdown table plus Gaps & Conflicts section."""
    lines = [
        "# SOC 2 / ISO 27001 / NIST 800-53 Rev 5 Crosswalk",
        "",
        "Pivot: SOC 2 Trust Services Criteria (Common Criteria). "
        "NIST 800-53 Rev 5 is the bridge column; "
        "ISO 27001:2022 Annex A is the third column.",
        "",
        "| SOC 2 CC | NIST 800-53 | ISO 27001:2022 | Confidence | Rationale |",
        "| --- | --- | --- | --- | --- |",
    ]

    for row in rows:
        lines.append(
            f"| {_md_cell(row['soc2_cc'])} | {_md_cell(row['nist_800_53'])} | "
            f"{_md_cell(row['iso_27001_2022'])} | {_md_cell(row['confidence'])} | "
            f"{_md_cell(row['rationale'])} |"
        )

    gap_rows = [row for row in rows if row["confidence"] != "Strong"]
    lines.extend(["", "## Gaps & Conflicts", ""])
    for row in gap_rows:
        lines.extend(
            [
                f"### {row['soc2_cc']} / {row['nist_800_53']} ({row['confidence']})",
                "",
                row["rationale"],
                "",
            ]
        )

    return "\n".join(lines) + "\n"


def render_json(rows: list[dict[str, str]]) -> str:
    """Return normalized rows as a JSON array string."""
    return json.dumps(rows, indent=2) + "\n"


def render_csv(rows: list[dict[str, str]]) -> str:
    """Return normalized rows as CSV with README field names."""
    buf = io.StringIO(newline="")
    writer = csv.DictWriter(buf, fieldnames=FIELDNAMES, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue()


def emit_markdown(rows: list[dict[str, str]], path: Path) -> None:
    """Write a human-readable Markdown table plus Gaps & Conflicts section."""
    path.write_text(render_markdown(rows), encoding="utf-8", newline="")


def emit_json(rows: list[dict[str, str]], path: Path) -> None:
    """Write normalized rows as a JSON array."""
    path.write_text(render_json(rows), encoding="utf-8", newline="")


def emit_csv(rows: list[dict[str, str]], path: Path) -> None:
    """Write normalized rows as CSV with README field names."""
    path.write_text(render_csv(rows), encoding="utf-8", newline="")


def check_drift(
    rows: list[dict[str, str]],
    md_path: Path,
    json_path: Path,
    csv_path: Path,
    *,
    source_label: str = "mappings.yaml",
) -> list[str]:
    """Compare freshly rendered artifacts to on-disk files; return drift messages."""
    artifacts = (
        (md_path, render_markdown(rows)),
        (json_path, render_json(rows)),
        (csv_path, render_csv(rows)),
    )
    messages: list[str] = []

    for path, expected in artifacts:
        try:
            actual = path.read_bytes()
        except OSError as exc:
            messages.append(
                f"error: {path}: {exc} (expected from {source_label})"
            )
            continue

        if actual == expected.encode("utf-8"):
            continue

        messages.append(
            f"error: {path}: drift vs {source_label} (rebuild required)"
        )

    return messages


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build crosswalk artifacts from mappings.yaml"
    )
    parser.add_argument(
        "--source",
        required=True,
        type=Path,
        help="Path to mappings.yaml",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help=(
            "Validate mappings and verify committed artifacts match a fresh build "
            "(no emit)"
        ),
    )
    parser.add_argument("--out-md", type=Path, help="Output Markdown path")
    parser.add_argument("--out-json", type=Path, help="Output JSON path")
    parser.add_argument("--out-csv", type=Path, help="Output CSV path")
    args = parser.parse_args()

    try:
        data = load_mappings(args.source)
    except (OSError, yaml.YAMLError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    errors = validate_mappings(data)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    if args.check:
        md_path = args.out_md or DEFAULT_OUT_MD
        json_path = args.out_json or DEFAULT_OUT_JSON
        csv_path = args.out_csv or DEFAULT_OUT_CSV
        rows = normalize_rows(data["mappings"])
        drift_messages = check_drift(
            rows,
            md_path,
            json_path,
            csv_path,
            source_label=str(args.source),
        )
        if drift_messages:
            for message in drift_messages:
                print(message, file=sys.stderr)
            return 1
        return 0

    missing_outputs = [
        name
        for name, value in (
            ("--out-md", args.out_md),
            ("--out-json", args.out_json),
            ("--out-csv", args.out_csv),
        )
        if value is None
    ]
    if missing_outputs:
        parser.error(
            "the following arguments are required when not using --check: "
            + ", ".join(missing_outputs)
        )
    try:
        rows = normalize_rows(data["mappings"])
        emit_markdown(rows, args.out_md)
        emit_json(rows, args.out_json)
        emit_csv(rows, args.out_csv)
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
