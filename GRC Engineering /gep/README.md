# GRC Engineering — Hands-On Labs

Hands-on learning repository documenting my journey through the GRC Engineering Club, focused on building, enforcing, testing, and verifying security controls through infrastructure automation.

The objective is to develop practical GRC engineering skills by connecting compliance requirements with Infrastructure as Code (IaC), Policy as Code (PaC), automated control validation, and audit-ready evidence.

This repository documents implementation steps, technical challenges, troubleshooting, lessons learned, and the business applications of each lab.

---

## Project Objectives

- Build secure and compliant cloud infrastructure using Terraform.
- Translate security requirements into technical controls.
- Develop and test automated compliance policies.
- Implement Policy as Code using Open Policy Agent (OPA) and Rego.
- Generate and verify infrastructure compliance evidence.
- Learn how automation can improve control testing and audit readiness.
- Connect GRC engineering practices to real-world security, risk management, and compliance operations.

## Technologies

| Technology | Purpose |
|---|---|
| Terraform | Infrastructure as Code |
| AWS | Cloud infrastructure and security controls |
| Google Cloud Platform | Cloud infrastructure and security controls |
| Open Policy Agent (OPA) | Automated policy evaluation |
| Rego | Policy as Code language |
| Conftest | Terraform policy compliance testing |
| tfsec | Terraform security configuration scanning |
| GitHub Actions | Automated CI/CD compliance validation |
| GitHub OIDC | Temporary AWS authentication for CI workflows |
| Git and GitHub | Version control and documentation |
| Git Bash | Command-line environment |
| Visual Studio Code | Development environment |
| Cosign | Cryptographic signing and verification |
| SHA-256 | Evidence integrity verification |

## Lab Progress

| Lab | Project | Status |
|---|---|---|
| 2.3 | Building Your First Compliant Resource — AWS S3 | Completed |
| 2.4 | Terraform Modules for Compliance — GCP | Completed |
| 2.5 | IaC as Compliance Evidence — AWS | Completed |
| 3.3 | Writing Compliance Policies in Rego — GCP | Completed |
| 3.4 | Integrating Policy as Code with Terraform | Completed |
| 4.3 | Building a GRC Evidence Pipeline — AWS + GitHub Actions | Completed |
| 4.4 | Evidence Management and Chain of Custody — AWS | In Progress |

---

## Lab Documentation

### Lab 2.3 — Building Your First Compliant Resource

**Cloud Platform:** Amazon Web Services (AWS)

**Status:** Completed

**Objective:** Build a compliant AWS S3 bucket using Terraform and demonstrate how security controls can be defined and implemented through Infrastructure as Code.

**Implementation:**
- Configured Terraform for AWS.
- Created an S3 bucket using Terraform.
- Implemented server-side encryption.
- Configured S3 public access restrictions.
- Enabled bucket versioning.
- Generated Terraform execution plans.
- Collected infrastructure configuration evidence.

**Security controls implemented:**
- Encryption at rest using AES-256.
- S3 Public Access Block configuration.
- S3 bucket versioning.

**Key learning outcomes:**
- Understanding Terraform resource configurations.
- Implementing security requirements through code.
- Validating cloud infrastructure before deployment.
- Connecting technical cloud controls to compliance requirements.

**Source Code:**
[Compliant AWS S3 Terraform Configuration](terraform/primitives/compliant-s3/)

**Current Status:** Completed.

---

### Lab 2.4 — Terraform Modules for Compliance

**Cloud Platform:** Google Cloud Platform (GCP)

**Status:** Completed

**Objective:** Develop reusable Terraform modules that implement consistent security controls for Google Cloud Storage resources.

**Implementation:**
- Configured Terraform with Google Cloud.
- Developed a reusable Google Cloud Storage module.
- Created development and production Terraform configurations.
- Implemented secure storage configuration requirements.
- Built negative test configurations to evaluate noncompliant scenarios.
- Validated Terraform configurations and execution plans.
- Documented configuration and troubleshooting steps.

