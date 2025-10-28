# Support Scripts for Lab 1: AWS Account Governance

This directory contains helpful scripts to assist with implementing, validating, and cleaning up the security controls deployed in Lab 1.

## Available Scripts

### 1. verify-compliance.sh

A utility script to check the compliance status of AWS Config rules in your account.

**Usage**:
```bash
# Default region (us-east-1)
./verify-compliance.sh

# Specify a region
./verify-compliance.sh us-west-2
```

**Features**:
- Displays compliance status for all AWS Config rules
- Shows count of non-compliant resources for each rule
- Provides a summary of compliant vs. non-compliant rules
- Works with the AWS Config setup from the lab

**Requirements**:
- AWS CLI installed and configured
- AWS Config enabled in your account
- Bash shell environment

### 2. cleanup.sh

A script to remove the security controls and resources created in Lab 1. Use this to clean up your AWS account after completing the lab.

**Usage**:
```bash
# Default region (us-east-1)
./cleanup.sh

# Specify a region
./cleanup.sh us-west-2
```

**Features**:
- Smart cleanup that detects whether CloudFormation was used
- Systematically removes all security controls in the proper order
- Provides guidance for manual cleanup tasks
- Confirms before proceeding with deletion

**Warning**:
This script removes security controls. Only use it in a lab/learning environment, not in production.

### 3. security-posture-report.sh

A comprehensive script that generates a detailed report of your AWS account's security posture by evaluating multiple security services.

**Usage**:
```bash
# Default region (us-east-1)
./security-posture-report.sh

# Specify a region
./security-posture-report.sh us-west-2
```

**Features**:
- Evaluates core security services (CloudTrail, Config, Security Hub, GuardDuty, Access Analyzer)
- Analyzes IAM security (password policy, MFA status, credential age)
- Checks AWS Config compliance status across all rules
- Summarizes Security Hub findings by severity
- Lists Access Analyzer findings identifying external access
- Verifies budget configurations
- Provides prioritized security recommendations
- Generates a comprehensive text report file

**Requirements**:
- AWS CLI installed and configured
- Appropriate read permissions across multiple AWS services
- `jq` command-line JSON processor installed
- Bash shell environment

**Output**:
The script generates a detailed report file named `security-posture-report-YYYY-MM-DD.txt` containing all findings and recommendations.

## Using These Scripts

1. Make the scripts executable:
   ```bash
   chmod +x verify-compliance.sh cleanup.sh security-posture-report.sh
   ```

2. Ensure you have the AWS CLI installed and configured with appropriate credentials:
   ```bash
   aws configure
   ```

3. Install jq if needed for the security posture report:
   ```bash
   # For Debian/Ubuntu
   sudo apt-get install jq
   
   # For Red Hat/CentOS
   sudo yum install jq
   
   # For macOS with Homebrew
   brew install jq
   ```

4. Run the scripts as needed during or after completing the lab

## Adding Your Own Scripts

Feel free to create additional scripts to enhance your learning experience. Some ideas:

- **auto-remediate.sh**: Automatically fix common compliance issues
- **cost-analyzer.sh**: Analyze the costs of the security controls deployed
- **compliance-mapper.sh**: Map AWS controls to specific compliance frameworks

## Troubleshooting

If you encounter issues with these scripts:

1. Ensure AWS CLI is properly installed and configured
2. Verify that you have sufficient permissions in your AWS account
3. Check that the resources referenced in the scripts exist in your account
4. Make sure you're targeting the correct AWS region
5. For the security posture report, ensure jq is installed and functioning

For specific error messages, consult the AWS CLI documentation for the respective services. 
