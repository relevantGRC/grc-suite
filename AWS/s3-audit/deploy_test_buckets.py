"""
deploy_test_buckets.py
Creates test S3 buckets with different security configurations.
Used to test s3_audit.py with various compliance scenarios.
Buckets created:
    1. grce-audit-compliant - Full public access block (should PASS)
    2. grce-audit-no-block - No public access block (should FAIL)
    3. grce-audit-partial - Partial public access block (should WARN)
Usage:
    python deploy_test_buckets.py
Cleanup:
    aws s3 rb s3://grce-audit-compliant-<account_id>
    aws s3 rb s3://grce-audit-no-block-<account_id>
    aws s3 rb s3://grce-audit-partial-<account_id>
Requirements:
    - boto3 installed (pip install boto3)
    - AWS credentials configured (aws configure)
"""
# Import associated AWS module for script.
import boto3

# Setup: Create AWS clients and get account info

# S3 client for bucket operations
s3 = boto3.client('s3')

# STS client to get account ID (so we don't hardcode it).
sts = boto3.client('sts')

# Session to get the configured region.
session = boto3.session.Session()
region = session.region_name

# Get account ID dynamically - makes bucket names unique and portable.
account_id = sts.get_caller_identity()['Account']
print(f"Region: {region}")
print(f"Account ID: {account_id}")

# Configuration: Define buckets to create.
# List of dictionaries - each dict defines one bucket and its settings.
buckets_to_deploy = [
    {
        "name": f"grce-audit-compliant-{account_id}",
        "public_block": "full",  # All 4 settings True → PASS
    },
    {
        "name": f"grce-audit-no-block-{account_id}",
        "public_block": "none",  # No settings → FAIL
    },
    {
        "name": f"grce-audit-partial-{account_id}",
        "public_block": "partial"  # Some settings True → WARN
    }
]

print(f"Will create {len(buckets_to_deploy)} buckets.")

# Main Loop: Create and configure each bucket.
for bucket_config in buckets_to_deploy:
    bucket_name = bucket_config["name"]

    # Step 1: Create the bucket
    # Note: us-east-1 doesn't need LocationConstraint, other regions require it.
    try:
        if region == "us-east-1":
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': region}
            )
        print(f"Created {bucket_name}.")
    except s3.exceptions.BucketAlreadyOwnedByYou:

        # Bucket already exists in our account.
        print(f"Already exists: {bucket_name}")

    # Step 2: Configure public access block based on config
    public_block = bucket_config["public_block"]

    if public_block == "full":

        # Enable ALL four public access block settings.
        s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
        )
        print(f"    → Full public access block enabled")

    elif public_block == "partial":

        # Enable only SOME settings (to trigger WARN in audit).
        s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False
            }
        )
        print(f"  → Partial public access block (will trigger WARN)")

    elif public_block == "none":

        # Remove public access block entirely (to trigger FAIL in audit)
        try:
            s3.delete_public_access_block(Bucket=bucket_name)
            print(f"  → Public access block removed (will trigger FAIL)")
        except:
            # Might not exist yet.
            pass
