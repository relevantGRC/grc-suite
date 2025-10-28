#!/bin/bash
# verify-compliance.sh - Script to check compliance status of AWS Config rules
# Part of GRC Portfolio Lab 1: AWS Account Governance

echo "=== AWS Config Compliance Status Checker ==="
echo "This script checks the compliance status of AWS Config rules in your account."
echo

# Set default region or get from command line
DEFAULT_REGION="us-east-1"
REGION=${1:-$DEFAULT_REGION}

echo "Using AWS Region: $REGION"
echo

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "Error: AWS CLI is not installed. Please install it first."
    exit 1
fi

# Check if AWS CLI is configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "Error: AWS CLI is not configured. Please run 'aws configure' first."
    exit 1
fi

# Get list of AWS Config Rules
echo "Fetching AWS Config rules..."
CONFIG_RULES=$(aws configservice describe-config-rules --region $REGION --query "ConfigRules[].ConfigRuleName" --output text)

if [ -z "$CONFIG_RULES" ]; then
    echo "No AWS Config rules found in region $REGION. Please make sure AWS Config is enabled."
    exit 1
fi

echo "Found $(echo $CONFIG_RULES | wc -w) rules."
echo

# Check compliance status for each rule
echo "=== Compliance Status ==="
echo "Rule Name                               | Status      | # Resources | Resource IDs"
echo "----------------------------------------|-------------|-------------|--------------------"

for RULE in $CONFIG_RULES; do
    # Get compliance status
    COMPLIANCE_STATUS=$(aws configservice describe-compliance-by-config-rule \
        --config-rule-names "$RULE" \
        --region $REGION \
        --query "ComplianceByConfigRules[0].Compliance" \
        --output text)
    
    if [ "$COMPLIANCE_STATUS" == "INSUFFICIENT_DATA" ]; then
        RESOURCE_COUNT="N/A"
        RESOURCE_IDS="N/A"
    else
        # Get non-compliant resources if any
        NON_COMPLIANT=$(aws configservice get-compliance-details-by-config-rule \
            --config-rule-name "$RULE" \
            --compliance-types NON_COMPLIANT \
            --region $REGION \
            --query "EvaluationResults[].EvaluationResultIdentifier.EvaluationResultQualifier.ResourceId" \
            --output text)
        
        # Count resources and format for display
        if [ -z "$NON_COMPLIANT" ]; then
            RESOURCE_COUNT="0"
            RESOURCE_IDS="All Compliant"
        else
            RESOURCE_COUNT=$(echo $NON_COMPLIANT | wc -w)
            RESOURCE_IDS=$(echo $NON_COMPLIANT | tr '\t' ',' | cut -c 1-20)
            if [ ${#RESOURCE_IDS} -gt 20 ]; then
                RESOURCE_IDS="${RESOURCE_IDS}..."
            fi
        fi
    fi
    
    # Truncate rule name if too long
    DISPLAY_RULE=$RULE
    if [ ${#DISPLAY_RULE} -gt 40 ]; then
        DISPLAY_RULE="${DISPLAY_RULE:0:37}..."
    fi
    
    # Pad rule name for alignment
    printf "%-40s | %-11s | %-11s | %s\n" "$DISPLAY_RULE" "$COMPLIANCE_STATUS" "$RESOURCE_COUNT" "$RESOURCE_IDS"
done

echo
echo "=== Summary ==="
# Get overall compliance
COMPLIANT_COUNT=$(aws configservice describe-compliance-by-config-rule \
    --region $REGION \
    --query "ComplianceByConfigRules[?Compliance=='COMPLIANT'].ConfigRuleName" \
    --output text | wc -w)
    
NON_COMPLIANT_COUNT=$(aws configservice describe-compliance-by-config-rule \
    --region $REGION \
    --query "ComplianceByConfigRules[?Compliance=='NON_COMPLIANT'].ConfigRuleName" \
    --output text | wc -w)

INSUFFICIENT_DATA_COUNT=$(aws configservice describe-compliance-by-config-rule \
    --region $REGION \
    --query "ComplianceByConfigRules[?Compliance=='INSUFFICIENT_DATA'].ConfigRuleName" \
    --output text | wc -w)

TOTAL_RULES=$(echo $CONFIG_RULES | wc -w)

echo "Compliant rules: $COMPLIANT_COUNT/$TOTAL_RULES"
echo "Non-compliant rules: $NON_COMPLIANT_COUNT/$TOTAL_RULES"
echo "Rules with insufficient data: $INSUFFICIENT_DATA_COUNT/$TOTAL_RULES"

echo
echo "For detailed information on non-compliant resources, run:"
echo "aws configservice get-compliance-details-by-config-rule --config-rule-name RULE_NAME --compliance-types NON_COMPLIANT --region $REGION"
echo

if [ $NON_COMPLIANT_COUNT -gt 0 ]; then
    echo "⚠️  Action required: Address non-compliant resources to improve your security posture."
else
    echo "✅ All evaluated rules are compliant. Great job on your security configuration!"
fi 
