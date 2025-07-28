# AWS Security Services Reference Guide

## Additional Resources

### AWS Documentation
- [Security Documentation](https://docs.aws.amazon.com/security/)
- [Security Blog](https://aws.amazon.com/blogs/security/)
- [Whitepapers](https://aws.amazon.com/whitepapers/#security)
- [Reference Architectures](https://aws.amazon.com/architecture/)

### Tools and Utilities
- [AWS CLI](https://aws.amazon.com/cli/)
- [CloudFormation](https://aws.amazon.com/cloudformation/)
- [AWS CDK](https://aws.amazon.com/cdk/)
- [AWS SDK](https://aws.amazon.com/tools/)

### Best Practices
- [Security Pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/)
- [Security Checklist](https://d1.awsstatic.com/whitepapers/Security/AWS_Security_Checklist.pdf)
- [Compliance Programs](https://aws.amazon.com/compliance/programs/)
- [Partner Solutions](https://aws.amazon.com/security/partner-solutions/)

## Identity and Access Management

### AWS IAM
- **Purpose**: Manage access to AWS services and resources
- **Key Features**:
  - Users, groups, and roles
  - Policy management
  - Access key management
  - MFA support
- **Best Practices**:
  - Use least privilege
  - Implement MFA
  - Rotate credentials
  - Regular access reviews

### AWS SSO
- **Purpose**: Centralized access management
- **Key Features**:
  - Single sign-on
  - Directory integration
  - Permission sets
  - Access portal
- **Best Practices**:
  - Configure MFA
  - Use permission sets
  - Regular user reviews
  - Monitor access

## Network Security

### AWS Network Firewall
- **Purpose**: Network traffic filtering
- **Key Features**:
  - Stateful inspection
  - Protocol detection
  - Domain filtering
  - IPS capabilities
- **Best Practices**:
  - Layer defense
  - Monitor logs
  - Regular updates
  - Test rules

### AWS WAF
- **Purpose**: Web application protection
- **Key Features**:
  - Rule sets
  - Rate limiting
  - IP blocking
  - Bot control
- **Best Practices**:
  - Use managed rules
  - Custom rules
  - Monitor metrics
  - Regular updates

## Data Protection

### AWS KMS
- **Purpose**: Key management
- **Key Features**:
  - Key rotation
  - Access control
  - Audit logging
  - Integration
- **Best Practices**:
  - Enable rotation
  - Monitor usage
  - Access controls
  - Regular audits

### AWS Macie
- **Purpose**: Data discovery and protection
- **Key Features**:
  - Data discovery
  - Classification
  - Monitoring
  - Alerts
- **Best Practices**:
  - Regular scans
  - Custom identifiers
  - Alert review
  - Remediation

## Detection and Response

### Amazon GuardDuty
- **Purpose**: Threat detection
- **Key Features**:
  - ML detection
  - Threat intel
  - API monitoring
  - DNS monitoring
- **Best Practices**:
  - Enable all features
  - Review findings
  - Automate response
  - Regular tuning

### AWS Security Hub
- **Purpose**: Security posture management
- **Key Features**:
  - Compliance checks
  - Finding aggregation
  - Automated response
  - Dashboards
- **Best Practices**:
  - Enable standards
  - Review findings
  - Custom actions
  - Regular review

## Infrastructure Protection

### AWS Shield
- **Purpose**: DDoS protection
- **Key Features**:
  - Layer 3/4 protection
  - Layer 7 protection
  - Cost protection
  - DRT support
- **Best Practices**:
  - Enable Advanced
  - Configure alerts
  - Monitor metrics
  - Regular testing

### AWS Systems Manager
- **Purpose**: System management
- **Key Features**:
  - Patch management
  - Configuration
  - Automation
  - Session management
- **Best Practices**:
  - Regular patching
  - Secure sessions
  - Monitor changes
  - Audit access

## Compliance and Governance

### AWS Config
- **Purpose**: Resource configuration tracking
- **Key Features**:
  - Configuration history
  - Compliance rules
  - Resource inventory
  - Change tracking
- **Best Practices**:
  - Enable recording
  - Custom rules
  - Regular review
  - Remediation

### AWS Audit Manager
- **Purpose**: Audit management
- **Key Features**:
  - Evidence collection
  - Framework mapping
  - Assessment management
  - Report generation
- **Best Practices**:
  - Regular assessments
  - Custom frameworks
  - Evidence review
  - Report sharing


## Service Comparison Matrix

| Service | Purpose | Use Case | Integration Points |
|---------|---------|----------|-------------------|
| GuardDuty | Threat Detection | Continuous monitoring | Security Hub, EventBridge |
| Macie | Data Protection | PII discovery | Security Hub, S3 |
| WAF | Application Protection | Web filtering | CloudFront, ALB |
| Shield | DDoS Protection | Network defense | WAF, Route 53 |
| Config | Compliance | Configuration tracking | Security Hub, S3 |

## Cost Optimization

### Service Pricing
- GuardDuty: Per volume
- Macie: Per GB
- WAF: Per rule/request
- Config: Per rule/item
- KMS: Per key/operation

### Optimization Tips
1. Enable necessary features
2. Monitor usage
3. Regular cleanup
4. Use tiered pricing
5. Consolidate resources
