# S3 Backup Lambda Function with EventBridge Triggers

This Lambda function automates the backup of objects from a specified S3 bucket to another backup S3 bucket, triggered by EventBridge on a cron schedule. It creates daily, weekly (on Sundays), and monthly (on the 1st day of the month) backups based on the current date.

## Setup

1. **AWS Setup:**
   - Ensure you have an AWS account with appropriate permissions to create and manage Lambda functions, S3 buckets, and EventBridge rules.

2. **Environment Variables:**
   - Configure the following environment variables in your Lambda function:
     - `SOURCE_BUCKET`: The name of the source S3 bucket from which objects will be backed up.
     - `BACKUP_BUCKET`: The name of the destination S3 bucket where backups will be stored.

3. **Dependencies:**
   - This function requires the `boto3` library to interact with AWS services. Ensure it's included in your Lambda deployment package.

4. **Lambda Function Configuration:**
   - Create a new Lambda function in your AWS account.
   - Copy the provided `lambda_handler` function code into the Lambda function editor.

5. **EventBridge Triggers:**
   - Set up EventBridge rules with cron expressions to trigger this Lambda function at the desired intervals:
     - **Daily Backup:** Cron expression for daily backups.
     - **Weekly Backup:** Cron expression for weekly backups (e.g., every Sunday).
     - **Monthly Backup:** Cron expression for monthly backups (e.g., on the 1st day of the month).

6. **Permissions:**
   - Grant necessary permissions to the Lambda function to interact with S3 buckets (`s3:GetObject`, `s3:PutObject`, etc.) through IAM roles.
   - Ensure the Lambda function has permissions to trigger from EventBridge rules (`events:PutRule` and `events:PutTargets` permissions).

## Function Details

The Lambda function performs the following tasks:

- Retrieves objects from the `SOURCE_BUCKET` S3 bucket.
- Creates daily backups named with the current date (`YYYY-MM-DD`) in the `BACKUP_BUCKET`.
- On Sundays, creates weekly backups named with the current year and week number (`YYYY-W`) in the `BACKUP_BUCKET`.
- On the 1st day of each month, creates monthly backups named with the current year and month (`YYYY-MM`) in the `BACKUP_BUCKET`.


## Usage

- Once deployed and EventBridge rules are set up, the Lambda function will automatically execute its backup tasks based on the cron schedules defined in EventBridge.
