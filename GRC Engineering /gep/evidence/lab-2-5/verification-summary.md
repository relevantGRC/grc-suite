# Lab 2.5 — Compliance Evidence Verification

## Evidence Identification

- Run ID: test-001
- S3 vault: cgep-lab-grc-evidence-vault-ec861859
- Object key: runs/test-001/bundle.tar.gz
- Capture timestamp: 2026-11-02T22:36:55Z
- Evidence bundle size: 5,284 bytes
- S3 version ID: bi6ufmqMyBFZ1poHMkFrWw0.LE2jkdoz

## Control Verification

| Test | Actual result | Assessment |
|---|---|---|
| Terraform deployment | 7 resources created | Passed |
| S3 Object Lock | GOVERNANCE | Passed |
| Retention expiration | 2026-11-03T22:36:58.488Z | Verified |
| Delete protected version | AccessDenied | Passed |
| Post-deletion HEAD request | Object accessible | Passed |
| At-rest encryption | AES256 | Verified |
| SHA-256 integrity | All 4 files matched manifest | Passed |
| Cosign signing | Signature bundle generated | Completed |
| Signature upload | Confirmed in S3 | Completed |
| Independent signature verification | Not performed | Pending |

## Evidence Files Verified

- plan.json
- state.json
- commit.txt
- version.txt
- manifest.json

## Assessment Notes

The deletion test demonstrated that an ordinary
DeleteObject request without governance bypass
was denied while retention was active.

GOVERNANCE mode does not provide absolute
immutability against authorized bypass requests.

SHA-256 comparisons establish consistency with
the recorded manifest, not independent proof of
the accuracy of source evidence.

The public repository intentionally excludes
Terraform state, binary plans, and the raw
evidence bundle because they may contain
sensitive infrastructure information.

## Remaining Activities

- Complete AWS resource cleanup.
- Remove temporary elevated IAM permissions.
- Update README with final cleanup status.
