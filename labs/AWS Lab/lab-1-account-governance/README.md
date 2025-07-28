# Lab 1: AWS Account Governance and Security Foundations

## Learning Objectives

By completing this lab, you will be able to:

- Implement AWS account security foundations following best practices
- Configure AWS IAM Identity Center (SSO) and enforce MFA
- Set up AWS Config for compliance monitoring
- Implement AWS Security Hub for centralized security management
- Establish cost controls and budget alerts

## AWS Services Used

- AWS IAM Identity Center (formerly AWS SSO)
- AWS Identity and Access Management (IAM)
- AWS Config
- AWS Security Hub
- AWS CloudTrail
- AWS Budgets

## Estimated Time to Complete

2-3 hours

## AWS Free Tier Usage

This lab primarily uses services that are included in the AWS Free Tier or have minimal costs:
- AWS Config: Free Tier includes 5 rules per month
- AWS Security Hub: 30-day free trial
- AWS CloudTrail: Free Tier includes one trail

**Estimated cost if running continuously beyond Free Tier**: $1-5 per day

## Prerequisites

Before starting this lab, you should have:

1. An AWS account with administrator access
2. AWS CLI configured on your local machine
3. Basic familiarity with AWS console navigation
4. Git installed on your local machine

## Architecture Overview

This lab implements a foundational security architecture including:

- Centralized logging with CloudTrail
- Compliance monitoring with AWS Config
- Security posture management with Security Hub
- Cost management with AWS Budgets

## Lab Components

- [Step-by-Step Guide](step-by-step-guide.md) - Detailed implementation instructions
- [Validation Checklist](validation-checklist.md) - Verify your implementation
- [Assessment Worksheet](assessment-worksheet.md) - Document your implementation and reflections
- [Architecture Diagram Template](architecture-diagram-template.md) - Guide for creating visual diagrams

## Deployment Options

This lab can be implemented through two main approaches:

### 1. Manual Implementation
Follow the [Step-by-Step Guide](step-by-step-guide.md) to manually configure each service through the AWS Management Console or CLI. This approach provides a hands-on learning experience by directly interacting with each service.

### 2. Semi-Automated Deployment 
For a hybrid implementation approach, use the provided automation tools:

- **CloudFormation Template**: 
  - Located in [code/cloudformation/](code/cloudformation/)
  - Specifically focuses on deploying essential AWS Config rules
  - Designed to be used after manually setting up AWS Config
  - Introduces Infrastructure as Code concepts with a focused template
  - See the CloudFormation README for detailed instructions

- **Support Scripts**:
  - Located in [code/scripts/](code/scripts/)
  - Includes scripts for validating compliance, generating security reports, and cleanup
  - Automates common tasks in the lab

## Module Overview

### Module 1: Identity Center and IAM Security Foundations
Configure AWS IAM Identity Center, enable MFA, and implement least privilege access with permission sets

### Module 2: Logging and Monitoring
Set up CloudTrail and CloudWatch for comprehensive logging and monitoring

### Module 3: AWS Config and Compliance
Deploy AWS Config and configure compliance rules

### Module 4: Security Hub Implementation
Enable Security Hub and configure security standards

### Module 5: Cost Controls
Implement AWS Budgets and cost optimization

## Skills Demonstrated

Completing this lab demonstrates your ability to:

- Implement AWS security best practices
- Deploy compliance automation
- Configure centralized security monitoring
- Manage costs in the AWS environment
- Use Infrastructure as Code (IaC) for security configurations
- Evaluate security posture and identify improvements
- Document security controls and their business value
- Design creative solutions to security challenges

## Next Steps

After completing this lab, continue exploring the other AWS security domains as they become available in future lab releases. Stay tuned for our upcoming labs focusing on Identity and Access Management and other crucial security domains.
