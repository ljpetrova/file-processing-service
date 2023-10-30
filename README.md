```
                                    +-------------------------+
                                    |  uploadApi              |
                                    |   ┌─────────────────┐   |
                                    |   | Handle File Upload  |
                                    |   └─────────────────┘   |
                                    +------------|------------+
                                                 |
                                                 |
                                                 v
                                +-------------------------+
                                |  preprocessRawFile      |
                                |   ┌─────────────────┐   |
                                |   | Preprocess Files|   |
                                |   └─────────────────┘   |
                                +------------|------------+
                                                 |
                                                 |
                                                 v
                                +-------------------------+
                                |  deleteRawFile          |
                                |   ┌─────────────────┐   |
                                |   | Delete File     |   |
                                |   └─────────────────┘   |
                                +------------|------------+
                                                 |
                                                 |
                                                 v
+-------------------------+            +-------------------------+
|  AWS S3 Bucket          |            |  AWS SQS Queue          |
|                         |            |                         |
|                         |            |                         |
|                         |            |                         |
+-------------------------+            +-------------------------+
        ^                                                   |
        |                                                   |
        +---------------------------------------------------+
                                |
                                |
                                v
+-------------------------+     +-------------------------+
|  AWS SNS Topic          |     |  AWS Lambda Function    |
|  (ProcessedFileDeletionTopic) |  (RawFileDeletionQueue) |
|                         |     |                         |
|                         |     |                         |
+-------------------------+     +-------------------------+


### This architecture involves the following components:

## AWS Lambda Functions:

1. **uploadApi:**
   - Handles file upload events via HTTP POST method.

2. **preprocessRawFile:**
   - Processes files when they are created in the specified S3 bucket.

3. **deleteRawFile:**
   - Deletes files from the S3 bucket and performs soft deletion in the associated database.

## AWS Services:

1. **S3 Bucket:**
   - Stores uploaded raw files.

2. **SQS Queue (RawFileDeletionQueue):**
   - Receives messages for file deletion events.

3. **SNS Topic (ProcessedFileDeletionTopic):**
   - Coordinates the deletion of processed files.


```
