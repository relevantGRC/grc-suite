# NIST RMF Control Mapping
## GRC AWS AC-2 Account Management Monitor

---

## AC-2 - Account Management

**Control Requirement:**
The organization manages information system accounts including establishing, activating, modifying, reviewing, disabling, and removing accounts.

| Requirement | Implementation | AWS Service | Evidence |
|---|---|---|---|
| Account creation policy | IAM user tagging with AccountType, ReviewDate, Status | AWS IAM | Screenshot 01 |
| Periodic review | ReviewDate tag enforced by Lambda scanner | Lambda | Screenshot 08 |
| Temporary account management | Contractor/guest accounts flagged when past review date | Lambda + Config | Screenshot 11 |
| Account removal | Inactive accounts flagged for immediate action | Lambda | Screenshot 11 |

**Violations Detected:**
- alice.contractor - contractor account past review date (2023-07-15)
- bob.tempuser - temporary account past review date (2023-01-01)
- guest.vendor2023 - guest account past review date (2023-06-01)

---

## AC-2(1) - Automated System Account Management

**Control Requirement:**
The organization employs automated mechanisms to support the management of information system accounts.

| Requirement | Implementation | AWS Service | Evidence |
|---|---|---|---|
| Automated account detection | Lambda scans all IAM users automatically | Lambda | Screenshot 08 |
| Inactive account detection | Scanner checks last activity and Status tag | Lambda + IAM | Screenshot 11 |
| Active key detection | Scanner checks for active keys on inactive accounts | Lambda + IAM | Screenshot 03 |
| Automated alerting | HTML report emailed to stakeholders automatically | SES | Screenshot 11 |

**Violations Detected:**
- bob.tempuser - inactive account has 1 active access key (CRITICAL)
- svc.legacy.api - inactive account has 1 active access key (CRITICAL)
- john.doe.inactive - inactive account has 1 active access key (CRITICAL)

---

## AC-2(2) - Removal of Temporary/Emergency Accounts

**Control Requirement:**
The information system automatically removes or disables temporary and emergency accounts after an organization-defined time period.

| Requirement | Implementation | AWS Service | Evidence |
|---|---|---|---|
| Temporary account tracking | AccountType tag identifies temporary accounts | AWS IAM | Screenshot 01 |
| Automatic expiration check | Lambda evaluates ReviewDate against current date | Lambda | Screenshot 08 |
| Inactive account detection | Config rule flags unused credentials | AWS Config | Screenshot 06 |
| Compliance reporting | Violations documented in daily report | S3 + SES | Screenshot 07, 11 |

**Config Rule:**
- iam-user-unused-credentials-check (maxCredentialUsageAge: 90)

---

## AC-2(4) — Automated Audit Actions

**Control Requirement:**
The information system automatically audits account creation, modification, enabling, disabling, and removal actions.

| Requirement | Implementation | AWS Service | Evidence |
|---|---|---|---|
| Account creation logging | Every CreateUser API call logged | CloudTrail | Screenshot 04 |
| Policy attachment logging | AttachUserPolicy events captured | CloudTrail | Screenshot 04 |
| Access key logging | CreateAccessKey events captured | CloudTrail | Screenshot 04 |
| Log storage | All logs stored in S3 and CloudWatch | S3 + CloudWatch | Screenshot 05, 07 |
| Excessive privilege detection | Lambda flags admin/power policies | Lambda | Screenshot 02, 11 |

**CloudTrail Events Captured:**
- CreateUser
- TagUser
- AttachUserPolicy
- CreateAccessKey
- DeleteAccessKey

**Violations Detected:**
- AdminUser_Jose - AmazonGuardDutyFullAccess + AdministratorAccess (HIGH)
- alice.contractor - PowerUserAccess on contractor account (HIGH)
- grcengineer-admin - AdministratorAccess (HIGH)

---

## AU-6 — Audit Record Review, Analysis, and Reporting

**Control Requirement:**
The organization reviews and analyzes information system audit records for indications of inappropriate or unusual activity and reports findings to designated officials.

| Requirement | Implementation | AWS Service | Evidence |
|---|---|---|---|
| Audit record review | Lambda analyzes all IAM accounts daily | Lambda | Screenshot 08 |
| Analysis | Violations evaluated against RMF controls | Lambda | Screenshot 11 |
| Reporting | HTML report generated with findings | Lambda + SES | Screenshot 11 |
| Record retention | JSON reports stored in S3 with versioning | S3 | Screenshot 07 |
| Stakeholder notification | Report emailed to verified recipients daily | SES | Screenshot 10, 11 |

**Report Contents:**
- Total accounts scanned
- Compliant vs non-compliant count
- Compliance percentage
- Per-account violation details
- Control references for each finding
- Severity ratings (CRITICAL/HIGH/MEDIUM)

---

## CA-7 - Continuous Monitoring

**Control Requirement:**
The organization develops a continuous monitoring strategy and implements a continuous monitoring program.

| Requirement | Implementation | AWS Service | Evidence |
|---|---|---|---|
| Automated scanning | Lambda function scans daily | Lambda | Screenshot 08 |
| Scheduled execution | EventBridge cron runs every day at 8AM ET | EventBridge | Screenshot 09 |
| Real-time logging | CloudWatch captures all executions | CloudWatch | Screenshot 05 |
| Config rules | AWS Config evaluates compliance continuously | AWS Config | Screenshot 06 |
| Trend tracking | Multiple JSON reports stored in S3 over time | S3 | Screenshot 07 |
| Stakeholder updates | Daily email keeps stakeholders informed | SES | Screenshot 11 |

**Schedule:**
```
cron(0 13 * * ? *)
= Every day at 8:00 AM Eastern Time
= Every day at 1:00 PM UTC
```

---

## Control Coverage Summary

```
Control   Status    AWS Services                    Violations Found
AC-2      Active    IAM, Lambda, Config             3 accounts
AC-2(1)   Active    Lambda, IAM, SES                3 CRITICAL
AC-2(2)   Active    Config, Lambda                  2 accounts
AC-2(4)   Active    CloudTrail, CloudWatch, Lambda  3 HIGH
AU-6      Active    S3, SES, Lambda                 Reports generated
CA-7      Active    EventBridge, Lambda, CloudWatch Running daily
```

---

## Remediation Recommendations

| Finding | Recommended Action | Priority |
|---|---|---|
| Inactive accounts with active keys | Immediately disable access keys | CRITICAL |
| Accounts past review date | Review and disable or extend | HIGH |
| Excessive privilege | Apply least privilege principle | HIGH |
| No password policy | Enforce strong password policy | MEDIUM |

---

*Control mapping based on NIST SP 800-53 Revision 5*
