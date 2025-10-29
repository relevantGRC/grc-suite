package main

# This rule denies policies that include Action = "*"
deny[msg] {
  statement := input.resource.aws_iam_policy[_].policy.Statement[_]
  statement.Action == "*"
  msg = "Wildcard action '*' is not allowed."
}

# This rule denies policies that include Resource = "*"
deny[msg] {
  statement := input.resource.aws_iam_policy[_].policy.Statement[_]
  statement.Resource == "*"
  msg = "Wildcard resource '*' is not allowed."
}
