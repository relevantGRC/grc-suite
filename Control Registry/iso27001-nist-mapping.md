---
framework_primary: ISO 27001:2022
framework_mapping: NIST 800-53 Rev 5
status: Verified Reference
last_updated: 2026-05-12
---

# ISO 27001:2022 to NIST 800-53 Rev 5 Mapping Registry

## 1. Theme Summary Table
| Theme | Controls | Primary 800-53 Families | Coverage Character |
| :--- | :---: | :--- | :--- |
| **A.5 Organizational** | 37 | PM, PL, CA, IR, RA, SA, SR, PS, AT | Governance and management layer |
| **A.6 People** | 8 | PS, AT | Human risk layer |
| **A.7 Physical** | 14 | PE, MA, MP | Physical boundary layer |
| **A.8 Technological** | 34 | AC, IA, SC, SI, CM, AU, CP, SA | Technical control layer |
| **Total** | **93** | | |

---

## 2. Detailed Control Mappings

### Theme A.5 — Organizational Controls
> [!NOTE] Divergence Note
> ISO 27001 A.5 is outcomes-based governance. NIST 800-53 PM and PL families are prescriptive, requiring specific artifacts (SSP, PIA, ISCP) that ISO does not mandate by name.

| ISO ID | Control Description | NIST 800-53 Rev 5 Equivalent |
| :--- | :--- | :--- |
| **A.5.1** | Policies for information security | PM-1, PL-1, SA-1, AC-1 (all -1 policy controls) |
| **A.5.2** | Information security roles and responsibilities | PM-2, PS-2, AC-5 |
| **A.5.3** | Segregation of duties | AC-5, PS-2 |
| **A.5.5** | Contact with authorities | IR-6, PM-15 |
| **A.5.7** | Threat intelligence (New) | PM-16, SI-5, RA-3(2) |
| **A.5.12** | Classification of information | RA-2, MP-3 |
| **A.5.15** | Access control policy | AC-1, AC-2, AC-3 |
| **A.5.16** | Identity management | IA-1, IA-2, IA-4 |
| **A.5.17** | Authentication information | IA-5 |
| **A.5.19** | Information security in supplier relationships | SA-9, SR-3, SR-5 |
| **A.5.20** | Addressing security within supplier agreements | SA-4, SA-9(3), SR-3 |
| **A.5.21** | Managing security in the ICT supply chain | SR-1 through SR-12 |
| **A.5.22** | Monitoring and review of supplier services | SA-9(2), SR-6 |
| **A.5.23** | Information security for use of cloud services (New) | SA-9, SA-12, SR-3, SC-7 |
| **A.5.24** | Incident management planning and preparation | IR-1, IR-8 |
| **A.5.25** | Assessment and decision on security events | IR-4, IR-5, IR-6 |
| **A.5.26** | Response to security incidents | IR-4, IR-5, IR-6, IR-9 |
| **A.5.27** | Learning from security incidents | IR-4(4), CP-2 |
| **A.5.28** | Collection of evidence | IR-4, AU-9 |
| **A.5.29** | Security during disruption | CP-1, CP-2, CP-4 |
| **A.5.30** | ICT readiness for business continuity (New) | CP-2, CP-7, CP-8, CP-11 |
| **A.5.35** | Independent review of information security | CA-2, CA-7 |
| **A.5.36** | Compliance with policies and standards | CA-7, PM-14 |
| **A.5.37** | Documented operating procedures | PL-1, SA-1 (all operational procedures) |

### Theme A.6 — People Controls
> [!NOTE] Divergence Note
> ISO 27001 A.6.3 awareness training frequency is organization-defined. NIST 800-53 AT-2/AT-3 specifies role-based training and insider threat content as named requirements.

| ISO ID | Control Description | NIST 800-53 Rev 5 Equivalent |
| :--- | :--- | :--- |
| **A.6.1** | Screening | PS-3 |
| **A.6.2** | Terms and conditions of employment | PS-6, PS-7 |
| **A.6.3** | Information security awareness, education and training | AT-2, AT-3, AT-4 |
| **A.6.4** | Disciplinary process | PS-8 |
| **A.6.5** | Responsibilities after termination or change | PS-4, PS-5 |
| **A.6.6** | Confidentiality or non-disclosure agreements | PS-6 |
| **A.6.7** | Remote working | AC-17, PE-17 |
| **A.6.8** | Information security event reporting (New) | IR-6, SE-2 |

