# NIST RMF AC-2 Account Management Monitor
### AWS Free Tier | GRC Engineering Project


---

## Project Overview

This project demonstrates a fully automated **NIST RMF Account Management Compliance Monitor** built entirely on the **AWS Free Tier**. It continuously scans IAM accounts, evaluates them against NIST RMF controls, generates a professional HTML compliance reports, and automatically emails them to stakeholders.

This is a real-world GRC engineering implementation that proves the following NIST RMF controls are operational:

| Control | Name | Implementation |
|---|---|---|
| AC-2 | Account Management | IAM user tagging + review date enforcement |
| AC-2(1) | Automated Account Management | Lambda automated scanning |
| AC-2(2) | Removal of Temporary/Inactive Accounts | Inactive account detection |
| AC-2(4) | Automated Audit Actions | CloudTrail + CloudWatch logging |
| AU-6 | Audit Record Review and Reporting | S3 retention + SES email delivery |
| CA-7 | Continuous Monitoring | EventBridge daily schedule |

---

## Security Disclaimer

> All AWS Account IDs, ARNs, access key IDs, and email addresses have been redacted from screenshots using browser developer tools prior to capture. This project uses **fake test accounts only**, no real user data was used. Test accounts were created solely to demonstrate compliance violations for GRC documentation purposes.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    DATA SOURCES                         │
│  AWS IAM → CloudTrail → AWS Config → Fake Test Accounts │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                 MONITORING ENGINE                        │
│     CloudWatch Logs → CloudWatch Alarms → Config Rules  │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│            AUTOMATION (CA-7 Continuous Monitoring)       │
│              Lambda Function → EventBridge               │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│               REPORTING (AU-6 Audit Review)              │
│            S3 Bucket → Report Generator → SES Email      │
└─────────────────────────────────────────────────────────┘
```

---

## Fake Test Accounts & Violations

Five fake IAM accounts were created to simulate real-world compliance violations:

| Username | Type | Violation | Control Triggered |
|---|---|---|---|
| alice.contractor | Contractor | Past review date + PowerUserAccess | AC-2, AC-2(4) |
| bob.tempuser | Temporary | Past review date + active access key | AC-2, AC-2(1) |
| svc.legacy.api | Service | Inactive since 2021 + active key | AC-2(1), AC-2(2) |
| guest.vendor2023 | Guest | Past review date | AC-2 |
| john.doe.inactive | Employee | Never disabled + active access key | AC-2(1), AC-2(2) |

---

## Compliance Results

```
Total Accounts:    7
Compliant:         0
Non-Compliant:     7
Compliance Rate:   0%
Controls Assessed: AC-2, AC-2(1), AC-2(2), AC-2(4), AU-6, CA-7
```

---

## AWS Services Used

| Service | Purpose | Control | Free Tier |
|---|---|---|---|
| AWS IAM | User/role management | AC-2 | Always free |
| CloudTrail | API audit logging | AC-2(4) | 1 free trail |
| AWS Config | Compliance rules | AC-2(1), AC-2(2) | Free 12 months |
| Lambda | Automated scanner | CA-7 | 1M req/month |
| S3 | Report storage | AU-6 | 5GB free |
| SES | Stakeholder emails | AU-6 | 62K emails/month |
| EventBridge | Daily scheduling | CA-7 | 14M events/month |
| CloudWatch | Log monitoring | AC-2(4) | 5GB free |


---

## Repository Structure

```
grc-aws-ac2-monitor/
├── README.md                    ← You are here
├── lambda/
│   └── account_scanner.py       ← Main Lambda scanner
├── screenshots/
│   ├── 01-iam-users.png         ← All fake accounts
│   ├── 02-alice-contractor.png  ← Tags + PowerUserAccess
│   ├── 03-bob-tempuser.png      ← Inactive + active key
│   ├── 04-cloudtrail.png        ← Green logging status
│   ├── 05-cloudwatch-logs.png   ← Lambda execution logs
│   ├── 06-config-noncompliant.png ← NON_COMPLIANT rule
│   ├── 07-s3-reports.png        ← JSON reports stored
│   ├── 08-lambda-function.png   ← Code + test results
│   ├── 09-eventbridge.png       ← Daily schedule enabled
│   ├── 10-ses-verified.png      ← Verified identities
│   └── 11-compliance-email.png  ← Full HTML report
└── docs/
    └── control-mapping.md       ← Detailed control mapping
```

---

## Setup Instructions

### Prerequisites
- AWS Account (Free Tier)
- AWS CLI installed
- Python 3.12
- Verified email addresses in SES

### Phase 1: Enable Core Services
```bash
# Enable CloudTrail
aws cloudtrail create-trail \
  --name grc-account-monitor \
  --s3-bucket-name grc-cloudtrail-logs-[account-id]

