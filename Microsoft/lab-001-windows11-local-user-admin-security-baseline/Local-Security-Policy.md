#  Local Security Policy Configuration Baseline

## 1. Objective & Scope
The objective of this configuration layer is to harden the local authentication subsystem against credential guessing, automated dictionary attacks, and local brute-force exploits. This baseline establishes strict mathematical boundaries for local password metrics and account lockout behaviors using the Local Security Policy snap-in (`secpol.msc`).

---

## 2. Hardening Configurations

All controls detailed below are applied under the following policy path:  
`Computer Configuration \ Windows Settings \ Security Settings \ Account Policies \`

### Password Policy
*Path: `...\Account Policies \ Password Policy \`*

| Policy Setting | Baseline Value | Strategic Rationale / Security Control |
| :--- | :--- | :--- |
| **Enforce password history** | `10 passwords remembered` | Prevents token reuse cycle; mitigates the risk of a user cycling through minor variations of a previously compromised credential. |
| **Maximum password age** | `999 days` | Balancing cryptographic lifespans with user experience. Minimizes forced frequent changes that lead to poor password hygiene (e.g., writing down credentials). |
| **Minimum password length** | `12 characters` | Significantly increases baseline character entropy, rendering local offline brute-force or rainbow table attacks computationally expensive. |
| **Password must meet complexity requirements** | `Enabled` | Enforces character variance (uppercase, lowercase, digits, and special characters) to disrupt simple dictionary-based attacks. |
| **Store passwords using reversible encryption** | `Disabled` | Ensures credentials are securely hashed inside the Security Accounts Manager (SAM) database, preventing cleartext extraction if the SAM file is leaked. |

###  Account Lockout Policy
*Path: `...\Account Policies \ Account Lockout Policy \`*

| Policy Setting | Baseline Value | Strategic Rationale / Security Control |
| :--- | :--- | :--- |
| **Account lockout duration** | `15 minutes` | Imposes a temporary operational freeze on a target account, degrading an attacker's ability to run high-speed automated brute-force scripts. |
| **Account lockout threshold** | `5 invalid attempts` | Striks a calculated balance between user friction (accidental typos) and rapid automated credential-stuffing mitigation. |
| **Reset account lockout counter after** | `15 minutes` | Defines the rolling window inside which failed authentication attempts are tracked sequentially before resetting the threshold counter. |
| **Allow administrator account lockout** | `Disabled` | Prevents malicious external actors from intentionally tripping the lockout threshold to cause an administrative Denial of Service (DoS). |

---

## 3. Threat Mitigation Rationale

* **Credential Entropy Enforcement:** By combining a 12-character minimum length with mandatory complexity flags, the total combinations of the keyspace expand exponentially. This disrupts automated cracking patterns.
* **Rate-Limiting via Lockout:** Without a lockout threshold, local endpoints can process thousands of authentication attempts per minute. Forcing a 15-minute operational cooldown after 5 failures breaks the momentum of online brute-force scripts.
* **DoS Protections:** Disabling the administrator account lockout ensures that even during a sustained credential-stuffing attack on the endpoint, legitimate administrators maintain system access via physical console or secondary management vectors to initiate incident response protocols.

---

## 4. Verification & Audit Trail

The final state of these policy modifications was verified locally via `secpol.msc` and cross-referenced against the local system state.

### Evidence Artifact Repository
* **Password Baseline Mapping:** Verified configuration visible in `evidence/password-policy.png`.
* **Lockout Baseline Mapping:** Verified threshold enforcement visible in `evidence/account-lockout-policy.png`.
