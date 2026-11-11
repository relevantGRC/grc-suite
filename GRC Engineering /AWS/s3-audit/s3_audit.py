"""
s3_audit.py
Audits all S3 buckets in your AWS account for security compliance.
Checks performed:
    1. Encryption - Is server-side encryption enabled?
    2. Public Access Block - Are all four public access block settings enabled?
Output:
    [PASS] - Check passed
    [WARN] - Partially configured (some settings missing)
    [FAIL] - Not configured
Usage:
    python s3_audit.py
Requirements:
    - boto3 installed (pip install boto3)
    - AWS credentials configured (aws configure)
"""
# Import associated AWS module for script.
import boto3

# Setup: Create AWS client and get all buckets.
# Create S3 client to interact with AWS S3 service. 
s3 = boto3.client('s3')

# Get list of all buckets in the account. 
response = s3.list_buckets()
buckets = response['Buckets']

# Counter to track how many buckets pass all checks.
compliant_count = 0
total_buckets = len(buckets)
print(f"Found {len(buckets)} buckets.\n")

# Main loop to check each bucket for compliance
for bucket in buckets:
    bucket_name = bucket['Name']
    print(f"Checking bucket: {bucket_name}")

    # Flags to track if each check passes (start as False)
    encryption_ok = False
    public_block_ok = False

    # Check 1: Encryption
    # If encryption isn't configured, AWS throws an error (not empty response).
    try:
        enc = s3.get_bucket_encryption(Bucket=bucket_name)

        # Dig into the nested response to get the encryption type (e.g., "AES256")
        enc_type = enc['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']
        print(f"    [PASS] Encryption: {enc_type}")
        encryption_ok = True
    except s3.exceptions.ClientError:
        print(f"    [FAIL] Encryption: Not configured")

    # Check 2: Public Access Block
    # Buckets should have all four public access block settings set to True.
    try:
        pab = s3.get_public_access_block(Bucket=bucket_name)
        block_config = pab['PublicAccessBlockConfiguration']

        # all() returns True only if ALL four settings are True.
        all_blocked = all([
            block_config.get('BlockPublicAcls', False),
            block_config.get('IgnorePublicAcls', False),
            block_config.get('BlockPublicPolicy', False),
            block_config.get('RestrictPublicBuckets', False)
        ])

        if all_blocked:
            print(f"    [PASS] Public Access Block: Enabled")
            public_block_ok = True
        else:
            print(f"    [WARN] Public Access Block: Partially configured")
            
    except s3.exceptions.ClientError:
        print(f"    [FAIL] Public Access Block: Not configured")

    # Count fully compliant buckets. Only counts if BOTH checks passed.
    if encryption_ok and public_block_ok:
        compliant_count += 1

# Summary
print("\n" + "=" * 40)
print(f"Summary: {compliant_count} of {total_buckets} buckets fully compliant.")
