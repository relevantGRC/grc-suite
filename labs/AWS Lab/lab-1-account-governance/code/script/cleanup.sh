#!/bin/bash
# cleanup.sh - Script to remove resources created in Lab 1
# Part of GRC Portfolio Lab 1: AWS Account Governance

# CAUTION: This script removes security controls. Only use in a lab/learning environment.

echo "=== GRC Portfolio Lab 1: Cleanup Script ==="
echo "WARNING: This script will remove security controls set up in Lab 1."
echo "Only use this in a lab or learning environment, not in production."
echo

# Set default region or get from command line
DEFAULT_REGION="us-east-1"
REGION=${1:-$DEFAULT_REGION}

echo "Using AWS Region: $REGION"
echo

# Confirm before proceeding
read -p "Are you sure you want to remove security controls? (Type 'yes' to confirm): " CONFIRMATION
if [ "$CONFIRMATION" != "yes" ]; then
    echo "Cleanup cancelled."
    exit 0
fi

echo "Starting cleanup..."
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

# 1. Disable and delete CloudFormation stack (if used)
echo "Checking for CloudFormation stack 'GRC-Lab-Account-Governance'..."
if aws cloudformation describe-stacks --stack-name GRC-Lab-Account-Governance --region $REGION &> /dev/null; then
    echo "Found CloudFormation stack. Deleting..."
    aws cloudformation delete-stack --stack-name GRC-Lab-Account-Governance --region $REGION
    echo "Stack deletion initiated. Stack will be removed shortly."
    echo "Note: S3 buckets with data will remain to prevent data loss."
    echo
    echo "Once the stack deletion is complete, you can manually empty and delete the S3 buckets."
    exit 0
fi

# If CloudFormation wasn't used, clean up individual resources

# 2. Disable Security Hub
echo "Disabling Security Hub..."
if aws securityhub get-enabled-standards --region $REGION &> /dev/null; then
    # Disable standards first
    echo "Disabling Security Hub standards..."
    STANDARDS=$(aws securityhub get-enabled-standards --region $REGION --query 'StandardsSubscriptions[].StandardsSubscriptionArn' --output text)
    for STANDARD in $STANDARDS; do
        aws securityhub batch-disable-standards --standards-subscription-arns $STANDARD --region $REGION
        echo "Disabled standard: $STANDARD"
    done
    
    # Disable Security Hub
    aws securityhub disable-security-hub --region $REGION
    echo "Security Hub disabled."
else
    echo "Security Hub is not enabled."
fi
echo

# 3. Disable AWS Config
echo "Disabling AWS Config..."
CONFIG_RECORDER=$(aws configservice describe-configuration-recorders --region $REGION --query 'ConfigurationRecorders[0].name' --output text 2>/dev/null)
if [ "$CONFIG_RECORDER" != "None" ] && [ -n "$CONFIG_RECORDER" ]; then
    # Stop recorder
    aws configservice stop-configuration-recorder --configuration-recorder-name $CONFIG_RECORDER --region $REGION
    echo "Stopped configuration recorder: $CONFIG_RECORDER"
    
    # Delete rules
    echo "Deleting AWS Config rules..."
    RULES=$(aws configservice describe-config-rules --region $REGION --query 'ConfigRules[].ConfigRuleName' --output text)
    for RULE in $RULES; do
        aws configservice delete-config-rule --config-rule-name $RULE --region $REGION
        echo "Deleted rule: $RULE"
    done
    
    # Delete delivery channel
    CHANNEL=$(aws configservice describe-delivery-channels --region $REGION --query 'DeliveryChannels[0].name' --output text 2>/dev/null)
    if [ "$CHANNEL" != "None" ] && [ -n "$CHANNEL" ]; then
        aws configservice delete-delivery-channel --delivery-channel-name $CHANNEL --region $REGION
        echo "Deleted delivery channel: $CHANNEL"
    fi
    
    # Delete configuration recorder
    aws configservice delete-configuration-recorder --configuration-recorder-name $CONFIG_RECORDER --region $REGION
    echo "Deleted configuration recorder: $CONFIG_RECORDER"
else
    echo "AWS Config is not enabled."
fi
echo

