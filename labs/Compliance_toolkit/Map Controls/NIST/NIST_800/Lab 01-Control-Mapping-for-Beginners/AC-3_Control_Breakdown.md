# AC-3 Control Breakdown: Access Enforcement

**Control ID:** AC-3  
**Control Name:** Access Enforcement  
**Source:** NIST SP 800-53 Rev. 5

---

## Official Control Text

> “The system enforces approved authorizations for logical access to information and system resources in accordance with applicable access control policies.”

---

## What This Means (Plain English)

Only the right people should be able to access the right things.

Think of it like a key card system:  
- Not everyone gets into every room  
- Access is based on job role and need  
- The system has to check whether you're allowed in

---

## Real-World Example

Imagine your app uses:
- **GitLab** to store your code  
- **Vault** to store secrets like passwords and API tokens

Access Enforcement means:
- Only authorized users can view or edit the code in GitLab
- Only specific services or people can pull secrets from Vault

If everyone had access to everything, there would be no security.

---

## Key Questions to Ask

- Who decides who gets access?
- How do we enforce that decision?
- What happens when someone leaves the team?
- How do we know the right people still have access?

---

## Tools That Help Enforce This

| Tool   | How It Helps                                    |
|--------|-------------------------------------------------|
| Vault  | Grants secrets only to users or services with permission |
| GitLab | Controls who can read, write, or approve changes to code |
| IAM Systems (e.g., Okta, AWS IAM) | Set and enforce roles and permissions globally |

---

## How to Map This Control

| Category            | Your Entry                                                       |
|---------------------|------------------------------------------------------------------|
| Tool(s) Used        | Vault, GitLab                                                    |
| How Tool Supports Control | Vault restricts secret access. GitLab manages code access.     |
| Pipeline Stage      | Source (GitLab), Build/Deploy (Vault)                            |
| Gaps or Notes       | Manual user offboarding may still be required                    |

---

## cATO

Mapping this control helps demonstrate how access is enforced automatically. This is the foundation of continuous monitoring and proving your system is secure at all times, not just during audits.
