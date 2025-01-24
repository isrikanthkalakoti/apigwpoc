import json
import boto3
import datetime

s3 = boto3.client('s3')
bucket_name = 'my-file-transfer-aws-bucket'
content_to_write = ""
response_body = ""

def lambda_handler(event, context):
   
    
    try:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        current_timestamp = str(datetime.datetime.now())
        file_name = f'payload_{current_date}.txt'
        req_payload = current_timestamp + "--->>>> Trace id : " + event.get('headers').get('X-Amzn-Trace-Id') + " and Request is " + json.dumps(event.get('body'))
        
        try:
            response = s3.get_object(Bucket=bucket_name,Key=file_name)
            existing_content = response['Body'].read().decode('utf-8')
            content_to_write = existing_content + '\n' + req_payload
        except s3.exceptions.NoSuchKey:
            content_to_write = req_payload

        response_body = json.dumps('Uploaded to s3 successfully!')
        content_to_write = content_to_write+ " " + "and Response status: 200 and payload is " + response_body
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=content_to_write.encode('utf-8'))


        return {
            'statusCode': 200,
            'body': response_body
        }
    except Exception as e:
        response_body = json.dumps('Error: ' + str(e))
        content_to_write = content_to_write+ " " + "and Response status: 500 and " + response_body
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=content_to_write.encode('utf-8'))
        return {
            'statusCode': 500,
            'body': response_body
        }
