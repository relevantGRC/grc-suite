"""
compliance_report.py

Generates a unified HTML compliance report from multiple AWS audits.

Audits Included:
    1. S3 Buckets - Encryption and public access block settings
    2. IAM Users - MFA compliance for console users
    3. Security Groups - Overly permissive inbound rules

Features:
    - Executive summary with pass/fail/warn counts
    - Professional HTML styling (AWS-themed)
    - Account ID and timestamp metadata
    - Color-coded status indicators

How it works:
    - Each audit is a function that returns a list of findings
    - Findings are dictionaries with standardized 'status' field
    - Jinja2 template renders findings into HTML tables
    - Report saved as timestamped HTML file

Usage:
    python compliance_report.py

Requirements:
    - boto3 installed (pip install boto3)
    - jinja2 installed (pip install jinja2)
    - AWS credentials configured (aws configure)
"""

import boto3
from datetime import datetime
from jinja2 import Template

# ---------------------------------------------------------------------------
# AWS Clients
# ---------------------------------------------------------------------------

s3 = boto3.client('s3')
iam = boto3.client('iam')
ec2 = boto3.client('ec2')
sts = boto3.client('sts')

# ---------------------------------------------------------------------------
# Audit Functions - Each returns structured data
# ---------------------------------------------------------------------------

def audit_s3_buckets():
    """Audit S3 buckets for encryption and public access settings."""
    findings = []
    
    response = s3.list_buckets()
    buckets = response['Buckets']
    
    for bucket in buckets:
        bucket_name = bucket['Name']
        result = {
            'name': bucket_name,
            'encryption': 'FAIL',
            'encryption_type': None,
            'public_access_block': 'FAIL',
            'status': 'FAIL'
        }
        
        # Check encryption
        try:
            enc = s3.get_bucket_encryption(Bucket=bucket_name)
            enc_type = enc['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']
            result['encryption'] = 'PASS'
            result['encryption_type'] = enc_type
        except:
            pass
        
        # Check public access block
        try:
            pab = s3.get_public_access_block(Bucket=bucket_name)
            block_config = pab['PublicAccessBlockConfiguration']
            all_blocked = all([
                block_config.get('BlockPublicAcls', False),
                block_config.get('IgnorePublicAcls', False),
                block_config.get('BlockPublicPolicy', False),
                block_config.get('RestrictPublicBuckets', False)
            ])
            if all_blocked:
                result['public_access_block'] = 'PASS'
            else:
                result['public_access_block'] = 'WARN'
        except:
            pass
        
        # Overall status
        if result['encryption'] == 'PASS' and result['public_access_block'] == 'PASS':
            result['status'] = 'PASS'
        elif result['encryption'] == 'FAIL' or result['public_access_block'] == 'FAIL':
            result['status'] = 'FAIL'
        else:
            result['status'] = 'WARN'
        
        findings.append(result)
    
    return findings


def audit_iam_users():
    """Audit IAM users for MFA compliance."""
    findings = []
    
    iam_users = iam.list_users()
    users = iam_users['Users']
    
    for user in users:
        username = user['UserName']
        result = {
            'username': username,
            'has_console': False,
            'mfa_enabled': False,
            'status': 'INFO'
        }
        
        # Check MFA devices
        mfa_response = iam.list_mfa_devices(UserName=username)
        mfa_devices = mfa_response['MFADevices']
        result['mfa_enabled'] = len(mfa_devices) > 0
        
        # Check console access
        try:
            iam.get_login_profile(UserName=username)
            result['has_console'] = True
        except:
            pass
        
        # Determine status
        if result['has_console'] and result['mfa_enabled']:
            result['status'] = 'PASS'
        elif result['has_console'] and not result['mfa_enabled']:
            result['status'] = 'FAIL'
        else:
            result['status'] = 'INFO'
        
        findings.append(result)
    
    return findings


def audit_security_groups():
    """Audit security groups for overly permissive rules."""
    RISKY_PORTS = {22, 3389, 3306, 5432, 1433, 27017}
    findings = []
    
    security_groups = ec2.describe_security_groups()
    sg_list = security_groups['SecurityGroups']
    
    for sg in sg_list:
        result = {
            'name': sg['GroupName'],
            'id': sg['GroupId'],
            'vpc_id': sg.get('VpcId', 'N/A'),
            'open_ports': [],
            'risky_ports': [],
            'status': 'PASS'
        }
        
        for rule in sg['IpPermissions']:
            from_port = rule.get('FromPort', 'All')
            
            for ip_range in rule.get('IpRanges', []):
                if ip_range.get('CidrIp') == '0.0.0.0/0':
                    if from_port in RISKY_PORTS:
                        result['risky_ports'].append(from_port)
                        result['status'] = 'FAIL'
                    else:
                        result['open_ports'].append(from_port)
                        if result['status'] != 'FAIL':
                            result['status'] = 'WARN'
        
        findings.append(result)
    
    return findings


def get_account_info():
    """Get AWS account information."""
    identity = sts.get_caller_identity()
    return {
        'account_id': identity['Account'],
        'user_arn': identity['Arn']
    }


