# Lab 02: AD DS Deployment Preparation

![Platform](https://img.shields.io/badge/Platform-Windows%20Server%202022-blue)
![Technology](https://img.shields.io/badge/Technology-Active%20Directory-blue)
![Focus](https://img.shields.io/badge/Focus-AD%20DS%20Preparation-orange)
![Domain](https://img.shields.io/badge/Domain-mrtg.local-purple)
![Stage](https://img.shields.io/badge/Stage-Pre--Promotion-lightgrey)
![Validation](https://img.shields.io/badge/Validation-Ready%20for%20Promotion-brightgreen)

---

## Objective

Prepare `MRTG-DC01` for deployment as the first Active Directory domain controller in the Monroe Redstone Technology Group environment.

This lab installs the Active Directory Domain Services role and its management tools, prepares the new forest configuration, and validates that the server is ready for domain controller promotion.

The promotion, forest creation, DNS validation, and activation of domain authentication are completed in Lab 03.

---

## Business Scenario

Monroe Redstone Technology Group requires a centralized identity platform for authentication, authorization, policy enforcement, and IAM governance.

Before a domain controller can provide these services, the server must be equipped with the required Active Directory components and pass deployment prerequisite checks.

This lab addresses the need to:

- Prepare the first identity server for AD DS deployment
- Install the AD DS role and supporting management tools
- Prepare a new forest for `mrtg.local`
- Validate promotion prerequisites
- Separate deployment preparation from domain activation
- Create a controlled handoff point for Lab 03

---

## Lab Summary

In this lab, I prepared `MRTG-DC01` for Active Directory Domain Services deployment.

The AD DS role and supporting management tools were installed through Server Manager. The Active Directory Domain Services Configuration Wizard was then used to prepare a new forest configuration for `mrtg.local`.

The prerequisite checks passed successfully, confirming that `MRTG-DC01` was ready for promotion in Lab 03.

---

## Environment

| Component | Details |
|---|---|
| Server | `MRTG-DC01` |
| Operating System | Windows Server 2022 |
| Planned Domain | `mrtg.local` |
| Deployment Type | New forest |
| Installed Role | Active Directory Domain Services |
| Management Tools | AD DS tools, Group Policy Management, and PowerShell module |
| Virtualization Platform | Hyper-V |
| Organization | Monroe Redstone Technology Group |
| Promotion Status | Prepared in Lab 02 and completed in Lab 03 |

---

## Prerequisites

- Windows Server 2022 installed on `MRTG-DC01`
- Server renamed to `MRTG-DC01`
- Administrative access to the server
- Network configuration prepared for domain controller deployment
- Windows Server installation and updates completed
- Planned internal domain name of `mrtg.local`

---

## Scope

### Included

- AD DS role installation
- AD DS management tool installation
- Group Policy Management installation
- New forest configuration preparation
- Root domain entry for `mrtg.local`
- AD DS prerequisite validation
- DNS delegation warning review
- Promotion readiness confirmation

### Not Included

- Completed domain controller promotion
- Completed forest creation
- Full DNS zone validation
- DNS SRV record validation
- Kerberos authentication validation
- Domain health validation
- Organizational Unit design
- Group Policy enforcement
- Domain-joined client validation

---

## Deployment Architecture

This lab prepares `MRTG-DC01` to become the first domain controller in the MRTG environment.

```text
MRTG-DC01
|-- Active Directory Domain Services
|-- Group Policy Management
|-- AD DS and AD LDS Tools
|-- Active Directory PowerShell Module
|-- Active Directory Administrative Center
`-- AD DS Snap-ins and Command-Line Tools
```

Planned forest root domain:

```text
mrtg.local
```

The server remains in the preparation stage until promotion is completed in Lab 03.

---

## AD DS Deployment Model

The initial AD DS deployment is divided into two controlled phases.

| Phase | Lab | Purpose |
|---|---|---|
| Preparation | Lab 02 | Install AD DS and validate promotion readiness |
| Activation | Lab 03 | Promote the server, create the forest, and validate domain services |

Separating preparation from activation makes the deployment easier to document, validate, and troubleshoot.

---

## AD DS Components

| Component | Purpose |
|---|---|
| Active Directory Domain Services | Provides the directory service and domain identity foundation |
| Group Policy Management | Supports centralized policy administration |
| Remote Server Administration Tools | Provides Windows Server management capabilities |
| AD DS and AD LDS Tools | Provides directory administration tools |
| Active Directory Module for Windows PowerShell | Supports Active Directory administration through PowerShell |
| Active Directory Administrative Center | Provides a graphical interface for directory administration |
| AD DS Snap-ins and Command-Line Tools | Provides traditional management consoles and command-line utilities |

---

## Implementation and Validation

### 1. Installed the AD DS Role and Management Tools

The Active Directory Domain Services role was selected for installation on `MRTG-DC01`.

The installation included:

- Active Directory Domain Services
- Group Policy Management
- Remote Server Administration Tools
- AD DS and AD LDS Tools
- Active Directory module for Windows PowerShell
- Active Directory Administrative Center
- AD DS snap-ins and command-line tools

![AD DS role installation](screenshots/lab-02-01-ad-ds-role-installation.png)

This provided the server components and management tools required for domain controller deployment.

---

### 2. Prepared the New Forest Configuration

The Active Directory Domain Services Configuration Wizard was opened to prepare the server for a new forest deployment.

The planned root domain was entered as:

```text
mrtg.local
```

This established the intended namespace for the MRTG Active Directory environment.

---

### 3. Completed the Prerequisite Check

The configuration wizard performed its prerequisite validation before promotion.

Validation result:

```text
All prerequisite checks passed successfully.
```

![AD DS prerequisite check](screenshots/lab-02-02-ad-ds-prerequisites-check.png)

The DNS delegation warning was reviewed and expected because `mrtg.local` is an isolated lab namespace without an external parent DNS zone.

The warning did not indicate a failed prerequisite check.

---

### 4. Confirmed Promotion Readiness

After the prerequisite checks completed successfully, `MRTG-DC01` was considered ready for domain controller promotion.

The promotion itself was intentionally reserved for Lab 03 to preserve a clear separation between preparation and activation.

---

## Security and IAM Relevance

A domain controller is a Tier 0-equivalent identity asset because it controls authentication, authorization, directory data, and security policy processing.

This lab supports secure identity infrastructure deployment through:

- Controlled installation of privileged server roles
- Validation before domain activation
- Separation of preparation and promotion activities
- Documentation of identity infrastructure changes
- Review of deployment warnings
- Evidence-based confirmation of readiness
- Preparation for centralized authentication and policy enforcement

Documenting the preparation stage improves change traceability and reduces the chance of deploying an incomplete identity platform.

---

## Risks Addressed

This lab reduces the risk of:

- Missing AD DS role components
- Missing administrative tools
- Incomplete deployment preparation
- Failed or ignored prerequisite checks
- Undocumented domain controller changes
- Unclear separation between preparation and activation
- Weak handoff between deployment phases
- An unstable foundation for future IAM controls

---

## Control Mapping

| Control Area | Lab Contribution |
|---|---|
| Identity Infrastructure | Prepares `MRTG-DC01` for AD DS deployment |
| Change Control | Documents role installation before promotion |
| Privileged Infrastructure | Identifies the future domain controller as a highly sensitive identity asset |
| Operational Consistency | Separates preparation from domain activation |
| Deployment Validation | Confirms that prerequisite checks passed |
| Audit Readiness | Captures evidence of role installation and readiness validation |
| IAM Foundation | Prepares centralized authentication and policy services |

---

## Validation Results

| Validation Item | Result |
|---|---|
| AD DS role installed | Passed |
| Group Policy Management installed | Passed |
| Remote Server Administration Tools installed | Passed |
| AD DS and AD LDS Tools installed | Passed |
| Active Directory PowerShell module installed | Passed |
| Active Directory Administrative Center installed | Passed |
| AD DS snap-ins and command-line tools installed | Passed |
| New forest deployment selected | Passed |
| `mrtg.local` entered as the root domain | Passed |
| AD DS prerequisite checks completed | Passed |
| Prerequisite checks passed | Passed |
| DNS delegation warning reviewed | Passed |
| Server ready for promotion | Passed |

---

## Evidence Collected

| Evidence | File |
|---|---|
| AD DS role and management tools | `screenshots/lab-02-01-ad-ds-role-installation.png` |
| AD DS prerequisite validation | `screenshots/lab-02-02-ad-ds-prerequisites-check.png` |

---

## What I Would Improve in Production

In a production environment, I would:

- Use a formal domain controller deployment checklist
- Select a domain namespace based on a registered organizational domain instead of `.local`
- Confirm server naming standards before promotion
- Validate static IP addressing and DNS configuration
- Document administrative ownership
- Restrict domain controller access to approved Tier 0 administrators
- Define backup and recovery requirements before activation
- Create a formal change record
- Confirm time synchronization requirements
- Review DNS delegation requirements
- Securely document Directory Services Restore Mode procedures
- Capture pre-change and post-change validation evidence
- Confirm domain and forest functional-level requirements
- Review capacity, availability, and site placement requirements

---

## Lessons Learned

This lab reinforced that installing the AD DS role is not the same as activating a domain controller.

Active Directory deployment is a phased process that includes server preparation, role installation, configuration, promotion, and post-deployment validation.

Separating these stages makes the work easier to document, troubleshoot, and explain while creating clear validation points throughout the deployment.

---

## Outcome

Lab 02 successfully prepared `MRTG-DC01` for Active Directory Domain Services deployment.

The lab confirmed that:

- The AD DS role was installed
- Required management tools were installed
- A new forest deployment was prepared
- `mrtg.local` was entered as the planned root domain
- AD DS prerequisite checks passed
- The DNS delegation warning was reviewed and understood
- `MRTG-DC01` was ready for domain controller promotion

This lab established the controlled preparation point before activating the MRTG Active Directory environment.

---

## Next Lab

[Lab 03: Domain Controller Promotion](../Lab-03-Domain-Controller-Promotion/)

Lab 03 promotes `MRTG-DC01`, creates the `mrtg.local` forest, configures Active Directory-integrated DNS, and validates the core domain services.
