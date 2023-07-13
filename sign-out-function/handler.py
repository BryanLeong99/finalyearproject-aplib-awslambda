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
    
    user_token = event['queryStringParameters']['user_token']
    user_id = get_user_id(user_token)
    
    sql = "UPDATE user_setting SET enabled_notification=0 WHERE user_id=%s"
    val = (user_id)
    cursor = connection.cursor()
    cursor.execute(sql, val)
    connection.commit()
    cursor.close()
    
    data_array = collections.OrderedDict()
    data_array['status'] = "success"
    
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