import boto3
import json
import base64
import gzip
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PayloadData')

def lambda_handler(event, context):
    # Extract the log events from the CloudWatch event
    encoded_zipped_data = event['awslogs']['data']
    zipped_data = base64.b64decode(encoded_zipped_data)
    data_bytes = gzip.decompress(zipped_data)
    data = json.loads(data_bytes.decode('utf-8'))
    #print("data is " + str(data))
    
    log_events = data['logEvents']
    payload_id = str(uuid.uuid4())
    for log_event in log_events:
        timestamp = log_event['timestamp']
        message = log_event['message'].replace('\n', '')
        if 'Method request headers' in message:
            req_header = message.split('Method request headers:')[1]
        if 'Method request body' in message:
            req_payload = message.split('Method request body before transformations:')[1]
        if 'Method response body' in message:
            res_payload = message.split('Method response body after transformations:')[1]
        if 'Method response headers' in message:
            res_header = message.split('Method response headers:')[1]
    table.put_item(
        Item={
                'PayloadID' : payload_id,
                'LogGroup': data['logGroup'],
                'LogStream': data['logStream'],
                'Timestamp' : datetime.utcfromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S'),
                'RequestHeader': json.dumps(req_header),
                'RequestPayload': json.dumps(req_payload),
                'ResponseHeader': json.dumps(res_header),
                'ResponsePayload': json.dumps(res_payload)     
            }   
    ) 
    return {
        'statusCode': 200,
        'body': json.dumps('Logs Processed successfully')
        }    

        
