# METADATA
# title: SC-28 - Encryption at Rest (AWS S3)
# description: "Every aws_s3_bucket must have an aws_s3_bucket_server_side_encryption_configuration that references it."
# custom:
#   control_id: SC-28
#   framework: nist-800-53
#   severity: high
#   remediation: "Add aws_s3_bucket_server_side_encryption_configuration { bucket = aws_s3_bucket.<name>.id ... } for the bucket."
package compliance.sc28_aws

import rego.v1

deny contains msg if {
    bucket := bucket_addresses[_]
    not has_encryption(bucket)
    msg := sprintf(
        "[SC-28] %s: aws_s3_bucket has no matching aws_s3_bucket_server_side_encryption_configuration. Remediation: add one referencing this bucket.",
        [bucket],
    )
}

bucket_addresses contains addr if {
    some r in input.configuration.root_module.resources
    r.type == "aws_s3_bucket"
    addr := sprintf("aws_s3_bucket.%s", [r.name])
}

has_encryption(bucket_addr) if {
    some r in input.configuration.root_module.resources
    r.type == "aws_s3_bucket_server_side_encryption_configuration"
    some ref in r.expressions.bucket.references
    references_bucket(ref, bucket_addr)
}

references_bucket(ref, bucket_addr) if ref == bucket_addr
references_bucket(ref, bucket_addr) if ref == sprintf("%s.id", [bucket_addr])
references_bucket(ref, bucket_addr) if ref == sprintf("%s.bucket", [bucket_addr])
