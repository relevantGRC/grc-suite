# OU Design and GPO Enforcement

![Platform](https://img.shields.io/badge/Platform-Windows%20Server%202022-blue)
![Technology](https://img.shields.io/badge/Technology-Active%20Directory-blue)
![Tooling](https://img.shields.io/badge/Tooling-ADUC%20%26%20GPMC-purple)
![Focus](https://img.shields.io/badge/Focus-OU%20Design%20%26%20GPO%20Enforcement-orange)
![Security](https://img.shields.io/badge/Security-Access%20Control-red)
![Validation](https://img.shields.io/badge/Validation-gpresult%20%26%20RDP%20Access-brightgreen)

---

## Objective

Create a structured Organizational Unit design in the `mrtg.local` domain and validate Group Policy enforcement against a domain-joined workstation.

This lab builds on the operational domain created in Lab 03 by introducing OU-based organization, scoped Group Policy targeting, and group-based Remote Desktop access.

---

## Business Scenario

Monroe Redstone Technology Group requires an Active Directory structure that supports scalable administration, policy enforcement, and access control.

Without a clean OU structure, users and computers become difficult to manage. Group Policy becomes harder to target, administrative responsibilities are less clear, and troubleshooting takes longer.

This lab addresses the need to:

- Organize users and computers into logical OUs
- Separate workstation and server computer objects
- Prepare the directory for scalable Group Policy targeting
- Apply workstation and user security settings
- Validate computer-side and user-side policy application
- Confirm that unauthorized Remote Desktop access is denied
- Grant approved access through security group membership
- Validate successful access after remediation

---

## Lab Summary

In this lab, I created the foundational MRTG Organizational Unit structure in Active Directory.

The structure separated users, computers, groups, administrative accounts, and service accounts. Department OUs were created for IT, Security, HR, Finance, Operations, Engineering, and Executives. Computer objects were separated into Workstations and Servers OUs.

The `MRTG-Workstation-Baseline` GPO was linked to the Workstations OU, and the `MRTG-User-Session-Lock` policy was configured for user session protection.

Policy application was validated with `gpresult`. Remote Desktop access was initially denied because the test user lacked the required authorization. Access was then granted through the `GG_Remote_Desktop_Users` security group and validated through a successful domain sign-in.

---

## Environment

| Component | Details |
|---|---|
| Domain | `mrtg.local` |
| Domain Controller | `MRTG-DC01` |
| Client Workstation | `MRTG-CLIENT-01` |
| Test User | `john.smith` |
| Access Group | `GG_Remote_Desktop_Users` |
| Workstation GPO | `MRTG-Workstation-Baseline` |
| User GPO | `MRTG-User-Session-Lock` |
| Tools | Active Directory Users and Computers, Group Policy Management, and `gpresult` |
| Virtualization Platform | Hyper-V |
| Organization | Monroe Redstone Technology Group |

---

## Prerequisites

- Operational `mrtg.local` Active Directory domain
- `MRTG-DC01` functioning as the domain controller and DNS server
- `MRTG-CLIENT-01` joined to the domain
- Test user account `john.smith`
- Administrative access to Active Directory and Group Policy Management
- Network connectivity between the domain controller and workstation

---

## Scope

### Included

- MRTG OU structure creation
- Department-based user OU creation
- Computer OU segmentation
- Workstations and Servers OU creation
- Workstation computer object placement
- Workstation baseline GPO linking
- GPO scope and security filtering review
- User session lock policy configuration
- Computer policy validation with `gpresult`
- User policy validation with `gpresult`
- Remote Desktop denied-access testing
- Group-based Remote Desktop access remediation
- Successful domain user sign-in validation

### Not Included

- Password policy hardening
- Account lockout policy hardening
- Fine-grained password policies
- NTFS and share permissions
- Advanced administrative delegation
- SIEM integration
- Additional domain controller deployment
- Local administrator password management

---

## OU Architecture

The `_MRTG` OU provides the administrative structure for the lab environment.

```text
mrtg.local
`-- _MRTG
    |-- Users
    |   |-- IT
    |   |-- Security
    |   |-- HR
    |   |-- Finance
    |   |-- Operations
    |   |-- Engineering
    |   `-- Executives
    |-- Computers
    |   |-- Workstations
    |   |   `-- MRTG-CLIENT-01
    |   `-- Servers
    |-- Groups
    |-- Admin Accounts
    `-- Service Accounts
```

This structure supports:

- Logical organization of directory objects
- Targeted Group Policy application
- Separation of users and computers
- Separation of workstations and servers
- Department-based identity administration
- Future delegation and lifecycle workflows
- Scalable access-control design

---

## Group Policy Design

### Workstation Policy

The workstation baseline was linked to the Workstations OU.

```text
_MRTG
`-- Computers
    `-- Workstations
        |-- MRTG-CLIENT-01
        `-- MRTG-Workstation-Baseline
```

| GPO | Target | Purpose |
|---|---|---|
| `MRTG-Workstation-Baseline` | Workstations OU | Applies baseline workstation settings |
| `MRTG-User-Session-Lock` | Applicable user OU scope | Enforces password protection for user sessions |

The workstation GPO used the default `Authenticated Users` security filtering.

For computer-side settings, the workstation computer account must have permission to read and apply the GPO.

---

## Access Control Model

Remote Desktop access was managed through security group membership.

| Condition | Result |
|---|---|
| User is not in the approved access group | Remote Desktop sign-in is denied |
| User is added to the approved access group | Access becomes authorized |
| User starts a new authentication session | Updated group membership is included in the access token |
| User signs in successfully | Access control is validated |

Security group:

```text
GG_Remote_Desktop_Users
```

Test user:

```text
john.smith
```

This follows a core IAM principle: assign access through approved groups instead of granting permissions directly to individual users.

---

## Implementation and Validation

### 1. Created the MRTG User OU Structure

The `_MRTG` structure was created and reviewed in Active Directory Users and Computers.

Department OUs included:

- IT
- Security
- HR
- Finance
- Operations
- Engineering
- Executives

![OU structure](screenshots/lab-04-01-ou-structure.png)

This established a logical structure for future identity lifecycle and access-management workflows.

---

### 2. Created the Computer OU Structure

The Computers OU was divided into separate endpoint categories.

```text
Workstations
Servers
```

![Computer OU structure](screenshots/lab-04-02-computer-ou-structure.png)

This separation allows workstations and servers to receive different policies and administrative controls.

---

### 3. Placed the Workstation in the Correct OU

The `MRTG-CLIENT-01` computer object was placed in the Workstations OU.

![Workstation OU membership](screenshots/lab-04-03-workstation-ou-membership.png)

Correct OU placement ensured that workstation-targeted Group Policy settings could apply to the computer.

---

### 4. Configured the User Session Lock Policy

The `MRTG-User-Session-Lock` GPO was configured to require password protection for the screen saver.

Configured setting:

```text
Password protect the screen saver = Enabled
```

![User session lock GPO setting](screenshots/lab-04-04-user-session-lock-gpo-setting.png)

This reduces the risk of an unattended authenticated session remaining accessible.

---

### 5. Linked the Workstation Baseline GPO

The `MRTG-Workstation-Baseline` GPO was linked to the Workstations OU.

![Workstation baseline GPO linked](screenshots/lab-04-05-workstation-baseline-gpo-linked.png)

This targeted the workstation baseline according to the computer object's OU placement.

---

### 6. Reviewed GPO Scope and Security Filtering

The scope of `MRTG-Workstation-Baseline` was reviewed in Group Policy Management.

Security filtering:

```text
Authenticated Users
```

![GPO scope and security filtering](screenshots/lab-04-06-gpo-scope-and-security-filtering.png)

This confirmed that the GPO was linked to the intended OU and had valid security filtering.

---

### 7. Validated Computer Policy Application

Computer-side Group Policy application was validated on `MRTG-CLIENT-01`.

Command used:

```cmd
gpresult /r
```

Applied GPOs included:

```text
MRTG-Workstation-Baseline
Default Domain Policy
```

![Computer policy applied](screenshots/lab-04-07-computer-policy-applied.png)

This confirmed that the workstation received the intended computer policy.

---

### 8. Validated User Policy Application

User-side Group Policy application was reviewed for:

```text
MRTG\john.smith
```

The result showed that `MRTG-User-Session-Lock` applied to the user session.

![User policy applied](screenshots/lab-04-08-user-policy-applied.png)

This confirmed that the user-targeted policy was within the correct scope and applied successfully.

---

### 9. Confirmed Remote Desktop Access Was Denied

A Remote Desktop sign-in was attempted using the `john.smith` account.

The sign-in failed because the user did not have the required authorization to sign in through Remote Desktop Services.

![RDP access denied](screenshots/lab-04-09-rdp-access-denied.png)

This confirmed that access was denied by default when the required entitlement was absent.

---

### 10. Updated Remote Desktop Group Membership

`john.smith` was added to the `GG_Remote_Desktop_Users` security group.

![Remote Desktop Users group membership](screenshots/lab-04-10-remote-desktop-users-group-membership.png)

This remediated the access issue through group-based authorization rather than a direct user permission.

A new authentication session was required for the updated group membership to appear in the user's access token.

---

### 11. Validated the Successful Domain Sign-In

After the group membership update, the user successfully signed in.

Command used:

```cmd
whoami
```

Validated result:

```text
mrtg\john.smith
```

![Successful domain user login](screenshots/lab-04-11-successful-domain-user-login.png)

This confirmed that the group-based access change produced the intended result.

---

## Security and IAM Relevance

This lab demonstrates how directory structure, policy scope, and security groups work together to support identity governance.

Organizational Units provide logical organization and Group Policy scope. Security groups represent access entitlements. Validation tools confirm that the intended control reached the correct user or computer.

This lab supports:

- OU-based policy targeting
- Department-based identity organization
- Workstation and server separation
- Centralized user session protection
- Group-based access control
- Deny-by-default behavior
- Least-privilege access assignment
- Native policy validation
- Evidence-based access remediation

Organizational Units are useful for policy application and administrative delegation, but they are not security boundaries by themselves.

---

## Risks Addressed

This lab reduces the risk of:

- Unstructured directory growth
- Incorrect Group Policy targeting
- Workstations and servers receiving the same controls
- Manual endpoint configuration drift
- Direct user-level permission assignments
- Unvalidated access changes
- Inconsistent access remediation
- Weak evidence during troubleshooting or access reviews

---

## Control Mapping

| Control Area | Lab Contribution |
|---|---|
| Directory Organization | Creates the structured MRTG OU hierarchy |
| Policy Targeting | Links workstation policy to the Workstations OU |
| Endpoint Governance | Applies and validates the workstation baseline |
| Session Protection | Requires password protection for user sessions |
| Access Control | Manages Remote Desktop authorization through group membership |
| Least Privilege | Confirms denial before approved access is granted |
| Operational Validation | Uses `gpresult` and user sign-in testing |
| Audit Readiness | Captures OU, GPO, membership, denial, and success evidence |

---

## Validation Results

| Validation Item | Result |
|---|---|
| Department user OUs created | Passed |
| Workstations OU created | Passed |
| Servers OU created | Passed |
| `MRTG-CLIENT-01` placed in Workstations OU | Passed |
| User session lock policy configured | Passed |
| `MRTG-Workstation-Baseline` linked to Workstations OU | Passed |
| GPO scope and security filtering reviewed | Passed |
| Computer-side policy applied to `MRTG-CLIENT-01` | Passed |
| User-side policy applied to `john.smith` | Passed |
| Remote Desktop access denied before authorization | Passed |
| `john.smith` added to `GG_Remote_Desktop_Users` | Passed |
| Successful domain user sign-in validated | Passed |

---

## Evidence Collected

| Evidence | File |
|---|---|
| OU structure | `screenshots/lab-04-01-ou-structure.png` |
| Computer OU structure | `screenshots/lab-04-02-computer-ou-structure.png` |
| Workstation OU membership | `screenshots/lab-04-03-workstation-ou-membership.png` |
| User session lock GPO setting | `screenshots/lab-04-04-user-session-lock-gpo-setting.png` |
| Workstation baseline GPO link | `screenshots/lab-04-05-workstation-baseline-gpo-linked.png` |
| GPO scope and security filtering | `screenshots/lab-04-06-gpo-scope-and-security-filtering.png` |
| Computer policy application | `screenshots/lab-04-07-computer-policy-applied.png` |
| User policy application | `screenshots/lab-04-08-user-policy-applied.png` |
| Remote Desktop access denial | `screenshots/lab-04-09-rdp-access-denied.png` |
| Remote Desktop group membership | `screenshots/lab-04-10-remote-desktop-users-group-membership.png` |
| Successful domain user sign-in | `screenshots/lab-04-11-successful-domain-user-login.png` |

---

## What I Would Improve in Production

In a production environment, I would:

- Document and approve an enterprise OU design standard
- Separate production, testing, server, workstation, and administrative systems
- Use organization-approved naming standards
- Create focused GPOs with clearly defined purposes
- Test GPO changes in pilot OUs before broader deployment
- Review GPO inheritance, enforcement, and blocked inheritance
- Minimize broad security filtering
- Document the mapping between access groups and endpoint permissions
- Require an approved access request before adding users to remote-access groups
- Review Remote Desktop access regularly
- Monitor changes to privileged and remote-access groups
- Use time-bound access where supported
- Use formal change management for GPO modifications
- Maintain rollback and recovery procedures for policy changes

---

## Lessons Learned

This lab reinforced that Active Directory governance begins with structure.

Organizational Units are not simply folders. They provide scope for policy application and administrative delegation. Security groups provide the authorization layer for access entitlements.

The main takeaway is that both policy and access changes require validation. Group Policy should be confirmed with tools such as `gpresult`, while access should be tested from the user's perspective.

The Remote Desktop test also demonstrated deny-by-default behavior: access failed until the user received the approved group membership.

---

## Outcome

Lab 04 successfully established the foundational OU design, Group Policy enforcement, and group-based access control for the MRTG environment.

The lab confirmed that:

- The MRTG OU hierarchy was created
- Department-based user OUs were established
- Workstations and Servers OUs were created
- `MRTG-CLIENT-01` was placed in the Workstations OU
- The workstation baseline GPO was linked
- The user session lock policy was configured
- Computer-side policy applied successfully
- User-side policy applied successfully
- Remote Desktop access was denied before authorization
- Access was granted through `GG_Remote_Desktop_Users`
- The domain user sign-in succeeded after remediation

The environment now has a structured foundation for identity lifecycle management, access control, delegation, and policy governance.

---

## Next Lab

[Lab 05: Identity Lifecycle Management](../Lab-05-Identity-Lifecycle-Management/)

Lab 05 implements Joiner, Mover, and Leaver workflows for managing user identities throughout the MRTG environment.
