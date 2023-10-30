import json
from datetime import datetime

from src.storage.files_storage import FilesRepository


def handler(event, _):
    try:
        files = event["body"].get(
            "files", []
        )  # Assuming 'files' is a list of files [{'name': 'filename1', 'content': 'filecontent1'}, {...}]

        if files:
            folder_name = f'raw_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}'
            files_repository = FilesRepository()
            for file_data in files:
                file_content = file_data["content"]
                file_name = file_data["name"]

                files_repository.upload_to_s3_and_save_metadata_to_db(
                    file_content, file_name, folder_name)

        return {
            "statusCode": 200,
            "body": json.dumps("All files uploaded successfully!"),
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps("Error while uploading files!")}
