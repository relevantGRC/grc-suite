# Lab 2.3 — Building Your First Compliant Resource

## Overview

Implement an AWS S3 storage configuration using Terraform, with security controls aligned to NIST SP 800-53.

The lab demonstrates how security requirements can be translated into Infrastructure as Code (IaC) and supported with machine-readable compliance evidence.

## Technologies Used

- Terraform 1.17.0
- AWS CLI
- Amazon S3
- Git and GitHub

## Terraform Configuration

| File | Description |
|---|---|
| `main.tf` | AWS S3 resources and security configurations |
| `variables.tf` | Terraform input variables |
| `outputs.tf` | Infrastructure output values |
| `README.md` | Technical implementation and evidence documentation |

## Security Control Mapping

| NIST SP 800-53 | Security Control Implementation |
|---|---|
| SC-28 | Server-side encryption |
| AC-3 | Public access restrictions |
| AU-3 | S3 access logging |
| AU-6 | Dedicated logging infrastructure |
| CM-6 | Configuration settings, versioning, and tagging |

## Implementation

The Terraform configuration defines an AWS S3 storage environment incorporating:

- Primary S3 bucket for storage
- Dedicated S3 bucket for access logging
- Server-side encryption using AES-256
- Public access restrictions
- Bucket versioning
- Access logging configuration
- Compliance tagging

## Machine-Readable Compliance Evidence

Terraform plan and state-derived evidence is available for technical assessment and compliance verification.

- [Terraform Plan Evidence](../../../evidence/lab-2-3/public/plan.json)
- [Terraform State-Derived Evidence](../../../evidence/lab-2-3/public/state.json)

The evidence supports inspection of Terraform resource configurations, security settings, and infrastructure attributes.

## Evidence Validation

The evidence files were validated for JSON integrity and reviewed using targeted checks for common sensitive information.

The published copies were processed to redact selected identifiers while preserving information needed for technical review.

## GRC and Audit Considerations

Infrastructure as Code provides a consistent approach to implementing security controls.

Machine-readable evidence supports:

- Control configuration assessment
- Security baseline verification
- Audit traceability
- Infrastructure change review
- Compliance reporting

Technical configurations and evidence should be evaluated together to determine whether defined security requirements are satisfied.

## Key Takeaways

- Terraform enables repeatable deployment of cloud security controls.
- Security requirements can be incorporated into infrastructure configurations.
- AWS S3 supports encryption, access restrictions, versioning, and logging controls.
- Machine-readable evidence strengthens technical assurance and audit readiness.
- Infrastructure configurations can be reviewed against established compliance requirements.

## Official Lab Reference

[GRC Engineering Club — Lab 2.3](https://github.com/GRCEngClub/cgep-labs/blob/main/guides/02_03_first_compliant_resource.md)
