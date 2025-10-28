# Architecture Diagram Template: Security Controls as Code

Below is a template structure for visualizing your AWS security controls architecture. Use this as a guide for creating a detailed, professional diagram for your portfolio.

## Example Structure

- **AWS Account**
  - **VPC**
    - Public Subnet(s)
    - Private Subnet(s)
    - Security Groups (with rules for least privilege)
    - Network ACLs
    - Flow Logs
  - **S3 Bucket** (for logs, with access controls and encryption, public access block)
  - **CloudWatch** (alarms, metrics, dashboards)
  - **Security Hub** (centralized findings)
  - **IAM Roles/Policies** (for least privilege, e.g., S3 read-only)
  - **Secrets Manager/SSM** (for secrets management)
  - (Optional) **AWS Config**, **SNS Topics**, etc.

## Tips for Use
- Use AWS Architecture Icons for clarity
- Annotate security boundaries and data flows
- Add notes on control objectives for each resource

---

Customize this template to match your implementation and reflect on how each component contributes to security and compliance.
