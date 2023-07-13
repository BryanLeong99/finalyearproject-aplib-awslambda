import pymysql
import json
import collections

#configuration
endpoint = 'ap-lib.csbgkjm5xdpr.us-east-1.rds.amazonaws.com';
username = 'admin'
password = 'H4LRH5JLmLKeBvNH'
database_name = 'ap_lib'

def lambda_handler(event, context):
    #connection
    connection = pymysql.connect(endpoint, user = username, passwd = password, db = database_name)
    
    starting_time = event['queryStringParameters']['starting_time']
    ending_time = event['queryStringParameters']['ending_time']
    room_id = event['queryStringParameters']['room_id']
    
    sql = "UPDATE discussion_room SET starting_time=%s, ending_time=%s WHERE discussion_room_id=%s"
    val = (int(starting_time), int(ending_time), room_id)
    cursor = connection.cursor()
    cursor.execute(sql, val)
    connection.commit()
    
    cursor.close()
    
    data_array = collections.OrderedDict()
    data_array['status'] = 'success'
    
    response = {}
    response['statusCode'] = 200
    response['headers'] = {
        "Access-Control-Allow-Headers" : "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
    }
    response['body'] = json.dumps(data_array)
    
    return response
