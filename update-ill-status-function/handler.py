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
    
    request_id = event['queryStringParameters']['request_id']
    status_id = event['queryStringParameters']['status_id']
    record_id = record_id_generator()
    
    sql = "INSERT INTO ill_status_record VALUES (%s, UNIX_TIMESTAMP(NOW()), %s, %s)"
    val = (record_id, status_id, request_id)
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

def record_id_generator():
    cursor = connection.cursor()
    cursor.execute("SELECT ill_status_record_id FROM ill_status_record ORDER BY ill_status_record_id DESC LIMIT 1")
    rows = cursor.fetchall()
    cursor.close()
    
    last_id_number = int(str(rows[0])[4:16])
    new_id = "IL" + (str(last_id_number + 1).zfill(12))
    
    return new_id
    