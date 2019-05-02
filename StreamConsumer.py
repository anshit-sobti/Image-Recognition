import boto3
import json
from datetime import datetime
import time
from ConfigParser import SafeConfigParser
import os

config = SafeConfigParser()
config.read('twitter-rekognition.config')

region = os.environ['AWS_DEFAULT_REGION'];
print("region: " + region)

my_stream_name = config.get('firehose', 'deliverystream_name')

kinesis_client = boto3.client('kinesis', region_name=region)

response = kinesis_client.describe_stream(StreamName=my_stream_name)

my_shard_id = response['StreamDescription']['Shards'][0]['ShardId']

shard_iterator = kinesis_client.get_shard_iterator(StreamName=my_stream_name,
                                                      ShardId=my_shard_id,
                                                      ShardIteratorType='LATEST')

my_shard_iterator = shard_iterator['ShardIterator']

record_response = kinesis_client.get_records(ShardIterator=my_shard_iterator,
                                              Limit=2)

while 'NextShardIterator' in record_response:
    record_response = kinesis_client.get_records(ShardIterator=record_response['NextShardIterator'],
                                                  Limit=2)

    print record_response

    # wait for 5 seconds
    time.sleep(5)
