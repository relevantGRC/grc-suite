# Lab 1: AWS Account Governance - Validation Checklist

Use this checklist to verify that you have properly implemented all the security controls in the AWS Account Governance lab. Each check includes verification steps to confirm your implementation is working as expected.

## Module 1: Identity Center and IAM Security Foundations

### MFA Configuration

- [ ] **1.1 Root user has MFA enabled**
  - Verification:
    - Go to IAM > Dashboard
    - Confirm "Root MFA" shows "Enabled"
    - Or check Security Hub > CIS AWS Foundations Benchmark > Control 1.5

### AWS IAM Identity Center Configuration

- [ ] **1.2 AWS IAM Identity Center is enabled**
  - Verification:
    - Go to AWS IAM Identity Center
    - Confirm service is enabled
    - Verify Identity Source is properly configured

- [ ] **1.3 Administrative user is created in Identity Center**
  - Verification:
    - Go to IAM Identity Center > Users
    - Confirm administrative user exists
    - Verify user details are properly configured

- [ ] **1.4 MFA is enabled for Identity Center user**
  - Verification:
    - Go to IAM Identity Center > Users > [Your admin user]
    - Under MFA devices tab, confirm at least one MFA device is registered

- [ ] **1.5 Permission sets are properly configured**
  - Verification:
    - Go to IAM Identity Center > Permission sets
    - Confirm AdministratorAccess permission set exists
    - Verify any additional permission sets (e.g., ReadOnlyAccess)

- [ ] **1.6 User is assigned to AWS account with appropriate permission set**
  - Verification:
    - Go to IAM Identity Center > AWS accounts
    - Select your AWS account
    - Verify administrative user is assigned with AdministratorAccess permission set

- [ ] **1.7 IAM Access Analyzer is enabled**
  - Verification:
    - Go to IAM > Access analyzer
    - Confirm analyzer named "AccountAnalyzer" exists and is active

## Module 2: Logging and Monitoring

### CloudTrail Configuration

- [ ] **2.1 CloudTrail is enabled with proper settings**
  - Verification:
    - Go to CloudTrail > Trails
    - Confirm "AccountTrail" exists
    - Verify trail settings:
      - Multi-region trail is enabled
      - Management events are logged (Read and Write)
      - Log file validation is enabled
      - SSE-KMS encryption is enabled

- [ ] **2.2 CloudTrail S3 bucket is properly secured**
  - Verification:
    - Go to CloudTrail > Trails > AccountTrail
    - Check S3 bucket name
    - Go to S3 > [your CloudTrail bucket]
    - Verify bucket policy restricts access
    - Confirm that public access is blocked

### CloudWatch Alarms

- [ ] **2.3 CloudTrail changes alarm is configured**
  - Verification:
    - Go to CloudWatch > Alarms
    - Confirm "CloudTrailChangesAlarm" exists
    - Verify the alarm is properly configured to trigger on CloudTrail changes
    - Confirm the alarm is linked to an SNS topic

- [ ] **2.4 Root login alarm is configured**
  - Verification:
    - Go to CloudWatch > Alarms
    - Confirm root login alarm exists
    - Verify it triggers when root user logs in
    - Confirm the alarm is linked to an SNS topic

- [ ] **2.5 IAM policy changes alarm is configured**
  - Verification:
    - Go to CloudWatch > Alarms
    - Confirm IAM policy changes alarm exists
    - Verify it triggers on policy modifications
    - Confirm the alarm is linked to an SNS topic

- [ ] **2.6 Console login failures alarm is configured**
  - Verification:
    - Go to CloudWatch > Alarms
    - Confirm console login failures alarm exists
    - Verify it triggers after multiple failed login attempts
    - Confirm the alarm is linked to an SNS topic

## Module 3: AWS Config and Compliance

- [ ] **3.1 AWS Config is enabled with proper settings**
  - Verification:
    - Go to AWS Config > Settings
    - Confirm recording is enabled for all resource types
    - Verify global resources are included
    - Confirm delivery channel is configured with S3 bucket

- [ ] **3.2 Key AWS Config rules are enabled**
  - Verification:
    - Go to AWS Config > Rules
    - Confirm the following rules are enabled:
      - cloudtrail-enabled
      - iam-password-policy
      - mfa-enabled-for-iam-console-access
      - root-account-mfa-enabled
      - s3-bucket-public-write-prohibited
      - restricted-ssh
      - restricted-common-ports

