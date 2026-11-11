"""
iam_audit.py
Audits the AWS root account and all IAM users for MFA and access key compliance.
Account-level checks:
    - Root account MFA status (enabled/disabled)
    - Root account MFA device type (hardware/virtual; FedRAMP High prefers hardware)
    - Password policy compliance (length, complexity, rotation, reuse prevention)
Per-user checks:
    1. Console Access - Does the user have a password to log into AWS Console?
    2. MFA Status - If they have console access, is MFA enabled?
    3. Access Key Age - Are any active access keys older than 90 days?
    4. User Activity - Has the user been inactive for 90+ days?
Output:
    [PASS] - Console user with MFA enabled / Access key within rotation period
    [FAIL] - Console user WITHOUT MFA / Active access key over 90 days old
    [INFO] - No console access (programmatic only, MFA not required)
    [N/A]  - No access keys exist for the user
Alerting:
    If IAM_AUDIT_SNS_TOPIC_ARN is set, a summary of non-compliant findings
    is published to the given SNS topic at the end of the audit run.
Usage:
    python iam_audit.py [--output-dir PATH] [--format {csv,json,both}] [--quiet]
    python iam_audit.py --help
Requirements:
    - boto3 installed (pip install boto3)
    - AWS credentials configured (aws configure)
"""

# Import associated AWS module for script.
import argparse
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from datetime import datetime, timezone
import csv
import json
import os


def export_to_csv(audit_results, root_info, policy_info, timestamp, output_dir='.'):
    """
    Export audit results to CSV file with timestamp in filename.

    Account-level findings appear as special rows before the per-user rows:
        <ROOT>                    - Root MFA status with mfa_type populated
        <POLICY_OVERALL>          - Aggregate pass/fail for the password policy
        <POLICY_*>                - One row per individual policy check,
                                    with 'details' field holding
                                    "expected X, actual Y"

    Per-user rows leave mfa_type and details blank since those fields are
    account-level, not user-level.

    Args:
        audit_results: List of dictionaries containing user audit data
        root_info: Dictionary from audit_root_account() with root MFA details
        policy_info: Dictionary from audit_password_policy() with password
                     policy configured flag, status, and per-check list
        timestamp: ISO 8601 timestamp string for filename
        output_dir: Directory to write the CSV into (default: current dir).
                    Created if missing. Idempotent via exist_ok=True.

    Returns:
        filename: Full path to the created CSV file
    """
    # exist_ok=True makes the call idempotent: no error if the directory
    # already exists, mkdir -p semantics for nested paths like "reports/2026".
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"iam_audit_{timestamp}.csv")

    fieldnames = [
        'username', 'has_console_access', 'mfa_enabled', 'mfa_type',
        'compliance_status', 'access_key_count', 'oldest_key_age_days',
        'key_compliance_status', 'last_activity_date', 'days_inactive',
        'activity_status', 'details'
    ]

    # Root has no access keys tracked here, no concept of console-vs-
    # programmatic (console always available), and no activity timestamp
    # accessible via IAM APIs. Non-applicable fields are empty strings so
    # downstream readers (pandas, Excel) parse them cleanly.
    root_row = {
        'username': '<ROOT>',
        'has_console_access': True,
        'mfa_enabled': root_info['root_mfa_enabled'],
        'mfa_type': root_info['root_mfa_type'],
        'compliance_status': root_info['root_mfa_status'],
        'access_key_count': '',
        'oldest_key_age_days': '',
        'key_compliance_status': 'N/A',
        'last_activity_date': '',
        'days_inactive': '',
        'activity_status': 'N/A',
        'details': ''
    }

    # Build password policy rows. Overall summary first, then one row per
    # individual check so auditors can see which specific rules failed.
    policy_rows = []
    checks = policy_info['password_policy_checks']

    if policy_info['password_policy_configured']:
        passed = sum(1 for c in checks if c['status'] == 'PASS')
        overall_details = f"{passed} of {len(checks)} checks passed"
    else:
        overall_details = 'No password policy configured on the account'

    policy_rows.append({
        'username': '<POLICY_OVERALL>',
        'has_console_access': '',
        'mfa_enabled': '',
        'mfa_type': '',
        'compliance_status': policy_info['password_policy_status'],
        'access_key_count': '',
        'oldest_key_age_days': '',
        'key_compliance_status': 'N/A',
        'last_activity_date': '',
        'days_inactive': '',
        'activity_status': 'N/A',
        'details': overall_details
    })

    for c in checks:
        policy_rows.append({
            'username': f"<POLICY_{c['name']}>",
            'has_console_access': '',
            'mfa_enabled': '',
            'mfa_type': '',
            'compliance_status': c['status'],
            'access_key_count': '',
            'oldest_key_age_days': '',
            'key_compliance_status': 'N/A',
            'last_activity_date': '',
            'days_inactive': '',
            'activity_status': 'N/A',
            'details': f"expected {c['expected']}, actual {c['actual']}"
        })

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(root_row)
        writer.writerows(policy_rows)
        writer.writerows(audit_results)

    return filename


