# Lab Objective: Local Identity & Access Management

## 1. Purpose of the Lab
The primary objective of this lab is to operationalize real-world **Identity and Access Management (IAM)** on a standalone Windows 11 endpoint. By configuring and validating Administrator, Standard User, and Restricted (Child) accounts on a shared system, this lab demonstrates the practical application of the **Principle of Least Privilege (PoLP)**, the enforcement of baseline security controls, and the empirical validation of role-based access boundaries.

## 2. The Security Context: Why Role-Based Access Matters
Implementing strict access controls at the local endpoint level significantly reduces the system's attack surface. The deliberate separation between administrative and standard user contexts achieves the following critical governance objectives:
* **Malware Containment:** Limits the potential "blast radius" of malicious code by preventing execution with system-level privileges.
* **Configuration Integrity:** Prevents unauthorized or accidental modifications to core operating system settings, network configurations, and security policies.
* **Auditability & Accountability:** Ensures that all elevated system changes require explicit authentication via User Account Control (UAC), providing a clear and traceable audit log for compliance verification (aligning with frameworks like NIST 800-53 AC-2).

## 3. Emulating Enterprise Tier 1 Operations
This lab environment simulates core Tier 1 IT Support and Security Operations Center (SOC) responsibilities. The tasks executed herein mirror the standard operating procedures required to protect systems and users in managed enterprise environments, specifically:
* Provisioning and managing user identities across varying organizational trust levels.
* Assigning and enforcing appropriate execution permissions.
* Validating local security policy configurations (`secpol.msc`).
* Troubleshooting access failures and ensuring that applied security controls successfully block unauthorized actions without impeding legitimate user functions.
