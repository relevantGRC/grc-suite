# Evidence Logger

A Python tool that generates timestamped, structured audit evidence files from AWS IAM policy compliance checks. Built for GRC engineers, compliance analysts, and assessors who need defensible, tamper-resistant evidence artifacts during FedRAMP High and CJIS v6.0 audits.

## Compliance Controls Addressed

| NIST 800-53 Rev 5 | FedRAMP High | CJIS v6.0 | Validation Method |
|--------------------|:------------:|:---------:|-------------------|
| AU-2 Event Logging | Yes | — | Every check generates a structured audit record |
| AU-3 Content of Audit Records | Yes | — | Records include timestamp, target file, finding, severity |
| AU-9 Protection of Audit Information | Yes | — | Timestamped filenames prevent overwrite; dedicated `evidence/` directory |
| AU-12 Audit Record Generation | Yes | — | Records generated automatically on every invocation |
| AC-3 Access Enforcement | Yes | — | Flags wildcard `Resource: "*"` policy statements |
| AC-6 Least Privilege | Yes | — | Flags wildcard `Action: "*"` policy statements |
| AU-6 Audit Record Review | Yes | 1-year retention, weekly review | Evidence files feed the CJIS audit-review workflow |

## Purpose

During GRC audits, you need to prove:

- When a check was performed
- What was checked
- What issues were found

This script automates evidence generation so you have audit-ready documentation. The repository includes `test_policy.json` to exercise the script.

## Features

- **Timestamped filenames** — never overwrites previous evidence (AU-9)
- **Dedicated evidence directory** — separates audit records from operational data (AU-9)
- **Structured findings** — every record includes timestamp, target, finding, severity (AU-3)
- **Overly permissive policy detection** — flags wildcard `Action: "*"` (AC-6) and wildcard `Resource: "*"` (AC-3)
- **Human-readable output** — assessors can read the evidence file directly during walkthroughs

## Requirements

- Python 3.6 or higher
- No external dependencies (uses standard library only)

## Usage

1. Place the IAM policy JSON file in the same directory as the script.
2. Update the `policy_file` variable if your file has a different name.
3. Run the script:

```bash
python evidence_logger.py
```

4. Check the generated evidence file inside the `evidence/` directory:

```
evidence/evidence_2025-12-09_17-27-15_policy_check.txt
```

## Example Output

```
================================================================================
COMPLIANCE EVIDENCE LOG
================================================================================
Timestamp: 2025-12-09_17-27-15

Checking: test_policy.json

[FAIL] Statement "DangerousAdmin": Action is "*"
[FAIL] Statement "DangerousAdmin": Resource is "*"

Result: 2 issues found

================================================================================
END OF LOG
================================================================================
```

## How an Auditor Uses This Output

An assessor reviewing a FedRAMP High or CJIS v6.0 authorization package can use these evidence files as direct artifacts of AU-2 / AU-3 / AU-12 control implementation. The timestamped filename and append-only directory structure satisfy AU-9 (protection of audit information), and the structured findings provide the "who, what, when, outcome" required by AU-3. During an assessor walkthrough, each evidence file maps one-to-one to a NIST 800-53A assessment objective — for example, AU-3 "Determine if the system generates audit records with content that includes timestamp, source, outcome of the event."

## FedRAMP 20x Alignment

This script supports FedRAMP 20x compliance-as-code by producing structured, machine-readable-adjacent evidence on every run. A future enhancement will emit OSCAL Assessment Results JSON, allowing the output to feed continuous monitoring pipelines (compliance-trestle, OSCAL-based tooling) without manual transformation. The append-only timestamping pattern is a foundational unit for KSI metric reporting under FedRAMP 20x.

## CJIS v6.0 Relevance

CJIS v6.0 (audit standard from April 1, 2026) introduces a hard delta on **AU-6**: agencies handling CJI must retain audit records for **1 year** and conduct **weekly review** of those records. This script's evidence files are the unit of that retention and the input to that review. A future enhancement will add S3 archival with Object Lock (WORM compliance mode) so the 1-year retention is enforced at the storage layer, not just by file naming.

## Future Improvements

- Accept policy filename as a command-line argument
- Scan multiple policies in a directory
- Add more compliance checks (e.g., `Effect: Allow` without `Condition`, principal wildcards)
- Output JSON / OSCAL Assessment Results format for FedRAMP 20x pipelines
- S3 archival of evidence files with Object Lock (CJIS AU-6 1-year retention)

## Framework Reference

Control family mappings and AWS implementation details are documented in [nist-800-53-rev-5-to-aws-mapping](https://github.com/relevantGRC/nist-800-53-rev-5-to-aws-mapping).

## License

MIT License
