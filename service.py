import os
import boto
from boto.ec2.regioninfo import RegionInfo

def connect_dynamodb(region):
    """
    connect to the right dynamodb 
    """

    endpoint = "dynamodb.{0}.amazonaws.com".format(region)
    region_info = RegionInfo(name=region, endpoint=endpoint)

    dDB = boto.connect_dynamodb( os.environ.get('DYNAMODB_ACCESS_KEY'), os.environ.get('DYNAMODB_SECRET_ACCESS_KEY'), region=region_info)
    return dDB

def get_table(con, table):
    """
    get reference to a specific table 
    """
    return con.get_table(table)

def get_item(table, item):
    """
    get item from specific table 
    """
    return str(table.get_item(item))

def set_item(table, index, parameters):
    """
    add a new index with in a specific table with specific parameters 
    """

    item = table.new_item( index, attrs=parameters)
    item.put()
