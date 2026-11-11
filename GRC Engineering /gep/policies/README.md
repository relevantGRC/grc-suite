# Lab 3.3 - Compliance Policies in Rego

These policies evaluate Google Cloud resources in Terraform plan JSON
before infrastructure deployment.

## SC-28 - Encryption at Rest
- File: sc28_encryption.rego
- Framework: NIST SP 800-53 SC-28
- Severity: High
- Requirement: Google Cloud Storage buckets must use CMEK.
- Remediation: Configure an encryption block with a customer-managed KMS key.

## AC-3 - Access Enforcement
- File: ac3_no_public.rego
- Framework: NIST SP 800-53 AC-3
- Severity: Critical
- Requirement: Enforce bucket public access protections and prevent publicly accessible SSH/RDP management ports.
- Remediation: Enforce uniform bucket-level access and public access prevention; restrict or remove unsafe firewall rules.

## CM-6 - Configuration Settings
- File: cm6_required_tags.rego
- Framework: NIST SP 800-53 CM-6
- Severity: Medium
- Requirement: Supported resources must have project, environment, managed_by, and compliance_scope labels.
- Remediation: Add missing required labels.

## Validation
- Eight automated unit tests.
- Four intentional violations detected in the original Terraform plan.
- All four addressed in the corrected plan.
- Final policy evaluations returned zero violations.
- No cloud resources deployed.

## Evidence
See evidence/lab-3-3/opa-test-results.json for automated unit test results.

## Lab 3.4 - AWS Policy Variants

The policy library supports GCP and AWS implementations of three NIST SP 800-53 controls.

| Control | GCP Policy (Lab 3.3) | AWS Policy (Lab 3.4) |
|---|---|---|
| SC-28 - Encryption at Rest | sc28_encryption.rego | sc28_encryption_aws.rego |
| AC-3 - Access Enforcement | ac3_no_public.rego | ac3_no_public_aws.rego |
| CM-6 - Configuration Settings | cm6_required_tags.rego | cm6_required_tags_aws.rego |

### AWS Control Requirements

- SC-28: Each S3 bucket requires a matching explicit server-side encryption configuration.
- AC-3: Each S3 bucket requires all four public-access-block settings enabled.
- CM-6: Applicable AWS resources require Project, Environment, ManagedBy, and ComplianceScope tags.

### Automated Policy Gate

The policy gate evaluates a saved Terraform plan using Conftest and AWS-specific Rego policies.

Run from the repository root:

    bash scripts/policy-gate.sh --workspace terraform/primitives/compliant-s3

A compliant configuration returns exit code 0.
A noncompliant configuration returns exit code 1.

### Lab 3.4 Audit Evidence

- evidence/lab-3-4/conftest-pass.json - compliant test results
- evidence/lab-3-4/conftest-fail.json - negative test demonstrating SC-28 enforcement

The lab performs Terraform plan evaluation only. No infrastructure is deployed.

The policies demonstrate selected configuration checks, not comprehensive NIST compliance.