### Theme A.7 — Physical Controls
> [!NOTE] Divergence Note
> NIST 800-53 PE controls in a FedRAMP context require explicit documentation of inheritance from a CSP, a concept ISO 27001 does not formally mandate.

| ISO ID | Control Description | NIST 800-53 Rev 5 Equivalent |
| :--- | :--- | :--- |
| **A.7.1** | Physical security perimeters | PE-3, PE-17 |
| **A.7.2** | Physical entry controls | PE-2, PE-3, PE-4 |
| **A.7.3** | Securing offices, rooms and facilities | PE-5 |
| **A.7.4** | Physical security monitoring (New) | PE-6 |
| **A.7.5** | Protecting against environmental threats | PE-9, PE-12, PE-13, PE-14, PE-15, PE-18 |
| **A.7.6** | Working in secure areas | PE-5 |
| **A.7.7** | Clear desk and clear screen | AC-11 |
| **A.7.8** | Equipment siting and protection | PE-9, PE-12 |
| **A.7.9** | Security of assets off-premises | MP-5, PE-17 |
| **A.7.10** | Storage media | MP-2, MP-3, MP-4, MP-5, MP-7 |
| **A.7.11** | Supporting utilities | PE-9, PE-11 |
| **A.7.12** | Cabling security | PE-4, PE-9 |
| **A.7.13** | Equipment maintenance | MA-2, MA-3, MA-5 |
| **A.7.14** | Secure disposal or re-use of equipment | MP-6 |

### Theme A.8 — Technological Controls
> [!NOTE] Divergence Note
> ISO A.8.5 requires "secure authentication," while NIST IA-2, IA-2(1), IA-2(6), and IA-5 specify exact mandates for phishing-resistant MFA and authenticator management.

| ISO ID | Control Description | NIST 800-53 Rev 5 Equivalent |
| :--- | :--- | :--- |
| **A.8.1** | User endpoint devices | CM-2, CM-6, SC-28 |
| **A.8.2** | Privileged access rights | AC-2, AC-6, AC-6(1), AC-6(5) |
| **A.8.3** | Information access restriction | AC-3, AC-17 |
| **A.8.4** | Access to source code | CM-10, SA-15 |
| **A.8.5** | Secure authentication | IA-2, IA-2(1), IA-2(6), IA-5, IA-8 |
| **A.8.6** | Capacity management | SC-5, CP-2 |
| **A.8.7** | Protection against malware | SI-3, SI-8 |
| **A.8.8** | Management of technical vulnerabilities | RA-5, SI-2, SI-5 |
| **A.8.9** | Configuration management (New) | CM-2, CM-3, CM-6, CM-8 |
| **A.8.10** | Information deletion (New) | MP-6, SI-12 |
| **A.8.11** | Data masking (New) | SC-28, AC-3 |
| **A.8.12** | Data leakage prevention (New) | SC-7, AC-4, SI-12 |
| **A.8.13** | Information backup | CP-9, CP-10 |
| **A.8.14** | Redundancy of facilities | CP-7, CP-8, CP-11 |
| **A.8.15** | Logging | AU-2, AU-3, AU-9, AU-12 |
| **A.8.16** | Monitoring activities (New) | AU-6, IR-5, SI-4 |
| **A.8.17** | Clock synchronization | AU-8 |
| **A.8.18** | Use of privileged utility programs | AC-6, CM-7 |
| **A.8.19** | Installation of software | CM-7, CM-11 |
| **A.8.20** | Network security | SC-5, SC-7 |
| **A.8.21** | Security of network services | SA-9, SC-7 |
| **A.8.22** | Segregation of networks | SC-7, AC-4 |
| **A.8.23** | Web filtering | SC-7, SI-3, AC-4 |
| **A.8.24** | Use of cryptography | SC-8, SC-13, SC-28 |
| **A.8.25** | Secure development lifecycle | SA-8, SA-11, SA-15 |
| **A.8.26** | Application security requirements | SA-8, SA-11 |
| **A.8.27** | Secure architecture and engineering | SA-8, SC-39 |
| **A.8.28** | Secure coding (New) | SA-8, SA-11(1), SA-15 |
| **A.8.29** | Security testing in dev/prod | CA-8, SA-11, RA-5 |
| **A.8.30** | Outsourced development | SA-4, SA-12 |
| **A.8.31** | Separation of dev, test, and prod | CM-4, SC-3 |
| **A.8.32** | Change management | CM-3, CM-4 |
| **A.8.33** | Test information | SA-11, PM-25 |
| **A.8.34** | Protection during audit testing | CA-8 |
