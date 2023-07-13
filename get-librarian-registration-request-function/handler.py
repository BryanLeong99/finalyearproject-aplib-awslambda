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
    
    sql = "SELECT request_id, full_name, tp_number, user_email, user_contact_number, request_date FROM librarian_registration_request WHERE request_status=0"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    
    full_data_array = []
    for row in rows:
        data_array = collections.OrderedDict()
        data_array['requestId'] = row[0]
        data_array['fullName'] = row[1]
        data_array['tpNumber'] = row[2]
        data_array['email'] = row[3]
        data_array['contactNumber'] = row[4]
        data_array['date'] = row[5]
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