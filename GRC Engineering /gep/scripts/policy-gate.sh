#!/usr/bin/env bash
# scripts/policy-gate.sh
# Usage: policy-gate.sh --workspace <path> [--policy <dir>]
# Requires a saved tfplan inside the workspace.
set -euo pipefail

POLICY_DIR="policies"
WORKSPACE=""
EVIDENCE_DIR="evidence/lab-3-4"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --workspace) WORKSPACE="$2"; shift 2 ;;
    --policy)    POLICY_DIR="$2"; shift 2 ;;
    *) echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

[[ -z "$WORKSPACE" ]] && {
  echo "Usage: $0 --workspace <path>" >&2
  exit 2
}

mkdir -p "$EVIDENCE_DIR"

terraform -chdir="$WORKSPACE" show -json tfplan > "$WORKSPACE/plan.json"

EXIT=0
{
  echo "["
  FIRST=1

  for ns in compliance.sc28_aws compliance.ac3_aws compliance.cm6_aws; do
    [[ $FIRST -eq 1 ]] && FIRST=0 || printf ","

    set +e
    OUT=$(conftest test --policy "$POLICY_DIR" --namespace "$ns" --output=json "$WORKSPACE/plan.json")
    STATUS=$?
    set -e

    [[ $STATUS -eq 0 ]] || EXIT=1
    printf '%s' "$OUT"
  done

  echo
  echo "]"
} > "$EVIDENCE_DIR/conftest-results.json"

if [[ $EXIT -eq 0 ]]; then
  echo "policy-gate: PASS"
else
  echo "policy-gate: FAIL"
  echo "See $EVIDENCE_DIR/conftest-results.json"
fi

exit $EXIT
