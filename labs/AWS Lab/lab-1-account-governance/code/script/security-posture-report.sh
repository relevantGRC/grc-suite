#!/bin/bash
# security-posture-report.sh - Comprehensive AWS Security Posture Report
# Part of GRC Portfolio Lab 1: AWS Account Governance

# This script generates a comprehensive security posture report by gathering data from:
# - AWS Config
# - Security Hub
# - IAM Credential Report
# - GuardDuty (if enabled)
# - Access Analyzer
# - CloudTrail status

echo "=== AWS Security Posture Report ==="
echo "Generating a comprehensive security assessment of your AWS account"
echo "$(date)"
echo

# Set default region or get from command line
DEFAULT_REGION="us-east-1"
REGION=${1:-$DEFAULT_REGION}
OUTPUT_FILE="security-posture-report-$(date +%Y-%m-%d).txt"

echo "Using AWS Region: $REGION"
echo "Report will be saved to: $OUTPUT_FILE"
echo

# Create or clear the output file
> $OUTPUT_FILE

# Add header to report
{
    echo "AWS SECURITY POSTURE REPORT"
    echo "==========================="
    echo "Date: $(date)"
    echo "Region: $REGION"
    echo "Account: $(aws sts get-caller-identity --query 'Account' --output text)"
    echo
} >> $OUTPUT_FILE

# Check if AWS CLI is installed and configured
if ! command -v aws &> /dev/null; then
    echo "Error: AWS CLI is not installed. Please install it first."
    exit 1
fi

if ! aws sts get-caller-identity &> /dev/null; then
    echo "Error: AWS CLI is not configured. Please run 'aws configure' first."
    exit 1
fi

# Function to check if a service is enabled
is_service_enabled() {
    local service=$1
    local command=$2
    
    if eval "$command" &> /dev/null; then
        echo "✅ $service is enabled"
        return 0
    else
        echo "❌ $service is not enabled"
        return 1
    fi
}

# Function to add a section to the report
add_section() {
    local title=$1
    {
        echo
        echo "===== $title ====="
        echo
    } >> $OUTPUT_FILE
}

# Check core security services
echo "Checking core security services..."
{
    add_section "CORE SECURITY SERVICES STATUS"
    
    # Check CloudTrail
    if aws cloudtrail describe-trails --region $REGION --query 'trailList[0]' --output text &> /dev/null; then
        echo "✅ CloudTrail is enabled"
        TRAIL_NAME=$(aws cloudtrail describe-trails --region $REGION --query 'trailList[0].Name' --output text)
        TRAIL_STATUS=$(aws cloudtrail get-trail-status --name $TRAIL_NAME --region $REGION --query 'IsLogging' --output text)
        echo "   Trail Name: $TRAIL_NAME"
        echo "   Logging Enabled: $TRAIL_STATUS"
    else
        echo "❌ CloudTrail is not enabled"
    fi
    
    # Check AWS Config
    if aws configservice describe-configuration-recorders --region $REGION --query 'ConfigurationRecorders[0]' --output text &> /dev/null; then
        echo "✅ AWS Config is enabled"
        RECORDER_NAME=$(aws configservice describe-configuration-recorders --region $REGION --query 'ConfigurationRecorders[0].name' --output text)
        RECORDER_STATUS=$(aws configservice describe-configuration-recorder-status --region $REGION --query 'ConfigurationRecordersStatus[0].recording' --output text)
        echo "   Recorder Name: $RECORDER_NAME"
        echo "   Recording Enabled: $RECORDER_STATUS"
    else
        echo "❌ AWS Config is not enabled"
    fi
    
    # Check Security Hub
    if aws securityhub describe-hub --region $REGION &> /dev/null; then
        echo "✅ Security Hub is enabled"
        
        # Get enabled standards
        STANDARDS=$(aws securityhub describe-standards --region $REGION --query 'Standards[].StandardsArn' --output text)
        echo "   Enabled Standards:"
        if [ -n "$STANDARDS" ]; then
            for STANDARD in $STANDARDS; do
                echo "   - $(echo $STANDARD | awk -F '/' '{print $NF}')"
            done
        else
            echo "   - No standards enabled"
        fi
    else
        echo "❌ Security Hub is not enabled"
    fi
    
    # Check GuardDuty
    if aws guardduty list-detectors --region $REGION --query 'DetectorIds[0]' --output text &> /dev/null; then
        DETECTOR_ID=$(aws guardduty list-detectors --region $REGION --query 'DetectorIds[0]' --output text)
        if [ "$DETECTOR_ID" != "None" ]; then
            echo "✅ GuardDuty is enabled"
            DETECTOR_STATUS=$(aws guardduty get-detector --detector-id $DETECTOR_ID --region $REGION --query 'Status' --output text)
            echo "   Detector ID: $DETECTOR_ID"
            echo "   Status: $DETECTOR_STATUS"
        else
            echo "❌ GuardDuty is not enabled"
        fi
    else
        echo "❌ GuardDuty is not enabled"
    fi
    
    # Check IAM Access Analyzer
    if aws accessanalyzer list-analyzers --region $REGION --query 'analyzers[0]' --output text &> /dev/null; then
        echo "✅ IAM Access Analyzer is enabled"
        ANALYZER_NAME=$(aws accessanalyzer list-analyzers --region $REGION --query 'analyzers[0].name' --output text)
        ANALYZER_STATUS=$(aws accessanalyzer list-analyzers --region $REGION --query 'analyzers[0].status' --output text)
        echo "   Analyzer Name: $ANALYZER_NAME"
        echo "   Status: $ANALYZER_STATUS"
    else
        echo "❌ IAM Access Analyzer is not enabled"
    fi
} >> $OUTPUT_FILE

