package s3

deny[reason] {
  input.PublicAccessBlockConfiguration.BlockPublicAcls == false
  reason = "S3 bucket allows public ACLs"
}
