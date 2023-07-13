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
    
    contact_number = event['queryStringParameters']['contact_number']
    email = event['queryStringParameters']['email']
    user_token = event['queryStringParameters']['user_token']
    user_id = get_user_id(user_token)
    
    sql = "SELECT user_contact_number FROM user_info WHERE (user_contact_number='" + contact_number + "' OR user_email='" + email + "') AND NOT user_id='" + user_id[0] + "'"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()

    cursor.close()
    
    data_array = collections.OrderedDict()
    
    if (len(rows) > 0):
        data_array['status'] = 'fail'
    else:
        data_array['status'] = 'success'
        
    response = {}
    response['statusCode'] = 200
    response['body'] = json.dumps(data_array)
    
    return response;

def get_user_id(user_token):
    #connection
    connection = pymysql.connect(endpoint, user = username, passwd = password, db = database_name)
    cursor = connection.cursor()
    cursor.execute("SELECT user_id FROM authentication_log WHERE authentication_token='" + user_token + "'")
    rows = cursor.fetchall()
    cursor.close()
    
    return rows[0]