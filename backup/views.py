from django.conf import settings
from django.shortcuts import render, redirect
from .services.db_backup import backup_files_to_s3, backup_database
from .restore import restore_database

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BackupRecord
import boto3
from django.utils import timezone

@login_required
def backup_view(request):
    if request.method == "POST":
        # Backup files to S3
        backup_files_to_s3(settings.MEDIA_ROOT, 'your_s3_bucket_name', 'backups/')

        # Backup MySQL database
        backup_database('your_db_instance_identifier')

        return render(request, 'backup/backup.html', {'message': 'Backup completed successfully!'})
    return render(request, 'backup/backup.html')

@login_required
def restore_view(request):
    if request.method == "POST":
        # restore database and files
        restore_database('your_db_instance_identifier', 'your_snapshot_id')

        return render(request, 'backup/restore.html' , {'message': 'Restore completed successfully!'})
    return render(request , 'backup/restore.html')

"""
@login_required
def backup_view(request):
    if request.method == 'POST':
        # Code to trigger backup process using boto3
        s3 = boto3.client('s3')
        # Example: Backup all data to S3
        # s3.upload_file('/path/to/local/file', 'bucket-name', 'file-in-s3')
        
        # Create a record of the backup
        BackupRecord.objects.create(user=request.user, backup_type='Manual')
        messages.success(request, 'Backup successfully started.')
        return redirect('backup')
    
    return render(request, 'backup/backup.html')

@login_required
def restore_view(request):
    if request.method == 'POST':
        # Code to trigger restore process using boto3
        s3 = boto3.client('s3')
        # Example: Restore data from S3
        # s3.download_file('bucket-name', 'file-in-s3', '/path/to/local/file')
        
        messages.success(request, 'Restore process started.')
        return redirect('restore')
    
    return render(request, 'backup/restore.html')
"""