**Security controls addressed:**
- Cloud Storage encryption configuration.
- Public access restrictions.
- Uniform bucket-level access.
- Resource configuration standardization.

**Key learning outcomes:**
- Developing reusable Infrastructure as Code modules.
- Applying consistent security configurations across environments.
- Testing compliant and noncompliant infrastructure definitions.
- Supporting standardized security controls through automation.

**Source Code:**
- [GCP Terraform Module](terraform/modules/compliant-gcs-bucket/)
- [GCP Compliant Configuration](terraform/primitives/compliant-gcs/)
- [GCP Production Configuration](terraform/primitives/compliant-gcs-prod/)
- [GCP Negative Testing](terraform/primitives/compliant-gcs-negative/)

**Current Status:** Completed.

---

### Lab 2.5 — Infrastructure as Code as Compliance Evidence

**Cloud Platform:** Amazon Web Services (AWS)

**Status:** Completed

**Objective:** Demonstrate how Infrastructure as Code artifacts can be collected, stored, protected, and verified as supporting compliance evidence.

**Implementation:**
- Created Terraform-managed AWS infrastructure.
- Configured a dedicated evidence storage environment.
- Developed an automated evidence capture workflow.
- Collected Terraform plan and state artifacts.
- Generated an evidence bundle containing infrastructure configuration information.
- Uploaded evidence to Amazon S3.
- Implemented evidence retention protections using S3 Object Lock.
- Verified object retention enforcement.
- Downloaded and inspected the stored evidence bundle.
- Calculated SHA-256 hashes to support integrity verification.
- Used Cosign to generate cryptographic signature evidence.
- Documented verification activities and troubleshooting steps.

**Security and compliance capabilities:**
- Automated infrastructure evidence collection.
- Evidence integrity verification.
- Protected evidence storage.
- Retention enforcement.
- Cryptographic signing.
- Reproducible audit evidence workflows.

**Key learning outcomes:**
- Understanding how IaC can support audit evidence collection.
- Automating evidence capture and preservation.
- Verifying evidence integrity.
- Understanding the role of retention controls in audit readiness.
- Connecting infrastructure automation to GRC and third-party risk management processes.

**Source Code:**
- [Evidence Capture Script](scripts/capture-evidence.sh)
- [Terraform Evidence Vault](terraform/primitives/evidence-vault/)

**Evidence and Documentation:**
- [Lab 2.5 Evidence Documentation](evidence/lab-2-5/README.md)
- [Evidence Verification Report](evidence/lab-2-5/verification-summary.md)
- [AWS Evidence Upload Receipt](evidence/lab-2-5/receipt.json)

