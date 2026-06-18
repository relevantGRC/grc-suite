An automated Compliance-as-Code and Evidence Generation repository designed to map native AWS infrastructure telemetry to the ISO/IEC 27001:2022 Annex A control framework.
This repository tracks custom automated Lambda scanners, security boundaries, and logging pipelines to prove continuous operational compliance to external ISMS auditors.

## 🏗️ Architecture Blueprint
                     ┌────────────────── [ AWS Organizations / SCPs ] ──────────────────┐
                     │                                                                  │
[IAM / Users] ───► [EventBridge] ───► [AWS Lambda] ───► [CloudWatch / Metric Filters]  │
                     │                    │                                             │
                     ▼                    ▼                                             ▼
             [Tagging Policy]     [IAM Credential Report]                       [Amazon SES Alerts]
                                          │
                                          ▼
                               ┌─────────────────────┐
                               │  S3 Security Bucket │
                               │  (Object Lock /     │
                               │   Compliance Mode)  │
                               └─────────────────────┘
## 📊 Control Mapping & Evidence Matrix
This solution maps specific cloud architecture implementations directly to the ISO/IEC 27001:2022 Annex A controls, establishing a continuous monitoring loop.
|ISO 27001:2022 |Control	Domain / Control Name|	AWS Technical Implementation|	Automation / Evidence Artifact|
|-|-|-|-|
A.5.15	Access control	

## 🛠️ Repository Directory Structure

```Plaintext
grc-aws-iso27001-monitor/
├── .github/
│   └── workflows/
│       └── policy-ci.yml           # IaC security scanning pipeline (Checkov)
├── policies/
│   └── scp-tagging-enforcement.json# SCP ensuring resources cannot skip lifecycle tags
├── terraform/
│   ├── main.tf                     # Deploys Config, Security Hub, CloudTrail
│   ├── s3-log-bucket-immutable.tf  # Provisions Object Locked bucket for A.8.12
│   └── variables.tf
├── src/
│   └── lambda/
│       ├── access_lifecycle_scanner.py # Pulls credential reports for A.8.16
│       └── inactive_user_remediator.py # Automated lifecycle remediation for A.8.18
├── cloudwatch/
│   └── metric-filters-alarms.json  # Definitions for high-risk monitoring alerts
└── README.md                       # This documentation map
