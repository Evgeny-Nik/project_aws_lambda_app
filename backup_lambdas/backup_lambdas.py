import boto3
import datetime
import os

s3 = boto3.client('s3')




def lambda_handler(event, context):
    source_bucket = os.getenv('SOURCE_BUCKET')
    backup_bucket = os.getenv('BACKUP_BUCKET')

    # Get the current date for backup file naming
    date = datetime.datetime.now()
    daily_backup = date.strftime('%Y-%m-%d')
    weekly_backup = date.strftime('%Y-%W')
    monthly_backup = date.strftime('%Y-%m')

    backup_status = {'daily': [], 'weekly': [], 'monthly': []}

    try:
        # List all objects in the source bucket
        objects = s3.list_objects(Bucket=source_bucket)

        for obj in objects.get('Contents'):
            file_name = obj['Key']

            copy_source = {
                'Bucket': source_bucket,
                'Key': file_name
            }
            # Create daily backup
            try:
                s3.copy(copy_source, backup_bucket, f'{daily_backup}/{file_name}')
                backup_status['daily'].append(file_name)
            except Exception as e:
                print(f"Failed to create daily backup for {file_name}: {e}")

            # Create weekly backup on Sundays
            if date.weekday() == 6:
                try:
                    s3.copy(copy_source, backup_bucket, f'{weekly_backup}/{file_name}')
                    backup_status['weekly'].append(file_name)
                except Exception as e:
                    print(f"Failed to create weekly backup for {file_name}: {e}")

            # Create monthly backup on the 1st day of the month
            if date.day == 1:
                try:
                    s3.copy(copy_source, backup_bucket, f'{monthly_backup}/{file_name}')
                    backup_status['monthly'].append(file_name)
                except Exception as e:
                    print(f"Failed to create monthly backup for {file_name}: {e}")

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'An error occurred: {str(e)}'
        }

    return {
        'statusCode': 200,
        'body': backup_status
    }
