# Lab 01: Control Mapping for Absolute Beginners

**Title: “What Even Is a Control?”**  
A fully guided introduction to mapping security controls to tools and pipeline stages, with absolutely no prior experience required.

---

## What You’ll Learn

Control mapping is how we prove a system is secure using real evidence. In this lab, you'll learn how to translate a control into plain language, find which tools help satisfy it, and identify where it fits in your software pipeline.

By the end, you’ll be able to:

- Understand what a security control is and why we map them
- Define what “control mapping” means in real life
- Break a control down into plain language
- Connect a control to a tool or process in a DevSecOps pipeline
- Understand how this work supports continuous authorization (cATO)

---

## Prerequisites

None. You don’t need to know code, tools, or even what RMF stands for. This lab is written to walk you through it like we’re pairing together on your first day.

---

## Scenario

You just joined a team building an application for the government. To launch the app, they need something called an "Authorization to Operate" (ATO), which proves the system meets certain security requirements. Those requirements are defined as controls. Your job is to help the team show how they meet those controls—also known as control mapping.

---

## Materials Provided

- README of the NIST SP 800-53 control AC-3: Access Enforcement
- A spreadsheet example template for control mapping
- A pretend secure release (SecRel) pipeline diagram with tool names (Trivy, Vault, GitLab, etc.)

---

## Step-by-Step Instructions

### Step 1: Understand the Control

Open the README with the AC-3 control.

Let’s break it down together:

- The control says the system must “enforce approved authorizations for logical access to information.”
- Translation: Only let people access what they’re allowed to access.
- Even simpler: Don’t let just anyone into the house. Only people with a key.

Now ask yourself:

- Who decides who gets in?
- What tool checks the key at the door?

Write this down in the "Control Breakdown" section of your spreadsheet.

---

### Step 2: Match It to the Pipeline

Open the pipeline diagram.

Walk through it visually:

- Vault is a tool that stores secrets (like passwords and keys).
- GitLab is used for code and can also manage who can change what.
- Trivy scans for vulnerabilities in code or containers.

Ask yourself:

- Does Vault help enforce who can access secrets? Yes.
- Does GitLab control who can access code repos? Yes.
- Do these tools help us meet the requirement of “access enforcement”? Definitely.

Create a your spreadsheet to replicate the columns in Step 5:

- Under “Tools Used,” write Vault and GitLab.
- Under “How Tool Supports Control,” describe what each tool does in plain language.
  Example: “Vault only gives out secrets to people with the right permissions.”

---

### Step 3: Identify the Stage in the Pipeline

Controls don’t always apply everywhere.

Ask:

- When does access control matter?
  - When someone logs into GitLab
  - When secrets are retrieved from Vault during a deployment

Look at the pipeline again. Identify where those things happen.

In your spreadsheet:

- Under “Stage in Pipeline,” write:
  - GitLab = Source Code Management Stage
  - Vault = Build and Deploy Stage

---

### Step 4: Evaluate Gaps

Some controls won’t be fully covered by tools alone.

Ask:

- What happens if someone is offboarded but still has access?
- Who checks permissions regularly?

In your spreadsheet:

- Under “Gaps or Notes,” write anything that isn’t automated (like offboarding or audits).

---

### Step 5: Map It All

You should now have a full row in your spreadsheet:

| Control ID | Control Name       | Tool(s) Used   | How Tool Supports Control                                   | Pipeline Stage     | Gaps or Notes                   |
|------------|--------------------|----------------|-------------------------------------------------------------|--------------------|----------------------------------|
| AC-3       | Access Enforcement | Vault, GitLab  | Vault controls secret access. GitLab controls who can push code. | Build, Deploy, Source Code | Manual offboarding may be needed. |

---

## cATO

Continuous ATO is all about proving your security posture continuously. If you don’t know what tools are satisfying your controls, you can’t automate your monitoring and you’ll end up with a giant, manual checklist.

This lab helps build the foundation of that visibility:

Tools + Controls + Pipeline Stage = cATO Readiness

---

## Wrap-Up

You now know:

- What a control is
- How to interpret it in plain English
- How to map it to tools and pipeline stages
- Why this matters for real-world compliance and automation

---

## Downloads

- [View the SecRel Pipeline Diagram](./SecRel_Pipeline_Diagram.png)

---

Created by [Ashley Pearce](https://www.linkedin.com/in/ashley-thornhill)
