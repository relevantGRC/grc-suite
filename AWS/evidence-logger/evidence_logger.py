"""
evidence_logger.py

This script generates timestamped, audit-ready evidence files from policy compliance checks. 

This script:
    1. Loads a policy JSON file.
    2. Checks for overly permissive statements (Action: "*" or Resource: "*".)
    3. Writes findings to a timestamped evidence file to the "evidence" directory for audit purposes.
"""
# Import appropriate modules for script.
from datetime import datetime
import json
from pathlib import Path

# Generates a timestamp for a unique file name. 
timestamp = datetime.now()
timestamp_str = timestamp.strftime("%Y-%m-%d_%H-%M-%S")

# Creates evidence folder if it doesn't exists.
evidence_dir = Path("evidence")
evidence_dir.mkdir(exist_ok=True)

# Builds filename with directory path.
filename = evidence_dir / f"evidence_{timestamp_str}_policy_check.txt"

# Declares which policy file to work with. 
policy_file = "test_policy.json"

# Creates evidence file and performs compliance check. 
with open(filename, "w") as f:
    f.write("=" * 80 + "\n")
    f.write("COMPLIANCE EVIDENCE LOG\n")
    f.write("=" * 80 + "\n")
    f.write(f"Timestamp: {timestamp_str}\n")
    f.write(f"\nChecking: {policy_file}\n\n")

    # Load the policy file. 
    with open(policy_file, "r") as pf:
        policy = json.load(pf)

    # Counter to track total issues found. 
    issues = 0 

    # Iterate through each statement in policy.
    for statement in policy.get("Statement", []):

        # Check for wildcard Action (grants all actions).
        if statement.get("Action") == "*":
            f.write(f"[FAIL] Statement \"{statement.get('Sid')}\": Action is \"*\"\n")
            issues += 1
        
        # Check for wildcard Resource (applies to all resources).
        if statement.get("Resource") == "*":
            f.write(f"[FAIL] Statement \"{statement.get('Sid')}\": Resource is \"*\"\n")
            issues += 1

    # Write summary of findings.
    f.write(f"\nResult: {issues} issues found\n")

    f.write("\n" + "=" * 80 + "\n")
    f.write("END OF LOG\n")
    f.write("=" * 80 + "\n")

# Confirm file creation to user (runs after file is closed).
print(f"Evidence file created: {filename}")
