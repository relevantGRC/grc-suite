# policies/tests/cm6_required_tags_test.rego
package compliance.cm6_test

import data.compliance.cm6
import rego.v1

complete := {"planned_values": {"root_module": {"resources": [{
	"address": "google_storage_bucket.good", "type": "google_storage_bucket",
	"values": {"labels": {"project": "x", "environment": "dev", "managed_by": "terraform", "compliance_scope": "cge-p-lab"}},
}]}}}

missing := {"planned_values": {"root_module": {"resources": [{
	"address": "google_storage_bucket.bad", "type": "google_storage_bucket",
	"values": {"labels": {"project": "x"}},
}]}}}

no_labels := {"planned_values": {"root_module": {"resources": [{
	"address": "google_storage_bucket.naked", "type": "google_storage_bucket",
	"values": {},
}]}}}

test_complete_passes if {
	count(cm6.deny) == 0 with input as complete
}

test_partial_fails if {
	some msg in cm6.deny with input as missing
	contains(msg, "CM-6")
}

test_no_labels_fail if {
	some msg in cm6.deny with input as no_labels
	contains(msg, "CM-6")
}