# Create S3 report bucket
aws s3 mb s3://grc-reports-[account-id] --region us-east-1
```

### Phase 2: Create Test Accounts
```bash
# Create fake IAM users
aws iam create-user --user-name alice.contractor
aws iam create-user --user-name bob.tempuser
aws iam create-user --user-name svc.legacy.api
aws iam create-user --user-name guest.vendor2023
aws iam create-user --user-name john.doe.inactive

# Tag users with RMF metadata
aws iam tag-user --user-name alice.contractor \
  --tags Key=AccountType,Value=contractor \
         Key=ReviewDate,Value=2023-07-15 \
         Key=Status,Value=active

# Create violations
aws iam create-access-key --user-name bob.tempuser
aws iam create-access-key --user-name svc.legacy.api
aws iam attach-user-policy \
  --user-name alice.contractor \
  --policy-arn arn:aws:iam::aws:policy/PowerUserAccess
```

### Phase 3: Deploy Lambda
```bash
# Create Lambda execution role
aws iam create-role \
  --role-name grc-lambda-execution-role \
  --assume-role-policy-document file://trust-policy.json

# Deploy Lambda function
# See lambda/account_scanner.py for full code
```

### Phase 4: Schedule Daily Scan
```bash
# Create EventBridge schedule
aws scheduler create-schedule \
  --name grc-daily-ac2-scan \
  --schedule-expression "cron(0 13 * * ? *)" \
  --schedule-expression-timezone "America/New_York" \
  --target '{"Arn": "LAMBDA_ARN", "RoleArn": "ROLE_ARN"}' \
  --flexible-time-window '{"Mode": "OFF"}' \
  --state ENABLED
```

---

## Screenshots

### 01: IAM Users List
All 5 fake test accounts visible in IAM console alongside admin accounts.

![IAM Users](screenshots/01-iam-users.png)


---

### 02: alice.contractor - Tags + PowerUserAccess
Shows contractor account with past review date and excessive PowerUserAccess privilege attached that triggers AC-2 and AC-2(4) violations.

![alice.contractor](screenshots/02-alice-contractor.png)

![alice.contractor](screenshots/02-alice-contractorb.png)

---

### 03: bob.tempuser - Inactive + Active Key
Shows temporary account marked inactive but still holding an active access key that triggers AC-2(1) CRITICAL violation.

![bob.tempuser](screenshots/03-bob-tempuser.png)

---

### 04: CloudTrail Green Logging Status
Trail actively logging all IAM API calls to S3 and CloudWatch that satisfies AC-2(4) automated audit actions.

![CloudTrail](screenshots/04-cloudtrail.png)

---

### 05: CloudWatch Lambda Execution Logs
Lambda execution log showing successful scan and email delivery that proves CA-7 continuous monitoring is operational.

![CloudWatch](screenshots/05-cloudwatch.png)

![CloudWatch](screenshots/05-cloudwatchb.png)

![CloudWatch](screenshots/05-cloudwatchc.png)

---

### 06: AWS Config NON-COMPLIANT Rule
Config rule flagging account password policy violation that satisfies AC-2(2) automated compliance detection.

![Config](screenshots/06-config.png)

---

### 07: S3 Reports Bucket
Compliance reports stored in S3 with versioning enabled that satisfies AU-6 audit record retention.

![S3](screenshots/07-s3-reports.png)

![S3](screenshots/07-s3-reportsb.png)

---

### 08: Lambda Function Code + Test Results
Scanner code deployed and test results showing 7 non-compliant accounts detected that proves AC-2(1) automated detection.

![Lambda](screenshots/08-lambda-function.png)

---

### 09: EventBridge Daily Schedule
Schedule running daily at 8:00 AM Eastern that satisfies CA-7 continuous monitoring requirement.

![EventBridge](screenshots/09-eventbridge-schedule.png)

---

### 10: SES Verified Identities
Stakeholder email addresses verified that proves AU-6 reporting channel is configured.

![SES](screenshots/10-ses-verified.png)

---

### 11: Full HTML Compliance Email Report
End-to-end pipeline working that professional HTML report delivered to stakeholder inbox showing all violations across AC-2, AC-2(1), AC-2(2), AC-2(4) controls.

![Email Report](screenshots/11-compliance-email.png)

---

##  Key Findings

```
CRITICAL Violations (3):
  → bob.tempuser:      Inactive account with active access key
  → svc.legacy.api:    Inactive account with active access key
  → john.doe.inactive: Inactive account with active access key

HIGH Violations (6):
  → alice.contractor:  Past review date + excessive privilege
  → guest.vendor2023:  Guest account past review date
  → AdminUser_Jose:    Excessive privilege (AdministratorAccess)
  → grcengineer-admin: Excessive privilege (AdministratorAccess)
```

---

## References

- [NIST SP 800-53 AC-2](https://csrc.nist.gov/projects/cprt/catalog#/cprt/framework/version/SP_800_53_5_1_0/home?element=AC-2)
- [NIST RMF Overview](https://csrc.nist.gov/projects/risk-management)
- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [AWS Free Tier](https://aws.amazon.com/free/)

---

*This project is for educational purposes only. All test accounts and violations are simulated.*