# Get AWS Config compliance status
echo "Checking AWS Config compliance status..."
add_section "AWS CONFIG COMPLIANCE STATUS" >> $OUTPUT_FILE

if is_service_enabled "AWS Config" "aws configservice describe-configuration-recorders --region $REGION --query 'ConfigurationRecorders[0]' --output text"; then
    # Get compliance status
    COMPLIANT_RULES=$(aws configservice describe-compliance-by-config-rule --region $REGION --query 'ComplianceByConfigRules[?Compliance==`COMPLIANT`].ConfigRuleName' --output text | wc -w)
    NON_COMPLIANT_RULES=$(aws configservice describe-compliance-by-config-rule --region $REGION --query 'ComplianceByConfigRules[?Compliance==`NON_COMPLIANT`].ConfigRuleName' --output text | wc -w)
    INSUFFICIENT_DATA_RULES=$(aws configservice describe-compliance-by-config-rule --region $REGION --query 'ComplianceByConfigRules[?Compliance==`INSUFFICIENT_DATA`].ConfigRuleName' --output text | wc -w)
    TOTAL_RULES=$((COMPLIANT_RULES + NON_COMPLIANT_RULES + INSUFFICIENT_DATA_RULES))
    
    {
        echo "Total Rules: $TOTAL_RULES"
        echo "Compliant Rules: $COMPLIANT_RULES"
        echo "Non-Compliant Rules: $NON_COMPLIANT_RULES"
        echo "Insufficient Data Rules: $INSUFFICIENT_DATA_RULES"
        echo
        
        # List non-compliant rules if any
        if [ $NON_COMPLIANT_RULES -gt 0 ]; then
            echo "Non-Compliant Rules:"
            NON_COMPLIANT_RULE_NAMES=$(aws configservice describe-compliance-by-config-rule --region $REGION --query 'ComplianceByConfigRules[?Compliance==`NON_COMPLIANT`].ConfigRuleName' --output text)
            for RULE in $NON_COMPLIANT_RULE_NAMES; do
                echo "- $RULE"
                
                # Get non-compliant resources for this rule
                NON_COMPLIANT_RESOURCES=$(aws configservice get-compliance-details-by-config-rule --config-rule-name $RULE --compliance-types NON_COMPLIANT --region $REGION --query 'EvaluationResults[].EvaluationResultIdentifier.EvaluationResultQualifier.ResourceId' --output text)
                
                if [ -n "$NON_COMPLIANT_RESOURCES" ]; then
                    echo "  Non-Compliant Resources:"
                    for RESOURCE in $NON_COMPLIANT_RESOURCES; do
                        echo "  - $RESOURCE"
                    done
                fi
            done
        fi
    } >> $OUTPUT_FILE
else
    echo "AWS Config is not enabled. Cannot get compliance status." >> $OUTPUT_FILE
fi

# Check IAM security status
echo "Checking IAM security status..."
add_section "IAM SECURITY STATUS" >> $OUTPUT_FILE

