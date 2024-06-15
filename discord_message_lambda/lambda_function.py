from discord import SyncWebhook
import os

def lambda_handler(event, context):
    URL = os.environ.get("DISCORD_URL")
    message = event.get('message')
    if not message:
        return {
            'statusCode': 400,
            'body': 'message is empty'
        }
    webhook = SyncWebhook.from_url(URL)
    try:
        webhook.send(message)
        return {
            'statusCode': 200,
            'body': 'Discord message was successfully sent'
        }
    except DiscordException as e:
        # Log the error (optional)
        return {
            'statusCode': 500,
            'body': f'Failed to send Discord message: {e}'
        }