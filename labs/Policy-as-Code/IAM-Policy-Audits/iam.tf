resource "aws_iam_policy" "bad_policy" {
  name        = "bad_policy"
  path        = "/"
  description = "A terrible idea."

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "*"
        Resource = "*"
      }
    ]
  })
}
