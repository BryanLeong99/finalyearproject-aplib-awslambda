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
    
    sql = "SELECT user_contact_number FROM user_info WHERE user_contact_number='" + contact_number + "'"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    
    data_array = collections.OrderedDict()
    
    if (len(rows) > 0):
        data_array['status'] = 'found'
    else:
        data_array['status'] = 'not found'
        
    response = {}
    response['statusCode'] = 200
    response['body'] = json.dumps(data_array)
    
    return response;

