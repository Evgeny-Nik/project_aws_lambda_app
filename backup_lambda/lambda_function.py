import boto3
import datetime

s3 = boto3.client('s3')


def lambda_handler(event, context):
    source_bucket = 'lambda-func-bocket'
    backup_bucket = 'lambda-api-backup-bucket'

    # Get the current date for backup file naming
    date = datetime.datetime.now()
    daily_backup = date.strftime('%Y-%m-%d')
    weekly_backup = date.strftime('%Y-%W')
    monthly_backup = date.strftime('%Y-%m')

    # List all objects in the source bucket
    objects = s3.list_objects(Bucket=source_bucket)

    backup_status = {'daily': [], 'weekly': [], 'monthly': []}

    for object in objects['Contents']:
        file_name = object['Key']

        # Copy the object to the backup bucket
        copy_source = {
            'Bucket': source_bucket,
            'Key': file_name
        }

        # Create daily, weekly and monthly backups
        s3.copy(copy_source, backup_bucket, f'{daily_backup}/{file_name}')
        backup_status['daily'].append(file_name)

        if date.weekday() == 6:  # If it's Sunday, create a weekly backup
            s3.copy(copy_source, backup_bucket, f'{weekly_backup}/{file_name}')
            backup_status['weekly'].append(file_name)

        if date.day == 1:  # If it's the first day of the month, create a monthly backup
            s3.copy(copy_source, backup_bucket, f'{monthly_backup}/{file_name}')
            backup_status['monthly'].append(file_name)


    return backup_status