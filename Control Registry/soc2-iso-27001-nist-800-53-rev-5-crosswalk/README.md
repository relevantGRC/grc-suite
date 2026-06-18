![SOC 2](https://img.shields.io/badge/SOC%202-Trust%20Services%20Criteria-2b6cb0?style=flat)
![ISO 27001](https://img.shields.io/badge/ISO%2FIEC-27001%3A2022-005387?style=flat)
![NIST 800-53](https://img.shields.io/badge/NIST-800--53%20Rev%205-004990?style=flat)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776ab?style=flat)

# SOC 2 / ISO 27001 / NIST 800-53 Rev 5 Crosswalk

A crosswalk that pivots on **SOC 2 Trust Services Criteria (Common Criteria)** and maps **NIST 800-53 Rev 5** and **ISO 27001:2022 Annex A** onto each criterion — every row carrying a confidence label (Strong / Partial / Contextual) and a short "why this mapping" rationale. The mapping data lives in a single `mappings.yaml`; a small Python build script emits Markdown, JSON, and CSV, with a `--check` validate-only gate so the artifacts never drift from the source.

> **Status:** v1.0. The crosswalk below is generated from `mappings.yaml` by `build_crosswalk.py` — rebuild the Markdown, JSON, and CSV artifacts with the commands in [Quickstart](#quickstart).

## Why This Exists

A security program that answers to more than one framework ends up maintaining the same control intent in three different places — one spreadsheet for SOC 2, one for ISO 27001, one for NIST. This crosswalk collapses that into a single source of truth. It pivots on SOC 2 Common Criteria — the auditor-language most commercial programs already speak — maps the NIST 800-53 Rev 5 and ISO 27001:2022 Annex A equivalents onto each criterion, and is explicit about where a mapping is clean versus where the frameworks genuinely diverge.

I built it to **learn cross-framework control mapping by doing it** — reading the source standards, deciding each equivalence myself, and writing down the reasoning rather than copying a vendor's mapping table.

## Why SOC 2 as the Pivot

NIST 800-53 has the most granular catalog (1000+ controls), but it's engineer-language. SOC 2 Common Criteria (~33 CC) is the auditor-language commercial programs already understand. Pivoting on SOC 2 keeps the crosswalk compact and readable while preserving engineering precision through the NIST column. NIST 800-53 stays the bridge — every SOC 2 row maps to one or more NIST controls; the reverse isn't true.

## Scope (v1.0)

- **Frameworks:** SOC 2 TSC (pivot), NIST 800-53 Rev 5, ISO 27001:2022 Annex A
- **Control families:** Access Control (AC), Identification & Authentication (IA), Audit & Accountability (AU), Configuration Management (CM)
- **Planned (v1.1+):** CIS Controls v8 IG3 column, NIST CSF 2.0 overlay
- **Out of scope:** OT/ICS-specific frameworks (e.g., NERC CIP) — a separate concern, not a crosswalk row

## Controls Addressed

Generated from `mappings.yaml` by `build_crosswalk.py` — and also emitted as [`crosswalk.md`](crosswalk.md), [`crosswalk.json`](crosswalk.json), and [`crosswalk.csv`](crosswalk.csv). The pivot is SOC 2 Common Criteria; NIST 800-53 Rev 5 is the bridge column and ISO 27001:2022 Annex A the third. Each row carries a Strong / Partial / Contextual confidence label and a "why this mapping" rationale.

| SOC 2 CC | NIST 800-53 | ISO 27001:2022 | Confidence | Rationale |
| --- | --- | --- | --- | --- |
| CC6.1 | AC-3 | A.5.15 / A.8.3 | Strong | AC-3 enforces approved authorizations for logical access at the system and application layer. CC6.1 frames logical-access security architecture and enforcement mechanisms. ISO A.5.15 (access control) and A.8.3 (information access restriction) address the same enforcement intent from policy and technical restriction angles. |
| CC6.2 | AC-2 | A.5.16 / A.5.18 | Strong | AC-2 governs the full account lifecycle — approve before create, modify, disable, remove, and periodic review. CC6.2 covers registration and authorization of new users before credentials are issued. ISO A.5.16 (identity management) and A.5.18 (access rights) map to provisioning and rights assignment during onboarding. |
| CC6.3 | AC-6 / AC-2 | A.8.2 / A.8.3 | Strong | AC-6 authorizes only the access necessary for assigned tasks (least privilege). AC-2 supports modification and removal when roles change. CC6.3 covers role-based access, modification, and removal including least privilege and segregation of duties. ISO A.8.2 (privileged access rights) and A.8.3 (information access restriction) align with privilege minimization and access boundaries. |
| CC6.6 | IA-2 | A.8.5 / A.5.16 | Strong | IA-2 requires unique identification and authentication of organizational users. CC6.6 addresses measures against threats from outside the boundary, including authentication strength. ISO A.8.5 (secure authentication) and A.5.16 (identity management) cover the authentication mechanism and the identity binding it depends on. |
| CC6.6 | IA-5 | A.5.17 | Partial | IA-5 manages the authenticator lifecycle — issuance, strength, default changes, rotation, and revocation. CC6.6 blends authentication mechanism and credential management. ISO separates A.5.17 (authentication information / authenticator management) from A.8.5 (secure authentication mechanism). An ISO audit may require the authenticator-policy artifact separately even when SOC 2 and NIST evidence already covers the mechanism. |
| CC7.2 | AU-2 | A.8.15 | Strong | AU-2 requires identifying event types the system can log, selecting the subset to log, and reviewing that selection for investigative adequacy. CC7.2 monitors system components for anomalies. ISO A.8.15 (logging) aligns with defining and maintaining what gets logged. |
| CC7.3 | AU-6 | A.8.16 | Strong | AU-6 requires reviewing and analyzing audit records on a defined frequency, reporting findings, and adjusting depth when risk changes. CC7.3 evaluates security events for potential incidents. ISO A.8.16 (monitoring activities) maps to the analytic loop over logged events. |
| CC8.1 | CM-2 | A.8.9 | Partial | CM-2 develops and maintains a baseline configuration under configuration control, reviewed on defined frequency and on install or upgrade. CC8.1 frames broad change management — authorize, design, test, approve, and implement changes. ISO A.8.9 (configuration management) is config-to-config alignment, but the hop to the CC8.1 change pivot is loose. CM-2 keeps a foot in the change door via baseline maintained under configuration control. |
| CC8.1 | CM-6 | A.8.9 | Contextual | CM-6 establishes and implements restrictive configuration settings, documents deviations, and monitors changes to settings. CC8.1 expects change authorization and approval evidence. CM-6 is pure hardened-settings state — a STIG or SCAP scan demonstrates configuration posture but does not satisfy a change-approval ticket. ISO A.8.9 aligns on configuration management; A.8.32 (change management) is the closer ISO frame for the SOC 2 pivot. |

## Gaps & Conflicts

The value of the crosswalk is being explicit about where a single piece of evidence satisfies all three frameworks and where it doesn't — that's where multi-framework programs actually spend effort. The three non-Strong rows and their practical implications:

- **CC6.6 → IA-5 / A.5.17 (Partial).** ISO splits authenticator management (A.5.17) from the authentication mechanism (A.8.5), which NIST IA-5 and SOC 2 CC6.6 blend together — so an ISO audit may demand the authenticator-policy artifact separately even when the SOC 2 / NIST evidence already covers the mechanism.
- **CC8.1 → CM-2 / A.8.9 (Partial).** CM-2's "baseline under configuration control" maps cleanly to ISO A.8.9 config-to-config, but the hop to SOC 2 CC8.1's broad *change*-management pivot is loose — CM-2 only keeps a foot in the change door.
- **CC8.1 → CM-6 / A.8.9 (Contextual).** CM-6 is pure hardened-settings *state*: a STIG/SCAP scan proves configuration posture but doesn't satisfy a change-approval ticket, so ISO A.8.32 (change management) — not A.8.9 — is the closer frame for the SOC 2 pivot.

## How an Auditor Uses This Output

For a given SOC 2 Common Criterion, the row names the corresponding NIST 800-53 Rev 5 control(s) and ISO 27001:2022 Annex A control, the confidence in that equivalence, and the rationale. An auditor can reuse one piece of evidence across frameworks where the mapping is **Strong**, and knows to collect framework-specific evidence where it's **Partial** or **Contextual**. `crosswalk.csv` drops into a workpaper or GRC platform without manual transcription; `crosswalk.json` feeds an evidence pipeline.

## Automation & Compliance-as-Code

- **Single source of truth:** mappings live in version-controlled YAML, not a spreadsheet — diffable and reviewable in pull requests.
- **Machine-readable outputs:** the build emits JSON and CSV alongside the Markdown table, so the crosswalk feeds tooling, not just human eyes.
- **Validate-only gate:** `build_crosswalk.py --check` validates the source schema, row count, and framework ID patterns, then rebuilds all three artifacts in memory and fails if any committed file has drifted from `mappings.yaml` (non-zero exit on validation or drift) — a CI gate that rejects malformed mappings and stale artifacts before they merge.

## Sample Output

Real rows from the emitted artifacts (regenerate any time with the build command):

`crosswalk.csv`
```csv
soc2_cc,nist_800_53,iso_27001_2022,confidence,rationale
CC6.1,AC-3,A.5.15 / A.8.3,Strong,AC-3 enforces approved authorizations for logical access at the system and application layer. CC6.1 frames logical-access security architecture and enforcement mechanisms. ISO A.5.15 (access control) and A.8.3 (information access restriction) address the same enforcement intent from policy and technical restriction angles.
```

`crosswalk.json`
```json
{
  "soc2_cc": "CC6.1",
  "nist_800_53": "AC-3",
  "iso_27001_2022": "A.5.15 / A.8.3",
  "confidence": "Strong",
  "rationale": "AC-3 enforces approved authorizations for logical access at the system and application layer. CC6.1 frames logical-access security architecture and enforcement mechanisms. ISO A.5.15 (access control) and A.8.3 (information access restriction) address the same enforcement intent from policy and technical restriction angles."
}
```

## Quickstart

```bash
git clone https://github.com/0xBahalaNa/soc2-iso27001-nist-crosswalk.git
cd soc2-iso27001-nist-crosswalk
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Build all artifacts from the YAML source
python build_crosswalk.py --source mappings.yaml \
  --out-md crosswalk.md --out-json crosswalk.json --out-csv crosswalk.csv

# CI validate-only mode (no emit; non-zero exit on validation failure or artifact drift)
python build_crosswalk.py --source mappings.yaml --check
```

## Forward Path (v1.1+)

- Add a CIS Controls v8 IG3 column
- Add a NIST CSF 2.0 overlay (Functions / Categories / Subcategories)
- Expand to additional families (System & Information Integrity, Incident Response)
