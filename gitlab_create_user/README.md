# GitLab User and Project Creation Lambda Function

This Lambda function automates the creation of GitLab users and associated projects based on data parsed from a Google Sheet. It also manages user access within specified GitLab groups.

## Setup

1. **AWS Setup:**
   - Ensure you have an AWS account with appropriate permissions to create and manage Lambda functions, as well as access to EC2 instances and IAM roles.

2. **Environment Variables:**
   - Configure the following environment variables in your Lambda function:
     - `GITLAB_TOKEN`: Personal access token for GitLab API.
     - `GITLAB_INSTANCE_ID`: Instance ID of the EC2 instance hosting GitLab.
     - `GITLAB_GROUP_NAME`: Name of the GitLab group where projects will be created.
     - `GITLAB_GROUP_DESC`: Description for the GitLab group.
     - Ensure these variables are securely stored and accessible to the Lambda function.

3. **Dependencies:**
   - This function requires the `gitlab`, `pandas`, and `boto3` libraries to interact with GitLab API, parse Google Sheets data, and manage AWS services. Ensure they are included in your Lambda deployment package.

4. **Lambda Function Configuration:**
   - Create a new Lambda function in your AWS account.
   - Copy the provided `lambda_handler` function code into the Lambda function editor.

5. **Permissions:**
   - Grant necessary permissions to the Lambda function:
     - Permissions to interact with GitLab users, groups, and projects.
     - Permissions to interact with AWS EC2 instances (`ec2:DescribeInstances` for retrieving instance IP).
     - Permissions to log events (`CloudWatchLogsFullAccess` for logging).

## Function Details

The Lambda function performs the following tasks:

- Retrieves the instance IP of the EC2 instance hosting GitLab using the provided `GITLAB_INSTANCE_ID`.
- Parses data from a Google Sheet URL to extract user information.
- Creates a GitLab group if it doesn't exist, or fetches an existing one based on `GITLAB_GROUP_NAME`.
- Creates GitLab users based on parsed data and adds them as reporters to the GitLab group.
- Creates individual projects for each user within the GitLab group.

## Usage

- Once deployed and configured with the required environment variables, the Lambda function can be triggered through various AWS services or API Gateway endpoints.
Example input json:
   ```json
   {
     "google_sheet_url": "<your_google_sheet_url>"
   }
   ```
- It automates the setup of GitLab users and projects based on data sourced from a Google Sheet, facilitating streamlined user and project management workflows.
