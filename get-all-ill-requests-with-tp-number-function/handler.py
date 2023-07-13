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
    user_id = event['queryStringParameters']['user_id']
    
    sql = "SELECT i.ill_request_id, i.resource_title, s.status_name, s.ill_status_id, r.record_datetime FROM ill_request AS i JOIN ill_status_record AS r ON i.ill_request_id=r.ill_request_id JOIN ill_status_info AS s ON r.ill_status_id=s.ill_status_id WHERE i.user_id=%s AND r.ill_status_record_id=(SELECT r.ill_status_record_id FROM ill_status_record AS r WHERE r.ill_request_id=i.ill_request_id ORDER BY r.ill_status_record_id DESC LIMIT 1)"
    cursor = connection.cursor()
    val = (user_id)
    cursor.execute(sql, val)
    rows = cursor.fetchall()
    cursor.close()
    
    full_data_array = []
    
    for row in rows:
        data_array = collections.OrderedDict()
        data_array['requestId'] = row[0]
        data_array['title'] = row[1]
        data_array['statusName'] = row[2]
        data_array['statusId'] = row[3]
        data_array['date'] = row[4]
        full_data_array.append(data_array)
    
    response = {}
    response['statusCode'] = 200
    response['headers'] = {
        "Access-Control-Allow-Headers" : "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
    }
    response['body'] = json.dumps(full_data_array)
    
    return response