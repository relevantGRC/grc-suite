# Lab 1: AWS Account Governance - Step-by-Step Implementation Guide

This guide provides detailed instructions for implementing AWS account security governance controls following best practices from the AWS Well-Architected Framework.

## Prerequisites

Before beginning this lab, ensure you have:

- An AWS account with administrator access
- AWS CLI installed and configured on your local machine
- AWS CloudFormation knowledge for deployment
- Basic familiarity with AWS Console navigation

## Estimated Time

- **Complete Lab**: 2-3 hours
- **Module 1**: 30 minutes
- **Module 2**: 45 minutes
- **Module 3**: 45 minutes
- **Module 4**: 30 minutes
- **Module 5**: 15 minutes

## Module 1: Identity Center and IAM Security Foundations

In this module, you'll implement AWS IAM Identity Center (formerly AWS SSO) and baseline IAM security controls to protect your AWS account.

### Step 1.1: Enable MFA for Root User

1. Sign in to the AWS Management Console as the root user
2. In the navigation bar, click on your account name, then "Security credentials"
3. In the "Multi-factor authentication (MFA)" section, click "Assign MFA device"
4. Choose your preferred MFA device type (Virtual, Security Key, or Hardware)
5. Follow the on-screen instructions to complete the setup
6. Verify that MFA status shows "Assigned" for your root user

**Important**: Store your MFA device and backup codes securely. Losing access to your MFA device without backup recovery options could lock you out of your account.

### Step 1.2: Enable AWS IAM Identity Center

1. Navigate to the AWS IAM Identity Center service in the AWS Management Console
2. Click "Enable" to start the setup process
3. Choose "Default IAM Identity Center directory" as the identity source
   - Note: For production environments, you might prefer Microsoft Active Directory, Okta, or another identity provider
4. Click "Next" to complete the setup

### Step 1.3: Create an Administrative User in Identity Center

1. In the IAM Identity Center console, navigate to "Users" in the left sidebar
2. Click "Add user"
3. Fill out the user details:
   - Username (e.g., "admin")
   - Email address
   - First name and Last name
   - Confirm email
