
terraform {
  required_version = ">= 1.6"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }

    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

provider "aws" {
  region = "us-east-1"

  # CM-6: Apply required compliance tags
  default_tags {
    tags = {
      Project         = var.project_name
      Environment     = var.environment
      ManagedBy       = "terraform"
      ComplianceScope = "cge-p-lab"
    }
  }
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

locals {
  effective_suffix = var.bucket_suffix != "" ? var.bucket_suffix : random_id.bucket_suffix.hex

  primary_name = "${var.project_name}-${var.environment}-data-${local.effective_suffix}"
  log_name     = "${var.project_name}-${var.environment}-logs-${local.effective_suffix}"
}

# Primary bucket
resource "aws_s3_bucket" "primary" {
  bucket = local.primary_name
}

# SC-28: Encrypt stored data
# Lab 4.3 exception: SSE-S3 accepted for this lab only.
# Review customer-managed KMS requirement by 2026-12-31.
#tfsec:ignore:aws-s3-encryption-customer-key:exp:2026-12-31
resource "aws_s3_bucket_server_side_encryption_configuration" "primary" {
  bucket = aws_s3_bucket.primary.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# CM-6: Enable versioning
resource "aws_s3_bucket_versioning" "primary" {
  bucket = aws_s3_bucket.primary.id

  versioning_configuration {
    status = "Enabled"
  }
}

# AC-3: Block public access
# Lab 4.3 green test: All four public-access-block settings remain enabled.
resource "aws_s3_bucket_public_access_block" "primary" {
  bucket                  = aws_s3_bucket.primary.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# AU-3 / AU-6: Bucket for access logs
resource "aws_s3_bucket" "log" {
  bucket = local.log_name
}

# Lab 4.3: Enable versioning for audit log recovery
resource "aws_s3_bucket_versioning" "log" {
  bucket = aws_s3_bucket.log.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_ownership_controls" "log" {
  bucket = aws_s3_bucket.log.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "log" {
  depends_on = [aws_s3_bucket_ownership_controls.log]

  bucket = aws_s3_bucket.log.id
  acl    = "log-delivery-write"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "log" {
  bucket = aws_s3_bucket.log.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "log" {
  bucket                  = aws_s3_bucket.log.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Send primary bucket access logs to log bucket
resource "aws_s3_bucket_logging" "primary" {
  bucket        = aws_s3_bucket.primary.id
  target_bucket = aws_s3_bucket.log.id
  target_prefix = "access-logs/"
}