{
    # Check password policy
    echo "Password Policy:"
    aws iam get-account-password-policy 2>/dev/null | jq -r '.PasswordPolicy | {
        MinimumPasswordLength,
        RequireSymbols,
        RequireNumbers,
        RequireUppercaseCharacters,
        RequireLowercaseCharacters,
        AllowUsersToChangePassword,
        MaxPasswordAge,
        PasswordReusePrevention,
        HardExpiry
    }' >> $OUTPUT_FILE || echo "No password policy is set" >> $OUTPUT_FILE
    
    # Check root account MFA
    echo
    echo "Root Account:"
    ROOT_MFA=$(aws iam get-account-summary --query 'SummaryMap.AccountMFAEnabled' --output text)
    if [ "$ROOT_MFA" == "1" ]; then
        echo "MFA Enabled: Yes"
    else
        echo "MFA Enabled: No (SECURITY RISK)"
    fi
    
    # Generate credential report
    aws iam generate-credential-report &>/dev/null
    
    # Check users with console access but no MFA
    echo
    echo "IAM Users without MFA:"
    aws iam get-credential-report --query 'Content' --output text | base64 -d | \
    awk -F, 'NR>1 && $4=="true" && $8=="false" {print $1 " (SECURITY RISK)"}' >> $OUTPUT_FILE || \
    echo "Unable to generate credential report" >> $OUTPUT_FILE
    
    # Check for API keys older than 90 days
    echo
    echo "IAM Users with API keys older than 90 days:"
    aws iam get-credential-report --query 'Content' --output text | base64 -d | \
    awk -F, 'NR>1 && $9=="true" && $11!="N/A" && $11!="" {cmd="date -d " $11 " +%s"; cmd | getline key_date; close(cmd); \
    now=systime(); diff=(now-key_date)/86400; if (diff>90) print $1 " - Key1 Age: " int(diff) " days (ROTATION RECOMMENDED)"}' >> $OUTPUT_FILE
    
    aws iam get-credential-report --query 'Content' --output text | base64 -d | \
    awk -F, 'NR>1 && $14=="true" && $16!="N/A" && $16!="" {cmd="date -d " $16 " +%s"; cmd | getline key_date; close(cmd); \
    now=systime(); diff=(now-key_date)/86400; if (diff>90) print $1 " - Key2 Age: " int(diff) " days (ROTATION RECOMMENDED)"}' >> $OUTPUT_FILE
} >> $OUTPUT_FILE 2>/dev/null || echo "Could not generate complete IAM report. Check permissions." >> $OUTPUT_FILE

# Security Hub findings
echo "Checking Security Hub findings..."
add_section "SECURITY HUB FINDINGS" >> $OUTPUT_FILE

if is_service_enabled "Security Hub" "aws securityhub describe-hub --region $REGION"; then
    {
        # Get finding count by severity
        echo "Findings by Severity:"
        echo "Critical: $(aws securityhub get-findings --region $REGION --filters '{"SeverityLabel": [{"Value": "CRITICAL", "Comparison": "EQUALS"}]}' --query 'length(Findings)' --output text)"
        echo "High: $(aws securityhub get-findings --region $REGION --filters '{"SeverityLabel": [{"Value": "HIGH", "Comparison": "EQUALS"}]}' --query 'length(Findings)' --output text)"
        echo "Medium: $(aws securityhub get-findings --region $REGION --filters '{"SeverityLabel": [{"Value": "MEDIUM", "Comparison": "EQUALS"}]}' --query 'length(Findings)' --output text)"
        echo "Low: $(aws securityhub get-findings --region $REGION --filters '{"SeverityLabel": [{"Value": "LOW", "Comparison": "EQUALS"}]}' --query 'length(Findings)' --output text)"
        echo
        
        # List critical findings
        echo "Critical Findings:"
        CRITICAL_FINDINGS=$(aws securityhub get-findings --region $REGION --filters '{"SeverityLabel": [{"Value": "CRITICAL", "Comparison": "EQUALS"}]}' --query 'Findings[].{Title: Title, ResourceId: Resources[0].Id, Description: Description}')
        echo "$CRITICAL_FINDINGS" | jq -r '.[] | "- " + .Title + " (" + .ResourceId + ")"' || echo "No critical findings"
    } >> $OUTPUT_FILE
else
    echo "Security Hub is not enabled. Cannot get findings." >> $OUTPUT_FILE
fi

# Access Analyzer findings
echo "Checking Access Analyzer findings..."
add_section "ACCESS ANALYZER FINDINGS" >> $OUTPUT_FILE

