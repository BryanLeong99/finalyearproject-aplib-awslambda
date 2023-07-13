import pymysql
import json
import collections

#configuration
endpoint = 'ap-lib.csbgkjm5xdpr.us-east-1.rds.amazonaws.com';
username = 'admin'
password = 'H4LRH5JLmLKeBvNH'
databaseName = 'ap_lib'

#connection
connection = pymysql.connect(endpoint, user = username, passwd = password, db = databaseName)

def lambda_handler(event, context):
    cursor = connection.cursor()
    
    fine_record_id = event['queryStringParameters']['fine_record_id']
    
    fine_record_id_array = fine_record_id.split(',')
    for fine_record in fine_record_id_array:
        sql = "UPDATE fine_record SET paid=%s WHERE fine_record_id=%s"
        val = (1, fine_record)
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