# 4. Delete CloudWatch Alarms
echo "Deleting CloudWatch Alarms..."
# Get alarms with specific prefixes used in the lab
ALARMS=$(aws cloudwatch describe-alarms --region $REGION --query "MetricAlarms[?starts_with(AlarmName, 'CloudTrail') || starts_with(AlarmName, 'IAMPolicy') || starts_with(AlarmName, 'RootLogin')].AlarmName" --output text)
for ALARM in $ALARMS; do
    aws cloudwatch delete-alarms --alarm-names $ALARM --region $REGION
    echo "Deleted alarm: $ALARM"
done
echo

# 5. Delete CloudWatch Log Metric Filters
echo "Deleting CloudWatch Log Metric Filters..."
LOG_GROUP="CloudTrail/CloudTrail"
FILTERS=$(aws logs describe-metric-filters --log-group-name $LOG_GROUP --region $REGION --query 'metricFilters[].filterName' --output text 2>/dev/null)
if [ -n "$FILTERS" ]; then
    for FILTER in $FILTERS; do
        aws logs delete-metric-filter --log-group-name $LOG_GROUP --filter-name $FILTER --region $REGION
        echo "Deleted metric filter: $FILTER"
    done
else
    echo "No metric filters found or CloudTrail log group doesn't exist."
fi
echo

# 6. Delete SNS Topics
echo "Deleting SNS Topics..."
TOPICS=$(aws sns list-topics --region $REGION --query "Topics[?contains(TopicArn, 'SecurityAlerts')].TopicArn" --output text)
for TOPIC in $TOPICS; do
    aws sns delete-topic --topic-arn $TOPIC --region $REGION
    echo "Deleted topic: $TOPIC"
done
echo

# 7. Disable CloudTrail
echo "Disabling CloudTrail..."
TRAILS=$(aws cloudtrail describe-trails --region $REGION --query 'trailList[?name==`AccountTrail`].name' --output text)
for TRAIL in $TRAILS; do
    aws cloudtrail stop-logging --name $TRAIL --region $REGION
    aws cloudtrail delete-trail --name $TRAIL --region $REGION
    echo "Deleted trail: $TRAIL"
done
echo

# 8. Delete IAM Access Analyzer
echo "Deleting IAM Access Analyzer..."
ANALYZERS=$(aws accessanalyzer list-analyzers --region $REGION --query 'analyzers[?analyzerName==`AccountAnalyzer`].arn' --output text)
for ANALYZER in $ANALYZERS; do
    aws accessanalyzer delete-analyzer --analyzer-name $ANALYZER --region $REGION
    echo "Deleted analyzer: $ANALYZER"
done
echo

# 9. Reset IAM Password Policy
echo "Resetting IAM Password Policy to defaults..."
aws iam update-account-password-policy \
    --minimum-password-length 8 \
    --require-symbols false \
    --require-numbers false \
    --require-uppercase-characters false \
    --require-lowercase-characters false \
    --allow-users-to-change-password true \
    --max-password-age 0 \
    --password-reuse-prevention 0 \
    --hard-expiry false
echo "IAM Password Policy reset to defaults."
echo

# 10. Delete AWS Budgets
echo "Deleting AWS Budgets..."
BUDGETS=$(aws budgets describe-budgets --account-id $(aws sts get-caller-identity --query 'Account' --output text) --region $REGION --query 'Budgets[?BudgetName==`MonthlyBudget`].BudgetName' --output text)
for BUDGET in $BUDGETS; do
    aws budgets delete-budget --account-id $(aws sts get-caller-identity --query 'Account' --output text) --budget-name $BUDGET --region $REGION
    echo "Deleted budget: $BUDGET"
done
echo

echo "=== Cleanup Summary ==="
echo "Most resources have been removed, however some actions may need to be performed manually:"
echo
echo "1. S3 Buckets: Any S3 buckets containing CloudTrail logs or Config snapshots need to be emptied and deleted manually."
echo "2. IAM Users: The admin user created in the lab should be deleted manually if no longer needed."
echo "3. KMS Keys: Any KMS keys created for CloudTrail encryption will need to be scheduled for deletion manually."
echo
echo "To empty an S3 bucket, use: aws s3 rm s3://bucket-name --recursive"
echo "To delete an S3 bucket, use: aws s3 rb s3://bucket-name"
echo
echo "Cleanup complete! Security controls from Lab 1 have been removed." 
