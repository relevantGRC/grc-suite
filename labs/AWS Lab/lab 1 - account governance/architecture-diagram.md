# Creating a Visual Architecture Diagram for Lab 1

This guide will help you create a professional architecture diagram for your AWS Account Governance implementation.

## Tools for Creating Architecture Diagrams

You can use any of these tools to create your architecture diagram:

1. **Draw.io (diagrams.net)** - Free web-based tool
   - Visit [https://app.diagrams.net/](https://app.diagrams.net/)
   - Use the AWS icon library included in the tool

2. **Lucidchart** - Robust web-based tool (free tier available)
   - Visit [https://www.lucidchart.com](https://www.lucidchart.com)
   - Import the AWS architecture icons

3. **PowerPoint/Keynote** - If you already have these tools
   - Download AWS icon sets (see resources below)

4. **AWS Architecture Icons** - Official AWS icons
   - Download from [https://aws.amazon.com/architecture/icons/](https://aws.amazon.com/architecture/icons/)

## Diagram Components to Include

Your Lab 1 architecture diagram should include these key elements:

### 1. Core Security Services
- IAM (Password Policy, MFA, Admin User)
- CloudTrail
- AWS Config
- Security Hub
- CloudWatch Alarms
- SNS Notifications
- AWS Budgets

### 2. Data Flows
- Show how CloudTrail logs flow to S3
- Illustrate how AWS Config snapshots are stored
- Demonstrate how alerts flow from CloudWatch to SNS

### 3. Security Controls
- IAM password policy parameters
- CloudTrail multi-region logging
- S3 bucket encryption and access policies
- Config Rules

## Sample Layout Guide

Here's a suggested layout for your diagram:

```
┌─────────────────────────────────────────────────────────────────┐
│                        AWS Account                              │
│                                                                 │
│  ┌─────────────┐            ┌─────────────┐     ┌────────────┐  │
│  │             │            │             │     │            │  │
│  │  IAM        │            │ CloudTrail  │     │AWS Config  │  │
│  │  Controls   │────┐  ┌────│             │     │            │  │
│  │             │    │  │    │             │     │            │  │
│  └─────────────┘    │  │    └──────┬──────┘     └──────┬─────┘  │
│                     │  │           │                   │        │
│                     │  │           │                   │        │
│                     ▼  ▼           ▼                   ▼        │
│               ┌────────────────────────────────────────────┐   │
│               │                                            │   │
│               │     Security Hub                           │   │
│               │                                            │   │
│               └───────────────────┬────────────────────────┘   │
│                                   │                            │
│                                   │                            │
│                                   ▼                            │
│  ┌─────────────┐            ┌─────────────┐     ┌────────────┐ │
│  │             │            │             │     │            │ │
│  │ CloudWatch  │────────────│ SNS Topic   │     │ Budget     │ │
│  │ Alarms      │            │             │     │ Controls   │ │
│  │             │            │             │     │            │ │
│  └─────────────┘            └─────────────┘     └────────────┘ │
│                                   │                            │
│                                   │                            │
│                                   ▼                            │
│                         ┌──────────────────┐                   │
│                         │  Email Alerts    │                   │
│                         │                  │                   │
│                         └──────────────────┘                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Best Practices for Clear Diagrams

1. **Color Coding**
   - Use different colors for different types of services
   - Example: Security services in red, logging in blue, notifications in green

2. **Labels and Annotations**
   - Label each service with its name
   - Add brief descriptions for key components
   - Include relevant configuration details

3. **Grouping**
   - Group related services together
   - Use boxes or boundaries to show logical groups

4. **Arrows and Flows**
   - Use arrows to show data flow between services
   - Use different line styles for different types of connections

## Open-Ended Design Elements

As you create your own architecture diagram, consider adding these elements to demonstrate your understanding:

1. **Multi-Account Structure** - How would this architecture expand across multiple AWS accounts?

2. **Defense in Depth** - How would you represent multiple security layers?

3. **Future Enhancements** - What additional services would you add to improve security?

4. **Compliance Mapping** - How would you map these controls to specific compliance frameworks?

## Example Integration Points

Consider how your architecture connects with these additional AWS services:

- GuardDuty for threat detection
- Macie for sensitive data discovery
- Inspector for vulnerability assessment
- AWS Backup for data protection
- AWS Organizations for multi-account management

## Submission

After creating your architecture diagram:

1. Export it as a PNG or PDF file
2. Place it in the lab-1-account-governance directory
3. Update your documentation to reference your visual diagram
4. Consider adding a brief explanation of your design choices

Remember, your architecture diagram should tell a story about your security controls and how they work together to provide a comprehensive security posture. 