def export_to_json(audit_results, metadata, timestamp, output_dir='.'):
    """
    Export audit results to JSON file with metadata.

    Args:
        audit_results: List of dictionaries containing user audit data
        metadata: Dictionary containing audit metadata (timestamps, counts, rates)
        timestamp: ISO 8601 timestamp string for filename
        output_dir: Directory to write the JSON into (default: current dir).
                    Created if missing.

    Returns:
        filename: Full path to the created JSON file
    """
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"iam_audit_{timestamp}.json")

    report = {
        'metadata': {
            'audit_start': metadata['start_time'],
            'audit_end': metadata['end_time'],
            'elapsed_seconds': metadata['elapsed_seconds'],
            'total_users': metadata['total_users'],
            'compliance_rate': metadata['compliance_rate'],
            'key_compliance_rate': metadata['key_compliance_rate'],
            'activity_compliance_rate': metadata['activity_compliance_rate'],
            'inactive_users': metadata['inactive_users'],
            'root_mfa_enabled': metadata['root_mfa_enabled'],
            'root_mfa_type': metadata['root_mfa_type'],
            'root_mfa_status': metadata['root_mfa_status'],
            'password_policy': {
                'configured': metadata['password_policy_configured'],
                'status': metadata['password_policy_status'],
                'checks': metadata['password_policy_checks']
            }
        },
        'findings': audit_results
    }

    with open(filename, 'w') as jsonfile:
        json.dump(report, jsonfile, indent=4)

    return filename


