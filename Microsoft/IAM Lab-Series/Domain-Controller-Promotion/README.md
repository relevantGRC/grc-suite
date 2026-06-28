# Domain Controller Promotion and Identity Activation

![Platform](https://img.shields.io/badge/Platform-Windows%20Server%202022-blue)
![Technology](https://img.shields.io/badge/Technology-Active%20Directory-blue)
![Role](https://img.shields.io/badge/Role-Domain%20Controller-critical)
![Authentication](https://img.shields.io/badge/Authentication-Kerberos-brightgreen)
![Focus](https://img.shields.io/badge/Focus-Identity%20Activation-orange)
![Validation](https://img.shields.io/badge/Validation-Domain%20Controller%20Operational-lightgrey)

---

## Objective

Promote `MRTG-DC01` as the first domain controller in the `mrtg.local` Active Directory forest.

This lab activates the identity foundation prepared in Lab 02 by creating the new forest, validating Active Directory Domain Services, confirming DNS registration, verifying the domain context, and establishing a controlled post-promotion lab recovery point.

---

## Business Scenario

Monroe Redstone Technology Group requires a centralized identity authority for authentication, authorization, policy enforcement, and IAM governance.

Before users, groups, policies, access controls, and monitoring can be implemented, the organization needs an operational Active Directory domain.

This lab addresses the need to:

- Promote the prepared server as a domain controller
- Create the `mrtg.local` Active Directory forest
- Establish centralized domain authentication
- Validate Active Directory-integrated DNS zones
- Confirm domain controller service records
- Verify network and DNS configuration
- Validate the domain authentication context
- Preserve a controlled post-promotion lab baseline

---

## Lab Summary

In this lab, I promoted `MRTG-DC01` as the first domain controller for the new `mrtg.local` forest.

After promotion, I confirmed that the domain was visible in Active Directory Users and Computers, validated the Active Directory-integrated DNS zones, reviewed `_msdcs` service records, verified the server IP and DNS configuration, and confirmed the domain context from the command line.

A Hyper-V checkpoint was created as a temporary lab recovery point after the promotion and validation steps were completed.

This lab transitioned the MRTG environment from a prepared Windows Server into an operational identity platform.

---

## Environment

| Component | Details |
|---|---|
| Domain | `mrtg.local` |
| Domain Controller | `MRTG-DC01` |
| Operating System | Windows Server 2022 |
| Directory Service | Active Directory Domain Services |
| DNS | Active Directory-integrated DNS |
| Authentication Service | Kerberos |
| IPv4 Address | `192.168.10.10` |
| Subnet Mask | `255.255.255.0` |
| DNS Server | `192.168.10.10` |
| Virtualization Platform | Hyper-V |
| Organization | Monroe Redstone Technology Group |

---

## Prerequisites

- Windows Server 2022 installed on `MRTG-DC01`
- Active Directory Domain Services role installed
- AD DS management tools installed
- Static IPv4 configuration assigned
- Server configured to use the planned internal DNS service
- New forest deployment prepared for `mrtg.local`
- AD DS prerequisite checks completed successfully
- Administrative access to `MRTG-DC01`

---

## Scope

### Included

- New forest deployment
- Domain controller promotion
- `mrtg.local` forest creation
- Active Directory Users and Computers validation
- Active Directory-integrated DNS zone validation
- `_msdcs` service record validation
- Forward lookup zone validation
- Domain controller IP and DNS validation
- Domain context validation
- Domain name resolution validation
- Post-promotion Hyper-V checkpoint creation

### Not Included

- Organizational Unit design
- User and group provisioning
- Group Policy enforcement
- Domain-joined client configuration
- Additional domain controller deployment
- DHCP configuration
- Centralized logging
- Fine-grained password policies
- Production backup configuration

---

## Architecture

This lab establishes `MRTG-DC01` as the first domain controller in the MRTG environment.

```text
mrtg.local
`-- MRTG-DC01
    |-- Active Directory Domain Services
    |-- Active Directory-integrated DNS
    |-- Kerberos authentication service
    `-- Domain controller service registration
```

`MRTG-DC01` becomes the authoritative identity system for the lab domain.

```text
MRTG-DC01
`-- mrtg.local
    |-- Authentication
    |-- Authorization
    |-- Directory services
    |-- DNS service discovery
    `-- Future Group Policy processing
```

---

## Identity Activation Model

The initial identity deployment was divided into controlled phases.

| Phase | Lab | Purpose |
|---|---|---|
| Infrastructure | Lab 01 | Establish the virtual environment |
| Preparation | Lab 02 | Install AD DS and validate promotion readiness |
| Activation | Lab 03 | Promote the server and create `mrtg.local` |
| Governance Foundation | Lab 04 | Build the OU structure and begin policy enforcement |

This separation makes the identity deployment easier to document, validate, and troubleshoot.

---

## Domain Controller Services

After promotion, `MRTG-DC01` provides the following services:

| Service | Purpose |
|---|---|
| Active Directory Domain Services | Stores and manages domain identities and directory objects |
| Active Directory-integrated DNS | Supports domain name resolution and service discovery |
| Kerberos | Provides the primary domain authentication protocol |
| DNS Service Records | Allow clients and services to locate domain controllers |
| Directory Management | Supports future administration of users, groups, computers, OUs, and policies |

---

## Implementation and Validation

### 1. Configured the New Forest Deployment

The Active Directory Domain Services Configuration Wizard was used to configure a new forest.

Selected deployment operation:

```text
Add a new forest
```

Root domain name:

```text
mrtg.local
```

![New forest deployment configuration](screenshots/lab-03-01-new-forest-mrtg-local.png)

This initiated the identity activation process for the MRTG environment.

---

### 2. Promoted MRTG-DC01

The promotion process installed the required domain controller components, created the new forest, and restarted the server.

After the restart, `MRTG-DC01` operated as the first domain controller for `mrtg.local`.

---

### 3. Confirmed the Active Directory Domain

Active Directory Users and Computers was opened to confirm that the `mrtg.local` domain existed.

![Active Directory domain created](screenshots/lab-03-02-active-directory-domain-created.png)

This confirmed that the forest and domain were created successfully.

---

### 4. Validated DNS Service Records

DNS Manager was used to review the `_msdcs.mrtg.local` zone.

The zone contained the service location records used by systems and services to discover Active Directory domain controllers.

![DNS msdcs service records](screenshots/lab-03-03-dns-msdcs-service-records.png)

This confirmed that domain controller service registration was present.

---

### 5. Validated Forward Lookup Zones

DNS Manager was used to review the forward lookup zones.

Confirmed zones included:

```text
_msdcs.mrtg.local
mrtg.local
```

![DNS forward lookup zones](screenshots/lab-03-04-dns-forward-lookup-zones.png)

This confirmed that the Active Directory-integrated DNS zones were available.

---

### 6. Validated the Network Configuration

The following command was used to review the complete network configuration:

```cmd
ipconfig /all
```

Validated values included:

| Setting | Value |
|---|---|
| Host Name | `MRTG-DC01` |
| IPv4 Address | `192.168.10.10` |
| Subnet Mask | `255.255.255.0` |
| DNS Server | `192.168.10.10` |

![Domain controller IP configuration](screenshots/lab-03-05-domain-controller-ipconfig.png)

This confirmed that the domain controller used its own DNS service for Active Directory name resolution.

---

### 7. Validated the Domain Context and Name Resolution

The domain context and domain name resolution were reviewed from the command line.

Commands used:

```cmd
echo %USERDOMAIN%
whoami
ping mrtg.local
```

Validated results:

```text
USERDOMAIN = MRTG
whoami = mrtg\administrator
mrtg.local resolved to 192.168.10.10
```

![Domain authentication validation](screenshots/lab-03-06-domain-authentication-validation.png)

These results confirmed that the administrator session was operating in the MRTG domain context and that the domain name resolved successfully.

This evidence confirms the domain context but does not independently prove that a Kerberos ticket was used. Kerberos ticket validation would require tools such as `klist`.

---

### 8. Created a Post-Promotion Lab Checkpoint

A Hyper-V checkpoint was created after the promotion and validation steps were completed.

Checkpoint name:

```text
Post-DC-Promotion
```

![Post-DC promotion checkpoint](screenshots/lab-03-07-post-dc-promotion-checkpoint.png)

The checkpoint provided a temporary recovery point for the controlled lab environment. It was not treated as a replacement for a supported Active Directory backup.

---

## Security and IAM Relevance

This lab established the first Tier 0-equivalent identity asset in the MRTG environment.

A domain controller is a critical security system because it controls authentication, authorization, directory information, and policy processing for the domain.

This lab supports:

- Centralized identity and authentication services
- Active Directory-integrated DNS service discovery
- Kerberos authentication capability
- Controlled identity infrastructure activation
- Privileged infrastructure awareness
- Evidence-based deployment validation
- Documented network and DNS configuration

Compromise of a domain controller can lead to compromise of the entire identity domain. Access to `MRTG-DC01` must therefore be tightly restricted and monitored.

---

## Risks Addressed

This lab reduces the risk of:

- Failed or incomplete forest creation
- Missing Active Directory-integrated DNS zones
- Missing domain controller service records
- Incorrect DNS configuration
- Failed domain name resolution
- Undocumented identity infrastructure deployment
- Incomplete post-promotion validation
- Weak awareness of domain controller security sensitivity

---

## Control Mapping

| Control Area | Lab Contribution |
|---|---|
| Identity Activation | Promotes `MRTG-DC01` as the first domain controller |
| Centralized Authentication | Creates the `mrtg.local` domain and Kerberos authentication service |
| DNS Service Discovery | Validates `_msdcs` records and forward lookup zones |
| Network Validation | Confirms the static IP and DNS configuration |
| Domain Validation | Confirms the domain context and name resolution |
| Privileged Infrastructure | Establishes the first Tier 0-equivalent identity asset |
| Audit Readiness | Captures evidence of domain creation and service validation |
| Lab Recoverability | Creates a temporary post-promotion checkpoint |

---

## Validation Results

| Validation Item | Result |
|---|---|
| New forest deployment configured | Passed |
| `mrtg.local` entered as the root domain | Passed |
| `MRTG-DC01` promoted as a domain controller | Passed |
| `mrtg.local` visible in Active Directory Users and Computers | Passed |
| `_msdcs.mrtg.local` DNS zone present | Passed |
| `mrtg.local` DNS zone present | Passed |
| Domain controller service records present | Passed |
| Static IPv4 configuration validated | Passed |
| DNS self-reference validated | Passed |
| Domain context confirmed with `%USERDOMAIN%` | Passed |
| Domain identity confirmed with `whoami` | Passed |
| `mrtg.local` resolved to `192.168.10.10` | Passed |
| Post-promotion lab checkpoint created | Passed |

---

## Evidence Collected

| Evidence | File |
|---|---|
| New forest deployment configuration | `screenshots/lab-03-01-new-forest-mrtg-local.png` |
| Active Directory domain creation | `screenshots/lab-03-02-active-directory-domain-created.png` |
| DNS `_msdcs` service records | `screenshots/lab-03-03-dns-msdcs-service-records.png` |
| DNS forward lookup zones | `screenshots/lab-03-04-dns-forward-lookup-zones.png` |
| Domain controller IP configuration | `screenshots/lab-03-05-domain-controller-ipconfig.png` |
| Domain context and name resolution | `screenshots/lab-03-06-domain-authentication-validation.png` |
| Post-promotion lab checkpoint | `screenshots/lab-03-07-post-dc-promotion-checkpoint.png` |

---

## What I Would Improve in Production

In a production environment, I would:

- Use a namespace based on a registered organizational domain instead of `.local`
- Follow a formal domain controller promotion checklist
- Validate the DNS architecture before promotion
- Confirm domain and forest functional-level requirements
- Document privileged administrative ownership
- Restrict interactive sign-in to approved administrators
- Configure supported System State backups immediately
- Avoid treating hypervisor checkpoints as domain controller backups
- Review Windows Time service configuration
- Apply an approved domain controller security baseline
- Enable centralized security monitoring
- Validate replication and domain health
- Create a formal post-promotion health report
- Avoid installing unnecessary roles or applications
- Use formal change management for forest creation

---

## Lessons Learned

This lab reinforced that domain controller promotion is the point at which the identity platform becomes operational.

Installing AD DS prepares the server, but promotion creates the forest, activates directory services, registers DNS records, and enables domain authentication capabilities.

The primary takeaway is that a successful promotion wizard is not enough. Domain health must be reviewed through directory visibility, DNS zones, service records, network configuration, domain context, and name resolution.

---

## Outcome

Lab 03 successfully promoted `MRTG-DC01` as the first domain controller in the `mrtg.local` Active Directory forest.

The lab confirmed that:

- A new forest was created for `mrtg.local`
- `MRTG-DC01` became the first domain controller
- The domain was visible in Active Directory Users and Computers
- Active Directory-integrated DNS zones were created
- `_msdcs` service records were present
- The server used `192.168.10.10` for DNS
- The MRTG domain context was confirmed
- `mrtg.local` resolved successfully
- A controlled post-promotion lab checkpoint was created

The MRTG environment now has an operational Active Directory identity foundation.

---

## Next Lab

[Lab 04: OU Design and GPO Enforcement](../Lab-04-OU-Design-and-GPO-Enforcement/)

Lab 04 creates a structured Organizational Unit design and applies Group Policy controls for centralized identity and endpoint governance.
