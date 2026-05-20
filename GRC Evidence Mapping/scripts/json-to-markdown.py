import json
import os
from datetime import datetime

def build_markdown_evidence(json_filepath, markdown_filepath):
    """
    Reads a Checkov JSON output file and converts the passed/failed
    checks into a Markdown table for your governance vault.
    """
    
    # 1. Ensure the JSON file exists before trying to read it
    if not os.path.exists(json_filepath):
        print(f"Error: Could not find {json_filepath}")
        return

    # 2. Open and load the JSON data
    with open(json_filepath, 'r') as file:
        data = json.load(file)

    # Checkov sometimes outputs a list (if scanning multiple frameworks) 
    # or a single dictionary. This ensures we can handle both.
    reports = data if isinstance(data, list) else [data]
    
    # 3. Start building the Markdown text
    # We add a timestamp so you always know when the vault was last updated
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md_lines = [
        "# Automated Infrastructure Evidence",
        f"> **Last Pipeline Run:** {current_time}",
        "",
        "| Status | Check ID | Policy Description | Resource |",
        "| :--- | :--- | :--- | :--- |"
    ]
    
    # 4. Loop through the data and build the table rows
    for report in reports:
        results = report.get("results", {})
        
        # Pull out the successful controls
        for check in results.get("passed_checks", []):
            check_id = check.get("check_id", "Unknown")
            name = check.get("check_name", "No description")
            resource = check.get("resource", "Unknown resource")
            
            row = f"| 🟢 PASS | `{check_id}` | {name} | `{resource}` |"
            md_lines.append(row)
            
        # Pull out the failed controls
        for check in results.get("failed_checks", []):
            check_id = check.get("check_id", "Unknown")
            name = check.get("check_name", "No description")
            resource = check.get("resource", "Unknown resource")
            
            row = f"| 🔴 FAIL | `{check_id}` | {name} | `{resource}` |"
            md_lines.append(row)

    # 5. Save the generated Markdown into your vault
    # This automatically creates the folder path if it doesn't exist
    os.makedirs(os.path.dirname(markdown_filepath), exist_ok=True)
    
    # Join our list of lines with line breaks and write to the file
    with open(markdown_filepath, 'w') as file:
        file.write("\n".join(md_lines))
        
    print(f"Success! Evidence table written to {markdown_filepath}")

# ---------------------------------------------------------
# Execution: Pointing the script at our repository folders
# ---------------------------------------------------------
if __name__ == "__main__":
    # Define where the JSON comes from, and where the Markdown goes
    INPUT_JSON = "evidence/iso27001/daily-scan-results.json"
    OUTPUT_MD = "governance-vault/03-Evidence-Logs/iso27001-live-status.md"
    
    build_markdown_evidence(INPUT_JSON, OUTPUT_MD)
