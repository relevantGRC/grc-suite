# AC-12: Session Timeout Enforcement

## Overview

### What this lab is:
A click‑first, Codespaces‑friendly walkthrough that teaches you how to enforce session timeouts as Policy‑as‑Code using OPA/Rego + Conftest. You’ll intentionally ship a bad config, watch the policy catch it, then remediate and push a clean commit that turns CI green. 

### Who it’s for:
Engineers, SREs, AppSec/SecRel, security‑curious PMs and anyone who can open a Codespace and right‑click “New File.” Zero Rego experience needed.

### What you’ll build (for real):

- A Rego policy that enforces “idle sessions must terminate in ≤ 900 seconds (15 min).”
- A bad YAML config that fails the policy on purpose.
- A GitHub Action that runs the check on every PR/push and exports JSON + SARIF artifacts.
- A clean remediation commit that proves the control works.

### Success looks like:

- You see a red X in Actions with a message like
`AC-12: 'session_timeout' must not be 'never'`
- You fix the config to `900`, push again, and it flips to green.
- You can open `conftest_output.json` or `conftest_output.sarif` and literally point to the evidence for auditors.

### Why Codespaces:
Consistency. Everyone gets the same environment, same versions, same results. No “works on my machine” energy. Also, fewer tears.

---

## Why This Matters (aka: Security Without the Vibes)

Sessions that never expire are like leaving your badge on a café table with a Post‑it that says “take me.” In real orgs, people step away from shared workstations, browsers hold onto sessions, and attackers love long‑lived cookies. AC‑12 exists to shrink the attack window. If a session goes idle, it dies.

This lab bakes that principle directly into your pipeline so you don’t have to rely on hope, good intentions, or tribal knowledge. If someone tries to merge a config that sets `session_timeout: "never"` or `session_timeout: 7200`, the build blocks with a plain‑English reason. No finger‑wagging emails. No “we’ll fix it later.” 

### Business impact, not fear‑mongering:

- Cuts real risk: Stops insider walk‑ups and token replay from abandoned sessions.
- Reduces incident blast radius: Limits how long a stolen session is useful.
- Proves compliance on autopilot: CI artifacts = audit evidence you don’t have to hand‑craft.
- Scales across teams: One tiny policy, many repos, uniform enforcement.

### For GRC + leadership:
You’ll walk away with repeatable proof that AC‑12 is enforced (not just “documented”). Artifacts show detection and remediation, which is exactly what auditors ask for. Metrics like coverage, violations, remediation rate, MTTR roll up neatly from those same artifacts with no extra spreadsheet gymnastics.

---

## Real-World Case Study: The Hospital Kiosk

### Summary

A regional hospital’s Electronic Health Record (EHR) portal allowed medical staff to stay logged in for 8 hours of inactivity. One evening, a nurse logged into a hallway kiosk to update a patient chart, got called into an emergency, and left without logging out. The session remained open, all night.

### What Happened:

- The kiosk was in a semi-public hallway near the nurses’ station.
- At 2:13 AM, a janitorial contractor with network knowledge and limited physical access walked up, wiggled the mouse, and was instantly inside the nurse’s EHR session.
- They browsed patient files for over 20 minutes before leaving.
- Logs showed records were viewed but not edited, making the incident harder to catch in day-to-day monitoring.

### What Went Wrong

- Excessive session timeout — The system defaulted to 8 hours for all roles, including privileged medical staff.
- No idle lock or forced termination — Even minimal inactivity detection could have interrupted the session.
- No consistent enforcement across systems — Other apps in the same environment had shorter timeouts, but the EHR was “special-cased” to avoid “annoying” staff.
- Security left to human behavior — The nurse was expected to log out manually, but in emergencies, humans default to speed, not security.

### What Could Have Helped

- AC-12 Policy-as-Code enforcement in the CI/CD pipeline
If every deployment had been scanned for `session_timeout` > `900` seconds, this misconfiguration would never have reached production.
- Uniform timeout standard
Web apps and services with interactive sessions capped at 900 seconds (15 min) idle.
- Defense in depth
Idle lock at the OS/browser level + session termination at the app layer.
- No `“never”` option
Disallowing `session_timeout: "never"` or blank values prevents “accidental” infinite sessions.
- Auditable evidence
JSON/SARIF artifacts from CI runs showing the enforcement would give leadership proof the control is active and working.

---

## Learning Objectives

By completing this lab, you will:

- Understand how to identify privileged users in a configuration file
- Write a Rego policy to enforce MFA for admin accounts
- Run a test using Conftest to detect violations
- Connect this technical enforcement to broader security and GRC goals

---

## Lab Setup

This lab runs best in GitHub Codespaces. Choose to either fork the repo for a quickstart, or build it from scratch yourself for a better learning experience.

### Option A: Quickstart – Fork or Open the Repo

