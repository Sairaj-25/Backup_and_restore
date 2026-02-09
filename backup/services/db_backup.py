import boto3
import os
from datetime import datetime
from django.conf import settings

def backup_files_to_s3(local_folder, bucket_name, s3_folder):
    s3 = boto3.client('s3')

    for root, dirs, files in os.walk(local_folder):
        for file in files:
            local_path = os.path.join(root, file)
            s3_path = os.path.join(s3_folder, os.path.relpath(local_path, local_folder))

            s3.upload_file(local_path, bucket_name, s3_path)
            print(f"uploaded {local_path} to s3://{bucket_name}/{s3_path}")

def backup_database(db_instance_identifier):
    rds = boto3.client('rds')

    snapshot_id = f"{db_instance_identifier}-snapshot-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

    response = rds.create_db_snapshot(
        DBInstanceIdentifier=db_instance_identifier,
        DBSnapshotIdentifier=snapshot_id
    )

    print(f"Created snapshot: {snapshot_id}")
    return response

def restore_database(db_instance_identifier, snapshot_id):
    rds = boto3.clent('rds')

    response = rds.restore_db_instance_from_db_snapshot(
        DBInstanceIdentifier=db_instance_identifier,
        DBSnapshotIdentifier=snapshot_id
    )

    print(f"Restoring from snapshot: {snapshot_id}")
    return response