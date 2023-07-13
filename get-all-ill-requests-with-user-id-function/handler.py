import pymysql
import json
import collections

#configuration
endpoint = 'ap-lib.csbgkjm5xdpr.us-east-1.rds.amazonaws.com';
username = 'admin'
password = 'H4LRH5JLmLKeBvNH'
databaseName = 'ap_lib'

def lambda_handler(event, context):
    #connection
    connection = pymysql.connect(endpoint, user = username, passwd = password, db = databaseName)
    userToken = event['queryStringParameters']['user_token']
    userId = getUserId(userToken)
    
    sql = "SELECT i.ill_request_id, i.resource_title, s.status_name, r.record_datetime FROM ill_request AS i JOIN ill_status_record AS r ON i.ill_request_id=r.ill_request_id JOIN ill_status_info AS s ON r.ill_status_id=s.ill_status_id WHERE i.user_id='" + userId[0] + "' AND r.ill_status_record_id=(SELECT r.ill_status_record_id FROM ill_status_record AS r WHERE r.ill_request_id=i.ill_request_id ORDER BY r.ill_status_record_id DESC LIMIT 1)"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    
    fullDataArray = []
    for row in rows:
        dataArray = collections.OrderedDict()
        dataArray['requestId'] = row[0]
        dataArray['title'] = row[1]
        dataArray['status'] = row[2]
        dataArray['dateTime'] = row[3]
        fullDataArray.append(dataArray)
        
    response = {}
    response['statusCode'] = 200
    response['body'] = json.dumps(fullDataArray)
    
    return response
    

def getUserId(userToken):
    #connection
    connection = pymysql.connect(endpoint, user = username, passwd = password, db = databaseName)
    cursor = connection.cursor()
    cursor.execute("SELECT user_id FROM authentication_log WHERE authentication_token='" + userToken + "'")
    rows = cursor.fetchall()
    cursor.close()
    
    return rows[0]