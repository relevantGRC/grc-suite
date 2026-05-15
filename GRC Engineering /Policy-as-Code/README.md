This folder contains all Policy as Code labs.

# Policy-as-Code Framework

This repository implements Policy-as-Code aligned with:

- ISO/IEC 27001
- NIST SP 800-53
- ISO/IEC 42001 (AI Governance)

## Structure

- policies/ → Policy definitions + enforcement logic
- frameworks/ → Control mappings
- pipelines/ → CI/CD enforcement
- exceptions/ → Approved deviations
- evidence/ → Logs and artifacts

## Policy Engine

We use Open Policy Agent (OPA):
https://www.openpolicyagent.org/

## How It Works

1. Policies defined (YAML + Rego)
2. Mapped to controls
3. Enforced in CI/CD
4. Violations logged as evidence