**Official Lab Guide:**
[Lab 2.5 — IaC as Compliance Evidence](https://github.com/GRCEngClub/cgep-labs/blob/main/guides/02_05_iac_as_compliance_evidence.md)

**Current Status:** Completed — implementation, evidence capture, control testing, and optional signing. AWS infrastructure cleanup completed and verified. Temporary IAM permission removal awaits confirmation.

---

### Lab 3.3 — Writing Compliance Policies in Rego

**Cloud Platform:** Google Cloud Platform (GCP)

**Status:** Completed

**Objective:** Translate security and compliance requirements into automated Policy as Code controls using Open Policy Agent (OPA) and Rego.

**Implementation:**
- Created a Terraform test fixture containing compliant and intentionally noncompliant GCP resource configurations.
- Generated Terraform execution plans without deploying cloud infrastructure.
- Converted Terraform plans into JSON for automated policy evaluation.
- Developed three compliance policies using Rego.
- Created automated tests for compliant and noncompliant scenarios.
- Evaluated Terraform configurations against security requirements.
- Identified and remediated intentional control violations.
- Revalidated the corrected configurations.
- Generated machine-readable policy test evidence.

**Security Controls Implemented:**

| Control | Requirement | Severity |
|---|---|---|
| NIST SC-28 | Require customer-managed encryption keys for GCP storage buckets | High |
| NIST AC-3 | Enforce storage access protections and detect publicly accessible management ports | Critical |
| NIST CM-6 | Require standardized compliance labels on supported cloud resources | Medium |

**Automated Validation Results:**
- 8 of 8 automated policy tests passed.
- 4 intentional security configuration violations detected.
- 1 encryption configuration violation identified.
- 2 access control violations identified.
- 1 missing-label configuration violation identified.
- All 4 violations addressed.
- Final Terraform policy evaluations returned zero violations.
- No Google Cloud resources were deployed.

**Remediation Performed:**
- Added customer-managed encryption configuration to the noncompliant storage bucket.
- Enforced uniform bucket-level access and public access prevention.
- Added the four required compliance labels.
- Removed the unnecessary publicly accessible SSH firewall rule.
- Regenerated Terraform plans and verified the corrected results.

**Key Learning Outcomes:**
- Writing compliance requirements as executable Rego policies.
- Evaluating Terraform plans before cloud infrastructure deployment.
- Building automated positive and negative policy tests.
- Detecting security misconfigurations before deployment.
- Implementing a detect, remediate, retest, and verify workflow.
- Generating evidence to support compliance control testing.

**Source Code:**
- [Rego Compliance Policies](policies/)
- [Automated Rego Tests](policies/tests/)
- [Terraform Test Fixture](terraform/primitives/policy-fixture/main.tf)
- [Policy Documentation](policies/README.md)

**Compliance Evidence:**
- [OPA Automated Test Results](evidence/lab-3-3/opa-test-results.json)

**GitHub Commit:** `a205f81`

**Official Lab Guide:**
[Lab 3.3 — Writing Compliance Policies in Rego](https://github.com/GRCEngClub/cgep-labs/blob/main/guides/03_03_writing_compliance_policies_rego.md)

**Current Status:** Completed — three compliance policies implemented, eight automated tests passed, four intentional violations remediated, and supporting test evidence published.

---

### Lab 3.4 — Integrating Policy as Code with Terraform

**Cloud Platform:** Amazon Web Services (AWS)

**Status:** Completed

**Objective:** Integrate Policy as Code (PaC) with Terraform using Open Policy Agent (OPA), Rego, and Conftest to automatically evaluate infrastructure security configurations before deployment.

**Implementation:**
- Reused the compliant AWS S3 Terraform configuration from Lab 2.3.
- Extended the Rego policy library developed in Lab 3.3.
- Created three AWS-specific compliance policies.
- Generated Terraform execution plans and exported them to JSON.
- Integrated Conftest to evaluate AWS Terraform plans.
- Implemented a reusable automated policy gate using Bash.
- Tested compliant and intentionally noncompliant configurations.
- Generated machine-readable JSON compliance evidence.
- Validated policy syntax and regression tests.
- Published the policy definitions, automation script, and evidence to GitHub.

**Security Controls Implemented:**

| Control | Requirement | Severity |
|---|---|---|
| NIST SC-28 | Require explicit S3 server-side encryption configuration | High |
| NIST AC-3 | Require all four S3 Public Access Block settings | Critical |
| NIST CM-6 | Enforce standardized required AWS resource tags | Medium |

**Automated Validation Results:**
- 8 of 8 existing OPA regression tests passed.
- All 3 AWS-specific Conftest policy evaluations passed against the compliant Terraform plan.
- Generated a compliant Terraform plan containing 11 planned resources.
- Created an intentionally noncompliant Terraform configuration by removing the primary S3 bucket's encryption configuration.
- Generated a valid noncompliant Terraform plan containing 10 planned resources.
- Confirmed Conftest detected the SC-28 violation.
- Verified the negative test returned exit code 1.
- Confirmed the automated policy gate returned PASS for the compliant configuration and FAIL for the noncompliant configuration.
- Successfully generated JSON evidence for both test scenarios.
- No AWS infrastructure was deployed during this lab.

**Technical Challenges and Troubleshooting:**
- Installed Conftest and configured Git Bash to recognize the executable.
- Resolved Windows ZIP extraction and PATH configuration issues.
- Corrected AWS credential availability for Terraform.
- Updated the temporary negative-test workspace to remove an output reference to the intentionally deleted resource.
- Resolved Terraform plan generation errors.
- Verified that Conftest failures were caused by security policy violations rather than configuration or JSON parsing errors.
- Addressed GitHub synchronization issues while preserving previous lab work.

**Key Learning Outcomes:**
- Translating security and compliance requirements into executable policies.
- Integrating OPA, Rego, Conftest, and Terraform.
- Understanding the importance of cloud-specific policy coverage.
- Implementing automated positive and negative security control tests.
- Using policy evaluation exit codes to support deployment decisions.
- Building reusable compliance validation scripts.
- Generating structured audit evidence automatically.
- Understanding how Policy as Code can support preventive controls in CI/CD pipelines.

**GRC and Business Value:**
- Reduces repetitive manual infrastructure compliance reviews.
- Detects defined security configuration gaps before deployment.
- Supports consistent enforcement of technical security requirements.
- Produces repeatable evidence for compliance assessments.
- Improves control testing efficiency and audit readiness.
- Provides a foundation for continuous compliance validation.
- Supports risk-based cloud governance and infrastructure security assurance.

**Source Code:**
- [AWS SC-28 Encryption Policy](policies/sc28_encryption_aws.rego)
- [AWS AC-3 Public Access Policy](policies/ac3_no_public_aws.rego)
- [AWS CM-6 Required Tags Policy](policies/cm6_required_tags_aws.rego)
- [Automated Policy Gate Script](scripts/policy-gate.sh)
- [Policy Documentation](policies/README.md)

**Compliance Evidence:**
- [Compliant Policy Test Results](evidence/lab-3-4/conftest-pass.json)
- [Noncompliant Policy Test Results](evidence/lab-3-4/conftest-fail.json)

**Official Lab Guide:**
[Lab 3.4 — Integrating PaC with Terraform](https://github.com/GRCEngClub/cgep-labs/blob/main/guides/03_04_integrating_pac_with_terraform.md)

**Current Status:** Completed — AWS-specific policies implemented, automated compliance gate validated, positive and negative testing completed, and supporting JSON evidence generated.

**Note:** These tests validate selected security configuration requirements and do not independently establish full compliance with NIST SP 800-53.

---

### Lab 4.3 — Building a GRC Evidence Pipeline

**Cloud Platform:** Amazon Web Services (AWS) and GitHub Actions

**Status:** Completed

**Objective:** Extend the Policy as Code implementation from Lab 3.4 into a GitHub Actions workflow that automatically evaluates Terraform changes, performs security scanning, and captures compliance evidence.

**Implementation:**
- Configured AWS authentication through OpenID Connect (OIDC).
- Created an AWS IAM role for GitHub Actions with repository-specific trust conditions.
- Configured the GitHub repository variable `AWS_ROLE_ARN`.
- Integrated Terraform execution planning into GitHub Actions.
- Automated security policy evaluation using Conftest and AWS-specific Rego policies.
- Integrated tfsec to identify Terraform security configuration findings.
- Generated and retained evidence artifacts from GitHub Actions workflow executions.
- Configured GitHub branch protection to require successful security checks before merging into `main`.
- Tested intentionally noncompliant and compliant pull request scenarios.
- Verified security check results, evidence generation, and pull request outcomes.

**Security Controls Evaluated:**

| Control | Requirement | Validation |
|---|---|---|
| NIST SC-28 | Require explicit S3 server-side encryption configuration | Conftest / Rego |
| NIST AC-3 | Require all four S3 Public Access Block settings | Conftest / Rego and tfsec |
| NIST CM-6 | Enforce standardized required AWS resource tags | Conftest / Rego |

**Automated Validation Results:**
- AWS OIDC authentication completed successfully through GitHub Actions.
- Terraform execution plans generated successfully in the workflow.
- Conftest successfully evaluated the AWS-specific compliance policies.
- tfsec security scanning executed successfully against compliant Terraform configurations.
- All 11 OPA unit tests passed during additional policy testing.
- Generated and verified all four required evidence files:
  - `plan.json`
  - `plan.txt`
  - `conftest-results.json`
  - `tfsec.sarif`
- Red Pull Request #6 intentionally violated AC-3 by disabling an S3 Public Access Block setting.
- Confirmed the Red PR failed both Conftest and tfsec security validation.
- Green Pull Request #7 retained compliant security configurations and passed the required security check.
- Successfully merged the Green PR into `main`.
- Configured GitHub branch protection requiring the `grc-gate` check before future merges.
- Closed the intentionally failing pull request and deleted the remote test branches.

**Technical Challenges and Troubleshooting:**
- Configured AWS IAM permissions and GitHub OIDC trust conditions.
- Resolved authentication and infrastructure planning issues during workflow setup.
- Corrected security findings affecting the Terraform configuration.
- Updated the workflow to execute the required Lab 4.3 evidence pipeline.
- Validated AWS-specific policy failures through intentional negative testing.
- Verified the exact GitHub Actions status check required for branch protection.
- Preserved existing lab files and previous documentation while managing Git branches.
- Confirmed the workflow and protected branch configuration through GitHub CLI.

**Key Learning Outcomes:**
- Integrating infrastructure security validation into CI/CD workflows.
- Configuring temporary AWS authentication through GitHub OIDC.
- Running Terraform, Conftest, and tfsec through GitHub Actions.
- Evaluating infrastructure changes against defined security requirements.
- Demonstrating failing and passing security control checks.
- Using GitHub branch protection to enforce successful checks before merging.
- Generating repeatable, machine-readable evidence for compliance assessments.
- Understanding how automated policy evaluation can support preventive controls.

**GRC and Business Value:**
- Reduces manual infrastructure compliance validation.
- Detects security configuration violations during pull request reviews.
- Supports consistent security control enforcement.
- Helps prevent noncompliant infrastructure changes from being merged when required checks are enforced.
- Generates repeatable evidence supporting internal audits and compliance reviews.
- Improves traceability between infrastructure changes, security checks, and validation results.
- Establishes a foundation for automated evidence management and chain-of-custody processes.

**Source Code:**
- [GitHub Actions GRC Evidence Pipeline](.github/workflows/grc-gate.yml)
- [AWS OIDC Trust Configuration](terraform/primitives/oidc-trust/)
- [AWS Terraform Configuration](terraform/primitives/compliant-s3/)
- [AWS Rego Compliance Policies](policies/)

**Compliance Evidence:**
- [Red Pull Request #6 — Failed Security Validation](https://github.com/Cesarmora809/cgep-labs/pull/6)
- [Red GitHub Actions Run — Security Violation Detected](https://github.com/Cesarmora809/cgep-labs/actions/runs/42733050114)
- [Green Pull Request #7 — Successful Security Validation](https://github.com/Cesarmora809/cgep-labs/pull/7)
- [Successful Evidence Pipeline Run](https://github.com/Cesarmora809/cgep-labs/actions/runs/42732687452)

**Official Lab Guide:**
[Lab 4.3 — Building a GRC Evidence Pipeline (AWS + GitHub Actions)](https://github.com/GRCEngClub/cgep-labs/blob/main/guides/04_03_grc_evidence_pipeline.md)

**Current Status:** Completed — AWS OIDC authentication configured, GitHub Actions evidence pipeline operational, Conftest and tfsec validation successful, four required evidence files verified, red and green pull request demonstrations completed, branch protection enabled, and test branch cleanup completed.

**Note:** Security validation demonstrates the selected Terraform configuration controls under laboratory conditions. It does not independently establish comprehensive compliance with NIST SP 800-53 or prove the deployed state of AWS infrastructure.

---

### Lab 4.4 — Evidence Management and Chain of Custody

**Cloud Platform:** Amazon Web Services (AWS) and GitHub Actions

**Status:** In Progress

**Objective:** Build on the infrastructure compliance evidence workflows developed in Labs 2.5 and 4.3 to understand evidence integrity, cryptographic verification, and chain-of-custody practices for automated GRC engineering processes.

**Planned Implementation:**
- Follow the official Lab 4.4 evidence management and chain-of-custody instructions.
- Build upon the evidence collection and retention concepts introduced in Lab 2.5.
- Use the compliance evidence generated through the Lab 4.3 pipeline.
- Explore cryptographic signing and verification of evidence artifacts.
- Validate evidence integrity and document chain-of-custody results.
- Record the required implementation activities, verification results, and troubleshooting.

**Expected GRC and Business Value:**
- Improve confidence in the integrity of collected compliance evidence.
- Support traceability and verification of evidence artifacts.
- Reduce the risk of undetected evidence modification.
- Strengthen audit readiness through repeatable evidence verification.
- Improve the reliability of technical evidence used in security assurance and compliance activities.

**Official Lab Guide:**
[Lab 4.4 — Evidence Management and Chain of Custody (AWS)](https://github.com/GRCEngClub/cgep-labs/blob/main/guides/04_04_evidence_chain_of_custody.md)

**Current Status:** In Progress — Lab 4.4 identified as the next GRC Engineering Club exercise. Implementation and evidence verification are pending.

---

## Repository Structure

The repository is organized by infrastructure configurations, reusable modules, compliance policies, scripts, and supporting evidence.

- `terraform/` — Infrastructure as Code configurations.
- `terraform/modules/` — Reusable Terraform modules.
- `terraform/primitives/` — Individual infrastructure implementations and test fixtures.
- `policies/` — Rego compliance policies and documentation.
- `policies/tests/` — Automated compliance policy unit tests.
- `scripts/` — Automation and evidence collection scripts.
- `evidence/` — Lab-specific supporting evidence and verification records.
- `guides/` — Lab instructions and supporting guides, where included.
- `.github/workflows/` — GitHub Actions workflows for automated security and compliance checks.

Each completed lab includes relevant source code, validation results, documentation, and available supporting evidence.

## Security and Evidence Management

This repository follows security-conscious documentation practices.

- Do not commit cloud credentials, tokens, passwords, or private keys.
- Do not publish sensitive Terraform state files or plan artifacts.
- Use appropriate Git ignore rules for local and sensitive files.
- Review evidence before publishing it to a public repository.
- Preserve relevant control testing outputs and verification results.
- Use cryptographic integrity verification where applicable.
- Document remediation steps and unresolved control exceptions.

Laboratory compliance results demonstrate specific technical checks under test conditions. They do not independently establish full compliance with any security framework.

## GRC Engineering Perspective

GRC engineering combines risk management, compliance requirements, security controls, infrastructure automation, and technical validation.

The focus of this learning repository is to understand how security and compliance requirements can become measurable and repeatable technical processes.

Potential enterprise applications include:

- Automated cloud security configuration checks.
- Continuous compliance monitoring.
- Preventive security controls in deployment workflows.
- Automated evidence collection and integrity verification.
- Infrastructure configuration standardization.
- Improved audit readiness.
- More consistent control testing.
- Faster identification and remediation of security misconfigurations.
- Supporting technical assurance activities for third-party risk management.

The long-term goal is to evaluate how these capabilities can be implemented responsibly within enterprise environments using appropriate permissions, governance, approvals, and security controls.

---

## References

- [GRC Engineering Club — Official Labs](https://github.com/GRCEngClub/cgep-labs)
- [Terraform Documentation](https://developer.hashicorp.com/terraform/docs)
- [Open Policy Agent Documentation](https://www.openpolicyagent.org/docs)
- [Rego Policy Language](https://www.openpolicyagent.org/docs/policy-language)
- [AWS Documentation](https://docs.aws.amazon.com/)
- [Google Cloud Documentation](https://cloud.google.com/docs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [NIST SP 800-53 Security and Privacy Controls](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
