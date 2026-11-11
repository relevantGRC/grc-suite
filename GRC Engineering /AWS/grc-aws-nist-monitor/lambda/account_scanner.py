import boto3
import json
import datetime
from datetime import timezone

iam = boto3.client('iam')
s3  = boto3.client('s3')
ses = boto3.client('ses', region_name='us-east-1')

# ── UPDATE THESE 3 LINES ──────────────────────────────
BUCKET    = 'grc-reports-[your-account-id]'
SENDER    = 'your-sender-email@domain.com'
RECIPIENT = 'your-recipient-email@domain.com'
# ─────────────────────────────────────────────────────

def days_since(date_val):
    if not date_val:
        return 9999
    if isinstance(date_val, str):
        dt = datetime.datetime.fromisoformat(date_val.replace('Z',''))
    else:
        dt = date_val
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return (datetime.datetime.now(timezone.utc) - dt).days

def lambda_handler(event, context):
    users = iam.list_users()['Users']
    findings = []

    for user in users:
        username  = user['UserName']
        created   = user.get('CreateDate')
        age_days  = days_since(created)

        try:
            detail    = iam.get_user(UserName=username)['User']
            last_used = detail.get('PasswordLastUsed')
            inactive_days = days_since(last_used) if last_used else age_days
        except:
            inactive_days = age_days

        tags = {t['Key']: t['Value'] for t in
                iam.list_user_tags(UserName=username).get('Tags', [])}

        account_type  = tags.get('AccountType', 'unknown')
        review_date   = tags.get('ReviewDate',  'not-set')
        tagged_status = tags.get('Status',      'unknown')

        keys        = iam.list_access_keys(UserName=username)['AccessKeyMetadata']
        active_keys = [k for k in keys if k['Status'] == 'Active']

        policies     = iam.list_attached_user_policies(
                           UserName=username)['AttachedPolicies']
        policy_names = [p['PolicyName'] for p in policies]
        has_admin    = any('Admin' in p or 'Power' in p or 'Full' in p
                           for p in policy_names)

        violations = []

        # AC-2(2) — employee marked inactive never disabled
        if tagged_status == 'inactive' and account_type == 'employee':
            violations.append({
                'control':  'AC-2(2)',
                'severity': 'HIGH',
                'finding':  'Former employee account never disabled'
            })

        # AC-2(2) — inactive over 90 days
        if inactive_days > 90:
            violations.append({
                'control':  'AC-2(2)',
                'severity': 'HIGH',
                'finding':  f'Account inactive for {inactive_days} days'
            })

        # AC-2 — temp/guest/contractor past review date
        if account_type in ['temporary','guest','contractor']:
            try:
                rd = datetime.datetime.strptime(review_date, '%Y-%m-%d')
                if rd < datetime.datetime.now():
                    violations.append({
                        'control':  'AC-2',
                        'severity': 'HIGH',
                        'finding':  f'{account_type} account past review date ({review_date})'
                    })
            except:
                violations.append({
                    'control':  'AC-2',
                    'severity': 'MEDIUM',
                    'finding':  'Missing or invalid review date'
                })

        # AC-2(1) — inactive account with active keys
        if tagged_status == 'inactive' and active_keys:
            violations.append({
                'control':  'AC-2(1)',
                'severity': 'CRITICAL',
                'finding':  f'Inactive account has {len(active_keys)} active access key(s)'
            })

        # AC-2(4) — excessive privilege
        if has_admin:
            violations.append({
                'control':  'AC-2(4)',
                'severity': 'HIGH',
                'finding':  f'Excessive privilege: {", ".join(policy_names)}'
            })

        findings.append({
            'username':      username,
            'account_type':  account_type,
            'created_days':  age_days,
            'inactive_days': inactive_days,
            'review_date':   review_date,
            'active_keys':   len(active_keys),
            'policies':      policy_names,
            'violations':    violations,
            'compliant':     len(violations) == 0
        })

    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%S')
    report = {
        'report_title':      'NIST RMF AC-2 Account Management Compliance Report',
        'generated_utc':     timestamp,
        'controls_assessed': ['AC-2','AC-2(1)','AC-2(2)','AC-2(4)','AU-6','CA-7'],
        'total_accounts':    len(findings),
        'compliant':         sum(1 for f in findings if f['compliant']),
        'non_compliant':     sum(1 for f in findings if not f['compliant']),
        'findings':          findings
    }

    key = f'reports/{timestamp}-ac2-report.json'
    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=json.dumps(report, indent=2, default=str),
        ContentType='application/json'
    )

    html = build_html_report(report)
    send_email(html, timestamp)

    return {
        'status':        'success',
        'report_key':    key,
        'total':         len(findings),
        'compliant':     report['compliant'],
        'non_compliant': report['non_compliant']
    }


