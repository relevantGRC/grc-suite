# Module 2 — The Seven Core Clauses in Depth
## Clauses 4 through 10 · What each one actually requires

> - **Framework:** ISO/IEC 42001:2023 — AI Management System (AIMS)
> - **Module:** 2 of 10
> - **Status:** ✅ Complete

---

## Why this module is different from anything in NIST AI RMF

NIST AI RMF never specifies an exact document an auditor will request, because
there is no NIST AI RMF auditor. ISO 42001 is the opposite — every clause
exists because a certification auditor will, on a specific day, ask "show me
the document that proves you did this." This module makes sure you know
exactly what that document looks like for all seven clauses.

---

## Clause 4 — Context of the Organization

The foundation clause: before building an AIMS, do you actually understand
the organization you're building it for?

**Requirements:**
- **4.1** Understanding the organization and its context — internal issues
  (structure, governance maturity, technical capability) and external issues
  (regulatory environment, competitive pressure, customer expectations)
- **4.2** Understanding needs and expectations of interested parties —
  customers, regulators, employees, AI subjects (people affected by AI
  decisions), shareholders
- **4.3** Determining the scope of the AIMS — exactly which AI systems,
  business units, locations, and activities fall inside the boundary
- **4.4** AI management system — the umbrella requirement to establish,
  implement, maintain, and continually improve the AIMS

**Documentation produced:** a documented scope statement (1-2 pages) naming
exactly which systems, locations, and functions are included, plus a
stakeholder analysis.

**What an auditor checks:** whether declared scope genuinely reflects
practice. Auditors specifically probe for "scope gaming" — defining scope
narrowly to exclude the riskiest AI systems from certification while
implying broader coverage in marketing.

---

## Clause 5 — Leadership

Exists because a management system without genuine top management
commitment decays into a paperwork exercise the moment nobody is watching.

**Requirements:**
- **5.1** Leadership and commitment — ensuring policy/objectives align with
  strategic direction, AIMS requirements are integrated into business
  processes, resources are available, importance is communicated
- **5.2** AI policy — documented, appropriate to purpose, framework for
  objectives, commitment to requirements and continual improvement
- **5.3** Roles, responsibilities, and authorities — assigned and
  communicated, including AIMS conformance and performance reporting

**Documentation produced:** a signed, dated AI policy (typically one page,
principle-based), and an org chart or RACI matrix for AIMS authority.

**What an auditor checks:** auditors interview actual executives to verify
commitment is real, not delegated entirely to a compliance team. A common
finding: a well-written AI policy the CEO has never discussed in a
leadership meeting.

---

## Clause 6 — Planning

Where ISO 42001 gets close to NIST AI RMF territory — risk assessment —
framed within formal management system planning.

**Requirements:**
- **6.1.1** Actions to address risks and opportunities — determining what's
  needed to achieve AIMS outcomes, prevent undesired effects, improve
- **6.1.2** AI risk assessment — define and apply a process establishing
  risk criteria, identifying, analyzing, and evaluating AI risks, with
  documented results. **This maps directly onto NIST AI RMF Module 5** —
  the underlying risk assessment skill transfers completely
- **6.1.3** AI risk treatment — select treatment options and determine
  controls, explicitly referencing Annex A's controls catalog
- **6.1.4** AI system impact assessment — assessing potential consequences
  for individuals, groups, and society from the AI system across its
  lifecycle. **No direct NIST AI RMF equivalent in name**, though the
  underlying activity is familiar
- **6.2** AI objectives and planning to achieve them — measurable
  objectives with named owners, resources, timelines, evaluation methods

**Documentation produced:** a documented risk assessment methodology
(distinct from individual results), a risk treatment plan referencing
Annex A, AI system impact assessments per system, and measurable objectives
with owners and dates.

**What an auditor checks:** whether risk criteria were defined *before*
risks were assessed against them. A common finding: risk assessments
performed without first documenting risk acceptance criteria, making
results impossible to evaluate consistently.

---

## Clause 7 — Support

Covers the resources and infrastructure making everything else achievable
rather than aspirational.

**Requirements:**
- **7.1** Resources — people, infrastructure, technology needed for the AIMS
- **7.2** Competence — necessary competence determined, people qualified
  via education/training/experience, evidence retained
- **7.3** Awareness — staff aware of the AI policy, their contribution, and
  implications of nonconformance
- **7.4** Communication — what, when, with whom, how, and who communicates
  regarding the AIMS
- **7.5** Documented information — how AIMS documentation is created,
  formatted, reviewed, approved, distributed, and controlled

**Documentation produced:** training records and competence matrices, a
communication plan, and a documented information control procedure.

**What an auditor checks:** sample interviews with frontline staff to
verify genuine awareness — a blank stare when asked about the AI policy is
a finding regardless of how polished the written program looks.

---

## Clause 8 — Operation

Where the AIMS does its day-to-day work, containing the requirement most
unique to AI among all seven clauses.

**Requirements:**
- **8.1** Operational planning and control — plan, implement, control
  processes meeting AIMS requirements; keep documented evidence processes
  were carried out as planned
