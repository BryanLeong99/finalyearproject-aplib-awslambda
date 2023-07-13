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
    
    sql = "SELECT user_id, full_name, user_email, user_contact_number, tp_number FROM user_info WHERE tp_number=%s"
    val = (tp_number)
    cursor = connection.cursor()
    cursor.execute(sql, val)
    rows = cursor.fetchall()
    cursor.close()
    
    full_data_array = []
    for row in rows:
        data_array = collections.OrderedDict()
        data_array['userId'] = row[0]
        data_array['name'] = row[1]
        data_array['email'] = row[2]
        data_array['contactNumber'] = row[3] 
        data_array['tpNumber'] = row[4]
        full_data_array.append(data_array)
        
    response = {}
    response['statusCode'] = 200
    response['headers'] = {
        "Access-Control-Allow-Headers" : "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
    }
    response['body'] = json.dumps(full_data_array)
    
    return response;