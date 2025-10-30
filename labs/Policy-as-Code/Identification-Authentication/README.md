# Enforcing MFA for Privileged Accounts (IA-2(1))

## Overview

This lab teaches you how to enforce Multi-Factor Authentication (MFA) for administrator accounts using Policy-as-Code tools: Rego and Conftest. You’ll simulate a configuration file representing IAM settings, write a rule to detect missing MFA, and run a policy test to ensure enforcement.

No prior coding or GRC experience is required. This lab assumes a browser-based development environment (like Codespaces) with a built-in terminal and file editor.

---

## Why This Matters

Administrator accounts typically have access to sensitive settings, production environments, and user data. If one of these accounts is compromised, an attacker can:

- Reconfigure security settings
- Access or exfiltrate data
- Disable critical controls like logging or monitoring
- Laterally move into other systems and escalate privileges

Multi-Factor Authentication (MFA) adds an extra layer of protection, requiring users to verify their identity using a second factor like an authenticator app, even if a password is compromised.

---

## Real-World Case Study: Okta Breach (2022)

In early 2022, the LAPSUS$ hacking group exploited a subcontractor with admin access to Okta, one of the largest identity management providers.

### What happened:
1. A subcontractor account with admin privileges had no MFA enforcement.
2. Stolen credentials were used to log into the account remotely.
3. From there, attackers gained visibility into Okta’s internal tools.
4. Okta customers, which included government agencies and Fortune 500 companies, were potentially exposed.

### What went wrong:
- Lack of strong identity verification for a privileged account
- No automated enforcement or alerting to detect missing MFA

### What could have helped:
- A policy that automatically flagged administrator accounts without MFA

That’s what you’ll build in this lab.

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
curl -L https://github.com/open-policy-agent/conftest/releases/download/v0.45.0/conftest_0.45.0_Linux_x86_64.tar.gz -o conftest.tar.gz
tar -xzf conftest.tar.gz
sudo mv conftest /usr/local/bin/
conftest --version
```

If you see the version number, you're good to go.

---

## Step-by-Step Lab Instructions

### Step 1: Create the IAM Configuration File

This file simulates IAM settings as they might appear in a real cloud environment. Save the following as `iam_config.json`.

```json
{
  "users": [
    {
      "username": "admin_ashley",
      "role": "Administrator",
      "mfa_enabled": false
    },
    {
      "username": "sandbox_sam",
      "role": "User",
      "mfa_enabled": true
    }
  ]
}
```

#### Explanation:
- `users`: A list of accounts to evaluate
- `username`: Identifier for the user
- `role`: Access level for the user
- `mfa_enabled`: A boolean indicating whether MFA is active

In this file:
- `admin_ashley` is an administrator without MFA, a violation
- `sandbox_sam` is a user with MFA, acceptable

---

### Step 2: Write the Rego Policy

Create a `policy` folder, then create a file named `require_mfa.rego` and paste the following:

```rego
package main

deny[message] {
  some i
  user := input.users[i]
  user.role == "Administrator"
  not user.mfa_enabled
  message := sprintf("Admin user '%s' does not have MFA enabled.", [user.username])
}
```

#### Line-by-line Breakdown:
- `package iam.security`: Defines a namespace to organize the policy
- `deny[message] { ... }`: A rule that triggers if the condition inside is met
- `input.users[_] == user`: Iterates over all users in the input
- `user.role == "Administrator"`: Checks if the user is privileged
- `not user.mfa_enabled`: Ensures MFA is enabled; this fails if it's false or missing
- `message := ...`: Creates a message identifying the failing account

---

### Step 3: Run the Policy Test

Execute the following command in your browser-based terminal:

```bash
conftest test iam_config.json
```

#### What happens:
- Conftest reads the `iam_config.json` file
- It applies your policy from `require_mfa.rego`
- If any admin accounts do not have MFA enabled, the test fails

#### Expected output:

```
FAIL - iam_config.json - Admin user 'admin_ashley' does not have MFA enabled.
```

---

### Step 4: Fix the Misconfiguration

In `iam_config.json`, update Ashley’s user object:

```json
"mfa_enabled": true
```

Now rerun the policy:

```bash
conftest test iam_config.json
```

You should now see **no errors**, indicating compliance with IA-2(1).

---

### Step 5: Test With Another Admin

Add a second admin without MFA:

```json
{
  "username": "bobby_tables",
  "role": "Administrator",
  "mfa_enabled": false
}
```

Rerun the test. Your policy should now detect both Ashley and Bobby if neither has MFA. This mimics a real-world scenario where enforcement needs to scale across multiple users.

---

## Bonus Challenge

Update your Rego policy to also flag administrator accounts where:
- `mfa_enabled` is missing
- `mfa_enabled` is set to `null`

This ensures that incomplete or malformed configuration files are also caught, an essential GRC requirement.

---

## FAQ

**1. Why does MFA matter more for admin accounts than for user accounts?**  
Admins have privileged access that, if compromised, could result in serious damage to the system or data.

**2. What does `not user.mfa_enabled` check for?**  
It checks if MFA is either disabled or not defined at all for a user.

**3. What kind of accounts should this rule apply to?**  
Privileged accounts, including those with administrative or system-level access.

---

## Wrap-Up: Why This Lab Matters

In this lab, you created and tested a Policy-as-Code rule that enforces a core GRC control: **IA-2(1)** which requires MFA for privileged accounts.

Here’s why this matters beyond passing a compliance checklist:

### Continuous Authorization (cATO)
- In a traditional ATO process, this control might be manually checked once a year.
- In a cATO environment, this policy runs every time a change is made to IAM settings.
- You’ve just built a scalable, automated enforcement check critical for ongoing authorization and reduced audit friction.

### Security Posture
- Most account breaches stem from weak or missing identity controls.
- MFA is one of the highest-impact, lowest-effort defenses available.
- By ensuring it’s always enforced for privileged users, you dramatically reduce the blast radius of a breach.

### Governance and Evidence
- You now have automated enforcement **and** verifiable test results.
- That output can be integrated into a pipeline, logged, and stored in your Body of Evidence (BOE).
- This builds traceable, repeatable confidence that the system meets the requirements of NIST 800-53 AC-6(7).
