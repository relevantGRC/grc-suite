package main
import rego.v1

# AC-12: require a session timeout and cap it at 900 seconds (15 minutes)
# Expected input shape:
#   application:
#     settings:
#       session_timeout: number OR numeric string

# 1) Missing key entirely
deny contains msg if {
  not input.application.settings.session_timeout
  msg := "AC-12: 'session_timeout' is missing from application settings"
}

# 2) Empty string
deny contains msg if {
  input.application.settings.session_timeout == ""
  msg := "AC-12: 'session_timeout' is defined but empty"
}

# 3) Explicitly set to 'never'
deny contains msg if {
  input.application.settings.session_timeout == "never"
  msg := "AC-12: 'session_timeout' must not be 'never'"
}

# 4a) Too long when provided as a NUMBER
deny contains msg if {
  type_name(input.application.settings.session_timeout) == "number"
  input.application.settings.session_timeout > 900
  msg := sprintf(
    "AC-12: 'session_timeout' is %d seconds (exceeds 900)",
    [input.application.settings.session_timeout],
  )
}

# 4b) Too long when provided as a STRING containing only digits
deny contains msg if {
  val := input.application.settings.session_timeout
  type_name(val) == "string"
  regex.match("^[0-9]+$", val)
  to_number(val) > 900
  msg := sprintf(
    "AC-12: 'session_timeout' is %d seconds (exceeds 900)",
    [to_number(val)],
  )
}
