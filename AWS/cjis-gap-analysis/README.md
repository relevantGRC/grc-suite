# CJIS v6.0 to FedRAMP High Gap Analysis

Identifies where the CJIS Security Policy v6.0 exceeds FedRAMP High baseline requirements on a control-by-control basis. CJIS v6.0 (December 2024) aligns with NIST 800-53 Rev 5 and becomes the audit standard on April 1, 2026. This project produces a structured delta analysis showing the specific controls where a law enforcement agency's cloud deployment must go beyond its FedRAMP High authorization to satisfy CJIS requirements. Built for GRC engineers, compliance analysts, and assessors working in public safety technology environments.

## Why This Matters

A CSP with a FedRAMP High ATO already satisfies the majority of CJIS v6.0 requirements — both frameworks derive from NIST 800-53 Rev 5. But "majority" is not "all." CJIS imposes additional requirements in specific control areas that reflect the sensitivity of Criminal Justice Information (CJI). An agency or CSP that assumes FedRAMP High equivalence without analyzing the deltas risks audit findings, delayed authorizations, or — in the worst case — unauthorized access to CJI.

This project makes those deltas explicit, traceable, and machine-readable.

## Gap Summary

The gap analysis distinguishes two categories of gaps between CJIS v6.0 and FedRAMP High:

- **Implementation-level deltas** — controls present in both baselines, where CJIS imposes stricter parameters, scope, or methodology (e.g., CJIS requires fingerprint-based background checks for PS-3, while FedRAMP allows the organization to define screening method).
- **Control-level gaps** — controls present in the CJIS v6.0 baseline but absent from FedRAMP High entirely. An agency running FedRAMP High must implement these from scratch to satisfy CJIS. These are concentrated in the NIST 800-53 Rev 5 privacy overlay, reflecting CJI's status as sensitive personal data.

### Implementation-Level Deltas

Controls where CJIS v6.0 imposes stricter requirements than the FedRAMP High baseline:

| NIST 800-53 Rev 5 | FedRAMP High | CJIS v6.0 Delta | Category |
|--------------------|:------------:|------------------|----------|
| PS-3 Personnel Screening | Background investigation | Fingerprint-based background check (state/national) required for all CJI access | Personnel |
| PS-6 Access Agreements | Signed rules of behavior | CJIS Security Addendum required before CJI access | Personnel |
| IA-2 Identification & Authentication | MFA required | AAL2 phishing-resistant MFA; Advanced Authentication for CJI access | Authentication |
| IA-5 Authenticator Management | Complexity/rotation per baseline | Minimum 8-char passwords, specific complexity rules, 90-day max lifetime | Authentication |
| MP-6 Media Sanitization | Sanitize before disposal/reuse | Prescriptive sanitization procedures per media type; physical destruction requirements for CJI media | Media Protection |
| SC-12 Cryptographic Key Management | FIPS-validated modules | Agency-managed encryption keys; FIPS 140-2/140-3 validated modules | Encryption |
| SC-13 Cryptographic Protection | FIPS-validated crypto | Minimum 128-bit symmetric / 2048-bit asymmetric key lengths for CJI | Encryption |
| SC-28 Protection of Info at Rest | Encryption at rest required | Agency-managed CMK required for CJI at rest; agency retains key revocation authority | Encryption |
| AU-6 Audit Record Review | Review/analysis per baseline | Weekly audit log review; 1-year minimum retention for CJI-related events | Audit |
| AC-2 Account Management | Account lifecycle per baseline | Quarterly access reviews for CJI-authorized users | Access Control |
| IR-6 Incident Reporting | Report to US-CERT | Additional reporting to state CSA-designated recipient (CSO, SIB Chief, or Interface Agency Official per CJIS v6.0 IR-6, page 171) within state-defined timeframes | Incident Response |
| PE-17 Alternate Work Site | Authorize alternate sites | Specific controls for remote CJI access locations | Physical/Environmental |
| AT-2 Awareness Training | Annual security training | CJIS Security Awareness Training within 6 months of CJI access, biennial refresher | Training |

### Control-Level Gaps

Controls present in the CJIS v6.0 published control set (FBI CJIS Division, 2024-12-27) that are not in FedRAMP High. Baseline comparison tooling flagged 15 CJIS-only candidates; verification against the published v6.0 document confirmed 12. The three excluded candidates (SI-18, SI-18.4, SI-19 from the NIST 800-53 Rev 5 privacy overlay) are not in the v6.0 control set. See `analysis/gap-analysis.md` Methodology section for details.