- **8.2** AI system impact assessment (operational) — actually conducting
  and documenting impact assessments at relevant lifecycle points, not just
  planning to
- **8.3** Data for AI systems — addressed via Annex A controls covering
  data quality, provenance, and management specifically for AI data — an
  area ISO 42001 goes considerably deeper into than NIST AI RMF's general
  data governance language

**Documentation produced:** operational procedures per AI system in scope,
completed impact assessments, data quality/provenance records, and evidence
of operational controls being applied — logs, approvals, monitoring outputs.

**What an auditor checks:** whether operational evidence matches the
documented procedure — if the procedure says weekly monitoring, the auditor
checks the actual dates are weekly, not monthly with a weekly label.

---

## Clause 9 — Performance Evaluation

ISO 42001's Check phase — proving the system isn't just running, but being
watched, measured, and honestly assessed.

**Requirements:**
- **9.1** Monitoring, measurement, analysis, evaluation — what's monitored,
  methods, timing, who analyzes, when evaluated
- **9.2** Internal audit — planned, periodic self-audits of the AIMS against
  both the organization's own requirements and the standard's requirements.
  **Genuinely distinctive: the organization audits itself before any
  external certification audit ever happens**
- **9.3** Management review — top management reviews the AIMS at planned
  intervals: status of previous actions, changes in issues, performance
  information, audit results, improvement opportunities

**Documentation produced:** a monitoring/measurement plan with defined
metrics, internal audit schedules and reports (typically annual), and
management review minutes showing specific inputs and decisions.

**What an auditor checks:** whether the internal audit was genuinely
independent and rigorous. An internal audit program that never finds
anything wrong is itself suspicious, not reassuring.

---

## Clause 10 — Improvement

The Act phase — closing the PDCA loop by requiring demonstrable improvement
over time, not just a static system.

**Requirements:**
- **10.1** Continual improvement — improving suitability, adequacy, and
  effectiveness of the AIMS
- **10.2** Nonconformity and corrective action — react, control, correct,
  evaluate root cause need, implement action, review effectiveness, update
  the AIMS if necessary. Documented evidence of nonconformities, actions,
  and results must be retained

**Documentation produced:** a nonconformity and corrective action log
tracking each issue from identification through root cause to verified
closure — structurally similar to the Module 5 remediation tracker, applied
to management system nonconformities rather than AI system risks.

**What an auditor checks:** whether corrective actions addressed root
causes or just patched symptoms. A recurring nonconformity "fixed" the same
way each time signals root cause analysis isn't genuinely happening.

---

## The Annex A connection — controls vs. clauses

Clauses 4-10 define the **management system** requirements — the process of
governing. **Annex A** is a normative annex listing specific AI **controls**
an organization selects from based on its risk assessment — structurally
identical to how ISO 27001's Annex A provides a controls catalog for
information security. Clauses are about whether you run a real management
system; Annex A controls are about which specific AI safeguards you've
implemented as a result. Annex A gets its own dedicated module later in
this framework.

---

## Key terms

| Term | Plain meaning |
|---|---|
| AIMS scope | The documented boundary of which AI systems, units, and locations the management system (and certification) covers |
| Interested parties | Stakeholders affected by or with requirements regarding the organization's AI, including AI subjects |
| AI system impact assessment | A required assessment of consequences for individuals, groups, or society from an AI system across its lifecycle |
| Internal audit | A self-conducted audit of the AIMS against standard requirements, required before external certification audit |
| Management review | A required, recurring top-management review of the AIMS, with defined inputs and outputs |
| Nonconformity | A failure to meet a requirement of the standard or the organization's own AIMS documentation |
| Documented information | ISO's formal term for any controlled document or record the management system requires |

---

## Practice questions

1. Why is "scope" one of the most consequential decisions in Clause 4, and how can it be misused?
2. What's the difference between Clause 6's AI system impact assessment requirement and Clause 8's?
3. Why does ISO 42001 require an internal audit before any external certification audit?
4. What would an auditor look for to distinguish genuine leadership commitment from a policy document nobody engages with?
5. Why is a corrective action log that "never finds anything wrong" actually a red flag rather than reassuring?
6. How does Clause 6's risk assessment requirement relate to NIST AI RMF Module 5?

---

## How to explain it in an interview

> "ISO 42001 has seven core clauses mapped to the PDCA cycle — Context and
> Leadership in Plan, Planning, Support, and Operation in Do, Performance
> Evaluation in Check, and Improvement in Act. What makes implementing this
> different from a voluntary framework is that every clause produces
> specific documented evidence an auditor will request — a signed AI
> policy, a defined risk assessment methodology with documented criteria,
> AI system impact assessments, internal audit reports, and a management
> review record showing leadership actually engaged with the system. The
> clause I'd flag as most distinctly 'AI-specific' compared to a standard
> like ISO 27001 is the AI system impact assessment requirement in Clauses
> 6 and 8 — assessing consequences for individuals, groups, and society
> specifically, which general information security management systems
> don't require in the same way."

---

*Previous: [Module 1 — Overview](module-01-overview.md)*
*Next: Module 3 — Annex A Controls Catalog (coming soon)*
