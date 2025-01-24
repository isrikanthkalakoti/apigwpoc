import json
import boto3
import base64
s3 = boto3.client('s3')

BUCKET_NAME = 'my-file-transfer-aws-bucket'
def lambda_handler(event, context):
    print(event)
    bucket_name='my-file-transfer-aws-bucket'
    image_file_name='s3image.png'
    print("Bucket Name: ",bucket_name)
    print("Image file name: ", image_file_name)
    response = s3.get_object(
        Bucket=bucket_name,
        Key=image_file_name,
)
    print("Response from s3 : ",response)
    image_file_to_be_downloaded=response['Body'].read()
    return image_file_to_be_downloaded
