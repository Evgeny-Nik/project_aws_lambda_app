# S3 File Update with Wikipedia Summary Lambda Function

This Lambda function updates a file stored in an S3 bucket by appending a Wikipedia summary related to a specified topic.

## Setup

1. **AWS Setup:**
   - Ensure you have an AWS account with appropriate permissions to create and manage Lambda functions and access S3 buckets.

2. **Environment Variables:**
   - Set the following environment variables in your Lambda function configuration:
     - `BUCKET_NAME`: Name of the S3 bucket where the file is stored.
     - `FILE_KEY`: Key (path) of the file within the S3 bucket.

3. **Dependencies:**
   - This function requires the `boto3`, `wikipedia`, and `os` libraries.
   - Include these dependencies in your Lambda deployment package.

4. **Lambda Function Configuration:**
   - Create a new Lambda function in your AWS account.
   - Copy the provided `lambda_handler` function code into the Lambda function editor.

5. **Permissions:**
   - Ensure the Lambda function has permissions to:
     - Read from and write to the specified S3 bucket (`s3:GetObject`, `s3:PutObject`).
     - Log events (`CloudWatchLogsFullAccess` for logging).

## Function Details

The Lambda function performs the following tasks:

- Retrieves the topic and S3 bucket/key from the event.
- Downloads the existing file from the specified S3 bucket to a temporary local directory (`/tmp/`).
- Retrieves a summary from Wikipedia based on the provided topic.
- Appends the Wikipedia summary to the downloaded file.
- Uploads the updated file back to the original location in the S3 bucket.
- Generates a download link for the updated file in S3.


## Usage

- Once deployed and configured, the Lambda function can be triggered through various AWS services or API Gateway endpoints.
Example input json:
   ```
   {
     "topic": "Potatoes"
   }
   ```
- It's an example of maintaining a search history in an S3 bucket with content from Wikipedia summaries.