def audit_root_account(iam):
    """
    Audit the AWS root account for MFA status and device type.

    The root account is the highest-privilege identity in an AWS account
    and cannot be replaced by an IAM user. FedRAMP High and CJIS v6.0
    5.6.2.2 require MFA on privileged accounts; FedRAMP High further
    recommends a hardware MFA device for root specifically.

    get_account_summary() returns a SummaryMap of integer flags —
    AccountMFAEnabled is 0 or 1. To distinguish hardware from virtual MFA
    when enabled, we cross-reference against list_virtual_mfa_devices().
    The root account has no UserName (it is not an IAM user), so it is
    identified by its User.Arn ending in ':root'. If AccountMFAEnabled=1
    and the root device is NOT in the virtual list, the device is
    physical hardware.

    Args:
        iam: boto3 IAM client

    Returns:
        dict with keys:
            root_mfa_enabled (bool)
            root_mfa_type (str): 'hardware', 'virtual', or 'none'
            root_mfa_status (str): 'PASS' or 'FAIL'
    """
    # SummaryMap uses integer flags (0/1). dict.get() defaults to 0 if the
    # key ever disappears in a future API change (PCC3e Ch. 6).
    summary = iam.get_account_summary()
    mfa_enabled = summary['SummaryMap'].get('AccountMFAEnabled', 0) == 1

    mfa_type = 'none'
    if mfa_enabled:
        # Default to hardware; override to virtual only if we find a
        # virtual MFA device assigned to the root ARN. Paginate because
        # accounts may have many virtual MFA devices assigned to IAM users.
        mfa_type = 'hardware'
        vmfa_paginator = iam.get_paginator('list_virtual_mfa_devices')
        # Early-exit pattern: break both loops once we know root is virtual.
        found_root_virtual = False
        for page in vmfa_paginator.paginate(AssignmentStatus='Assigned'):
            for device in page['VirtualMFADevices']:
                # .get() chains safely through nested dicts (PCC3e Ch. 6).
                # Devices may lack a 'User' key if unassigned — though we
                # filter to 'Assigned' above, the defensive pattern still
                # protects against any schema surprises.
                user_arn = device.get('User', {}).get('Arn', '')
                if user_arn.endswith(':root'):
                    mfa_type = 'virtual'
                    found_root_virtual = True
                    break
            if found_root_virtual:
                break

    status = 'PASS' if mfa_enabled else 'FAIL'

    # Prominent banner at the top of audit output per issue AC #2.
    print("=" * 40)
    print("Root Account:")
    if mfa_enabled and mfa_type == 'hardware':
        print("  [PASS] MFA enabled (hardware). FedRAMP High preferred.")
    elif mfa_enabled and mfa_type == 'virtual':
        print("  [PASS] MFA enabled (virtual). FedRAMP High recommends hardware MFA for root.")
    else:
        print("  [FAIL] MFA NOT enabled. Critical security gap.")
    print("=" * 40)

    return {
        'root_mfa_enabled': mfa_enabled,
        'root_mfa_type': mfa_type,
        'root_mfa_status': status
    }


