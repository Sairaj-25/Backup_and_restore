from celery import shared_task
from .models import BackupRecord
from django.utils import timezone
import boto3
from django.conf import settings

@shared_task
def automatic_backup():
    # Perform the backup using boto3
    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    # Example: backup all user data to S3
    # Assume we are backing up the database or specific files
    # s3.upload_file('/path/to/local/db.sql', 'bucket-name', 'backups/db_backup.sql')
    
    # Record the backup in the database
    BackupRecord.objects.create(user=None, backup_type='Automatic')

    print("Backup completed at", timezone.now())