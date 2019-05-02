import os
import boto
from boto.ec2.regioninfo import RegionInfo

def connect_dynamodb(region):

    endpoint = "dynamodb.{0}.amazonaws.com".format(region)
    region_info = RegionInfo(name=region, endpoint=endpoint)

    dDB = boto.connect_dynamodb( os.environ.get('DYNAMODB_ACCESS_KEY'), os.environ.get('DYNAMODB_SECRET_ACCESS_KEY'), region=os.environ.get('AWS_DEFAULT_REGION'))
    return dDB

def get_table(con, table):

    return con.get_table(table)

def get_item(table, item):

    return str(table.get_item(item))

def set_item(table, index, parameters):


    item = table.new_item( index, attrs=parameters)
    item.put()