def audit_password_policy(iam):
    """
    Audit the account's IAM password policy against FedRAMP High requirements.

    FedRAMP High IA-5(1) parameterizes NIST 800-53 Rev 5 password requirements.
    CJIS v6.0 5.6.2.1 aligns with these same parameters as of December 2024.
    This function evaluates seven checks and returns overall status plus
    per-check detail so auditors can see expected vs actual for each rule.

    If no password policy is configured on the account,
    get_account_password_policy() raises NoSuchEntityException. Absence of a
    policy is itself a compliance failure, so we catch the exception and
    return a structured failure record rather than letting it crash the
    audit.

    Args:
        iam: boto3 IAM client

    Returns:
        dict with keys:
            password_policy_configured (bool): False if no policy exists
            password_policy_status (str): 'PASS' or 'FAIL' overall
            password_policy_checks (list[dict]): per-check records with
                keys name, expected, actual, status
    """
    print("=" * 40)
    print("Password Policy:")

    try:
        response = iam.get_account_password_policy()
        policy = response['PasswordPolicy']
    except iam.exceptions.NoSuchEntityException:
        # No policy on the account. Structured FAIL so downstream exports
        # can render it consistently with configured-but-failing policies.
        print("  [FAIL] No password policy configured on the account.")
        print("=" * 40)
        return {
            'password_policy_configured': False,
            'password_policy_status': 'FAIL',
            'password_policy_checks': []
        }

    # dict.get() with sensible defaults (PCC3e Ch. 6). MaxPasswordAge may
    # be absent when ExpirePasswords is False; PasswordReusePrevention may
    # be absent when set to 0. In both cases the defaults make the check
    # fail, which is the correct compliance outcome.
    min_len = policy.get('MinimumPasswordLength', 0)
    require_upper = policy.get('RequireUppercaseCharacters', False)
    require_lower = policy.get('RequireLowercaseCharacters', False)
    require_numbers = policy.get('RequireNumbers', False)
    require_symbols = policy.get('RequireSymbols', False)
    max_age = policy.get('MaxPasswordAge', 0)
    reuse_prevention = policy.get('PasswordReusePrevention', 0)

    # Declarative check list: each element is name, expected-as-string,
    # actual value, and pass/fail. Separating the check data from the
    # evaluation loop keeps the thresholds visible at a glance and makes
    # it easy to add, remove, or tune checks without rewriting control flow.
    checks = [
        {
            'name': 'MinimumPasswordLength',
            'expected': '>= 14',
            'actual': min_len,
            'status': 'PASS' if min_len >= 14 else 'FAIL'
        },
        {
            'name': 'RequireUppercaseCharacters',
            'expected': True,
            'actual': require_upper,
            'status': 'PASS' if require_upper else 'FAIL'
        },
        {
            'name': 'RequireLowercaseCharacters',
            'expected': True,
            'actual': require_lower,
            'status': 'PASS' if require_lower else 'FAIL'
        },
        {
            'name': 'RequireNumbers',
            'expected': True,
            'actual': require_numbers,
            'status': 'PASS' if require_numbers else 'FAIL'
        },
        {
            'name': 'RequireSymbols',
            'expected': True,
            'actual': require_symbols,
            'status': 'PASS' if require_symbols else 'FAIL'
        },
        {
            'name': 'MaxPasswordAge',
            'expected': '<= 60 days (and set)',
            'actual': max_age,
            # Both conditions must hold: expiry must be configured (max_age > 0
            # since 0 means "never expire") AND within the FedRAMP window.
            'status': 'PASS' if 0 < max_age <= 60 else 'FAIL'
        },
        {
            'name': 'PasswordReusePrevention',
            'expected': '>= 24',
            'actual': reuse_prevention,
            'status': 'PASS' if reuse_prevention >= 24 else 'FAIL'
        },
    ]

    passed = sum(1 for c in checks if c['status'] == 'PASS')
    overall = 'PASS' if passed == len(checks) else 'FAIL'

    # Print each check result, then an overall summary line.
    for c in checks:
        print(f"  [{c['status']}] {c['name']}: expected {c['expected']}, actual {c['actual']}")
    print(f"  Overall: {overall} ({passed} of {len(checks)} checks passed)")
    print("=" * 40)

    return {
        'password_policy_configured': True,
        'password_policy_status': overall,
        'password_policy_checks': checks
    }


