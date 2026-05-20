resource "google_storage_bucket" "audit_logs" {
  name     = "gcp-audit-logs-eac-2026"
  location = "US"
}
