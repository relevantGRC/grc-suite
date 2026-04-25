# IAM Policy Audit Lab – Hands-On GRC with Terraform & Rego

## Scenario: The IAM Wildcard Panic

You’re reviewing a Terraform pull request, and something doesn’t feel right.

> A policy block shows up with Action: `"*"` and Resource: `"*"`.

Your gut says, “this could destroy everything.”

This lab puts you in the seat of a GRC engineer who’s caught overly permissive IAM before it ever hits production.
You’ll write policy-as-code to make sure wildcard actions and resources are never silently approved again.

---

## Understand the Vulnerability

Before we write any code, let’s look at what we’re up against.

Here’s what a dangerously permissive IAM policy looks like:

- It uses `"Action": "*"` — this means **any** action is allowed. Read, write, delete, escalate privileges, turn off logging, you name it, it’s allowed.
- It uses `"Resource": "*"` — this means **everything** in the environment is fair game: all users, all buckets, all logs, all resources.
- It lacks any conditions, restrictions, or scope. There’s no limit to what this policy can access or who can assume it.

In human terms, it’s like giving someone the keys to your house, your car, your bank account and then setting your alarm code as “1234.”

### Why is this bad?

- It violates the principle of **least privilege**
- It makes it impossible to trace **who accessed what and why**
- It opens the door to **privilege escalation**, **data exfiltration**, and **misuse of sensitive systems**

This kind of policy is a direct violation of multiple NIST 800-53 controls, and it’s the root cause behind multiple real-world cloud breaches.

### What are we going to do about it?

You’ll write a Rego policy that catches these mistakes and stops them before they hit production.

We’re going to build a policy-as-code safety net. One that flags these risky IAM policies early in the dev cycle, so your team can fix them before they turn into headlines.

---

## Overview

In this lab, you’re going to uncover hidden dangers in your infrastructure as code (IaC). Specifically, we’re going to focus on IAM policies which are little blocks of JSON that either lock your environment down tight or blow the doors wide open.

By the end of this walkthrough, you'll be able to:

- Detect risky permissions before they hit production
- Understand how Rego policies work and how to write them
- Use Conftest to scan for security violations
- Learn why wildcard permissions and shared accounts are a bad time
- Build your confidence as a GRC engineer with hands-on skills that matter

This lab is designed for folks who’ve never written a line of code before, but who are ready to start making sense of the alphabet soup of IAM, Rego, and policy enforcement.

No AWS credentials, no fancy tooling. Just GitHub Codespaces and your brain.

---

## Controls Mapped in This Lab

Each of these NIST 800-53 controls has something to say about access management, traceability, and role enforcement. This lab covers:

- **AC-2(12)** – Avoids shared or overly broad policies that obscure individual accountability
- **AC-2(13)** – Supports traceability by requiring scoped, assignable permissions
- **AC-3** – Enforce access control decisions
- **AC-3(4)** – Enforce separation of duties
- **AC-4** – Control information flow (no wildcards or *:* madness)
- **AC-6** – Use least privilege principles
- **AC-6(1)** – Enforce roles and job-based access
- **AC-6(9)** – Restrict access to security-relevant info/functions
- **AC-22** – Limit access to sensitive policy controls or security logs via IAM

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

---

## 1. Break the World

Start with chaos. Deliberately apply an insecure IAM policy. Run your tests and watch them fail. This is proof that your detection method works. 

Create a file called `iam.tf` and paste the following vulnerable Terraform file:

```hcl
resource "aws_iam_policy" "bad_policy" {
  name        = "bad_policy"
  path        = "/"
  description = "A terrible idea."

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "*"
        Resource = "*"
      }
    ]
  })
}

```

**What’s happening here?**

- We're defining an IAM policy using Terraform syntax.
- `Action = "*"` means any action (read, write, delete, nuke your logs, anything).
- `Resource = "*"` means the action can apply to every single thing in the account.
- We’re encoding this policy as a JSON blob with `jsonencode`.

This is a textbook example of what **not** to do.

---

## 2. Simulate the Terraform Output

Terraform would normally convert this to a JSON plan file. We're skipping that complexity for now and simulating the output manually.

Create a file called `bad-policy.json` and paste this in:

```json
{
  "resource": {
    "aws_iam_policy": {
      "bad_policy": {
        "policy": {
          "Statement": [
            {
              "Effect": "Allow",
              "Action": "*",
              "Resource": "*"
            }
          ]
        }
      }
    }
  }
}

```

This is the structure Conftest expects when scanning a policy file. You’re pretending this is the output of your Terraform configuration.

