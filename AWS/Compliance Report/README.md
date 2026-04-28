# Compliance Report

A Python tool that aggregates findings from multiple AWS audit checks (S3, IAM, security groups) into a unified, professional HTML compliance report. Built for GRC engineers, compliance analysts, and assessors working in FedRAMP High and CJIS v6.0 environments where regular control assessments and continuous monitoring are binding obligations.

## Compliance Controls Addressed

| NIST 800-53 Rev 5 | FedRAMP High | CJIS v6.0 | Validation Method |
|--------------------|:------------:|:---------:|-------------------|
| CA-2 Control Assessments | Yes | — | The HTML report is the control-assessment artifact |
| CA-7 Continuous Monitoring | Yes | Continuous monitoring expected | Regular generation supports ongoing control assessment |
| AU-3 Content of Audit Records | Yes | — | Report includes timestamp, account, findings, severity, status |
| AU-12 Audit Record Generation | Yes | — | Every report run produces a structured, dated artifact |
| PM-31 Continuous Monitoring Strategy | Yes | — | Report integrates with the broader monitoring approach |
| SI-4 System Monitoring | Yes | — | Aggregates monitoring findings into a single review surface |

## Overview

Builds on previous audits (S3, IAM, Security Groups) and combines them into a single report generator using:

- **Functions** — Refactored audit logic into reusable functions
- **Jinja2** — HTML templating for professional reports
- **Data aggregation** — Unified findings from multiple sources

## Requirements

- Python 3.x
- `boto3` library
- `jinja2` library
- AWS CLI configured with credentials (`aws configure`)

### Install dependencies

```bash
pip install boto3 jinja2
```

## Usage

### Generate a compliance report

```bash
python compliance_report.py
```

**Sample output:**

```
============================================================
AWS Compliance Report Generator
============================================================

[1/4] Getting account information...
      Account: 365827925154

[2/4] Auditing S3 buckets...
      Found 1 buckets

[3/4] Auditing IAM users...
      Found 1 users

[4/4] Auditing security groups...
      Found 1 security groups

Generating HTML report...

✓ Report saved: compliance_report_20260121_162513.html

Open the HTML file in a browser to view the report.
```

### View the report

Open the generated `.html` file in any web browser.

## Report Contents

### Executive Summary
- Total passed checks (green)
- Total failed checks (red)
- Total warnings (yellow)

### S3 Bucket Audit (SC-28, AC-3, AC-21)

| Check | Description |
|-------|-------------|
| Encryption | Server-side encryption enabled? |
| Public Access Block | All four settings enabled? |

### IAM User Audit (IA-2, AC-2)

| Check | Description |
|-------|-------------|
| Console Access | Does user have AWS Console login? |
| MFA Enabled | Is MFA configured for console users? |

### Security Group Audit (SC-7, CM-7)

| Check | Description |
|-------|-------------|
| Open Ports | Ports open to `0.0.0.0/0` (non-risky) |
| Risky Ports | SSH, RDP, database ports open to internet |

## Status Legend

| Status | Meaning | Color |
|--------|---------|-------|
| `PASS` | Check passed | Green |
| `FAIL` | Critical issue | Red |
| `WARN` | Review recommended | Yellow |
| `INFO` | Informational only | Blue |

## How an Auditor Uses This Output

An assessor reviewing a FedRAMP High or CJIS v6.0 authorization package can use the HTML report as a single, executive-readable view of multi-control assessment status. The Executive Summary maps directly to the assessor's high-level adequacy determination across S3, IAM, and SG controls; the per-section tables drill into the specific check results so the assessor can spot-check individual findings. Generated regularly (weekly / monthly), the report becomes the artifact that satisfies CA-7 (Continuous Monitoring) — proof that controls are not just designed but continuously verified. Distributed to system owners, it also serves as the working document for closing out CA-5 (Plan of Action and Milestones) items.

## FedRAMP 20x Alignment

This script supports FedRAMP 20x compliance-as-code by aggregating multi-control findings into a single artifact suitable for KSI metric extraction and continuous monitoring dashboards. A future enhancement will add OSCAL Assessment Results JSON output alongside the HTML so the same data feeds compliance-trestle and OSCAL-based pipelines without re-collection. The dated, never-overwriting filename pattern (`compliance_report_<timestamp>.html`) is the foundational unit for trend analysis under FedRAMP 20x continuous-monitoring expectations.

## CJIS v6.0 Relevance

CJIS v6.0 (audit standard from April 1, 2026) requires continuous monitoring and weekly audit-record review for systems handling Criminal Justice Information (CJI). The compliance report is the *review surface* for that workflow — a single document an authorizing official, system owner, or CJIS coordinator reviews to confirm controls are satisfied and findings are being remediated on schedule. Combined with `cloudtrail-audit` (AU-6 review tooling), `evidence-logger` (timestamped evidence), and S3 Object Lock archival (1-year retention), the report becomes the visible top of a fully audit-defensible CJIS continuous-monitoring stack.

## Future Enhancements

- Add CloudTrail findings to report (AU-6 events)
- Export to PDF
- Email report automatically (CA-7 distribution)
- Add charts / graphs with Chart.js (KSI visualization)
- Compare with previous reports (trend analysis)
- Add remediation recommendations linked to control IDs
- Emit OSCAL Assessment Results JSON alongside HTML (FedRAMP 20x)

## Framework Reference

Control family mappings and AWS implementation details are documented in [nist-800-53-rev-5-to-aws-mapping](https://github.com/0xBahalaNa/nist-800-53-rev-5-to-aws-mapping).

## License

MIT
