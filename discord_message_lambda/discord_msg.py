from discord import SyncWebhook, DiscordException
import os





def lambda_handler(event, context):
    message = event.get('message')

    if not message:
        return {
            'statusCode': 400,
            'body': 'message is empty'
        }

    try:
        url = os.environ.get("DISCORD_URL")
        webhook = SyncWebhook.from_url(url)
    except DiscordException as e:
        # Log the error (optional)
        return {
            'statusCode': 500,
            'body': f'Failed to initialize Discord webhook: {e}'
        }

    try:
        webhook.send(message)
        return {
            'statusCode': 200,
            'body': 'Discord message was successfully sent'
        }
    except DiscordException as e:
        return {
            'statusCode': 500,
            'body': f'Failed to send Discord message: {e}'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'An unexpected error occurred: {e}'
        }