def audit_user(iam, user, quiet=False):
    """
    Audit a single IAM user for MFA, access key, and activity compliance.

    Checks whether the user has console access, whether MFA is enabled,
    whether any active access keys exceed the 90-day rotation threshold,
    and whether the user has been inactive for 90+ days.

    Args:
        iam: boto3 IAM client
        user: User dictionary from list_users() containing UserName,
              CreateDate, and optionally PasswordLastUsed
        quiet: When True, suppress per-user print output. Account-level
               banners and the final summary still print from run_audit.

    Returns:
        dict containing user audit results with keys: username,
        has_console_access, mfa_enabled, compliance_status,
        access_key_count, oldest_key_age_days, key_compliance_status,
        last_activity_date, days_inactive, activity_status
    """
    # Bind 'log' to print, or to a no-op lambda when quiet. Declaring this
    # once lets the per-user lines below stay uncluttered — no 'if not quiet'
    # scattered through the function.
    log = print if not quiet else lambda *args, **kwargs: None

    username = user['UserName']
    now_utc = datetime.now(timezone.utc)
    log(f"Checking: {username}")

    # Paginate list_mfa_devices() for completeness. Empty list means no MFA.
    mfa_paginator = iam.get_paginator('list_mfa_devices')
    mfa_devices = []
    for page in mfa_paginator.paginate(UserName=username):
        mfa_devices.extend(page['MFADevices'])

    # Check to see if user has console access. Throws except if no console access.
    try:
        iam.get_login_profile(UserName=username)
        has_console = True
    except iam.exceptions.NoSuchEntityException:
        has_console = False

    # Evaluate compliance based on both checks.
    if has_console and mfa_devices:
        log("    [PASS] MFA enabled for console user.")
        compliance_status = 'PASS'
    elif has_console and not mfa_devices:
        log("    [FAIL] Console access WITHOUT MFA!")
        compliance_status = 'FAIL'
    else:
        log("    [INFO] No console access (MFA not required).")
        compliance_status = 'INFO'

    # Check access key age for compliance with rotation policy.
    # IA-5(1) requires periodic authenticator rotation — 90-day threshold
    # matches CIS AWS Benchmark 1.14 and common FedRAMP/CJIS expectations.
    keys_paginator = iam.get_paginator('list_access_keys')
    access_keys = []
    for page in keys_paginator.paginate(UserName=username):
        access_keys.extend(page['AccessKeyMetadata'])

    # Track the oldest key and whether any active key exceeds 90 days.
    oldest_key_age = 0
    key_compliance = 'N/A'

    if access_keys:
        user_keys_compliant = True

        for key in access_keys:
            key_id = key['AccessKeyId']
            key_status = key['Status']
            # CreateDate is timezone-aware (UTC) from boto3, so we compare
            # against timezone-aware now() to avoid TypeError.
            key_age_days = (now_utc - key['CreateDate']).days
            oldest_key_age = max(oldest_key_age, key_age_days)

            # Only flag active keys — inactive keys are already disabled.
            if key_status == 'Active' and key_age_days > 90:
                log(f"    [FAIL] Access key ...{key_id[-4:]} is {key_age_days} days old (Active)")
                user_keys_compliant = False
            elif key_status == 'Active':
                log(f"    [PASS] Access key ...{key_id[-4:]} is {key_age_days} days old (Active)")
            else:
                log(f"    [INFO] Access key ...{key_id[-4:]} is {key_age_days} days old (Inactive)")

        if user_keys_compliant:
            key_compliance = 'PASS'
        else:
            key_compliance = 'FAIL'
    else:
        log("    [N/A] No access keys.")

    # Determine last activity date for inactivity detection.
    # AC-2(3) requires disabling accounts inactive beyond a defined threshold.
    # Start with CreateDate as baseline (timezone-aware UTC from boto3).
    last_activity = user['CreateDate']

    # PasswordLastUsed is only present if the user has signed in via console
    # at least once. dict.get() returns None when the key is missing (PCC3e
    # Ch. 6), avoiding a KeyError for programmatic-only users.
    password_last_used = user.get('PasswordLastUsed')
    if password_last_used and password_last_used > last_activity:
        last_activity = password_last_used

    # Check each access key's last used date for programmatic activity.
    # get_access_key_last_used() is a direct call (not paginated) since
    # it returns a single result per key.
    for key in access_keys:
        key_last_used_info = iam.get_access_key_last_used(
            AccessKeyId=key['AccessKeyId']
        )
        key_last_used = key_last_used_info['AccessKeyLastUsed'].get('LastUsedDate')
        if key_last_used and key_last_used > last_activity:
            last_activity = key_last_used

    days_inactive = (now_utc - last_activity).days

    if days_inactive > 90:
        log(f"    [FAIL] Inactive for {days_inactive} days (last activity: {last_activity.strftime('%Y-%m-%d')})")
        activity_status = 'FAIL'
    else:
        log(f"    [PASS] Active within 90 days (last activity: {last_activity.strftime('%Y-%m-%d')})")
        activity_status = 'PASS'

    return {
        'username': username,
        'has_console_access': has_console,
        'mfa_enabled': bool(mfa_devices),
        'compliance_status': compliance_status,
        'access_key_count': len(access_keys),
        'oldest_key_age_days': oldest_key_age,
        'key_compliance_status': key_compliance,
        'last_activity_date': last_activity.strftime('%Y-%m-%d'),
        'days_inactive': days_inactive,
        'activity_status': activity_status
    }