# ---------------------------------------------------------------------------
# Report Generation
# ---------------------------------------------------------------------------

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AWS Compliance Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #232f3e; border-bottom: 3px solid #ff9900; padding-bottom: 10px; }
        h2 { color: #232f3e; margin-top: 30px; }
        .summary { display: flex; gap: 20px; margin: 20px 0; }
        .summary-card { flex: 1; padding: 20px; border-radius: 8px; text-align: center; }
        .summary-card.pass { background: #d4edda; border: 1px solid #28a745; }
        .summary-card.fail { background: #f8d7da; border: 1px solid #dc3545; }
        .summary-card.warn { background: #fff3cd; border: 1px solid #ffc107; }
        .summary-card h3 { margin: 0; font-size: 36px; }
        .summary-card p { margin: 5px 0 0 0; color: #666; }
        table { width: 100%; border-collapse: collapse; margin: 15px 0; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #232f3e; color: white; }
        tr:hover { background: #f5f5f5; }
        .pass { color: #28a745; font-weight: bold; }
        .fail { color: #dc3545; font-weight: bold; }
        .warn { color: #ffc107; font-weight: bold; }
        .info { color: #17a2b8; font-weight: bold; }
        .metadata { color: #666; font-size: 14px; margin-bottom: 20px; }
        .section { margin-bottom: 40px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔒 AWS Compliance Report</h1>
        <div class="metadata">
            <p><strong>Account ID:</strong> {{ account_id }}</p>
            <p><strong>Generated:</strong> {{ timestamp }}</p>
            <p><strong>Region:</strong> {{ region }}</p>
        </div>
        
        <h2>Executive Summary</h2>
        <div class="summary">
            <div class="summary-card pass">
                <h3>{{ summary.passed }}</h3>
                <p>Passed</p>
            </div>
            <div class="summary-card fail">
                <h3>{{ summary.failed }}</h3>
                <p>Failed</p>
            </div>
            <div class="summary-card warn">
                <h3>{{ summary.warnings }}</h3>
                <p>Warnings</p>
            </div>
        </div>
        
        <div class="section">
            <h2>S3 Bucket Audit</h2>
            <p>Checking encryption and public access block settings.</p>
            <table>
                <tr>
                    <th>Bucket Name</th>
                    <th>Encryption</th>
                    <th>Public Access Block</th>
                    <th>Status</th>
                </tr>
                {% for bucket in s3_findings %}
                <tr>
                    <td>{{ bucket.name }}</td>
                    <td class="{{ bucket.encryption.lower() }}">{{ bucket.encryption }}{% if bucket.encryption_type %} ({{ bucket.encryption_type }}){% endif %}</td>
                    <td class="{{ bucket.public_access_block.lower() }}">{{ bucket.public_access_block }}</td>
                    <td class="{{ bucket.status.lower() }}">{{ bucket.status }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>
        
        <div class="section">
            <h2>IAM User Audit</h2>
            <p>Checking MFA compliance for console users.</p>
            <table>
                <tr>
                    <th>Username</th>
                    <th>Console Access</th>
                    <th>MFA Enabled</th>
                    <th>Status</th>
                </tr>
                {% for user in iam_findings %}
                <tr>
                    <td>{{ user.username }}</td>
                    <td>{{ 'Yes' if user.has_console else 'No' }}</td>
                    <td>{{ 'Yes' if user.mfa_enabled else 'No' }}</td>
                    <td class="{{ user.status.lower() }}">{{ user.status }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>
        
        <div class="section">
            <h2>Security Group Audit</h2>
            <p>Checking for overly permissive inbound rules (0.0.0.0/0).</p>
            <table>
                <tr>
                    <th>Security Group</th>
                    <th>ID</th>
                    <th>Open Ports</th>
                    <th>Risky Ports</th>
                    <th>Status</th>
                </tr>
                {% for sg in sg_findings %}
                <tr>
                    <td>{{ sg.name }}</td>
                    <td>{{ sg.id }}</td>
                    <td>{{ sg.open_ports | join(', ') if sg.open_ports else '-' }}</td>
                    <td>{{ sg.risky_ports | join(', ') if sg.risky_ports else '-' }}</td>
                    <td class="{{ sg.status.lower() }}">{{ sg.status }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>
        
        <div class="metadata" style="margin-top: 40px; text-align: center;">
            <p>Generated by GRC Automation Tool - Lesson 8</p>
        </div>
    </div>
</body>
</html>
"""


def generate_report(s3_findings, iam_findings, sg_findings, account_info):
    """Generate HTML report from audit findings."""
    
    # Calculate summary
    all_statuses = (
        [f['status'] for f in s3_findings] +
        [f['status'] for f in iam_findings] +
        [f['status'] for f in sg_findings]
    )
    
    summary = {
        'passed': all_statuses.count('PASS'),
        'failed': all_statuses.count('FAIL'),
        'warnings': all_statuses.count('WARN')
    }
    
    # Render template
    template = Template(HTML_TEMPLATE)
    html = template.render(
        account_id=account_info['account_id'],
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        region=boto3.session.Session().region_name,
        summary=summary,
        s3_findings=s3_findings,
        iam_findings=iam_findings,
        sg_findings=sg_findings
    )
    
    return html


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    print("=" * 60)
    print("AWS Compliance Report Generator")
    print("=" * 60)
    
    # Get account info
    print("\n[1/4] Getting account information...")
    account_info = get_account_info()
    print(f"      Account: {account_info['account_id']}")
    
    # Run audits
    print("\n[2/4] Auditing S3 buckets...")
    s3_findings = audit_s3_buckets()
    print(f"      Found {len(s3_findings)} buckets")
    
    print("\n[3/4] Auditing IAM users...")
    iam_findings = audit_iam_users()
    print(f"      Found {len(iam_findings)} users")
    
    print("\n[4/4] Auditing security groups...")
    sg_findings = audit_security_groups()
    print(f"      Found {len(sg_findings)} security groups")
    
    # Generate report
    print("\nGenerating HTML report...")
    html_content = generate_report(s3_findings, iam_findings, sg_findings, account_info)
    
    # Save report
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"compliance_report_{timestamp}.html"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✓ Report saved: {filename}")
    print("\nOpen the HTML file in a browser to view the report.")
