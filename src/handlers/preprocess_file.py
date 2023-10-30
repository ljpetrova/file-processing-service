import json
from aws_lambda_powertools import Logger, Tracer

from src.services.preprocessing_service import PreprocessingService

# Initialize Logger and Tracer
logger = Logger()
tracer = Tracer()

@logger.inject_lambda_context
@tracer.capture_lambda_handler
def handler(event, _):
    try:
        # Get the file details from the S3 event
        records = event.get("Records", [])
        files_to_process = [record["s3"]["object"]["key"] for record in records]
        
        processed_files = []
        for file in files_to_process:
            # Call the PreprocessingService (stubbed for now)
            processed_file = PreprocessingService.preprocess_file(file)
            processed_files.append(processed_file)

        # Log processed files
        logger.info(f"Processed files: {processed_files}")

        return {
            'statusCode': 200,
            'body': json.dumps(f'Files preprocessed: {processed_files}')
        }
    except Exception as e:
        error_message = f'Error occurred during preprocessing: {str(e)}'
        return {
            'statusCode': 500,
            'body': json.dumps(error_message)
        }