> If you want to dive straight into testing the policy and running the Rego, fork the GitHub repo and start on Step 4. Terraform and Conftest will be automatically installed and all necessary files are included.
> 

[GRC Playground](https://github.com/ashpearce/GRC-Playground)

---

### Option B: Build It Yourself (Recommended)

> Want to learn by building it from scratch? Great. Follow the instructions below to:
> 
- Create the Terraform file
- Write your own `policy.rego`
- Create a `conftest.yaml`
- Generate the Terraform plan and test it manually

### Step 1: Open a Codespace

1. Go to [https://github.com](https://github.com/) and open any repo you own (or fork [GRC Playground](https://github.com/ashpearce/GRC-Playground))
2. Click the green **`<> Code`** button
3. Choose **`Open with Codespaces → New codespace`**

### Step 2: Install Terraform

In your Codespaces terminal:

```bash
sudo apt-get update && sudo apt-get install -y gnupg software-properties-common curl unzip

curl -fsSL https://apt.releases.hashicorp.com/gpg | \
  sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
  https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
  sudo tee /etc/apt/sources.list.d/hashicorp.list

sudo apt update && sudo apt install terraform -y

```

Verify it works:

```bash
terraform --version
```

### Step 3: Install Conftest

Still in your terminal:

```bash
mkdir -p ~/.local/bin
curl -sSLf -o /tmp/conftest.tgz \
  "https://github.com/open-policy-agent/conftest/releases/download/v0.62.0/conftest_0.62.0_Linux_x86_64.tar.gz"
tar -xzf /tmp/conftest.tgz -C /tmp
mv /tmp/conftest ~/.local/bin/
chmod +x ~/.local/bin/conftest
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
conftest --version
```

If you see the version number, you're good to go.

### Why these two?
- Terraform: other controls in the Playground use it, so we normalize the environment.
- Conftest: a tiny runner that feeds files (YAML/JSON/HCL) into your Rego policy and prints pass/fail with useful messages + exportable artifacts.

---

## Step-by-Step Lab Instructions

### Step 1: Create the Policy
Create a `policy` folder, then create a file named `ac-12.rego` and paste the following:

```
package main
import rego.v1

# AC-12: require a session timeout and cap it at 900 seconds (15 minutes)
# Expected input shape:
#   application:
#     settings:
#       session_timeout: number OR numeric string

# 1) Missing key entirely
deny contains msg if {
  not input.application.settings.session_timeout
  msg := "AC-12: 'session_timeout' is missing from application settings"
}

# 2) Empty string
deny contains msg if {
  input.application.settings.session_timeout == ""
  msg := "AC-12: 'session_timeout' is defined but empty"
}

# 3) Explicitly set to 'never'
deny contains msg if {
  input.application.settings.session_timeout == "never"
  msg := "AC-12: 'session_timeout' must not be 'never'"
}

# 4a) Too long when provided as a NUMBER
deny contains msg if {
  type_name(input.application.settings.session_timeout) == "number"
  input.application.settings.session_timeout > 900
  msg := sprintf(
    "AC-12: 'session_timeout' is %d seconds (exceeds 900)",
    [input.application.settings.session_timeout],
  )
}

# 4b) Too long when provided as a STRING containing only digits
deny contains msg if {
  val := input.application.settings.session_timeout
  type_name(val) == "string"
  regex.match("^[0-9]+$", val)
  to_number(val) > 900
  msg := sprintf(
    "AC-12: 'session_timeout' is %d seconds (exceeds 900)",
    [to_number(val)],
  )
}
```


### Explanation:
`package main`: Creates a namespace `data.main`; Conftest expects to evaluate `data.main`.

`import rego.v1`: Uses modern Rego v1 syntax; it lets us write deny contains msg if `{ … }` cleanly.

The comment block documents the control and the input shape the policy expects (so future you knows how to feed it).

Rule 1: if the key is missing entirely, we fail with a precise message.

Rule 2: if the key exists but is the empty string, still a fail (configs do this a lot).

Rule 3: if someone sets "never", block it with prejudice (and a nice explain‑like‑I’m‑five message).

Rule 4a: if the value is a number and it’s greater than 900 seconds (15 minutes), fail and echo the actual value.

Rule 4b: if the value is a string of digits (e.g., "1200") and it’s > 900, also fail. Real configs switch between numbers and strings; we support both so developers can’t sidestep the rule.


### Best practices baked in:
- Deny‑style with human‑readable messages → devs fix faster.
- Handle mixed types (numbers and numeric strings).
- Explicitly disallow "never" (classic loophole).
- 900 seconds aligns with AC‑12 expectations and common enterprise policies.

---

### Step 2: Create the Bad Test Input
Create a `policy-tests` folder, then create a file named `ac-12-bad-config.yaml` and paste the following:

```
application:
  name: example-tenant
  env: prod
  version: 1.4.2
  features:
    remember_me: true           # UX thing; not a security control
    multi_region: [us-east1, eu-west1]
  logging:
    level: info
    redact_fields: [password, token]
  settings:
    session_timeout: "never"    # never is not valid
    idle_lock_enabled: false    # idle lock is NOT a substitute for termination
    max_concurrent_sessions: 5
    cookie_secure: true
    cookie_http_only: true
```

> Why this much “noise” around the bug? Because real configs are busy. A good policy should laser‑target the relevant field and ignore everything else.

### Why we use YAML and JSON test inputs
- YAML is human‑friendly and developers write configs like this.
- JSON is how many tools serialize YAML internally (and how extractors hand data to OPA).
- By testing both, you reduce “it passed locally but failed in CI” drama.

Inside the policy-tests/ folder, create a file named `ac-12-test-input.json` and paste this into it:

```
{
  "application": {
    "name": "example-tenant",
    "settings": {
      "session_timeout": 7200
    }
  }
}
```

> We’ll run YAML first to see the failure, then you can try JSON for variety.

---

### Step 3: Run the Policy Test

```
# Human-friendly table
conftest test policy-tests/ac-12-bad-config.yaml --policy policy -o table
```

You should see:

```
FAIL - policy-tests/ac-12-bad-config.yaml - AC-12: 'session_timeout' must not be 'never'
1 test, 0 passed, 0 warnings, 1 failure, 0 exceptions
```

Export artifacts (even on failure) so we can keep receipts:

```
conftest test policy-tests/ac-12-bad-config.yaml --policy policy -o json  > conftest_output.json  || true
conftest test policy-tests/ac-12-bad-config.yaml --policy policy -o sarif > conftest_output.sarif || true
```

Open `conftest_output.json` in the file tree (left side). We’ll analyze it soon.

---

### Step 3: Add a Minimal GitHub Action (so commits re-run the check)

```
Create .github/workflows/ac12-conftest.yml:

name: AC-12 Session Timeout Policy

on:
  pull_request:
  push:
    branches: [ main ]

jobs:
  conftest:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install Conftest
        run: |
          CONFT_VER="0.62.0"
          curl -L -o conftest.tar.gz "https://github.com/open-policy-agent/conftest/releases/download/v${CONFT_VER}/conftest_${CONFT_VER}_Linux_x86_64.tar.gz"
          tar -xzf conftest.tar.gz
          sudo mv conftest /usr/local/bin/
          conftest --version

      - name: Run AC-12 policy (table)
        run: conftest test policy-tests/ac-12-bad-config.yaml --policy policy -o table

      - name: Export JSON
        run: conftest test policy-tests/ac-12-bad-config.yaml --policy policy -o json > conftest_output.json || true

      - name: Export SARIF
        run: conftest test policy-tests/ac-12-bad-config.yaml --policy policy -o sarif > conftest_output.sarif || true

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: ac12-results
          path: |
            conftest_output.json
            conftest_output.sarif

      - name: Upload SARIF to code scanning
        if: always()
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: conftest_output.sarif
```

### What this does: 
Every push to main or any pull request checks your policy, exports machine‑readable results, and (optionally) publishes SARIF into GitHub’s Code Scanning UI so failures show up next to code.

---

### Step 4: Commit the failing state (so we see CI yell)

```
git add .
git commit -m "AC-12 lab: add deny policy + bad test input to demonstrate failure"
git push
```

Go to your repo’s Actions tab. You’ll see the workflow run with a red X. This is intentional. Now we fix it.

---

## Real‑world case study

Think of a busy hospital. A nurse logs into an EHR web app on a shared workstation to check labs, gets paged to an emergency, and sprints out. The browser tab remains open. The application’s session timeout is set for eight hours. Long enough to stream a Lord of the Rings extended cut, take a nap, and come back. Fifteen minutes later, a well‑meaning coworker sits down to “quickly check something,” and suddenly they’re inside a still‑active session with access to protected health information. No re‑auth, no idle termination, nothing. In a parallel universe, an attacker who shoulder‑surfed a session token could replay it before the timeout and waltz right in. The root cause isn’t exotic, it’s a config: overlong or nonexistent idle timeout. AC‑12 exists specifically to shut this door. Our pipeline policy makes sure this kind of misstep gets caught before it ever lands in production.

---

## Remediate the config locally (make it pass)

Open policy-tests/ac-12-bad-config.yaml and change just one line:

```
  settings:
-   session_timeout: "never"    # the problem; violates AC-12
+   session_timeout: 900        # max 15 minutes (AC-12 compliant)
    idle_lock_enabled: false
```

Run the policy again:

```
conftest test policy-tests/ac-12-bad-config.yaml --policy policy -o table
```

Expected:

```
1 test, 1 passed, 0 warnings, 0 failures, 0 exceptions
```

Export fresh artifacts:

```
conftest test policy-tests/ac-12-bad-config.yaml --policy policy -o json  > conftest_output.json
conftest test policy-tests/ac-12-bad-config.yaml --policy policy -o sarif > conftest_output.sarif
```

## Commit the fix (watch CI go green)

```
git add policy-tests/ac-12-bad-config.yaml conftest_output.json conftest_output.sarif
git commit -m "AC-12: remediate session_timeout to 900s; pipeline should pass"
git push
```

Back in Actions, the workflow should go green, and the SARIF entry will show as resolved/clean.

## Artifact review (and what to do with it)
Sample conftest_output.json (failure case)

```
[
  {
    "filename": "policy-tests/ac-12-bad-config.yaml",
    "msg": "AC-12: 'session_timeout' must not be 'never'",
    "metadata": null
  }
]

Sample conftest_output.sarif (failure case, truncated)
{
  "version": "2.1.0",
  "runs": [
    {
      "tool": { "driver": { "name": "conftest" } },
      "results": [
        {
          "ruleId": "AC-12-session-timeout",
          "level": "error",
          "message": { "text": "AC-12: 'session_timeout' must not be 'never'" },
          "locations": [
            { "physicalLocation": { "artifactLocation": { "uri": "policy-tests/ac-12-bad-config.yaml" } } }
          ]
        }
      ]
    }
  ]
}
```

### What can you do with these artifacts?

- Attach to tickets (Jira, etc.) as evidence of detection and remediation.
- Store in your GRC system (Nucleus, Tracer, SD Elements) to prove AC‑12 enforcement.
- Publish SARIF to GitHub Code Scanning so policy failures show up inline with code.
- Trend metrics (see below) by scraping JSON across repos to track risk burn‑down.

---

## Exceptions (edge cases that might qualify, and how to handle)

Reality check: sometimes you need more than 15 minutes. If you must deviate, make it rare, documented, and temporary.

<b> Edge case 1 — Clinical workflow continuity: </b>
A surgical anesthesia station needs longer sessions due to sterile field constraints.

- Compensating controls: proximity badge re‑auth, physical workstation lock, screen privacy filters, workstation auto‑lock with rapid SSO unlock, IP allowlist.

- Exception doc: reason, compensating controls, risk owner, expiry date, rollback plan.

<b> Edge case 2 — Kiosk with human‑in‑the‑loop guardrails: </b>
Patient check‑in kiosk uses device‑level lockdown and supervised flow.

- Compensating controls: kiosk mode (no browser chrome), automatic reset between users, physical monitoring, session binding to device ID, no sensitive data post‑check‑in.

- Exception doc: justification, how user data is wiped, monitoring procedures, expiry.

<b> Edge case 3 — High‑latency ops console during incident: </b>
An on‑call console used only during major incidents in a controlled SOC needs a slightly longer idle window to keep context.

- Compensating controls: short‑lived SSO tokens, step‑up auth for privileged actions, IP‑restricted access, SOC presence, full audit logging with session recording.

- Exception doc: incident‑only scope, time‑boxed (e.g., 14 days), review after post‑mortem.

## Control & GRC mapping (for the audit homies)

Control: NIST 800‑53 Rev.4 AC‑12 — Session Termination

CCI(s): CCI‑000057

Evidence: `conftest_output.json`, `conftest_output.sarif`, GitHub Actions run URL/screenshots, the PR that fixed the issue.

Policy location: `policy/policy.ac_12.rego`

Inputs tested: `policy-tests/ac-12-bad-config.yaml` (post‑fix shows compliance)

Owners: SecRel / AppSec; service team owns remediation

Retention: Keep artifacts for your audit cycle (e.g., 1–3 years depending on regime)

## Metrics to track (because vibes aren’t metrics)

Coverage — how many apps/repos run this AC‑12 check in CI.

Violations — count of failures per sprint (aim down).

False positives — should be tiny; fix input shape or policy if noisy.

Remediation rate — % of failures fixed vs. granted exceptions.

MTTR — average time from fail → fix.

Changelog — date/owner/reason for any policy change.

## Troubleshooting (quick hits)

Conftest command not found → reopen terminal or confirm `/usr/local/bin` is in PATH.

“unknown: rego.v1” → your Conftest is old; reinstall with the version above or remove `import rego.v1` and rewrite to v0 style.

Nothing happens in Actions → confirm the workflow file lives at `.github/workflows/ac12-conftest.yml` and you pushed to `main` or opened a PR.

It passes locally but fails in CI → feed the same exact file to both, or try the JSON version to match how CI serializes.

## Appendix: Run the JSON input too (optional)

```
# Failing JSON example (7200 seconds)
conftest test policy-tests/ac-12-test-input.json --policy policy -o table
# Then change 7200 -> 900 and run again to see a pass
```