| NIST 800-53 Rev 5 | Family | CJIS v6.0 Requirement | Cluster |
|--------------------|--------|------------------------|---------|
| SI-12.1 Limit PII Elements | System and Information Integrity | Limit PII elements processed across CJI lifecycle per org-defined list | Privacy, Retention |
| SI-12.2 Minimize PII in Testing, Training, Research | System and Information Integrity | De-identification, synthetic data, or masking for non-production CJI | Privacy, Retention |
| SI-12.3 Information Disposal | System and Information Integrity | Logical/cryptographic erasure or physical destruction at end of retention | Privacy, Retention |
| AU-3.3 Limit PII in Audit Records | Audit and Accountability | Log object IDs, not object content; minimize PII in audit records | PII Limitation |
| PE-8.3 Limit PII in Visitor Access Records | Physical and Environmental Protection | Visitor logs collect only operationally necessary PII elements | PII Limitation |
| AC-3.14 Individual Access | Access Control | Mechanism for individuals to access their own PII, with exemptions | PII Limitation |
| SC-7.24 PII Processing Rules at Boundaries | System and Communications Protection | Boundary enforcement of PII processing rules with exception tracking | PII Limitation |
| AT-3.5 Role-Based Training on PII Processing | Awareness and Training | Role-based training for personnel processing CJI (distinct from AT-2) | Training |
| IR-2.3 Breach Response Training | Incident Response | Breach-specific IR training with tabletop exercises and insider-misuse framing | Training |
| IR-8.1 IR Plan for Breaches | Incident Response | Notice determination, harm assessment, applicable privacy requirements | Incident Response Planning |
| PL-9 Central Management | Planning | Centrally manage a defined set of security and privacy controls | Central Management |
| SA-8.33 Minimization as Engineering Principle | System and Services Acquisition | Privacy-by-design in SDLC with PIA and architectural review | Engineering |

> **Note:** The implementation-level deltas table represents the initial scoping analysis. Additional controls may surface during full OSCAL baseline resolution.

## How an Auditor Uses This Output

A CJIS auditor reviewing a CSP's compliance posture starts with the FedRAMP High ATO package as a baseline, then uses this gap analysis to identify the specific controls requiring additional evidence or implementation. For each delta control, the analysis documents:

- **What FedRAMP High requires** — the baseline expectation already met
- **What CJIS v6.0 adds** — the additional or stricter requirement
- **Implementation guidance** — how to close the gap (policy, technical control, or process)
- **Evidence required** — what an auditor expects to see during a CJIS audit

This turns an ambiguous "is FedRAMP enough?" question into a concrete remediation checklist.

## FedRAMP 20x Alignment

The gap analysis data will be structured in OSCAL-compatible format, aligning with FedRAMP 20x compliance-as-code requirements. OSCAL profile comparison enables automated delta detection: import both the FedRAMP High profile and a CJIS v6.0 overlay, then programmatically identify where the CJIS profile adds parameters, constraints, or entirely new requirements. This machine-readable approach supports continuous compliance validation rather than point-in-time spreadsheet audits.

## CJIS v6.0 Context

CJIS Security Policy v6.0 was released in December 2024, completing the alignment with NIST 800-53 Rev 5. It replaces v5.9.x as the audit standard effective April 1, 2026. Key changes from v5.9.x include:

- Full adoption of NIST 800-53 Rev 5 control catalog (previously mapped to Rev 4)
- Updated Advanced Authentication requirements aligned with NIST SP 800-63-3
- Explicit FIPS 140-2/140-3 validation requirements for cryptographic modules
- Restructured policy sections mapping directly to 800-53 control families

For CSPs already operating under FedRAMP High, the v6.0 update is significant because it means CJIS and FedRAMP now share the same control catalog — making delta analysis cleaner and more precise than under v5.9.x.

## Project Structure

```
├── analysis/
│   └── gap-analysis.md             # Control-by-control delta analysis
├── data/
│   ├── fedramp-high-profile.json   # FedRAMP High baseline (OSCAL profile)
│   └── cjis-overlay.json           # CJIS v6.0 overlay (OSCAL profile)
├── scripts/
│   └── generate_gap_report.py      # Gap report generator (OSCAL → markdown)
├── output/
│   └── gap-report.md               # Generated gap report
├── README.md
└── LICENSE.txt
```

## License

MIT
