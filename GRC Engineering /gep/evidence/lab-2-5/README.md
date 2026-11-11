# Lab 2.5 — Infrastructure as Code as Compliance Evidence

**Platform:** Amazon Web Services (AWS)  
**Status:** Completed — technical implementation and testing  
**Lab Date:** November 2, 2026  
**Official Lab:** [GRC Engineering Club Lab 2.5](https://github.com/GRCEngClub/cgep-labs/blob/main/guides/02_05_iac_as_compliance_evidence.md)

## 1. Project Overview

This project demonstrates how Infrastructure as Code
(IaC) can produce machine-readable compliance evidence
that can be collected, hashed, preserved, and tested.

Using Terraform, AWS S3, Bash, SHA-256, and Cosign,
I implemented an automated evidence-capture workflow
and tested the controls protecting its evidence.

The objective was to go beyond documenting that a
security control exists and demonstrate that it
operates as intended.

## 2. Technologies Used

| Technology | Purpose |
|---|---|
| Terraform | Deploy AWS infrastructure |
| AWS S3 | Store compliance evidence |
| S3 Object Lock | Enforce evidence retention |
| AWS CLI | Deploy, inspect, and test AWS resources |
| Git Bash | Execute evidence automation |
| SHA-256 | Verify evidence integrity |
| Cosign | Cryptographically sign the archive |
| GitHub | Version control and documentation |

## 3. Architecture and Workflow

1. Deploy compliant S3 infrastructure using Terraform.
2. Deploy a separate evidence vault.
3. Enable versioning, encryption, and Object Lock.
4. Capture Terraform plan and state evidence.
5. Generate SHA-256 hashes and an evidence manifest.
6. Upload the evidence bundle to the S3 vault.
7. Record the uploaded object version and timestamp.
8. Verify the retention policy.
9. Attempt deletion of the protected object version.
10. Retrieve the evidence and verify its file hashes.
11. Sign the downloaded evidence archive with Cosign.
12. Upload the signature bundle to AWS S3.

## 4. Implemented Security Controls

| Control | Configuration |
|---|---|
| Encryption at rest | SSE-S3 AES-256 |
| Bucket versioning | Enabled |
| Object Lock | Enabled |
| Retention mode | GOVERNANCE |
| Default retention | 1 day |
| Public access | Blocked |
| Integrity verification | SHA-256 |
| Digital signing | Cosign keyless signing |

GOVERNANCE mode protects object versions against
ordinary deletion requests during retention, but
authorized users can bypass governance retention
with appropriate permissions.

## 5. Deployment Results

The evidence vault was successfully deployed
using Terraform.

**Terraform result:**
- 7 resources added
- 0 changed
- 0 destroyed

The vault configuration included Object Lock,
versioning, encryption, and public-access controls.

## 6. Compliance Evidence Captured

The evidence bundle contained:

- `plan.json` — Terraform plan in JSON format
- `state.json` — Terraform state evidence
- `commit.txt` — Git commit metadata
- `version.txt` — Terraform version information
- `manifest.json` — SHA-256 hashes and metadata

The archive was uploaded to a versioned S3
evidence vault.

**Capture Run ID:** `test-001`

## 7. Control Testing and Verification

| Test | Result |
|---|---|
| Terraform deployment | Passed |
| Evidence capture and upload | Passed |
| S3 object version identification | Passed |
| GOVERNANCE retention verification | Passed |
| Protected object deletion attempt | AccessDenied — Passed |
| Evidence availability after deletion attempt | Passed |
| AES-256 encryption verification | Passed |
| SHA-256 manifest comparison | 4 of 4 matched |
| Cosign signing | Completed |
| Signature upload to S3 | Completed |
| Independent Cosign verification | Not performed |

The deletion attempt returned:

`AccessDenied: Access Denied because object protected by object lock.`

The subsequent HEAD request confirmed that the
same protected object version remained accessible.

## 8. Challenges and Troubleshooting

### AWS IAM Permissions

**Issue:** Terraform initially failed because
the IAM user lacked `s3:CreateBucket` permission.

**Resolution:** Reviewed IAM permissions and
temporarily assigned AWS S3 access for the lab.

**Lesson:** Authentication and authorization
are distinct security controls.

### Missing Terraform Directory

**Issue:** The evidence-vault configuration was
initially created outside the Git repository.

**Resolution:** Moved the lab configuration into
the correct repository directory.

**Lesson:** Verify working directories before
initializing or applying Terraform.

### AWS CLI and Git Bash Path Compatibility

**Issue:** The AWS CLI could not parse the
Unix-style path passed to `--body`.

**Resolution:** Converted the local archive path
using `cygpath -w`.

**Lesson:** Native Windows tools and Git Bash
may interpret file paths differently.

### Evidence Upload and Retention

**Issue:** AWS initially returned `NoSuchKey`
because the evidence had not been uploaded.

**Resolution:** Corrected the capture script,
successfully uploaded the bundle, and verified
its specific S3 object version.

### Cosign Keyless Signing

**Issue:** Cosign required browser authentication.

**Resolution:** Authenticated through Sigstore
using an existing GitHub identity.

**Lesson:** Digital signing strengthens evidence
provenance but requires verification and
appropriate management of public signing identity.

### Git Synchronization

**Issue:** GitHub rejected the initial push
because remote changes were ahead of the
local repository.

**Resolution:** Fetched remote changes,
rebased the local commit, and pushed successfully.

### S3 Cleanup

**Issue:** An initial version-deletion command
returned `Invalid version id specified`.

**Status:** Cleanup is pending. Object versions,
retention restrictions, and bucket policy must
be handled before infrastructure destruction.

## 9. GRC and Audit Perspective

This lab demonstrates three important
evidence-management properties:

**Integrity:** SHA-256 hashes provide a method
for detecting changes relative to the manifest.

**Attribution:** Git metadata, AWS identity,
timestamps, and Cosign signing establish
supporting provenance information.

**Reproducibility:** Terraform configuration
and scripts document how infrastructure
and evidence were generated.

Relevant control areas include:

- NIST SP 800-53: AU-9, AU-11, SC-28, CM-6
- ISO/IEC 27001:2022: A.5.33 and A.8.24
- NIST CSF 2.0: PR.DS-01

These are control alignments, not a claim that
this individual lab demonstrates full compliance.

## 10. Evidence and Source Files

- [Evidence Receipt](receipt.json)
- [Control Verification Summary](verification-summary.md)
- [Terraform Evidence Vault](../../terraform/primitives/evidence-vault/)
- [Evidence Capture Script](../../scripts/capture-evidence.sh)

Raw Terraform state, binary plans, and the
original evidence archive are excluded from
this public repository because they may
contain sensitive infrastructure information.

## 11. Final Assessment

**Technical implementation: Completed**  
**Evidence integrity verification: Passed**  
**Object Lock negative testing: Passed**  
**Optional digital signing: Completed**  
**Independent signature verification: Not performed**  
**AWS resource cleanup: Pending**  
**Temporary IAM permission removal: Pending**

The project demonstrates a repeatable approach
to capturing, protecting, and validating
technical compliance evidence.

The remaining operational activities are
infrastructure cleanup and revocation of
temporary elevated IAM permissions.