def send_compliance_alert(audit_results, metadata):
    """
    Publish a summary alert to SNS when non-compliant findings exist.

    Reads the SNS topic ARN from the IAM_AUDIT_SNS_TOPIC_ARN environment
    variable. If unset, alerting is skipped so the audit remains runnable
    without any SNS configuration. If set but no findings exist, the alert
    is also skipped to avoid zero-finding noise. Maps to SI-4(5)
    (System-Generated Alerts).

    Args:
        audit_results: List of dictionaries from audit_user() calls
        metadata: Dictionary containing audit metadata (timestamps, rates, counts)

    Returns:
        str: SNS MessageId on successful publish, or None if alert was skipped
    """
    # os.environ.get() mirrors dict.get() — returns None when the variable
    # is unset instead of raising KeyError (PCC3e Ch. 6). Keeping the ARN
    # out of the code lets the same script run against any account without
    # a code change, and keeps ARNs out of git history.
    topic_arn = os.environ.get('IAM_AUDIT_SNS_TOPIC_ARN')
    if not topic_arn:
        print("\n[INFO] SNS alerting skipped (IAM_AUDIT_SNS_TOPIC_ARN not set).")
        return None

    # Collect failures across all three compliance dimensions so a single
    # alert covers the full audit, not just MFA.
    mfa_failures = [r for r in audit_results if r['compliance_status'] == 'FAIL']
    key_failures = [r for r in audit_results if r['key_compliance_status'] == 'FAIL']
    activity_failures = [r for r in audit_results if r['activity_status'] == 'FAIL']

    total_failures = len(mfa_failures) + len(key_failures) + len(activity_failures)

    if total_failures == 0:
        print("\n[INFO] SNS alerting skipped (no non-compliant findings).")
        return None

    # Build the alert body as a list of lines, then join once — cheaper than
    # repeated string concatenation and easier to reorder (PCC3e Ch. 4).
    lines = [
        f"IAM Audit Alert - {metadata['end_time']}",
        "",
        f"Non-compliant findings detected in audit of {metadata['total_users']} users.",
        "",
        "Summary:",
        f"  MFA compliance rate:      {metadata['compliance_rate']}",
        f"  Key compliance rate:      {metadata['key_compliance_rate']}",
        f"  Activity compliance rate: {metadata['activity_compliance_rate']}",
        "",
    ]

    if mfa_failures:
        lines.append(f"Console access WITHOUT MFA ({len(mfa_failures)}):")
        for r in mfa_failures:
            lines.append(f"  - {r['username']}")
        lines.append("")

    if key_failures:
        lines.append(f"Access keys exceeding 90-day rotation ({len(key_failures)}):")
        for r in key_failures:
            lines.append(f"  - {r['username']} (oldest key: {r['oldest_key_age_days']} days)")
        lines.append("")

    if activity_failures:
        lines.append(f"Inactive users 90+ days ({len(activity_failures)}):")
        for r in activity_failures:
            lines.append(
                f"  - {r['username']} ({r['days_inactive']} days inactive, "
                f"last activity: {r['last_activity_date']})"
            )
        lines.append("")

    message = "\n".join(lines)
    subject = f"IAM Audit Alert: {total_failures} non-compliant findings"

    # SNS Subject is capped at 100 ASCII characters — our format stays well
    # under that limit even for large finding counts.
    sns = boto3.client('sns')

    # SNS is a system boundary. The CSV/JSON are already written by the time
    # we reach this point, so a publish failure should not crash the audit —
    # log it and move on (CLAUDE.md: validate at system boundaries).
    try:
        response = sns.publish(
            TopicArn=topic_arn,
            Subject=subject,
            Message=message
        )
    except (ClientError, BotoCoreError) as e:
        print(f"\n[WARN] SNS alert failed to publish: {e}")
        return None

    print(f"\n[INFO] SNS alert published (MessageId: {response['MessageId']})")
    return response['MessageId']


