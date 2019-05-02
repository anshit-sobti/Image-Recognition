TABLE_NAME = "rekognitionTable"
import json
import boto3
import urllib
import os
import botocore

 
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)
s3 = boto3.client('s3')
IMAGE_BUCKET_NAME = os.environ['S3RekBucket']
 
 
def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
 
    json_content = {}
    

    try:
        s3object = s3.get_object(Bucket=bucket, Key=key)

        print("s3object: " + str(s3object))

        s3bodydec = s3object['Body'].read().decode()

        tweets = s3bodydec.split("}{")
        for tweet in tweets:
            record = ""
            if not tweet.startswith("{"):
                record = "{" + tweet

            else:
                record = tweet
            if not tweet.endswith("}"):
                record = record  + "}"
            print("Record = " + record)
            json_content = json.loads(record)
            
            print("Successfully received JSON object from S3: " + str(json_content))
            


            image_url = json_content['image_url']
            filename = image_url.split("/")[-1]

            destination = "images/" + json_content['id_str'] +'---' + filename

            urllib.request.urlretrieve(image_url, "/tmp/"+filename )

            print( "PUT TO S3 - Key: "+ destination + ", id_str: "+json_content['id_str'])
       

            s3.put_object(Bucket=IMAGE_BUCKET_NAME,
                Key=destination,
                Metadata={
                    'id_str':json_content['id_str']
                },
                Body=open("/tmp/"+filename, 'rb')
            )
       
            print("Successfully put image to S3")
            dynamoItem={
                'id_str': json_content['id_str'],
                'loc': json_content['loc'],
                'description': json_content['description'],
                'created': json_content['created'],
                'text': json_content['text'],
                'image_url': json_content['image_url'],
                'created': json_content['user_created'],
                'user_handle': json_content['name'],
                's3_url':IMAGE_BUCKET_NAME + '/' + destination    }

            print("Item: " + str(dynamoItem))

            response = table.put_item(Item=dynamoItem)
       
            print("Successfully put item to DynamoDB")
        
    
    except Exception as e:
        print("record: " + record)
        print(e)
        raise e
 
      
    return("SUCCESS")
 
