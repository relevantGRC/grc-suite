# AI Compliance

> A practical, engineering-first approach to AI Governance, Risk, and Compliance —
> translating frameworks into working systems, templates, automation scripts, and audit-ready evidence.

---

## What this repository is

This repository covers the major AI governance frameworks, translates them into operational controls and workflows, and engineers those into repeatable, measurable, and auditable systems.

It is both a learning record for all professionals. Every framework is documented from first principles. Every template is production-ready. Every script automates a real GRC task.

---

## Frameworks covered

| Framework | Status | Folder |
|---|---|---|
| NIST AI Risk Management Framework (AI RMF 1.0) | ✅ In progress | `frameworks/nist-ai-rmf/` |
| ISO/IEC 42001:2023 | ✅ In progress | `frameworks/iso-42001/` |
| EU AI Act | 🔜 Coming soon | `frameworks/eu-ai-act/` |

---

## Repository structure

```
ai-compliance-engineering/
│
├── README.md                          ← You are here
│
├── frameworks/
│   └── nist-ai-rmf/
│       ├── README.md                  ← Framework overview
│       ├── modules/                   ← Module-by-module learning notes
│       │   ├── module-01-overview.md
│       │   ├── module-02-four-functions.md
│       │   └── module-03-key-concepts.md
│       ├── references/                ← Quick-reference documents
│       │   ├── trustworthy-ai-properties.md
│       │   ├── ai-lifecycle-stages.md
│       │   ├── risk-types.md
│       │   └── human-oversight-levels.md
│       └── templates/                 ← Framework-specific templates
│
├── templates/                         ← Operational GRC templates
│   ├── intake/
│   │   └── ai-intake-workflow.md
│   ├── risk-assessment/
│   │   └── ai-risk-assessment-template.md
│   └── control-library/
│       └── ai-control-library.md
│
├── scripts/                           ← Automation scripts (coming after Module 8)
│
├── case-studies/                      ← Applied case studies by industry
│   ├── healthcare/
│   ├── banking/
│   ├── hr/
│   ├── government/
│   └── cybersecurity/
│
├── control-mappings/                  ← Cross-framework control mappings
│
├── dashboards/                        ← GRC dashboard apps (coming after Module 10)
│
└── .github/workflows/                 ← CI automation (coming after Module 9)
```

---

## GRC engineering philosophy

I approach AI Governance through the lens of Technical Compliance Engineering. My goal is to move beyond static spreadsheets and "check-the-box" audits, focusing instead on:
- Traceability by Design: Mapping abstract AI risk requirements (like transparency or fairness) to concrete technical artifacts, such as model cards, data lineage logs, and automated test results.
- Compliance as Code (CaC): Utilizing Infrastructure as Code (IaC) and Policy as Code (PaC) to ensure that AI governance guardrails are enforced automatically within the CI/CD pipeline rather than through manual intervention.
- Human-Centric Security: Aligning AI controls with the principle of psychological safety, ensuring that governance acts as an enabler for innovation rather than a bottleneck for engineering teams.

Approach to having a stong AI starts with:

1. **Start with the framework requirement** (e.g. ISO 42001, NIST AI RMF GOVERN function)
2. **Translate it into a policy or control** (e.g. AI Governance Policy, AI risk ownership)
3. **Engineer it into a workflow** (e.g. AI intake process, approval gate)
4. **Define the evidence** (e.g. signed approval record, risk register entry)
5. **Make it measurable** (e.g. dashboard metric, monitoring alert)
6. **Make it auditable** (e.g. version-controlled record, change log)

---

## How to use this repository

**If you are learning AI GRC:** Read the module notes in order under `frameworks/nist-ai-rmf/modules/`. Each module builds on the last. The reference documents are quick-lookup cards you will use repeatedly.

**If you are a hiring manager or client:** The templates under `templates/` are production-ready and can be adapted for immediate use. The case studies show applied thinking across industries. Scripts (coming) demonstrate engineering capability.

**If you are an auditor or reviewer:** Every document is version-controlled with commit history. The control library maps controls to framework requirements. The evidence checklist shows what documentation is maintained.

---

*Last updated: *
