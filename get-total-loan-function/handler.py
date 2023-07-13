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
    
    sql = "SELECT COUNT(loan_record_id) FROM loan_record WHERE FROM_UNIXTIME(loan_datetime, '%Y-%m-%d')=(SELECT DATE_FORMAT(CONVERT_TZ(NOW(),  '+00:00', '+08:00'), '%Y-%m-%d'))"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    sql = "SELECT COUNT(loan_record_id) FROM loan_record WHERE FROM_UNIXTIME(loan_datetime, '%Y-%m-%d')=(SELECT DATE_ADD(DATE_FORMAT(CONVERT_TZ(NOW(), '+00:00', '+08:00'), '%Y-%m-%d'), INTERVAL -1 DAY))"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows_last_day = cursor.fetchall()
    cursor.close()
    
    data_array = collections.OrderedDict()
    data_array['countToday'] = rows[0][0]
    data_array['countLastDay'] = rows_last_day[0][0]
        
    response = {}
    response['statusCode'] = 200
    response['headers'] = {
        "Access-Control-Allow-Headers" : "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
    }
    response['body'] = json.dumps(data_array)
    
    return response
    
