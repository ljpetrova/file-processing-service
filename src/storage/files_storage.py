import os

import boto3
import psycopg2  # Import the PostgreSQL adapter
from datetime import datetime
from aws_lambda_powertools import Logger, Tracer

s3 = boto3.client("s3")

# Configure your RDS details
db_host = "your-rds-endpoint"
db_user = "your-db-username"
db_pass = "your-db-password"
db_name = "your-db-name"

MB = 1024 * 1024
PRESIGNED_POST_MAX_FILESIZE = 20 * MB
logger = Logger()
tracer = Tracer()

'''
    FilesRepository is a class that handles all the interactions with S3 and RDS.
'''
class FilesRepository:
    
    '''
        upload_to_s3_and_save_metadata_to_db uploads the file to S3 and saves the metadata to RDS.
        file_content: The content of the file to be uploaded
        file_name: The name of the file to be uploaded
        folder_name: The name of the folder to be created in S3
    '''
    def upload_to_s3_and_save_metadata_to_db(
        self, file_content, file_name, folder_name
    ):
        s3_key = f"{folder_name}/{file_name}"
        bucket_name = os.environ["BUCKET_NAME"]

        # Upload to S3
        upload_id = s3.create_multipart_upload(Bucket=bucket_name, Key=s3_key)[
            "UploadId"
        ]
        part_info = s3.upload_part(
            Body=file_content,
            Bucket=bucket_name,
            Key=s3_key,
            PartNumber=1,
            UploadId=upload_id,
        )
        s3.complete_multipart_upload(
            Bucket=bucket_name,
            Key=s3_key,
            MultipartUpload={"Parts": [{"ETag": part_info["ETag"], "PartNumber": 1}]},
            UploadId=upload_id,
            PRESIGNED_POST_MAX_FILESIZE=PRESIGNED_POST_MAX_FILESIZE,
        )

        # Save metadata to RDS
        conn = psycopg2.connect(
            host=db_host, user=db_user, password=db_pass, dbname=db_name
        )
        cur = conn.cursor()

        # Prepare SQL query
        insert_query = (
            "INSERT INTO files (file_name, s3_key, folder_name) VALUES (%s, %s, %s)"
        )
        cur.execute(insert_query, (file_name, s3_key, folder_name))

        # Commit changes and close connection
        conn.commit()
        conn.close()

    '''
        delete_file_from_s3_and_soft_delete_from_db deletes the file from S3 and soft deletes the metadata from RDS.
        file_info: The information about the file to be deleted
    '''
    def delete_file_from_s3_and_soft_delete_from_db(self, file_info):
        bucket_name = file_info['bucket_name']
        file_key = file_info['file_key']

        # Delete file from S3
        s3.delete_object(Bucket=bucket_name, Key=file_key)

        # Soft delete from the database
        conn = psycopg2.connect(host=db_host, user=db_user, password=db_pass, dbname=db_name)
        cur = conn.cursor()

        # Prepare SQL query for soft delete with timestamp
        deleted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        soft_delete_query = "UPDATE files SET is_deleted = true, deleted_at = %s WHERE s3_key = %s"
        cur.execute(soft_delete_query, (deleted_at, file_key))

        # Commit changes and close connection
        conn.commit()
        conn.close()