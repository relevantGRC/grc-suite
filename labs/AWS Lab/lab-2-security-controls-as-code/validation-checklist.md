# Validation Checklist: Security Controls as Code

Use this checklist to verify that all baseline security controls have been implemented in your AWS CloudFormation templates and AWS environment.

- [ ] Principle of least privilege enforced for all resources
- [ ] Network segmentation (e.g., VPC, security groups, NACLs)
- [ ] Logging enabled for all critical resources (e.g., CloudTrail, S3 access logs)
- [ ] Monitoring and alerting configured (e.g., CloudWatch, Security Hub)
- [ ] No hardcoded secrets in code (use AWS Secrets Manager/SSM Parameter Store)
- [ ] Resource tags for ownership and environment
- [ ] Encryption at rest and in transit enabled

---

Add additional controls as required by your organization or instructor.
