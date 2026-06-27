# Validation & Permission Testing

## 1. Validation Protocol
Testing was performed by systematically attempting unauthorized actions across the defined identity tiers (Administrator, Standard User, and Restricted Child) to verify that defined Security Policies were enforced by the OS kernel and User Account Control (UAC) subsystem.

## 2. Test Scenario Matrix

| Scenario | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- |
| **Admin Software Install** | Allowed | Executed with elevated privileges | ✅ Pass |
| **Standard User Install** | Blocked / UAC Prompt | UAC intercepted; credentials required | ✅ Pass |
| **Restricted Child Install** | Blocked / Denied | Execution explicitly denied | ✅ Pass |
| **Child Web Access** | Blocked | Filter triggered; access denied | ✅ Pass |

---

## 3. Security Analysis: Principle of Least Privilege (PoLP)
The validation confirms a robust enforcement of the **Principle of Least Privilege**. By segregating access levels, the environment successfully restricts the system's attack surface:
* **Privilege Boundary Integrity:** The boundary between the Standard User context and Administrative context is rigid; UAC successfully prevents unauthorized escalation of privileges.
* **Restricted Context Isolation:** The Restricted Child profile effectively mitigates risks associated with "Shadow IT" and web-borne threats by enforcing a "Default Deny" posture for software installation and content navigation.
* **Operational Risk Reduction:** These tests validate that the baseline is configured to prevent accidental or malicious system modifications while maintaining standard operational functionality for authorized users.

---

## 4. Audit Trail Validation (Telemetry)
To confirm the system is actively recording authentication telemetry, local security auditing was enabled. Successful and failed logons were verified via the Windows Event Viewer.

### Critical Event Telemetry
* **Event ID 4625 (Logon Failure):** Successfully triggered by attempting an authentication with invalid credentials. This confirms the system captures unauthorized access attempts.
* **Event ID 4624 (Logon Success):** Captured upon verified administrative authentication. This establishes the baseline for legitimate account activity.

### Incident Response (IR) Relevance
The successful capture of these events confirms that the endpoint is capable of generating the telemetry required for forensic investigation. In an enterprise environment, this data would be ingested into a **SIEM (Security Information and Event Management)** platform to support:
1. **Accountability:** Establishing an empirical audit trail of system access.
2. **Detection:** Enabling rapid identification of anomalous authentication patterns (e.g., brute-force spikes).
3. **Timeline Reconstruction:** Providing a verified chronological log of system activity during security incident remediation.
