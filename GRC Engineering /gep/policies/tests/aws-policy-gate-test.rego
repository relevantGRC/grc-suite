package compliance.aws_policy_gate_test

import rego.v1

test_sc28_rejects_bucket_without_encryption if {
    plan := {
        "configuration": {
            "root_module": {
                "resources": [
                    {
                        "type": "aws_s3_bucket",
                        "name": "primary"
                    }
                ]
            }
        }
    }

    denials := data.compliance.sc28_aws.deny with input as plan
    count(denials) == 1
}

test_ac3_rejects_missing_public_access_block if {
    plan := {
        "configuration": {
            "root_module": {
                "resources": [
                    {
                        "type": "aws_s3_bucket",
                        "name": "primary"
                    }
                ]
            }
        }
    }

    denials := data.compliance.ac3_aws.deny with input as plan
    count(denials) == 1
}

test_cm6_rejects_missing_required_tags if {
    plan := {
        "planned_values": {
            "root_module": {
                "resources": [
                    {
                        "address": "aws_s3_bucket.primary",
                        "type": "aws_s3_bucket",
                        "values": {
                            "tags_all": {
                                "Project": "cgep-lab"
                            }
                        }
                    }
                ]
            }
        }
    }

    denials := data.compliance.cm6_aws.deny with input as plan
    count(denials) == 1
}