if is_service_enabled "IAM Access Analyzer" "aws accessanalyzer list-analyzers --region $REGION --query 'analyzers[0]' --output text"; then
    {
        ANALYZER_ARN=$(aws accessanalyzer list-analyzers --region $REGION --query 'analyzers[0].arn' --output text)
        if [ -n "$ANALYZER_ARN" ]; then
            FINDINGS=$(aws accessanalyzer list-findings --analyzer-arn $ANALYZER_ARN --region $REGION)
            FINDING_COUNT=$(echo $FINDINGS | jq -r '.findings | length')
            
            echo "Total External Access Findings: $FINDING_COUNT"
            echo
            
            if [ "$FINDING_COUNT" -gt 0 ]; then
                echo "External Access Findings:"
                echo $FINDINGS | jq -r '.findings[] | "- Resource: " + .resource + ", Principal: " + .principal + ", Action: " + .action'
            else
                echo "No external access findings detected."
            fi
        else
            echo "No active analyzer found."
        fi
    } >> $OUTPUT_FILE
else
    echo "IAM Access Analyzer is not enabled. Cannot get findings." >> $OUTPUT_FILE
fi

# Budget status
echo "Checking budget status..."
add_section "BUDGET STATUS" >> $OUTPUT_FILE

{
    ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' --output text)
    BUDGETS=$(aws budgets describe-budgets --account-id $ACCOUNT_ID --region $REGION 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        BUDGET_COUNT=$(echo $BUDGETS | jq -r '.Budgets | length')
        
        if [ "$BUDGET_COUNT" -gt 0 ]; then
            echo "Budgets Configured: $BUDGET_COUNT"
            echo
            echo "Budget Details:"
            echo $BUDGETS | jq -r '.Budgets[] | "- Name: " + .BudgetName + ", Limit: " + (.BudgetLimit.Amount|tostring) + " " + .BudgetLimit.Unit'
        else
            echo "No budgets configured. Consider setting up AWS Budgets for cost control."
        fi
    else
        echo "Unable to retrieve budget information. Check permissions."
    fi
} >> $OUTPUT_FILE

# Summary and recommendations
echo "Generating summary and recommendations..."
add_section "SUMMARY AND RECOMMENDATIONS" >> $OUTPUT_FILE

{
    echo "Security Posture Summary:"
    echo
    
    # CloudTrail check
    if aws cloudtrail describe-trails --region $REGION --query 'trailList[0]' --output text &> /dev/null; then
        echo "✅ CloudTrail is properly configured"
    else
        echo "❌ CRITICAL: CloudTrail is not enabled - Implement AWS CloudTrail for comprehensive API logging"
    fi
    
    # AWS Config check
    if aws configservice describe-configuration-recorders --region $REGION --query 'ConfigurationRecorders[0]' --output text &> /dev/null; then
        echo "✅ AWS Config is properly configured"
    else
        echo "❌ HIGH: AWS Config is not enabled - Implement AWS Config for resource compliance monitoring"
    fi
    
    # Security Hub check
    if aws securityhub describe-hub --region $REGION &> /dev/null; then
        echo "✅ Security Hub is properly configured"
    else
        echo "❌ HIGH: Security Hub is not enabled - Enable Security Hub for comprehensive security posture management"
    fi
    
    # Root MFA check
    ROOT_MFA=$(aws iam get-account-summary --query 'SummaryMap.AccountMFAEnabled' --output text)
    if [ "$ROOT_MFA" == "1" ]; then
        echo "✅ Root account MFA is enabled"
    else
        echo "❌ CRITICAL: Root account MFA is not enabled - Enable MFA for the root account immediately"
    fi
    
    # IAM password policy check
    if aws iam get-account-password-policy &> /dev/null; then
        MIN_LENGTH=$(aws iam get-account-password-policy --query 'PasswordPolicy.MinimumPasswordLength' --output text)
        if [ "$MIN_LENGTH" -ge 14 ]; then
            echo "✅ IAM password policy is sufficiently strong"
        else
            echo "⚠️ MEDIUM: IAM password policy minimum length ($MIN_LENGTH) is less than recommended (14)"
        fi
    else
        echo "❌ HIGH: No IAM password policy configured - Set up a strong password policy"
    fi
    
    # Budget check
    ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' --output text)
    if aws budgets describe-budgets --account-id $ACCOUNT_ID --region $REGION --query 'Budgets[0]' --output text &> /dev/null; then
        echo "✅ AWS Budgets is configured"
    else
        echo "⚠️ MEDIUM: No AWS Budgets configured - Set up budgets for cost control"
    fi
    
    echo
    echo "Top Recommendations:"
    echo
    
    # Count findings for prioritization
    CRITICAL_COUNT=0
    HIGH_COUNT=0
    
    # Check CloudTrail
    if ! aws cloudtrail describe-trails --region $REGION --query 'trailList[0]' --output text &> /dev/null; then
        CRITICAL_COUNT=$((CRITICAL_COUNT+1))
        echo "$CRITICAL_COUNT. CRITICAL: Enable CloudTrail for comprehensive API logging"
    fi
    
    # Check root MFA
    if [ "$ROOT_MFA" != "1" ]; then
        CRITICAL_COUNT=$((CRITICAL_COUNT+1))
        echo "$CRITICAL_COUNT. CRITICAL: Enable MFA for the root account"
    fi
    
    # Check AWS Config
    if ! aws configservice describe-configuration-recorders --region $REGION --query 'ConfigurationRecorders[0]' --output text &> /dev/null; then
        HIGH_COUNT=$((HIGH_COUNT+1))
        echo "$((CRITICAL_COUNT+HIGH_COUNT)). HIGH: Enable AWS Config for resource compliance monitoring"
    fi
    
    # Check Security Hub
    if ! aws securityhub describe-hub --region $REGION &> /dev/null; then
        HIGH_COUNT=$((HIGH_COUNT+1))
        echo "$((CRITICAL_COUNT+HIGH_COUNT)). HIGH: Enable Security Hub for comprehensive security posture management"
    fi
    
    # Check IAM password policy
    if ! aws iam get-account-password-policy &> /dev/null; then
        HIGH_COUNT=$((HIGH_COUNT+1))
        echo "$((CRITICAL_COUNT+HIGH_COUNT)). HIGH: Configure a strong IAM password policy"
    fi
    
    # Non-compliant rules
    if aws configservice describe-compliance-by-config-rule --region $REGION --query 'ComplianceByConfigRules[?Compliance==`NON_COMPLIANT`].ConfigRuleName' --output text &> /dev/null; then
        NON_COMPLIANT_COUNT=$(aws configservice describe-compliance-by-config-rule --region $REGION --query 'ComplianceByConfigRules[?Compliance==`NON_COMPLIANT`].ConfigRuleName' --output text | wc -w)
        if [ "$NON_COMPLIANT_COUNT" -gt 0 ]; then
            HIGH_COUNT=$((HIGH_COUNT+1))
            echo "$((CRITICAL_COUNT+HIGH_COUNT)). HIGH: Remediate $NON_COMPLIANT_COUNT non-compliant AWS Config rules"
        fi
    fi
    
    # Check IAM users without MFA
    IAM_NO_MFA=$(aws iam get-credential-report --query 'Content' --output text 2>/dev/null | base64 -d | awk -F, 'NR>1 && $4=="true" && $8=="false" {count++} END {print count}')
    if [ -n "$IAM_NO_MFA" ] && [ "$IAM_NO_MFA" -gt 0 ]; then
        HIGH_COUNT=$((HIGH_COUNT+1))
        echo "$((CRITICAL_COUNT+HIGH_COUNT)). HIGH: Enable MFA for $IAM_NO_MFA IAM users with console access"
    fi
    
    # Check Security Hub critical findings
    if aws securityhub describe-hub --region $REGION &> /dev/null; then
        CRITICAL_FINDINGS_COUNT=$(aws securityhub get-findings --region $REGION --filters '{"SeverityLabel": [{"Value": "CRITICAL", "Comparison": "EQUALS"}]}' --query 'length(Findings)' --output text)
        if [ -n "$CRITICAL_FINDINGS_COUNT" ] && [ "$CRITICAL_FINDINGS_COUNT" -gt 0 ]; then
            HIGH_COUNT=$((HIGH_COUNT+1))
            echo "$((CRITICAL_COUNT+HIGH_COUNT)). HIGH: Address $CRITICAL_FINDINGS_COUNT critical Security Hub findings"
        fi
    fi
    
    # No critical or high recommendations
    if [ $CRITICAL_COUNT -eq 0 ] && [ $HIGH_COUNT -eq 0 ]; then
        echo "No critical or high priority recommendations identified. Good job maintaining your security posture!"
    fi
} >> $OUTPUT_FILE

echo
echo "Security posture report completed successfully."
echo "Report saved to: $OUTPUT_FILE"
echo
echo "Review this report to identify security gaps and prioritize remediation actions."
echo "Consider implementing as many recommendations as possible to improve your security posture."
echo 
