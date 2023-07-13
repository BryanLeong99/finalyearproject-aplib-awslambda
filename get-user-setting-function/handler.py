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
    
    sql = "SELECT user_setting_id, device_build_os, device_name, enabled_notification FROM user_setting WHERE user_id=%s"
    val = (user_id)
    cursor = connection.cursor()
    cursor.execute(sql, val)
    rows = cursor.fetchall()
    cursor.close()
    
    full_data_array = []
    for row in rows:
        data_array = collections.OrderedDict()
        data_array['settingId'] = row[0]
        data_array['buildOs'] = row[1]
        data_array['deviceName'] = row[2]
        data_array['enabledNotification'] = row[3]
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


def get_user_id(user_token):
    #connection
    connection = pymysql.connect(endpoint, user = username, passwd = password, db = database_name)
    cursor = connection.cursor()
    cursor.execute("SELECT user_id FROM authentication_log WHERE authentication_token='" + user_token + "'")
    rows = cursor.fetchall()
    cursor.close()
    
    return rows[0]