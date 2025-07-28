# Lab 2: Security Controls as Code

## Overview
This lab is designed for Governance, Risk, and Compliance (GRC) professionals to build their technical portfolios by implementing baseline AWS security controls as code. You will deploy and validate these controls in a test or personal AWS account, demonstrating your hands-on skills for career development or job-seeking purposes. While the lab can be adapted for organizational use, it is primarily intended for educational and portfolio-building scenarios.

## Objectives
- Understand the concept of Security Controls as Code
- Implement basic security controls using AWS-native IaC (CloudFormation)
- Validate and review security configurations

## Prerequisites
- Basic knowledge of cloud infrastructure (AWS)
- Familiarity with AWS native IaC tools (CloudFormation recommended)

## Lab Steps
1. **Review Baseline Security Controls**
   - Principle of least privilege
   - Network segmentation
   - Logging and monitoring basics
2. **Deploy Security Controls with IaC**
   - Use provided CloudFormation templates
   - Customize for your environment
3. **Validate and Test**
   - Use checklists or scripts to validate controls are in place

## Lab Components
- [Step-by-Step Guide](step-by-step-guide.md) - Detailed implementation instructions
- [Validation Checklist](validation-checklist.md) - Verify your implementation
- [Assessment Worksheet](assessment-worksheet.md) - Document your implementation and reflections
- [Architecture Diagram](architecture-diagram.md) - Visualize your lab environment
- [Architecture Diagram Template](architecture-diagram-template.md) - Guide for creating visual diagrams

## New Security Controls Demonstrated
- S3 Bucket with encryption and public access block
- IAM Role with least privilege (S3 read-only)

## Skills Demonstrated
Completing this lab demonstrates your ability to:
- Implement AWS security best practices
- Deploy compliance automation
- Configure centralized security monitoring
- Use Infrastructure as Code (IaC) for security configurations
- Evaluate security posture and identify improvements
- Document security controls and their business value
- Design creative solutions to security challenges

## Getting Started
- Clone or download this lab folder.
- Review the CloudFormation templates in the `code/` directory.
- Follow the step-by-step instructions in `step-by-step-guide.md`.

## Resources
- [CloudFormation Documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)
- [AWS Security Best Practices](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-standards-fsbp.html)
- [cfn-lint](https://github.com/aws-cloudformation/cfn-lint) - Linting tool for CloudFormation templates (recommended for validation)
