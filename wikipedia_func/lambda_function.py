import boto3
import wikipedia
import os

s3_client = boto3.client('s3')


def lambda_handler(event, context):
    # Get the topic and S3 bucket/key from the event
    topic = event.get('topic')
    if not topic:
        return {
            'statusCode': 400,
            'body': 'topic is required'
        }

    # load env vars
    bucket_name = os.getenv("BUCKET_NAME")
    file_key = os.getenv("FILE_KEY")

    # Download the existing file from S3
    download_path = '/tmp/' + file_key
    try:
        s3_client.download_file(bucket_name, file_key, download_path)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Failed to download file from S3: {str(e)}"
        }

    # Get the Wikipedia summary
    try:
        content = wikipedia.summary(topic)
    except wikipedia.exceptions.DisambiguationError as e:
        return {
            'statusCode': 400,
            'body': f"Disambiguation error: {str(e)}"
        }
    except wikipedia.exceptions.PageError:
        return {
            'statusCode': 404,
            'body': 'Page not found'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"An error occurred while fetching Wikipedia summary: {str(e)}"
        }

    # Append the content to the downloaded file
    try:
        with open(download_path, 'a') as target_file:
            target_file.write(content + "\n")
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Failed to write to file: {str(e)}"
        }

    # Upload the updated file back to S3
    try:
        s3_client.upload_file(download_path, bucket_name, file_key)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Failed to upload file to S3: {str(e)}"
        }

    # Generate the download link for the S3 file
    s3_file_url = f"https://{bucket_name}.s3.amazonaws.com/{file_key}"

    return {
        'statusCode': 200,
        'download_link': s3_file_url
    }

