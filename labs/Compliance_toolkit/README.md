# GitLab Compliance Repository

This repository contains reusable compliance templates, security scanning configurations, and policy-as-code examples to enforce security and regulatory requirements in GitLab CI/CD pipelines using a GitHub-hosted source of truth.

## Purpose

To enable **GRC analysts**, **GRC engineers**, **security engineers**, and **developers** to:

- Integrate compliance controls directly into GitLab pipelines (Compliance as Code)
- Align with ISO 27001, NIST 800-53, SOC 2, and other frameworks
- Standardize pipeline enforcement across projects
- Automate security scans and policy-based approvals

---

## Repository Structure

```text
compliance-repo/
├── templates/              # CI/CD templates for security scans and controls coming soon
│   ├── sast-template.yml
│   ├── dependency-scanning.yml
│   ├── license-compliance.yml
│   ├── secret-detection.yml
│   └── policy-pipeline.yml
├── policies/               # Policy-as-code examples (YAML)
│   └── scan-approval-policy.yml
├── mappings/               # Compliance framework mappings
│   ├── iso27001-mapping.md
│   ├── nist800-53-mapping.md
│   └── soc2-mapping.md
├── README.md               # This file

```

## Policy-as-Code Example

The policies/ directory contains YAML policies that enforce:
- Merge Request approval rules
- Blocking merges on high/critical vulnerabilities
- Secret detection enforcement

## Compliance Framework Mappings

See the mappings/ folder for how each control maps to industry frameworks like:
- ISO/IEC 27001:2022
- NIST SP 800-53 Rev 5
- SOC 2
