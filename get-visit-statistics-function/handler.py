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
    
    sql = "SELECT visit_stat_id, DATE_FORMAT(FROM_UNIXTIME(stat_date), '%d/%m'), total_visit FROM visit_stat ORDER BY visit_stat_id DESC LIMIT 10"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    
    full_data_array = []
    for row in rows:
        data_array = collections.OrderedDict()
        data_array['statDate'] = row[1]
        data_array['total'] = row[2]
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
    