def build_html_report(report):
    rows = ''
    for f in report['findings']:
        if f['violations']:
            viols = ''
            for v in f['violations']:
                if v['severity'] == 'CRITICAL':
                    color = '#c0392b'
                elif v['severity'] == 'HIGH':
                    color = '#e67e22'
                else:
                    color = '#888888'
                viols += (
                    "<span style='color:" + color + ";font-weight:bold'>"
                    "[" + v['severity'] + "] " + v['control'] + ": " +
                    v['finding'] + "</span><br>"
                )
            row_bg = '#fff5f5'
        else:
            viols  = "<span style='color:#27ae60;font-weight:bold'>✓ COMPLIANT</span>"
            row_bg = '#f5fff5'

        inactive_display = (str(f['inactive_days'])
                           if f['inactive_days'] != 9999 else 'Never used')
        policies_display = (', '.join(f['policies'])
                           if f['policies'] else 'None')

        rows += (
            "<tr style='background:" + row_bg + "'>"
            "<td style='padding:8px;border:1px solid #ddd'>" + f['username'] + "</td>"
            "<td style='padding:8px;border:1px solid #ddd'>" + f['account_type'] + "</td>"
            "<td style='padding:8px;border:1px solid #ddd;text-align:center'>" + inactive_display + "</td>"
            "<td style='padding:8px;border:1px solid #ddd;text-align:center'>" + str(f['active_keys']) + "</td>"
            "<td style='padding:8px;border:1px solid #ddd'>" + policies_display + "</td>"
            "<td style='padding:8px;border:1px solid #ddd'>" + viols + "</td>"
            "</tr>"
        )

    compliant_pct = round(
        (report['compliant'] / report['total_accounts'] * 100)
        if report['total_accounts'] > 0 else 0
    )

    controls  = ', '.join(report['controls_assessed'])
    timestamp = report['generated_utc']

    html = (
        "<html><body style='font-family:Arial,sans-serif;"
        "max-width:960px;margin:auto;padding:20px'>"

        "<div style='background:#1a1a2e;color:white;padding:24px;"
        "border-radius:8px;margin-bottom:24px'>"
        "<h1 style='margin:0;font-size:22px'>"
        "NIST RMF - AC-2 Account Management</h1>"
        "<h2 style='margin:4px 0 0;font-size:16px;"
        "font-weight:normal;opacity:0.8'>"
        "Compliance Report - " + timestamp + " UTC</h2>"
        "</div>"

        "<div style='display:flex;gap:16px;margin-bottom:24px'>"
        "<div style='background:#e8f5e9;padding:16px 28px;"
        "border-radius:8px;text-align:center'>"
        "<div style='font-size:36px;font-weight:bold;color:#27ae60'>"
        + str(report['compliant']) + "</div>"
        "<div style='color:#555;font-size:13px'>Compliant</div></div>"

        "<div style='background:#ffebee;padding:16px 28px;"
        "border-radius:8px;text-align:center'>"
        "<div style='font-size:36px;font-weight:bold;color:#c0392b'>"
        + str(report['non_compliant']) + "</div>"
        "<div style='color:#555;font-size:13px'>Non-Compliant</div></div>"

        "<div style='background:#e3f2fd;padding:16px 28px;"
        "border-radius:8px;text-align:center'>"
        "<div style='font-size:36px;font-weight:bold;color:#1565c0'>"
        + str(report['total_accounts']) + "</div>"
        "<div style='color:#555;font-size:13px'>Total Accounts</div></div>"

        "<div style='background:#fff3e0;padding:16px 28px;"
        "border-radius:8px;text-align:center'>"
        "<div style='font-size:36px;font-weight:bold;color:#e65100'>"
        + str(compliant_pct) + "%</div>"
        "<div style='color:#555;font-size:13px'>Compliance Rate</div></div>"
        "</div>"

        "<h3 style='color:#1a1a2e'>Controls Assessed: " + controls + "</h3>"

        "<table style='width:100%;border-collapse:collapse;font-size:13px'>"
        "<thead><tr style='background:#1a1a2e;color:white'>"
        "<th style='padding:10px;text-align:left'>Username</th>"
        "<th style='padding:10px;text-align:left'>Type</th>"
        "<th style='padding:10px;text-align:center'>Inactive Days</th>"
        "<th style='padding:10px;text-align:center'>Active Keys</th>"
        "<th style='padding:10px;text-align:left'>Policies</th>"
        "<th style='padding:10px;text-align:left'>Findings</th>"
        "</tr></thead>"
        "<tbody>" + rows + "</tbody></table>"

        "<hr style='margin:32px 0;border:none;border-top:1px solid #eee'>"
        "<p style='color:#999;font-size:11px;text-align:center'>"
        "Generated by GRC Account Monitor | "
        "NIST RMF CA-7 Continuous Monitoring | "
        "Controls: AC-2, AC-2(1), AC-2(2), AC-2(4), AU-6, CA-7"
        "</p></body></html>"
    )
    return html


def send_email(html_body, timestamp):
    try:
        ses.send_email(
            Source=SENDER,
            Destination={'ToAddresses': [RECIPIENT]},
            Message={
                'Subject': {
                    'Data': f'[GRC Report] NIST RMF AC-2 Compliance — {timestamp}'
                },
                'Body': {
                    'Html': {'Data': html_body}
                }
            }
        )
        print(f'Email sent to {RECIPIENT}')
    except Exception as e:
        print(f'SES send failed: {e}')

# NOTE: Replace BUCKET, SENDER, and RECIPIENT
# variables with your own values before deploying.
# Do NOT commit real email addresses or account IDs.
