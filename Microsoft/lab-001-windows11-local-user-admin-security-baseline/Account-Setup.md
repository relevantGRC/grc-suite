# Account Setup & Access Control

## 1. Access Control Philosophy 

This lab enforces the **Principle of Least Privilege (PoLP)**. System interactions are strictly separated between standard operations and administrative configuration to mitigate security risks and maintain system stability.

### The Local Administrator Role
The Administrator account is strictly reserved for elevated system management. Administrator privileges are required to:
* Provision, modify, or deprecate local user accounts.
* Modify system-wide security policies (`secpol.msc`) and access controls.
* Install, remove, or update approved software and services.
* Access restricted file paths and review system-wide security logs via Event Viewer.

### Justification for Privilege Restriction
Routine daily usage under an Administrator context dramatically expands the endpoint's attack surface. Restricting standard usage to non-administrative accounts provides the following security benefits:
* **Malware Mitigation:** Prevents malicious payloads from silently executing with elevated, system-wide rights.
* **Configuration Integrity:** Prevents accidental or unauthorized modifications to core OS settings.
* **Audit Trail Clarity:** Ensures elevated actions require explicit User Account Control (UAC) prompts, creating clear intentionality in security logs.

---

## 2. Lab Account Provisioning 

To implement this separation of duties, the following local accounts were provisioned using the Local Users and Groups snap-in (`lusrmgr.msc`):

| Account Name | Account Type | Purpose / Scope of Access |
| :--- | :--- | :--- |
| `[YourAdminName]` | Administrator | Reserved for baseline configuration, policy enforcement, and lab maintenance. |
| `[YourStandardName]` | Standard User | Simulates a typical enterprise knowledge worker. Used for validation testing. |
| `[YourChildName]` | Standard (Restricted) | Simulates a highly restricted user. Used to test parental controls and app blocking. |

### Security Action: Securing the Default Administrator
*Note: The built-in Windows `Administrator` account has a well-known Security Identifier (SID) and is a common target for brute-force attacks. As part of this baseline, the default `Administrator` account was disabled and renamed to prevent automated enumeration.*
