# NIST AI Risk Management Framework (AI RMF 1.0)

> Published by the National Institute of Standards and Technology (NIST) in January 2023.
> A voluntary framework for managing risks in the design, development, deployment, and use of AI systems.

---

## In one sentence

The NIST AI RMF gives any organization a structured, flexible approach to identifying,
assessing, and managing the risks of AI systems — across their entire lifecycle.

---

## Why it was created

Before the AI RMF existed, organizations were building and deploying AI with no shared
language for risk. Different teams used different approaches, different words, and different
standards — or no standards at all. This led to real harm:

- Hiring algorithms that discriminated against women without anyone checking
- Healthcare AI that misdiagnosed patients due to unrepresentative training data
- Organizations with no idea which AI systems they even had running

NIST created the AI RMF to give every organization — regardless of size or industry —
a common vocabulary and practical structure for responsible AI risk management.

---

## Key characteristics

| Property | Detail |
|---|---|
| Voluntary | No law requires its use (unlike the EU AI Act) |
| Flexible | Adaptable to any organization, industry, or AI system |
| Lifecycle-based | Covers AI from planning through retirement |
| Non-prescriptive | Describes outcomes, not specific technical implementations |
| Globally relevant | Referenced internationally despite being a US framework |

---

## The four core functions

```
┌─────────────────────────────────────────────────────┐
│                      GOVERN                          │
│   Foundation: policies, roles, culture, oversight    │
└──────────────────────┬──────────────────────────────┘
                       │ enables
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
      MAP           MEASURE        MANAGE
   Identify        Evaluate        Treat &
   & document      & score         monitor
   risks           risks           risks
        └──────────────┼──────────────┘
                       │ feeds back into
                       ▼
                   (continuous cycle)
```

| Function | Plain meaning |
|---|---|
| GOVERN | Build the organizational foundation — policies, roles, accountability |
| MAP | Discover and document AI systems and their risks |
| MEASURE | Evaluate how serious each risk is through testing and analysis |
| MANAGE | Treat risks with controls, monitor continuously, respond to incidents |

---

## Documents in this section

| Document | Description |
|---|---|
| `modules/module-01-overview.md` | What it is, why it was created, who uses it |
| `modules/module-02-four-functions.md` | GOVERN, MAP, MEASURE, MANAGE — deep dive |
| `modules/module-03-key-concepts.md` | Trustworthy AI, lifecycle, risk types, impact |
| `references/trustworthy-ai-properties.md` | The seven properties reference card |
| `references/ai-lifecycle-stages.md` | Six lifecycle stages with risk touchpoints |
| `references/risk-types.md` | All AI risk types with examples |
| `references/human-oversight-levels.md` | In / on / out of the loop explained |

---

## Quick reference: risk rating matrix

| Severity \ Likelihood | Low | Medium | High |
|---|---|---|---|
| Critical | Medium | High | **CRITICAL** |
| High | Low | Medium | High |
| Medium | Low | Low | Medium |
| Low | Accept | Accept | Low |

---

## Official resources

- [NIST AI RMF 1.0 (PDF)](https://doi.org/10.6028/NIST.AI.100-1)
- [NIST AI RMF Playbook](https://airmf.nist.gov/)
- [NIST Trustworthy & Responsible AI Resource Center](https://www.nist.gov/artificial-intelligence)
