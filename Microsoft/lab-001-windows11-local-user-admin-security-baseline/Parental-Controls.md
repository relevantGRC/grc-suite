# Restricted User Baseline & Content Filtering

**Module:** Endpoint Governance & Identity Management  
**Section:** Restricted User Profile (Child Account)  
**Platform:** Windows 11 Pro  

---

## 1. Objective & Scope
This module demonstrates the configuration and validation of strict endpoint content filtering, application allow-listing, and temporal access controls. While executed using native consumer tools, these configurations simulate the access control policies typically applied to highly restricted enterprise environments (e.g., kiosk machines, frontline worker terminals, or strict contractor isolation).

---

## 2. Identity & Management Scope
* **Target Identity:** Restricted User (Child / Standard User)
* **Management Plane:** Microsoft Family Safety (Native MDM/Policy Enforcer)
* **Administrative Role:** Local Administrator (Configuration & Validation)
* **Policy Scope:** Global enforcement across all target account sessions and activities.

---

## 3. Temporal Access Controls (Screen Time)
**Status:** `Enforced`  
**Scope:** Local Device Level  

| Day | Permitted Duration | Authorization Window |
| :--- | :--- | :--- |
| **Sunday** | 2 Hours | 07:00 AM – 08:00 PM |
| **Monday – Friday** | 1 Hour / Day | 07:00 AM – 08:00 PM |
| **Saturday** | 2 Hours | 07:00 AM – 08:00 PM |

**Operational Behavior:**
* Access is strictly bound to defined temporal windows.
* Upon exhausting the daily duration threshold, the session is forcibly locked, blocking further utilization until the next authorized window.

---

## 4. Content Moderation & Web Filtering

### 4.1 Content Classification Enforcement
* **Control:** Media and Application Age Classification
* **Configured Threshold:** `Level 8`
* **Effect:** Automatically drops access requests to software, media, and web applications exceeding the defined maturity threshold.

### 4.2 DNS & Web Safety Filtering
* **Control:** Web and Search Query Filtering
* **Configured Value:** `Enforced`
* **Details:**
  * Unsanctioned browsers are blocked from executing.
  * Web traffic is restricted to approved browsers (Microsoft Edge) to ensure policy application.
  * SafeSearch parameters are hardcoded and locked for search engines (e.g., Bing).
* **Strategic Purpose:** Mitigates the risk of exposure to malicious domains and inappropriate content through automated web filtering.

---

## 5. Software Procurement Guardrails

### 5.1 Procurement Authorization (Ask to Buy)
* **Control:** Purchase & Installation Approval
* **Configured Value:** `Enforced`
* **Operational Behavior:** Intercepts all requests to acquire or install new software from the Microsoft Store, requiring out-of-band authorization from the Administrative Organizer.
* **Strategic Purpose:** Prevents unauthorized software deployment and shadow IT, maintaining the integrity of the baseline configuration.

---

## 6. Telemetry & Audit Logging

### 6.1 Automated Activity Reporting
* **Control:** Weekly Telemetry Summary
* **Configured Value:** `Enabled`
* **Operational Behavior:** Aggregates session data, application usage, and blocked access attempts into a weekly audit report distributed to the Administrator.

### 6.2 On-Demand Activity Telemetry
* **Control:** Real-time Activity Logging
* **Configured Value:** `Enabled`

---

## 7. Application Control (Allow-listing)

### 7.1 Enforcement Posture: Default Deny
Application access is governed by a strict "Default Deny" posture. Rather than attempting to block known bad software (block-listing), the system explicitly drops all execution requests except for explicitly approved binaries.

### 7.2 Sanctioned Software (Allow-list)
* **Microsoft Edge:** Approved for filtered web telemetry.
* **Roblox Client:** Sanctioned third-party application.

### 7.3 Blocked Software
All binaries and executables outside the allow-list are dynamically blocked. This includes native system applications, productivity suites, and unauthorized execution of the Microsoft Store.

### 7.4 Defense-in-Depth Mitigation
Sanctioned applications are not implicitly trusted. They remain subject to overlapping security controls, including temporal restrictions, web filtering, and continuous telemetry monitoring.

---

## 8. User Acceptance Testing (Validation)
* **Temporal Controls:** Verified session lockouts occur upon reaching the daily limit and outside the authorization window.
* **Web Safety:** Confirmed SafeSearch enforcement and verified that known restricted test domains are actively dropped.
* **Application Control:**
  * Confirmed `msedge.exe` and the sanctioned game client launch successfully under the restricted context.
  * Verified that attempting to launch unapproved native binaries triggers an immediate policy block prompt.
  * Confirmed Microsoft Store execution is restricted, blocking unauthorized provisioning.

---

## 9. Operational Notes
* *Architecture Constraint:* Microsoft Family Safety operates primarily as an implicit allow system that requires manual intervention to achieve a true "Default Deny" state. To achieve strict allow-listing, administrators must systematically explicitly block unapproved applications as they populate in the management plane.

---

## 10. Implementation Status
The Restricted User baseline has been successfully deployed, enforcing granular application allow-listing, web filtering, temporal controls, and procurement authorization.

**Status:** ✅ `Production-Ready`  
**Last Updated:** `2026-01-05`
