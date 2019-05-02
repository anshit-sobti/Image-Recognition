from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import json
import boto3
import os
import botocore
from urllib import urlopen
import uuid
import requests



consumer_secret =  "k0lTtj6DTsPfUWtkXynpQalFkF79xyovixmS1W6hMMN0VGJtgW"
consumer_key = "XunErNB3P5XXRCx06KvzpgXkg"
access_token = "1121188546318962690-R2cFYRzVMneHAPqczhO66yms9wrsG1"
access_token_secret = "v98uvfWzP6Yk4kPgYIFNLzGtYxUeqLUJdjPyTHuvsd801"
s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

user = "Dummy69710367"
Bucket = "image-dump-266"
url = "http://54.183.130.117:5000/api/v1/scripts"

dynamodb = boto3.resource('dynamodb')

TABLE_NAME = "request"
table = dynamodb.Table(TABLE_NAME)

print('Lamda s3 copy put....')
def lambda_handler(event, context):
    
    print event
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    print bucket
    print key
    
    outPutName = "/tmp/"+uuid.uuid4().hex
    print outPutName
    
    try:
        s3.Bucket(Bucket).download_file(key, outPutName)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
    meta_response = s3_client.head_object(Bucket=bucket, Key=key)
    
    files = {'data': open(outPutName,'rb')}
    r = requests.post(url, files=files)
    print r
    result = r.json()
    doc_id = result["response"]["doc_id"]
    print "doc_id ",doc_id
    id_str = meta_response['Metadata']['id_str']
    print "id_str ",id_str
    table.update_item(
            Key={"id_str": id_str},
            UpdateExpression="set suggestions = :m",
            ExpressionAttributeValues={
                ':m': doc_id
            },
            ReturnValues="UPDATED_NEW"
        ) 
    
    
    
    
    
    
    return("SUCCESS")