def run_audit(output_dir='.', output_format='both', quiet=False):
    """
    Run the full IAM audit across all users.

    Creates an IAM client, checks every user for MFA, access key, and
    activity compliance, prints a summary, and exports results based on
    the selected format.

    Defaults preserve the pre-CLI behavior: both files in the current
    directory, verbose per-user output. This keeps run_audit() callable
    programmatically (e.g., from tests or future evidence-logger hooks)
    without relying on argparse.

    Args:
        output_dir: Directory to write reports into. Created if missing.
                    Defaults to current directory.
        output_format: 'csv', 'json', or 'both' (default: 'both').
        quiet: When True, per-user output is suppressed. Account-level
               banners (root MFA, password policy) and the final
               summary still print.
    """
    # Create IAM client to interact with AWS IAM service.
    iam = boto3.client('iam')

    audit_start = datetime.now()

    # Root account check runs first so the banner appears above the per-user
    # output. Root is account-level (not per-user) so results are kept in a
    # separate dict rather than mixed into audit_results.
    root_info = audit_root_account(iam)

    # Password policy check is also account-level. Runs after root so the
    # two account-level banners print together before per-user output.
    policy_info = audit_password_policy(iam)

    # Paginate list_users() to retrieve all users regardless of account size.
    # Default API response is capped at 100 users per call.
    paginator = iam.get_paginator('list_users')
    users = []
    for page in paginator.paginate():
        users.extend(page['Users'])
    total_users = len(users)

    audit_results = []

    # Check each user for MFA, access key, and activity compliance.
    # The quiet flag propagates to per-user output only; audit_user() still
    # returns the same dict shape regardless.
    for user in users:
        result = audit_user(iam, user, quiet=quiet)
        audit_results.append(result)

    # Capture audit completion time and calculate elapsed time.
    audit_end = datetime.now()
    elapsed = (audit_end - audit_start).total_seconds()

    # Derive compliance counts from results.
    compliant_count = sum(1 for r in audit_results if r['compliance_status'] == 'PASS')
    no_console_count = sum(1 for r in audit_results if r['compliance_status'] == 'INFO')
    keys_compliant_count = sum(1 for r in audit_results if r['key_compliance_status'] == 'PASS')
    keys_noncompliant_count = sum(1 for r in audit_results if r['key_compliance_status'] == 'FAIL')
    inactive_count = sum(1 for r in audit_results if r['activity_status'] == 'FAIL')

    # Compliance summary of results.
    print("\n" + "=" * 40)
    print("MFA Compliance:")
    print(f"  Total users: {total_users}")
    print(f"  Compliant (MFA enabled): {compliant_count}")
    print(f"  No console access: {no_console_count}")
    print(f"  Non-compliant: {total_users - compliant_count - no_console_count}")

    # Users with at least one access key — denominator for key compliance rate.
    users_with_keys = keys_compliant_count + keys_noncompliant_count

    print(f"\nAccess Key Compliance (90-day rotation):")
    print(f"  Users with keys: {users_with_keys}")
    print(f"  Compliant: {keys_compliant_count}")
    print(f"  Non-compliant: {keys_noncompliant_count}")

    print(f"\nUser Activity (90-day inactivity threshold):")
    print(f"  Active: {total_users - inactive_count}")
    print(f"  Inactive (90+ days): {inactive_count}")

    # Calculate compliance rates for GRC reporting.
    compliance_rate = (compliant_count / total_users * 100) if total_users > 0 else 0
    key_compliance_rate = (keys_compliant_count / users_with_keys * 100) if users_with_keys > 0 else 0
    activity_compliance_rate = ((total_users - inactive_count) / total_users * 100) if total_users > 0 else 0

    # Display audit trail timestamps.
    print(f"\nAudit started: {audit_start.isoformat()}")
    print(f"Audit completed: {audit_end.isoformat()}")
    print(f"Elapsed time: {elapsed:.2f} seconds")
    print(f"MFA compliance rate: {compliance_rate:.1f}%")
    print(f"Key compliance rate: {key_compliance_rate:.1f}%")
    print(f"Activity compliance rate: {activity_compliance_rate:.1f}%")

    # Export results to CSV and JSON for compliance reporting.
    timestamp_str = audit_start.isoformat().replace(':', '-').split('.')[0]

    metadata = {
        'start_time': audit_start.isoformat(),
        'end_time': audit_end.isoformat(),
        'elapsed_seconds': elapsed,
        'total_users': total_users,
        'compliance_rate': f"{compliance_rate:.1f}%",
        'key_compliance_rate': f"{key_compliance_rate:.1f}%",
        'activity_compliance_rate': f"{activity_compliance_rate:.1f}%",
        'inactive_users': inactive_count,
        'root_mfa_enabled': root_info['root_mfa_enabled'],
        'root_mfa_type': root_info['root_mfa_type'],
        'root_mfa_status': root_info['root_mfa_status'],
        'password_policy_configured': policy_info['password_policy_configured'],
        'password_policy_status': policy_info['password_policy_status'],
        'password_policy_checks': policy_info['password_policy_checks']
    }

    # Gate each export on the selected format so --format csv/json skips the
    # other writer entirely. 'both' runs both branches. Using 'in' keeps the
    # conditional readable without repeating the two-branch comparison.
    csv_file = None
    json_file = None
    if output_format in ('csv', 'both'):
        csv_file = export_to_csv(
            audit_results, root_info, policy_info, timestamp_str,
            output_dir=output_dir,
        )
    if output_format in ('json', 'both'):
        json_file = export_to_json(
            audit_results, metadata, timestamp_str,
            output_dir=output_dir,
        )

    print(f"\nResults exported to:")
    if csv_file:
        print(f"  - {csv_file}")
    if json_file:
        print(f"  - {json_file}")

    # Publish SNS alert if configured and non-compliant findings exist.
    send_compliance_alert(audit_results, metadata)


