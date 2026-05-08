# S3 Audit

A Python tool that audits all S3 buckets in your AWS account for security compliance — encryption at rest and public access block enforcement. Built for GRC engineers, compliance analysts, and assessors working in FedRAMP High and CJIS v6.0 environments where bucket misconfigurations create direct evidence-handling risk.

## Compliance Controls Addressed

| NIST 800-53 Rev 5 | FedRAMP High | CJIS v6.0 | Validation Method |
|--------------------|:------------:|:---------:|-------------------|
| SC-28 Protection of Information at Rest | Yes | Agency-managed CMK required | `get_bucket_encryption` API check |
| SC-28(1) Cryptographic Protection | Yes | — | Verifies SSE-KMS or AES-256 algorithm |
| AC-3 Access Enforcement | Yes | — | `get_public_access_block` enforces deny-by-default |
| AC-21 Information Sharing | Yes | — | Public access block prevents inadvertent CJI exposure |
| CM-6 Configuration Settings | Yes | — | Verifies all four PAB settings are enabled |
| AU-12 Audit Record Generation | Yes | — | Every audit run produces compliance evidence |

## Overview

Two scripts:

1. **`s3_audit.py`** — Audits buckets for encryption and public access block compliance.
2. **`deploy_test_buckets.py`** — Creates test buckets with various configurations to exercise the audit script.

## Requirements

- Python 3.x
- `boto3` library
- AWS CLI configured with credentials (`aws configure`)

### Install dependencies

```bash
pip install boto3
```

## Usage

### Run the audit

```bash
python s3_audit.py
```

**Sample output:**

```
Found 4 buckets.

Checking bucket: my-secure-bucket
    [PASS] Encryption: AES256
    [PASS] Public Access Block: Enabled
Checking bucket: my-partial-bucket
    [PASS] Encryption: AES256
    [WARN] Public Access Block: Partially configured
Checking bucket: my-insecure-bucket
    [PASS] Encryption: AES256
    [FAIL] Public Access Block: Not configured

========================================
Summary: 1 of 3 buckets fully compliant.
```

### Deploy test buckets (optional)

```bash
python deploy_test_buckets.py
```

Creates 3 buckets with different configurations to test the audit script:

| Bucket | Public Block | Expected Result |
|--------|--------------|-----------------|
| `grce-audit-compliant-<account_id>` | Full | PASS |
| `grce-audit-no-block-<account_id>` | None | FAIL |
| `grce-audit-partial-<account_id>` | Partial | WARN |

## Compliance Checks

### 1. Encryption (SC-28, SC-28(1))

Verifies server-side encryption (SSE) is enabled.

- **PASS** — Encryption configured (AES-256 or SSE-KMS)
- **FAIL** — No encryption configured

### 2. Public Access Block (AC-3, AC-21, CM-6)

Verifies all four public access block settings are enabled:

- `BlockPublicAcls`
- `IgnorePublicAcls`
- `BlockPublicPolicy`
- `RestrictPublicBuckets`

- **PASS** — All 4 enabled
- **WARN** — Partial (some enabled)
- **FAIL** — None enabled

## How an Auditor Uses This Output

An assessor reviewing a FedRAMP High or CJIS v6.0 authorization package can run this script across the in-scope account to verify that every bucket holding regulated data satisfies the SC-28 (encryption at rest) and AC-3 / AC-21 (public access prevention) controls. The PASS / WARN / FAIL output maps directly to the assessor's adequacy determination: PASS is satisfied, WARN is a partial finding requiring remediation, FAIL is a control deficiency. Combining this run with `cloudtrail-audit` (logging) and `evidence-logger` (timestamped evidence packaging) produces the audit trail an assessor can reference back to NIST 800-53A assessment objectives.

## FedRAMP 20x Alignment

This script supports the FedRAMP 20x compliance-as-code direction by producing deterministic, automatable, and re-runnable control validation output. The boto3 API calls map cleanly to KSI metrics for continuous monitoring, and the per-bucket findings can be transformed into OSCAL Assessment Results entries for machine-readable compliance reporting. Future iterations will emit JSON output (see Future Enhancements) to feed compliance-trestle and OSCAL pipelines directly.

## CJIS v6.0 Relevance

CJIS v6.0 became the audit standard on April 1, 2026 and aligns with NIST 800-53 Rev 5 as of December 2024. The most material delta this script touches is **SC-28**: CJIS v6.0 requires encryption at rest using **agency-managed Customer Master Keys (CMKs)** for buckets storing CJI. AWS-managed encryption (AES-256 / SSE-S3) satisfies FedRAMP High SC-28 but does **not** satisfy CJIS v6.0 — agencies must provision their own KMS CMKs and configure SSE-KMS with those CMKs. A future enhancement to this script will report the encryption *key source* (not just whether encryption is on) to surface this delta during an audit.

## Cleanup

Delete test buckets when done to avoid charges:

```bash
aws s3 rb s3://grce-audit-compliant-<your_account_id>
aws s3 rb s3://grce-audit-no-block-<your_account_id>
aws s3 rb s3://grce-audit-partial-<your_account_id>
```

## Future Enhancements

- Export results to CSV / JSON for downstream OSCAL pipelines
- Report encryption key source (CMK ARN) to surface the CJIS SC-28 agency-CMK delta
- Add timestamp + structured findings record (feeds `evidence-logger`)
- Check bucket versioning (SI-12 — Information Management & Retention)
- Check bucket logging (AU-2)
- Filter buckets by tag (in-scope CJI vs general data)
- SNS / email alerts for non-compliant buckets

## Framework Reference

Control family mappings and AWS implementation details are documented in [nist-800-53-rev-5-to-aws-mapping](https://github.com/0xBahalaNa/nist-800-53-rev-5-to-aws-mapping).

## License

MIT
