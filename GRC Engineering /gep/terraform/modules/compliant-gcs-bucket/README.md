# Compliant GCS Bucket Module

This reusable Terraform module provisions a Google Cloud Storage bucket with a customer-managed encryption key and built-in compliance controls.

The module implements cryptographic key management (SC-12), cryptographic protection and key rotation (SC-13), encryption at rest (SC-28), access restrictions through uniform bucket-level access and public access prevention (AC-3), retention policy enforcement (AU-11), and required configuration labels (CM-6).

Production configurations must specify at least 365 days of retention. The module exposes a machine-readable compliance attestation for validation and audit evidence.
