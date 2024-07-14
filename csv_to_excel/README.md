# CSV to XLSX Conversion Lambda Function

This Lambda function converts a Base64-encoded CSV file received as an event into an XLSX format and returns the converted file as a Base64-encoded string.

## Setup

1. **AWS Setup:**
   - Ensure you have an AWS account with appropriate permissions to create and manage Lambda functions.

2. **Environment Variables:**
   - No specific environment variables are required for this function.

3. **Dependencies:**
   - This function requires the `base64` and `pandas` libraries for Base64 decoding and CSV parsing, respectively. Ensure they are included in your Lambda deployment package.

4. **Lambda Function Configuration:**
   - Create a new Lambda function in your AWS account.
   - Copy the provided `lambda_handler` function code into the Lambda function editor.

5. **Permissions:**
   - Grant necessary permissions to the Lambda function:
     - Permissions to log events (`CloudWatchLogsFullAccess` for logging).

## Function Details

The Lambda function performs the following tasks:

- Receives an event containing Base64-encoded CSV data (`body`) and a filename (`filename`).
- Decodes the Base64 data into CSV format.
- Parses the CSV data using `pandas` library.
- Converts the parsed data into XLSX format.
- Encodes the resulting XLSX data back into Base64 format.
- Returns the Base64-encoded XLSX data along with the original filename.

## Usage

- Once deployed and configured, the Lambda function can be triggered through various AWS services or API Gateway endpoints.
Example input json:
   ```json
   {
     "body": "<base64_encoded_csv_file_body>",
     "filename": "<file_name>"
   }
   ```
- It facilitates the conversion of CSV files to XLSX format, suitable for scenarios where XLSX output is required for further processing or storage.
