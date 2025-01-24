import json
import boto3
import base64

s3 = boto3.client('s3')
BUCKET_NAME = 'my-file-transfer-aws-bucket'

def lambda_handler(event, context):
    try:
        file_content = event['content']
        file_name = 'first_file_upload.pdf'
        

        s3.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=base64.b64decode(file_content))

        return {
        'statusCode': 200,
        'body': json.dumps('File uploaded successfully!')
        }
    except Exception as e:
        return {
        'statusCode': 500,
        'body': json.dumps('Error uploading file: ' + str(e))
        }
