import json
import os
from datetime import datetime

def convert_framework_json(json_filepath, markdown_filepath, framework_name):
    if not os.path.exists(json_filepath):
        print(f"Skipping: {json_filepath} not found yet.")
        return

    with open(json_filepath, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            print(f"Error reading {json_filepath}. File might be empty.")
            return

    reports = data if isinstance(data, list) else [data]
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    md_lines = [
        f"# Automated Infrastructure Evidence ({framework_name.upper()})",
        f"> **Last Compliance Check:** {current_time}",
        "",
        "| Status | Check ID | Framework Requirement / Description | Resource Path |",
        "| :--- | :--- | :--- | :--- |"
    ]
    
    has_results = False
    for report in reports:
        results = report.get("results", {})
        
        for check in results.get("passed_checks", []):
            has_results = True
            check_id = check.get("check_id", "Unknown")
            name = check.get("check_name", "No description")
            resource = check.get("resource", "Unknown resource")
            md_lines.append(f"| 🟢 PASS | `{check_id}` | {name} | `{resource}` |")
            
        for check in results.get("failed_checks", []):
            has_results = True
            check_id = check.get("check_id", "Unknown")
            name = check.get("check_name", "No description")
            resource = check.get("resource", "Unknown resource")
            md_lines.append(f"| 🔴 FAIL | `{check_id}` | {name} | `{resource}` |")

    if not has_results:
        md_lines.append("| ⚪ INFO | N/A | No active cloud infrastructure issues detected for this framework. | `N/A` |")

    os.makedirs(os.path.dirname(markdown_filepath), exist_ok=True)
    with open(markdown_filepath, 'w') as file:
        file.write("\n".join(md_lines))
    print(f"Successfully sync'd {framework_name.upper()} table to vault.")

if __name__ == "__main__":
    convert_framework_json("evidence/iso27001/daily-scan-results.json", "governance-vault/03-Evidence-Logs/iso27001-live-status.md", "iso27001")
    convert_framework_json("evidence/soc2/daily-scan-results.json", "governance-vault/03-Evidence-Logs/soc2-live-status.md", "soc2")
    convert_framework_json("evidence/nist/daily-scan-results.json", "governance-vault/03-Evidence-Logs/nist-live-status.md", "nist")
