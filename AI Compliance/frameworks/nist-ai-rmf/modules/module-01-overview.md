# Module 1 — What NIST AI RMF Is, Why It Was Created, and Who Uses It

> **Framework:** NIST AI Risk Management Framework (AI RMF 1.0)
> **Module:** 1 of 10
> **Status:** ✅ Complete

---

## What it is

The NIST AI RMF is a voluntary framework published by the US government in January 2023.
It gives organizations a structured way to think about, identify, and manage the risks
that AI systems create — before and after deployment.

Think of it as a **playbook**. When an organization builds, buys, or uses an AI system,
a lot of things can go wrong — bias in outputs, wrong predictions, security vulnerabilities,
privacy violations, or harm to people. The AI RMF gives teams a common language and
a structured process to manage those risks responsibly.

It is **voluntary** — no law forces you to use it. But it is widely respected and
increasingly expected by auditors, regulators, enterprise procurement teams, and boards.

---

## Why it was created

Before the AI RMF existed, organizations were deploying AI with no shared standards
for safety, fairness, or accountability. Real problems this caused:

- A hiring algorithm at a major company discriminated against women — nobody checked before launch
- A healthcare AI misdiagnosed patients because it was trained on unrepresentative data
- Organizations had no idea which AI systems they had running, let alone what risks they carried

NIST created the AI RMF to give every organization — regardless of size or industry —
a common vocabulary and practical structure for responsible AI risk management.

---

## Who should use it

The AI RMF was designed for anyone involved in AI — not just technologists.

**Organizations:**
- Companies that build AI products
- Companies that buy or use AI tools and platforms
- Government agencies deploying AI in public services
- Regulated industries (healthcare, banking, insurance, education)

**Roles:**
- AI Governance leads and officers
- GRC engineers and analysts
- Risk managers and enterprise risk teams
- Compliance officers
- Cybersecurity teams
- Internal audit
- Legal and privacy teams
- Product managers
- Executive leadership and boards
- Vendors selling AI to regulated industries

---

## Key terms

| Term | Plain language meaning |
|---|---|
| Risk | The possibility that an AI system causes harm — to people, the organization, or society |
| Risk management | Finding, understanding, and reducing risks to an acceptable level |
| AI system | Software that uses machine learning or similar techniques to make decisions or predictions |
| Trustworthy AI | AI that is safe, fair, explainable, private, secure, and accountable |
| Framework | A structured set of guidelines — flexible, not a rigid checklist |
| Stakeholder | Anyone affected by the AI system — users, customers, employees, regulators, the public |
| AI lifecycle | Every stage an AI system goes through — from planning and design to retirement |

---

## Real-world example

**First National Bank** wants to deploy an AI model to approve or deny personal loan applications.

**Without the AI RMF:** The data science team builds the model, tests for accuracy,
and pushes to production. Nobody asks: Is this model fair? Who is accountable?
How do we monitor it after launch?

**With the AI RMF:**
1. The system is inventoried and classified as high-risk (loan decisions affect people's lives)
2. Risks are mapped — bias, explainability, data quality, regulatory exposure
3. Risks are measured — fairness tests run, training data audited
4. Risks are managed — human review added for denials, monitoring set up, incident plan created

The model still launches — but with evidence of responsible governance.

---

## Mini case study

**Organization:** City of Riverton (municipal government)
**AI system:** Flags residents potentially eligible for housing assistance

**Problem:** No governance structure, no risk owner, no oversight process.

**AI RMF applied:**
- System formally documented with purpose and risk classification
- Risks identified: wrongful exclusion, data privacy, algorithmic bias by zip code
- Risk owner assigned (department head), accountability chain to city manager
- Human caseworker review required before any resident is contacted
- Quarterly monitoring of AI recommendations
- Resident contest process created

**Outcome:** Project moves forward with controls that protect residents and the city.

---

## Practice questions

1. What is the NIST AI RMF in one sentence?
2. Name three types of organizations that should use it
3. What problem was it created to solve?
4. What does "trustworthy AI" mean?
5. Why would a compliance officer care about this framework?

---

## How to explain it in an interview

> "The NIST AI RMF is a voluntary framework published by the US government that gives
> organizations a structured way to identify, assess, and manage the risks of AI systems
> throughout their lifecycle. It uses four core functions — Govern, Map, Measure, and
> Manage — to help teams build trustworthy AI and demonstrate accountability. I use it
> as the foundation for designing AI governance programs, building risk assessment
> processes, and preparing organizations for audits."

---

## GRC engineering takeaway

The AI RMF is not a document to read once — it is a system to engineer.
A GRC engineer's job is to take the framework's guidance and turn it into:
- Policies the organization actually follows
- Workflows that trigger at the right moments
- Controls with named owners and evidence requirements
- Dashboards that show compliance status in real time

*Next: [Module 2 — The Four Core Functions](module-02-four-functions.md)*