- [ ] **3.3 Custom Config rules are implemented**
  - Verification:
    - Go to AWS Config > Rules
    - Confirm any custom rules are present and in COMPLIANT state
    - Check that the underlying Lambda function(s) exist

## Module 4: Security Hub

- [ ] **4.1 Security Hub is enabled**
  - Verification:
    - Go to Security Hub
    - Confirm service is enabled and dashboard is accessible

- [ ] **4.2 Security standards are enabled**
  - Verification:
    - Go to Security Hub > Security standards
    - Confirm the following standards are enabled:
      - AWS Foundational Security Best Practices
      - CIS AWS Foundations Benchmark
      - PCI DSS (if applicable)

- [ ] **4.3 Security Hub integrations are configured**
  - Verification:
    - Go to Security Hub > Integrations
    - Confirm the following integrations are enabled:
      - AWS Config
      - IAM Access Analyzer
      - GuardDuty (if enabled)
      - Inspector (if enabled)

- [ ] **4.4 Critical and high security findings are addressed**
  - Verification:
    - Go to Security Hub > Findings
    - Filter by Critical and High severity
    - Confirm there are no unresolved critical findings
    - Document action plan for any high findings

## Module 5: Cost Controls

- [ ] **5.1 AWS Budget is configured**
  - Verification:
    - Go to AWS Cost Management > Budgets
    - Confirm a monthly cost budget exists
    - Verify budget alerts are configured at 50%, 80%, and 100%
    - Confirm proper email notifications are set up

- [ ] **5.2 Cost Explorer is enabled**
  - Verification:
    - Go to AWS Cost Management > Cost Explorer
    - Confirm Cost Explorer is enabled
    - Verify that saved reports have been created
    - Confirm report delivery is scheduled

## End-to-End Validation Test

Perform these tests to validate your implementation works as expected:

- [ ] **Test IAM Identity Center login**
  - Sign out and sign in through the AWS access portal URL
  - Use your Identity Center credentials and MFA
  - Expected result: Successful login and access to assigned AWS account

- [ ] **Test CloudTrail logging**
  - Make a permissions change (create/delete a test policy)
  - Wait 15 minutes
  - Check CloudTrail for the event
  - Expected result: Event should be logged

- [ ] **Test CloudWatch alarm**
  - Temporarily log in as root user (with MFA)
  - Wait for alarm to trigger
  - Expected result: Should receive an email alert

- [ ] **Test AWS Config rule**
  - Create a test S3 bucket with public write access
  - Wait 15-30 minutes
  - Check AWS Config
  - Expected result: Should show a compliance failure

- [ ] **Test Security Hub**
  - Review Security Hub dashboard
  - Expected result: Should show improved security score following implementations

- [ ] **Test Budget alert** (optional, requires spending money)
  - Deploy a small resource that will trigger a budget alert
  - Expected result: Should receive budget notification

## Troubleshooting Common Issues

If any validations fail, refer to these common issues and solutions:

1. **IAM Password Policy not working**
   - Ensure you clicked "Save changes" after configuring policy
   - Try setting policy via AWS CLI to bypass potential console issues

2. **CloudTrail not logging events**
   - Verify trail is enabled for all regions
   - Check S3 bucket permissions
   - Allow up to 15 minutes for events to appear

3. **CloudWatch alarms not triggering**
   - Verify SNS topic subscription was confirmed
   - Check metric filter syntax
   - Ensure alarm threshold is configured correctly

4. **AWS Config rules showing "Evaluating"**
   - Rules can take 30+ minutes to evaluate first time
   - Check IAM permissions for AWS Config service
   - Verify Config recorder is enabled

5. **Security Hub showing incomplete results**
   - Initial scan can take 24+ hours to complete
   - Ensure AWS Config is properly configured
   - Check IAM permissions for Security Hub

## Next Steps After Validation

Once all checks pass:
- [ ] Document your implemented security controls
- [ ] Take screenshots of key configurations for your portfolio
- [ ] Consider implementing the optional challenges in [challenges.md](challenges.md)
- [ ] Progress to [Lab 2: Identity and Access Management](../lab-2-identity-access-management/)

---

**Note**: Keep this checklist for future reference. It can be used during compliance audits to demonstrate your security controls. 