4. Click "Next"
5. On the "Add user to groups" page, click "Next" (we'll create groups in the next step)
6. Review the information and click "Add user"

### Step 1.4: Set Up MFA for Identity Center User

1. Stay in the IAM Identity Center console and navigate to "Users"
2. Select the administrative user you just created
3. Under the "MFA devices" tab, click "Register MFA device"
4. Choose your preferred MFA type (Authenticator app, Security key, or Built-in authenticator)
5. Follow the prompts to register the MFA device
6. Click "Register MFA device" to complete the process

### Step 1.5: Create Permission Sets

1. In the IAM Identity Center console, navigate to "Permission sets" in the left sidebar
2. Click "Create permission set"
3. Select "Predefined permission set"
4. Choose "AdministratorAccess" for your admin user
5. Click "Next"
6. Provide a name for the permission set (e.g., "AdministratorAccess")
7. Click "Next", review the information, and click "Create"
8. Repeat the process to create additional permission sets for different job functions:
   - Select "Predefined permission set" again
   - Choose "ReadOnlyAccess" for auditors or viewers
   - Click "Next", provide a name, and create the permission set

### Step 1.6: Assign Users to AWS Accounts

1. In the IAM Identity Center console, navigate to "AWS accounts" in the left sidebar
2. Select your AWS account
3. Click "Assign users or groups"
4. Select "Users" and choose your administrative user
5. Click "Next"
6. Select the "AdministratorAccess" permission set
7. Click "Next", review the information, and click "Submit"

### Step 1.7: Set up IAM Access Analyzer

1. Navigate to IAM Service
2. Click "Access analyzer" in the left navigation pane
3. Click "Create analyzer"
4. Set "Analyzer name" to "AccountAnalyzer"
5. For "Zone of trust", select "Current account"
6. Click "Create analyzer"

## Module 2: Logging and Monitoring Setup

In this module, you'll implement comprehensive logging and monitoring controls.

### Step 2.1: Configure CloudTrail

1. Navigate to CloudTrail service
2. Click "Create trail"
3. Set "Trail name" to "AccountTrail"
4. Under "Storage location", choose "Create new S3 bucket"
5. Set a unique bucket name (e.g., "accounttrail-logs-[account-id]")
6. Under "Additional settings":
   - Enable "Log file validation"
   - Enable "Enable for all accounts in my organization" if using AWS Organizations
   - Enable SSE-KMS encryption and choose "Create a new KMS key"
   - Set key alias to "cloudtrail-key"
7. Under "Additional configuration":
   - Select "Management events"
   - Select "All" for Read and Write events
   - Enable "Insights events" for enhanced monitoring
8. Click "Next" and then "Create trail"

### Step 2.2: Set up CloudWatch Alarms for CloudTrail

1. Navigate to CloudWatch service
2. Click "Alarms" in the left navigation pane
3. Click "Create alarm"
4. Click "Select metric"
5. Select "CloudTrail" > "By Trail Name"
6. Select your trail and the "Management events" metric
7. Click "Select metric"
8. Set the threshold to "Static", "Greater/Equal", and enter "1" as the value
9. Click "Next"
10. For alarm state, choose "In alarm"
11. Create a new SNS topic named "SecurityAlerts"
12. Add your email address as a notification target
13. Click "Create topic"
14. Click "Next", set name to "CloudTrailChangesAlarm"
15. Click "Create alarm"
16. Confirm the subscription in the email you receive

### Step 2.3: Create Key CloudWatch Alarms

Repeat the process to create the following essential security alarms:

1. **Root Login Alarm**:
   - Metric: CloudTrail metric filter for "$.userIdentity.type = Root"
   - Alarm: Trigger when ≥ 1

2. **IAM Policy Changes Alarm**:
   - Metric: CloudTrail metric filter for IAM policy changes
   - Alarm: Trigger when ≥ 1

3. **Console Login Failures Alarm**:
   - Metric: ConsoleSignInFailureCount
   - Alarm: Trigger when ≥ 3 in 5 minutes

## Module 3: AWS Config and Compliance

In this module, you'll set up AWS Config for continuous compliance monitoring.

### Step 3.1: Enable AWS Config

1. Navigate to AWS Config service
2. Click "Get started" or "Settings" (if already configured)
3. Under "Settings":
   - Select "Record all resources supported in this region"
   - Keep "Include global resources" checked
4. Under "Delivery method":
   - Choose "Create a new S3 bucket"
   - Set a unique bucket name (e.g., "config-bucket-[account-id]")
5. Enable "Enable Amazon SNS topic" and create a new topic named "ConfigAlerts"
6. Click "Next"
7. Skip adding rules for now (click "Next" without selecting any rules)
8. Click "Confirm" to enable AWS Config

### Step 3.2: Deploy Config Rules Using CloudFormation

Now that you have AWS Config set up, you'll use CloudFormation to deploy a set of fundamental security rules:

1. Navigate to the CloudFormation service
2. Click "Create stack" > "With new resources (standard)"
3. Under "Specify template":
   - Select "Upload a template file"
   - Click "Choose file" and select the `account-governance.yaml` file from the provided lab files
4. Click "Next"
5. Enter a stack name (e.g., "config-security-rules")
6. Click "Next", then "Next" again on the Configure stack options page
7. Review the settings and click "Create stack"
8. Wait for the stack creation to complete (Status: CREATE_COMPLETE)

This CloudFormation template deploys five essential AWS Config rules:
- IAM Password Policy check
- Root account MFA check
- IAM User MFA check
- CloudTrail enabled check
- S3 bucket public write protection check


## Module 4: Security Hub Implementation

In this module, you'll implement AWS Security Hub for centralized security management.

### Step 4.1: Enable Security Hub

1. Navigate to AWS Security Hub
2. Click "Go to Security Hub"
3. On the welcome page, click "Enable Security Hub"
4. Select the following security standards:
   - AWS Foundational Security Best Practices
   - CIS AWS Foundations Benchmark
   - PCI DSS v3.2.1 (if applicable to your organization)
5. Click "Enable Security Hub"

### Step 4.2: Configure Security Hub Settings

1. In Security Hub, click "Settings" in the left navigation pane
2. Under "Configuration":
   - Enable "Automatically enable new controls when added to standards"
   - Enable "Enable Security Hub in new accounts automatically"
3. Under "Integrations", enable the following:
   - Amazon GuardDuty (if enabled)
   - Amazon Inspector (if enabled)
   - AWS IAM Access Analyzer
   - AWS Config
4. Click "Save"

### Step 4.3: Review Security Hub Dashboard

1. In Security Hub, click "Summary" in the left navigation pane
2. Review your current security posture
3. Note any critical or high severity findings for immediate remediation
4. Click on "Insights" to review predefined security insights

## Module 5: Cost Controls and Budget Alerts

In this module, you'll implement cost management controls.

### Step 5.1: Set up AWS Budgets

1. Navigate to AWS Budgets (via AWS Cost Management)
2. Click "Create budget"
3. Select "Use a template" and choose "Monthly cost budget"
4. Set a realistic budget amount based on your expected usage
5. Configure alerts at 50%, 80%, and 100% of your budget
6. Add email recipients for the alerts
7. Click "Create budget"

### Step 5.2: Configure Cost Explorer

1. Navigate to Cost Explorer
2. Enable Cost Explorer if not already enabled
3. Create saved reports for:
   - Monthly costs by service
   - Costs by tag (once you've implemented tagging)
4. Schedule these reports to be emailed monthly

## Validation and Testing

After completing all modules, perform the following validation tests:

1. **IAM Password Policy**: Attempt to create a user with a weak password (should fail)
2. **MFA**: Attempt to access the console without MFA (should require MFA)
3. **CloudTrail**: Make a test API call and verify it appears in CloudTrail logs
4. **CloudWatch Alarms**: Trigger a test alarm to verify notifications
5. **AWS Config**: Make a change that violates a rule and verify that Config detects it
6. **Security Hub**: Review findings and verify that controls are properly evaluating
7. **Budgets**: Verify that budget alerts are properly configured

## Clean-up Instructions

If you deployed this lab for learning purposes and wish to avoid ongoing charges:

1. **AWS Config**: Turn off AWS Config recording
2. **CloudTrail**: Delete the CloudTrail trail
3. **S3**: Empty and delete the CloudTrail and Config S3 buckets
4. **CloudWatch**: Delete the CloudWatch alarms
5. **SNS**: Delete the SNS topics
6. **Security Hub**: Disable Security Hub

**Note**: Only perform these clean-up steps if you're sure you no longer need these security controls. In a production environment, these controls should remain enabled.

## Next Steps

After completing this lab, consider:

1. Enabling additional security services like Amazon GuardDuty for threat detection
2. Implementing more comprehensive tagging strategies for resource management
3. Setting up more detailed monitoring and alerting
4. Stay tuned for future lab releases that will build on these security foundations

## Additional Resources

- [AWS Security Best Practices](https://aws.amazon.com/architecture/security-identity-compliance/best-practices/)
- [AWS Well-Architected Framework - Security Pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)
- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [AWS CloudTrail Documentation](https://docs.aws.amazon.com/cloudtrail/)
- [AWS Config Documentation](https://docs.aws.amazon.com/config/)
- [AWS Security Hub Documentation](https://docs.aws.amazon.com/securityhub/) 
