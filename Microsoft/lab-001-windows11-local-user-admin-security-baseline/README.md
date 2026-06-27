# Lab 001: Windows 11 Local User & Admin Security Baseline

**Module:** Endpoint Governance & Identity Management  
**Environment:** Windows 11 Pro / Enterprise  
**Execution Time:** ~20 Minutes  

## Lab Objective
Establish a foundational security baseline for local identity and access management on a Windows 11 endpoint. This lab establishes a secure, predictable Windows 11 baseline intended to mirror entry-level government and contractor workstation configurations.

A practical Windows 11 Pro lab that simulates real Tier 1 IT support and entry-level security tasks. The lab focuses on configuring local user accounts, enforcing least privilege, and basic auditing. All actions are documented as internal IT notes rather than a tutorial.

---

## Compliance Framework Mapping

This baseline configuration satisfies specific controls within major governance frameworks:

| Framework | Control Family | Control ID | Control Description | Lab Application |
| :--- | :--- | :--- | :--- | :--- |
| **SOC 2** | Logical & Physical Access | CC6.1 | Logical access security software, infrastructure, and architectures have been implemented. | Enforcement of account lockout and password complexity. |
| **ISO 27001** | Access Control | A.9.2.1 | User registration and de-registration. | Renaming and disabling the default built-in Administrator. |
| **NIST 800-53** | Access Control | AC-2 | Account Management. | Separation of standard user operations from administrative privileges. |

---

## Environment
- **Operating System:** Windows 11 Pro
- **System Type:** Standalone local system (no domain)
- **Accounts Configured:**
  - Local Administrator account
  - Standard User account
  - Child / Restricted User account
- **Tools Used:**
  - Local Users and Groups
  - Local Security Policy (`secpol.msc`)
  - Event Viewer
  - Chris Titus Tech Utility (CTT)  
  Used to apply a controlled, Standard Windows configuration baseline.
  Aggressive debloating and service hardening were intentionally avoided
  to preserve lab stability, logging, and security controls.

## Repository Structure

- README.md — Lab overview, scope, and security concepts
- Lab-Objective.md — Purpose and framing of the lab
- Account-Setup.md — Account creation and administrator actions
- Local-Security-Policy.md — Password, lockout, and auditing policy configuration
- Permission-Testing.md — Validation of access controls across user roles
- Parental-Controls.md — Child account restrictions and testing
- Lessons-Learned.md — Reflections and takeaways from the lab
- evidence/ — Supporting screenshots for security policy configuration


## Skills Demonstrated
- Local user account creation and management
- Role-based access control using local accounts
- Enforcement of least privilege
- Permission testing across multiple user roles
- Enabling and verifying security auditing
- Clear, structured technical documentation

## Baseline Reference (CTT Standard)

The following screenshots document the CTT Standard configuration used as the
baseline for this lab.

This baseline:
- Reduces consumer features and telemetry
- Preserves Windows Update, Microsoft Defender, logging, and IPv6
- Avoids aggressive service hardening or debloating
- Maintains compatibility with certification labs and GovTech environments

## Validation and Final State

After applying the CTT Standard baseline, the system was validated to confirm
enterprise and lab compatibility.

Validation performed:
- Windows Update completed successfully post-hardening
- System rebooted without errors
- Microsoft Defender remained enabled and operational
- Core Windows services and logging preserved
- No aggressive service modifications applied


## Security Concepts Applied
- Least Privilege
- Account Separation
- Auditing and Accountability
- Basic Incident Response Readiness

This lab intentionally focuses on local account administration and security controls and does not include Active Directory, Group Policy, or enterprise tooling.

Note: This lab intentionally excludes Active Directory, Group Policy, and Entra ID to maintain focus on local endpoint security fundamentals.
