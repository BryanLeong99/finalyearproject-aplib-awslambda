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
    
    tp_number = event['queryStringParameters']['tp_number']
    email = event['queryStringParameters']['email']
    
    sql = "SELECT tp_number FROM user_info WHERE tp_number=%s OR user_email=%s"
    val = (tp_number, email)
    cursor = connection.cursor()
    cursor.execute(sql, val)
    rows = cursor.fetchall()
    
    sql = "SELECT tp_number FROM librarian_registration_request WHERE tp_number=%s OR user_email=%s"
    val = (tp_number, email)
    cursor = connection.cursor()
    cursor.execute(sql, val)
    rows1 = cursor.fetchall()
    
    sql = "SELECT full_name FROM tp_master_record WHERE tp_number=%s"
    val = (tp_number)
    cursor.execute(sql, val)
    rows2 = cursor.fetchall()
    cursor.close()

    data_array = collections.OrderedDict()
    if (len(rows) > 0 or len(rows1) > 0):
        if (len(rows) > 0):
            data_array['status'] = 'exists'
        else:
            data_array['status'] = 'in review'
    else:
        if (len(rows2) > 0):
            data_array['status'] = 'not exists'
        else:
            data_array['status'] = 'invalid tp'
    
    response = {}
    response['statusCode'] = 200
    response['headers'] = {
        "Access-Control-Allow-Headers" : "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
    }
    response['body'] = json.dumps(data_array)
    
    return response

