# Step-by-Step Guide: Security Controls as Code

## 1. Review Baseline Security Controls
Review and discuss the following baseline security controls, which you will implement and validate in this lab. Remember: these controls are for demonstration and portfolio-building in a test or personal AWS account, not for production use.

- Principle of least privilege
- Network segmentation (e.g., VPC, security groups, NACLs)
- Logging enabled for all critical resources (e.g., S3 access logs)
- S3 bucket with encryption and public access block
- IAM role with least privilege (S3 read-only)
- Monitoring and alerting configured (e.g., CloudWatch, Security Hub)
- No hardcoded secrets in code (use AWS Secrets Manager/SSM Parameter Store)
- Resource tags for ownership and environment
- Encryption at rest and in transit enabled

## 2. Deploy Security Controls with AWS CloudFormation
- Navigate to the `code/` directory.
- Review the sample CloudFormation template provided. The template now includes:
  - VPC, Security Group, Flow Logs
  - S3 bucket with encryption and public access block
  - IAM role with least privilege
- Before deploying, validate your template with cfn-lint (recommended).

## 2a. Validate Your Template with cfn-lint (Recommended)

Before deploying your CloudFormation template, use [cfn-lint](https://github.com/aws-cloudformation/cfn-lint) to catch syntax and best practice errors locally. This tool helps you avoid common mistakes and failed deployments.

- **Install:**
  ```sh
  pip install cfn-lint
  ```
- **Usage:**
  Run this command in the directory containing your template:
  ```sh
  cfn-lint security-controls-baseline.yaml
  ```
- **Why use cfn-lint?**
  - Detects YAML/JSON syntax errors
  - Flags unsupported or misspelled properties
  - Highlights best practice violations
  - Saves time by catching issues before deployment

**Tip:** Always run `cfn-lint` before deploying with the AWS CLI or Console!

## 2b. Deploy the CloudFormation Template

- Deploy the template to your AWS environment (preferably a test or personal account).

  ### How to Deploy the CloudFormation Template

  #### Option 1: Using the AWS Console
  1. Sign in to the [AWS Management Console](https://console.aws.amazon.com/).
  2. Navigate to the CloudFormation service.
  3. Click **Create stack** > **With new resources (standard)**.
  4. Under **Specify template**, select **Upload a template file**.
  5. Click **Choose file** and upload `security-controls-baseline.yaml` from the `code/` directory.
  6. Click **Next** and follow the prompts to configure stack details and options.
  7. Click **Create stack** to deploy.

  #### Option 2: Using the AWS CLI
  1. Ensure you have the [AWS CLI installed and configured](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).
  2. Run the following command from the `code/` directory:

     ```sh
     aws cloudformation create-stack \
       --stack-name security-controls-stack \
       --template-body file://security-controls-baseline.yaml \
       --capabilities CAPABILITY_NAMED_IAM
     ```

  3. Monitor stack creation in the AWS Console or with:
     ```sh
     aws cloudformation describe-stacks --stack-name security-controls-stack
     ```

- Customize the template to fit your learning or portfolio-building goals.

## 3. Validate and Test
- Use the `validation-checklist.md` to ensure all controls are implemented.
- Optionally, run AWS-native security tools (e.g., AWS Config, Security Hub) to validate your templates.

## 4. Cleanup
- Delete the deployed resources using CloudFormation to avoid unnecessary costs.

---

If you have questions, refer to the documentation links in the `README.md` or ask your instructor.
