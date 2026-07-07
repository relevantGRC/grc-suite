# Reference Card — The AI Lifecycle Stages

> **Source:** NIST AI RMF 1.0
> **Use:** Identifying where in the lifecycle a risk originates and which controls apply

---

## The six stages

```
Stage 1          Stage 2          Stage 3          Stage 4          Stage 5          Stage 6
Plan &     →    Collect &   →    Build &    →    Verify &   →    Deploy     →    Operate &
Design          Process          Train            Validate                         Monitor
                Data
```

---

## Stage-by-stage breakdown

### Stage 1 — Plan & design
**What happens:** AI system purpose, scope, and requirements are defined.
Architecture decisions are made. Governance requirements are established.

**GRC activities at this stage:**
- Involve GRC team from day one — not after the model is built
- Conduct initial risk classification
- Define governance requirements as system requirements
- Identify regulatory applicability
- Assign preliminary risk owner

**Common risks:**
- Building a system that should not be built (ethical or regulatory problem)
- Designing without fairness, privacy, or explainability in mind
- No GRC involvement until after deployment

**Key questions to ask:**
- What problem are we solving? Is AI the right tool?
- Who will be affected? Could they be harmed?
- What regulations apply?
- Who is accountable for this system?

---

### Stage 2 — Collect & process data
**What happens:** Training data is assembled, cleaned, and prepared.
Features are selected. Data pipelines are built.

**GRC activities at this stage:**
- Data quality assessment
- Data lineage documentation
- Privacy impact assessment
- Demographic representation analysis
- Proxy variable identification

**Common risks:**
- **Bias in training data** — the most common source of AI discrimination
- Privacy violations — collecting data without proper consent or legal basis
- Poor data quality — garbage in, garbage out
- Incomplete demographic coverage — model will underperform for underrepresented groups

**Key evidence to collect:**
- Data quality report
- Data lineage diagram
- Demographic coverage analysis
- Privacy review sign-off
- Data source documentation

---

### Stage 3 — Build & train
**What happens:** The model is developed and trained on the prepared data.
Hyperparameters are tuned. Initial performance is evaluated.

**GRC activities at this stage:**
- Secure development practices review
- Proxy variable review of selected features
- Overfitting / underfitting checks
- Initial fairness evaluation

**Common risks:**
- Proxy variables encoded in feature set
- Model memorizes training data (overfitting) — fails on real-world data
- Insecure development environment — model weights exposed
- Bias amplification — model learns and amplifies biases in training data

**Key evidence to collect:**
- Model training log
- Feature selection justification
- Initial performance metrics
- Development environment security review

---

### Stage 4 — Verify & validate
**The most important governance gate in the entire lifecycle.**

**What happens:** The model is tested rigorously before deployment.
Performance, fairness, security, and explainability are all evaluated.

**GRC activities at this stage:**
- Formal fairness testing across demographic groups
- Security and adversarial robustness testing
- Explainability assessment
- Regulatory compliance review
- AI Review Board approval
- Model card completion

**Common risks:**
- Insufficient testing — bias or performance gaps go undetected
- Testing only on in-distribution data — model fails on edge cases
- Approval gate skipped due to time pressure
- Results not formally documented

**Key evidence to collect:**
- Fairness testing report with demographic breakdown
- Security assessment results
- Explainability review
- AI Review Board approval record (signed)
- Completed model card

**The rule:** If the model does not pass validation, it does not deploy.
No exceptions for schedule pressure.

---

### Stage 5 — Deploy
**What happens:** The model goes into production and begins making real decisions.

**GRC activities at this stage:**
- Staged rollout (small user group first — expand only if metrics are healthy)
- Rollback plan documented and tested
- All stakeholders notified
- Monitoring dashboards activated
- Final deployment approval signed and filed

**Common risks:**
- Big-bang deployment with no rollback plan
- Insufficient stakeholder notification
- Monitoring not activated at launch
- Missing deployment approval documentation

**Key evidence to collect:**
- Deployment approval record
- Staged rollout plan and results
- Rollback procedure
- Stakeholder notification records
- Monitoring activation confirmation

---

### Stage 6 — Operate & monitor
**The longest stage — everything after deployment.**

**What happens:** The system runs in production. Performance is watched continuously.
Incidents are handled. The system is eventually retired.

**GRC activities at this stage:**
- Daily performance monitoring
- Periodic fairness audits
- Drift detection and model retraining when needed
- Incident detection, response, and documentation
- Annual risk reassessment
- Vendor change notification monitoring
- Decommissioning governance

**Common risks:**
- **Model drift** — performance degrades as real-world data changes from training data
- Emerging bias — demographic disparities develop post-deployment
- New regulatory requirements apply to an existing system
- Vendor updates model without notifying the organization
- Decommissioning leaves sensitive data unmanaged

**Key evidence to collect:**
- Monthly performance reports
- Quarterly fairness audit results
- Incident log
- Annual risk reassessment document
- Model retraining records
- Decommission record (when retired)

---

## Lifecycle governance checklist

| Stage | Key governance gate | Evidence produced |
|---|---|---|
| 1 — Plan | GRC review and initial risk classification | Intake form, risk tier assignment |
| 2 — Data | Data quality and privacy sign-off | Data quality report, PIA, lineage doc |
| 3 — Build | Feature review and secure dev confirmation | Feature justification log, security review |
| 4 — Validate | AI Review Board approval | Fairness test results, approval record, model card |
| 5 — Deploy | Final deployment sign-off | Deployment record, rollback plan |
| 6 — Monitor | Ongoing — quarterly audits, annual reassessment | Monitoring reports, audit results, incident log |