---

## 3. Write the Rego Policy

Create a `policy` folder, then create a file named `iam.rego` in the folder and paste the following:

```
package main

deny contains msg if {
  statement := input.resource.aws_iam_policy[_].policy.Statement[_]
  statement.Action == "*"
  msg := "Wildcard action '*' is not allowed."
}

deny contains msg if {
  statement := input.resource.aws_iam_policy[_].policy.Statement[_]
  statement.Resource == "*"
  msg := "Wildcard resource '*' is not allowed."
}

```

**Let’s break this down:**

- `package main` — This names your policy. Think of it like a folder or namespace.
- `deny[msg]` — This defines a rule that, if matched, denies the configuration and returns a message.
- `statement := input.resource.aws_iam_policy[_].policy.Statement[_]` —
This pulls out each statement from the IAM policy block.`_` is a wildcard index — basically, "give me all the things in this list."
- `statement.Action == "*"` — This checks if the statement uses an  action.
- `statement.Resource == "*"` — Same idea, but checking for full resource access.
- `msg = "..."` — This is the error that gets returned when the rule matches.

This Rego logic directly helps enforce **AC-3**, **AC-4**, and **AC-6**.

---

## 4. Run Conftest in Codespaces

Click the green Code button and choose Codespaces > Create codespace on main

From the root of your lab folder, run:

```bash
conftest test bad-policy.json

```

You should see:

```
FAIL - bad-policy.json - main - Wildcard action '*' is not allowed.
FAIL - bad-policy.json - main - Wildcard resource '*' is not allowed.

```

That’s your Rego policy doing its job.

---

## 5. Bonus Challenge: Fix the Policy

Try this:

- Change `Action` to something specific like `"s3:GetObject"`
- Change `Resource` to a real ARN like `"arn:aws:s3:::my-bucket/*"`

Then re-run Conftest and see if the test passes.

---

## 6. Bonus: Add GitHub Action for CI

Create the file `.github/workflows/policy-check.yml` and paste:

```yaml
name: Conftest Policy Check

on:
  push:
    paths:
      - '**/*.json'
      - '**/*.rego'
  pull_request:

jobs:
  conftest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install Conftest
        run: |
          wget <https://github.com/open-policy-agent/conftest/releases/download/v0.45.0/conftest_0.45.0_Linux_x86_64.tar.gz>
          tar -xzf conftest_0.45.0_Linux_x86_64.tar.gz
          sudo mv conftest /usr/local/bin
      - name: Run Conftest
        run: conftest test bad-policy.json

```

This runs your Rego policy check every time code is pushed. It’s how you shift left like a champ.

---

## The Impact

### Case File: AWS Role Abuse in the Wild

### Summary: 

Time and time again, organizations accidentally deploy IAM policies with *:* permissions. These wildcard grants allow malicious insiders or compromised processes to escalate privileges, disable logging, and access critical infrastructure.

How it usually happens:
- Developers write “quick and dirty” IAM policies with `*` actions and resources
- There’s no automated check in the CI/CD pipeline
- The policy is deployed to production and now it’s open season

### Root Cause:

- Wildcard permissions (`"Action"`: `"*"` and `"Resource"`: `"*"` in IAM)
- No least privilege enforcement
- No preventive policy validation before deployment

### Mitigation:
If you had a Rego policy like the one in this lab, it would catch and reject that IAM policy automatically. You wouldn’t have to manually catch every mistake, you’d shift IAM risk left, with real prevention instead of reactive audit findings.

---

## Wrap-Up

Look at you, writing Rego like it’s your second language.

You just:

- Caught a critical IAM misconfiguration that shows up in real breaches
- Wrote a Rego policy from scratch (go ahead, brag a little)
- Used Conftest like a pro to enforce it
- Learned how wildcard permissions are the cybersecurity version of handing your house keys to a raccoon

This wasn’t just a checkbox exercise. This was hands-on, real-world prep for the kind of stuff that actually matters in security. You’re no longer just reading about AC-6, you’re enforcing it in code.

If you got stuck, learned something new, or had a tiny panic attack followed by a victory fist pump, I want to hear about it.

- Connect with me on [LinkedIn](https://www.linkedin.com/in/ashley-thornhill) and show off your lab
- Found a bug or have a suggestion? Drop it as an issue in the [GRC Playground repo](https://github.com/ashpearce/GRC-Playground)
- Want to make the next lab even better? Fork it, remix it, and tag me when it’s cooler than mine

Compliance doesn’t have to be dry, and security doesn’t have to be slow. Have fun on the playground!
