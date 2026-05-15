package policies.access

default allow = true

deny[msg] {
  input.user.role == "admin"
  not input.user.mfa_enabled
  msg := "Admin users must have MFA enabled"
}

allow {
  not deny[_]
}
