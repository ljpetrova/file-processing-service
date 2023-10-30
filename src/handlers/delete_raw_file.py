import json

import boto3
import psycopg2

from src.storage.files_storage import FilesRepository

s3 = boto3.client("s3")

# Configure your RDS details
db_host = "your-rds-endpoint"
db_user = "your-db-username"
db_pass = "your-db-password"
db_name = "your-db-name"


def handler(event, _):
    try:
        # Assuming the event contains information about the files to delete
        files_to_delete = json.loads(event["Records"][0]["body"])
        if not files_to_delete:
            return {"statusCode": 200, "body": json.dumps("No files to delete!")}

        files_repository = FilesRepository()
        for file_info in files_to_delete:
            files_repository.delete_file_from_s3_and_soft_delete_from_db(file_info)

        return {"statusCode": 200, "body": json.dumps("Files deleted successfully!")}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps("Error while deleting files!")}
