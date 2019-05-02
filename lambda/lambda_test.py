from __future__ import print_function

import boto3
from decimal import Decimal
import json
import urllib
import os

print('Loading function')
this_region = os.environ['AWS_DEFAULT_REGION'];
print("region: " + this_region)

sns = boto3.client('sns')
s3 = boto3.client('s3')
ddb = boto3.resource('dynamodb')
table = ddb.Table('rekognitionTable')
rekognition = boto3.client('rekognition', this_region)


def detect_faces(bucket, key):
    response = rekognition.detect_faces(Image={"S3Object": {"Bucket": bucket, "Name": key}})
    return len(response['FaceDetails'])


def compare_faces(bucket, sourcekey, targetkey, threshold=70):
    response = rekognition.compare_faces(
        SourceImage={
            'S3Object': {
                'Bucket': bucket,
                'Name': sourcekey
            }
        },
        TargetImage={
            'S3Object': {
                'Bucket': bucket,
                'Name': targetkey
            }
        },
        SimilarityThreshold=threshold
    )

    message = ''
    tmp_str = targetkey.split("/")[-1]
    id_str = tmp_str.split("---")[0]
    print(id_str)

    for faceMatch in response['FaceMatches']:
        position = faceMatch['Face']['BoundingBox']
        similarity = str(faceMatch['Similarity'])
        record = table.get_item(Key={'id_str': id_str})
        table.update_item(
            Key={"id_str": id_str},
            UpdateExpression="set possible_match = :m, similarity=:s",
            ExpressionAttributeValues={
                ':m': 'true',
                ':s': similarity + '%'
            },
            ReturnValues="UPDATED_NEW"
        )

        print("Similarity = " + similarity)
        # We also use the DynamoDB record to provide additional twitter meta data in our message back to the subscribers of our SNS Topic
        message = ('Possible match for missing person in https://' + bucket + '.s3.amazonaws.com/' + targetkey + '\n' +
                   "Image originated from " + record['Item']['user_handle'] + ".\n" +
                   "Posted on " + record['Item']['created'] + ".\n" +
                   "Similarity of person in image to missing person : " + similarity + '%')

        send_notification(message)

    return message


def send_notification(notice):
    response = sns.publish(
        TopicArn=os.environ['SNSArn'],
        Message=notice
    )


def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    targetFile = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))

    print("bucket: " + bucket)
    print('targetFile: ' + targetFile)
    print("len(FaceDetails): " + str(detect_faces(bucket, targetFile)))

    if detect_faces(bucket, targetFile) <= 0:
        s3.delete_object(Bucket=bucket, Key=targetFile)
        print("No faces detected in " + targetFile + ". Deleting...")
    else:
        # Face(s) is/are present in the object
        print(
            "Faces detected in " + targetFile)  # We get the Missing Person photo, using the filename you provided when creating the CloudFormation stack
        sourceFile = os.environ['RefPhoto']
        print("Ref photo:" + sourceFile)
        try:

            response = compare_faces(bucket, sourceFile, targetFile)
            print(response)
            return response
        except Exception as e:
            print(e)
            raise e
