import json
import boto3
import urllib
import os
import botocore
from urllib import urlopen
from datetime import datetime
import time
 
print('Starting function')
s3 = boto3.client('s3')


COPY_IMAGE_BUCKET = "image-dump-266"
dynamodb = boto3.resource('dynamodb')

TABLE_NAME = "request"
table = dynamodb.Table(TABLE_NAME)

def to_java_date(py_timestamp):
    try:
        java_date =  int(time.mktime(py_timestamp.timetuple())) * 1000 + py_timestamp.microsecond / 1000
        return java_date
    except:
        #some error here, return None
        return None


def lambda_handler(event, context):
    
    print "Inside lambda"
    
    print event
 
    # Get the bucket name and key (File Name)
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    print "bucket ",bucket
    print "key ",key
 
    json_content = {}
    
   
    # Get the JSON object from S3 and parse it to a JSON string
    try:
        s3object = s3.get_object(Bucket=bucket, Key=key)
       
        # For debugging purposes
        print("s3object: " + str(s3object))
       
        # Parse the object to JSON format
        s3bodydec = s3object['Body'].read().decode()
        print s3bodydec
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
            

            # image_url contains the fully qualified image path name, so we want to
            # parse out the filename
            image_url = json_content['image_url']
            filename = image_url.split("/")[-1]
            # We prepend the Primary Key, id_str, as part of the filename, separating it with ---
            # The id_str is used in another Lambda function to retrieve the object's record in DynamoDB
            
            f_str = str(to_java_date(datetime.now()))
            
            destination = "images/" + f_str +'---' + filename
            # Download the image to a temp directory
            urllib.urlretrieve(image_url, "/tmp/"+filename )
            # Save the image from Twitter URL and write to the other S3 bucket   

             # For Debugging purposes
            print( "PUT TO S3 - Key: "+ destination + ", id_str: "+json_content['id_str'])
       
            # Put the file into the new bucket, with id_str saved as metadata
            s3.put_object(Bucket=COPY_IMAGE_BUCKET,
                Key=destination,
                Metadata={
                    'id_str':f_str
                },
                Body=open("/tmp/"+filename, 'rb')
            )
       
            print("Successfully put image to S3")
            
            dynamoItem={
                'id_str': f_str,
                'loc': json_content['loc'],
                'description': json_content['description'],
                'created': json_content['created'],
                'text': json_content['text'],
                'image_url': json_content['image_url'],
                'user_handle': json_content['name'],
                'tweet_id':json_content['id_str'],
                's3_url':COPY_IMAGE_BUCKET + '/' + destination    }
            # For debugging purposes
            print("Item: " + str(dynamoItem))
       
             # Put Item to DynamoDB table
            response = table.put_item(Item=dynamoItem)
        
        
            
                    
    
    except Exception as e:
        print(e)
        raise e
 
      
    return("SUCCESS")