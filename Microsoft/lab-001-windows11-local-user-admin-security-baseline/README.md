# Lab 001: Windows 11 Local User & Admin Security Baseline

**Module:** Endpoint Governance & Identity Management  
**Environment:** Windows 11 Pro / Enterprise  
**Execution Time:** ~20 Minutes  

## Lab Objective
Establish a foundational security baseline for local identity and access management on a Windows 11 endpoint. This lab focuses on disabling default attack vectors, enforcing password complexity, and generating verifiable technical artifacts to prove compliance.

---

## Compliance Framework Mapping

This baseline configuration satisfies specific controls within major governance frameworks:

| Framework | Control Family | Control ID | Control Description | Lab Application |
| :--- | :--- | :--- | :--- | :--- |
| **SOC 2** | Logical & Physical Access | CC6.1 | Logical access security software, infrastructure, and architectures have been implemented. | Enforcement of account lockout and password complexity. |
| **ISO 27001** | Access Control | A.9.2.1 | User registration and de-registration. | Renaming and disabling the default built-in Administrator. |
| **NIST 800-53** | Access Control | AC-2 | Account Management. | Separation of standard user operations from administrative privileges. |

---

## Step 1: Securing the Built-In Administrator Account
The default `Administrator` account has a well-known SID (Security Identifier) and is a primary target for brute-force attacks. We will rename it and ensure it is disabled.

**Via Local Group Policy Editor:**
1. Press `Win + R`, type `gpedit.msc`, and hit Enter.
2. NavigateNormally I can help with things like this, but I don't seem to have access to that content. You can try again or ask me for something else.