def parse_args():
    """
    Parse command-line arguments for the IAM audit.

    argparse builds the --help output automatically from the description
    and each add_argument() call, so we don't define --help ourselves.
    Hyphens in flag names become underscores on the Namespace, so
    '--output-dir' is read as 'args.output_dir'. Reference:
    https://docs.python.org/3/library/argparse.html

    Returns:
        argparse.Namespace with attributes: output_dir, format, quiet
    """
    parser = argparse.ArgumentParser(
        description=(
            'Audit the AWS root account and all IAM users for MFA, access '
            'key rotation, activity, and password policy compliance. '
            'Exports findings to CSV and/or JSON.'
        ),
    )
    parser.add_argument(
        '--output-dir',
        default='.',
        help='Directory to write CSV/JSON reports (default: current directory). Created if missing.',
    )
    # choices= enforces a whitelist at parse time — argparse rejects bad
    # values with a helpful error before run_audit() is ever called.
    parser.add_argument(
        '--format',
        choices=['csv', 'json', 'both'],
        default='both',
        help='Output format to write (default: both).',
    )
    # action='store_true' means the flag takes no value; presence sets True,
    # absence leaves the default False. Standard argparse idiom for boolean
    # toggles.
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress per-user output; print only account-level banners and the summary.',
    )
    return parser.parse_args()


def main():
    """
    CLI entry point. Parses arguments, then calls run_audit().

    Keeping argparse concerns out of run_audit() means the audit logic
    can still be invoked directly (e.g., from evidence-logger) without
    going through the CLI.
    """
    args = parse_args()
    run_audit(
        output_dir=args.output_dir,
        output_format=args.format,
        quiet=args.quiet,
    )


if __name__ == '__main__':
    main()
