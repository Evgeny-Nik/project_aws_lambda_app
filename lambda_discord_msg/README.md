# Discord Message Sender Lambda Function

This Lambda function receives and sends a message to a Discord channel using a webhook URL stored in AWS Lambda environment variables.

## Setup

1. **Discord Webhook Setup:**
   - Create a webhook in your Discord server where you want to send messages. Instructions can be found [here](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks).
   - Copy the webhook URL.

2. **AWS Lambda Setup:**
   - Create an AWS Lambda function in your AWS account.
   - Configure the function with appropriate permissions to log errors and send messages to Discord.

3. **Environment Variables:**
   - Add an environment variable named `DISCORD_URL` to your Lambda function configuration.
   - Set the value of `DISCORD_URL` to the webhook URL obtained from Discord.

4. **Deploy Function Code:**
   - Copy the provided `lambda_handler` function code into your Lambda function code editor.
   - Save and deploy the Lambda function.

## Function Details

The Lambda function is triggered by an event containing a `message` parameter. It performs the following steps:

- Retrieves the `message` from the event payload.
- Initializes a Discord webhook using the `DISCORD_URL` environment variable.
- Sends the `message` to the Discord channel using the webhook.
- Returns an appropriate HTTP response based on the success or failure of the operation.

## Usage

- Once deployed, trigger the Lambda function with a test or an event containing a `message` parameter to send messages to the configured Discord channel.
Example input json:
   ```json
   {
     "message": "<message_body>"
   }
   ```