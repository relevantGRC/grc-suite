#!/usr/bin/env python3
"""Generate a markdown mapping document from an OSCAL Component Definition JSON file.

Reads the nested OSCAL structure:
  component-definition → components[] → control-implementations[] → implemented-requirements[]

and produces a markdown table mapping NIST 800-53 Rev 5 controls to AWS services.
"""

import argparse
import json
import sys


def parse_args():
    """Parse command-line arguments for input and output paths.

    Uses argparse following the same CLI pattern as compliance-trestle:
    explicit --input and --output flags, no positional arguments, no hardcoded paths.
    """
    parser = argparse.ArgumentParser(
        description="Generate a NIST 800-53 Rev 5 to AWS mapping from OSCAL Component Definition JSON."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the OSCAL Component Definition JSON file.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path for the generated markdown file.",
    )
    parser.add_argument(
        "--fedramp-only",
        action="store_true",
        help="Only include controls with fedramp-high: true in the output.",
    )
    return parser.parse_args()


def load_component_definition(input_path):
    """Load and return the OSCAL Component Definition from a JSON file.

    Handles two expected failure modes separately so the error message
    tells you *what* went wrong (PCC3e Ch 10 — using specific exception
    types rather than a bare except).

    Returns the top-level component-definition dict on success.
    Prints an error message and exits with code 1 on failure.
    """
    try:
        with open(input_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {input_path}: {e}", file=sys.stderr)
        sys.exit(1)

    return data


def extract_mappings(component_definition):
    """Walk the OSCAL Component Definition and extract control-to-service mappings.

    Traverses three levels of nesting:
      1. components[] — each AWS service
      2. control-implementations[] — per-framework grouping (e.g., NIST 800-53 source)
      3. implemented-requirements[] — per-control detail

    For each implemented-requirement, extracts the control-id, description,
    and custom props (fedramp-high, cjis-delta).

    Returns a list of dicts, each representing one row in the output table.
    """
    mappings = []

    # Access the components array from the top-level component-definition object.
    # .get() returns an empty list if the key is missing, so the for loop
    # simply doesn't execute rather than raising a KeyError (PCC3e Ch 6 — dict.get()).
    components = component_definition.get("component-definition", {}).get("components", [])

    for component in components:
        service_title = component.get("title", "Unknown Service")

        # Second level: control-implementations[] — the per-framework grouping.
        control_implementations = component.get("control-implementations", [])

        for ctrl_impl in control_implementations:
            # Third level: implemented-requirements[] — the per-control detail.
            implemented_reqs = ctrl_impl.get("implemented-requirements", [])

            for req in implemented_reqs:
                control_id = req.get("control-id", "unknown")
                description = req.get("description", "")

                # Extract props into a dict keyed by prop name for easy lookup.
                # Props is a list of {"name": ..., "value": ...} objects.
                props = {p["name"]: p["value"] for p in req.get("props", [])}

                fedramp_high = props.get("fedramp-high", "false")
                cjis_delta = props.get("cjis-delta", "")

                mappings.append({
                    "control_id": control_id.upper(),
                    "service": service_title,
                    "description": description,
                    "fedramp_high": fedramp_high,
                    "cjis_delta": cjis_delta,
                })

    return mappings


def write_markdown(mappings, output_path, fedramp_only=False):
    """Write the extracted mappings to a markdown file as a table.

    When fedramp_only is True, the document title reflects the filtered scope.
    Uses a with statement for safe file handling — the file is closed
    automatically even if an error occurs during writing (PCC3e Ch 10).
    """
    try:
        with open(output_path, "w") as f:
            if fedramp_only:
                f.write("# NIST 800-53 Rev 5 to AWS Service Mapping — FedRAMP High Baseline\n\n")
            else:
                f.write("# NIST 800-53 Rev 5 to AWS Service Mapping\n\n")
            f.write("| Control ID | AWS Service | Description | FedRAMP High | CJIS Delta |\n")
            f.write("|------------|-------------|-------------|:------------:|------------|\n")

            for mapping in mappings:
                # Replace pipe characters in description text so they don't
                # break the markdown table structure.
                desc = mapping["description"].replace("|", "\\|")
                cjis = mapping["cjis_delta"].replace("|", "\\|")

                f.write(
                    f"| {mapping['control_id']} "
                    f"| {mapping['service']} "
                    f"| {desc} "
                    f"| {mapping['fedramp_high']} "
                    f"| {cjis if cjis else 'N/A'} "
                    f"|\n"
                )

            # CJIS v6.0 Delta Requirements section — only controls where CJIS
            # exceeds the FedRAMP High baseline. Filtered using a list
            # comprehension that checks for non-empty cjis_delta strings
            # (PCC3e Ch 4 — an empty string is falsy in Python, so
            # `if m["cjis_delta"]` filters out both "" and missing values).
            cjis_deltas = [m for m in mappings if m["cjis_delta"]]

            if cjis_deltas:
                f.write("\n## CJIS v6.0 Delta Requirements\n\n")
                f.write("Controls where CJIS v6.0 exceeds the FedRAMP High baseline.\n\n")
                f.write("| Control ID | AWS Service | CJIS Additional Requirement |\n")
                f.write("|------------|-------------|-----------------------------|\n")

                for mapping in cjis_deltas:
                    cjis = mapping["cjis_delta"].replace("|", "\\|")
                    f.write(
                        f"| {mapping['control_id']} "
                        f"| {mapping['service']} "
                        f"| {cjis} "
                        f"|\n"
                    )
    except OSError as e:
        print(f"Error: Could not write to {output_path}: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Generated mapping: {output_path}")


def main():
    args = parse_args()
    data = load_component_definition(args.input)
    mappings = extract_mappings(data)

    # Filter to FedRAMP High controls when --fedramp-only is passed.
    # List comprehension filters the mappings list by checking the fedramp_high
    # value in each dict (PCC3e Ch 4 — list comprehensions for filtering).
    if args.fedramp_only:
        mappings = [m for m in mappings if m["fedramp_high"] == "true"]

    write_markdown(mappings, args.output, fedramp_only=args.fedramp_only)


if __name__ == "__main__":
    main()
