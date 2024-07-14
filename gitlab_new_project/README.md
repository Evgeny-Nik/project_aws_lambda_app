# GitLab Project Setup Lambda Function

This Lambda function automates the setup of a GitLab project and associated tasks, including generating an executable file, initializing a Git repository, committing the file, and pushing it to the GitLab server.

## Setup

1. **AWS Setup:**
   - Ensure you have an AWS account with appropriate permissions to create and manage Lambda functions, as well as access to S3 buckets and EC2 instances.

2. **Environment Variables:**
   - Configure the following environment variables in your Lambda function:
     - `GITLAB_TOKEN`: Personal access token for GitLab API.
     - `GITLAB_USER`: GitLab username for generating GitLab project URLs.
     - `GITLAB_INSTANCE_ID`: Instance ID of the EC2 instance hosting GitLab.
     - `BUCKET_NAME`: Name of the S3 bucket for storing generated script file.
     - `REGION`: AWS region where the S3 bucket resides.

3. **Dependencies:**
   - This function requires the `gitlab` and `boto3` libraries to interact with GitLab and AWS services. Ensure they are included in your Lambda deployment package.

4. **Lambda Function Configuration:**
   - Create a new Lambda function in your AWS account.
   - Copy the provided `lambda_handler` function code into the Lambda function editor.

5. **Permissions:**
   - Grant necessary permissions to the Lambda function:
     - Permissions to interact with GitLab projects and access tokens.
     - Permissions to interact with S3 buckets (`s3:PutObject`, `s3:GetObject` for uploading and retrieving files).
     - Permissions to interact with EC2 instances (`ec2:DescribeInstances` for retrieving instance IP).

## Function Details

The Lambda function performs the following tasks:

- Retrieves the instance IP of the EC2 instance hosting GitLab using the provided `GITLAB_INSTANCE_ID`.
- Creates a GitLab project using the provided `project_name` and GitLab instance IP.
- Generates a Python script file (`agent_setup.py`) tailored for the GitLab project, which creates an executable file:
  - Initializes a Git repository.
  - Adds the generated executable file.
  - Commits the file with an initial commit message.
  - Pushes the commit to the `master` branch on the GitLab server.
- Uploads the generated executable file to the specified S3 bucket (`BUCKET_NAME`).
- Generates a presigned URL for downloading the uploaded executable file from S3.

## Usage

- Once deployed and configured with the required environment variables, the Lambda function can be triggered through various AWS services or API Gateway endpoints.
Example input json:
   ```json
   {
     "project_name": "MyProject",
     "file_extension": "py"
   }
   ```
- It automates the initial setup of GitLab projects, facilitating quick start of new projects.
