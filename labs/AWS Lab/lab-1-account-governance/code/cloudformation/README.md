# AWS Config Rules CloudFormation Template

This directory contains a CloudFormation template that implements essential AWS Config rules for monitoring security compliance in your AWS account.

## Template Overview

The `account-governance.yaml` template implements the following AWS Config rules:

- **IAM Password Policy** - Checks if your account's password policy meets security requirements
- **Root Account MFA** - Verifies that MFA is enabled for the root user 
- **IAM User MFA** - Checks if MFA is enabled for IAM users with console access
- **CloudTrail Enabled** - Confirms that AWS CloudTrail is properly configured
- **S3 Public Write** - Ensures S3 buckets don't allow public write access

## Prerequisites

Before deploying this template, you should have:

1. AWS account with permissions to create AWS Config Rules
2. AWS Config already enabled and configured in your account
3. Basic familiarity with AWS CloudFormation

## Important Notes 

1. **AWS Config Requirement**: This template deploys ONLY AWS Config rules, not all required resources. You must first manually configure AWS Config in your account as described in the lab's step-by-step guide.

2. **Partial Automation**: This template is intended for a semi-automated deployment approach and only handles the Config rules component of the lab. You'll still need to manually set up AWS Config, IAM Identity Center, CloudTrail, Security Hub, and other services as described in the step-by-step guide.

3. **AWS Organizations Compatibility**: If your account is part of an AWS Organization that uses organization-level Config rules, these account-level rules may be redundant.

## Deployment Instructions

### Using AWS Management Console

1. Sign in to the AWS Management Console and navigate to CloudFormation
2. Click "Create stack" > "With new resources (standard)"
3. Under "Specify template", select "Upload a template file"
4. Click "Choose file" and select the `account-governance.yaml` file
5. Click "Next"
6. Enter a Stack name (e.g., "config-security-rules")
7. Click "Next", review the stack options, and click "Next" again
8. Review the configuration, acknowledge IAM resource creation if prompted, and click "Create stack"
9. Wait for the stack creation to complete (typically 1-2 minutes)

### Using AWS CLI

```bash
aws cloudformation create-stack \
  --stack-name config-security-rules \
  --template-body file://account-governance.yaml \
  --capabilities CAPABILITY_IAM
```

## Post-Deployment Steps

After deploying the template:

1. Navigate to AWS Config in the console
2. Go to "Rules" to review your newly created Config rules
3. Wait a few minutes for the initial evaluation to complete
4. Check the compliance status of each rule and remediate any non-compliant resources

## Template Outputs

| Output | Description |
|--------|-------------|
| ConfigRulesDeployed | Confirmation that Config rules were successfully deployed |

## Security Benefits

- Provides automated, continuous assessment of security controls
- Helps identify security issues like missing MFA, weak password policies, and public S3 buckets
- Establishes a foundation for compliance monitoring
- Serves as an introduction to Infrastructure as Code (IaC) for security controls

## Cleanup

To remove all resources created by this template:

1. Go to the CloudFormation console
2. Select the stack you created
3. Click "Delete" and confirm the deletion

Alternatively, using AWS CLI:

```bash
aws cloudformation delete-stack --stack-name config-security-rules
```

## Troubleshooting

- **No Configuration Recorder**: If deployment fails with "NoAvailableConfigurationRecorder", ensure you have enabled AWS Config first
- **Permission errors**: Verify you have sufficient permissions to create AWS Config Rules 
- **Resource already exists**: If rules with the same names already exist, either delete them or modify the template
