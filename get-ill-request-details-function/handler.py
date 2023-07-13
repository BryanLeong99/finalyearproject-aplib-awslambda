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
    requestId = event['queryStringParameters']['request_id']
    
    sql = "SELECT r.ill_status_record_id, r.record_datetime, s.status_name, i.resource_title, i.organisation FROM ill_status_record AS r JOIN ill_status_info AS s ON r.ill_status_id=s.ill_status_id JOIN ill_request AS i ON r.ill_request_id=i.ill_request_id WHERE r.ill_request_id='" + requestId + "' ORDER BY r.ill_status_record_id"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    
    fullDataArray = []
    for row in rows:
        dataArray = collections.OrderedDict()
        dataArray['statusRecordId'] = row[0]
        dataArray['dateTime'] = row[1]
        dataArray['status'] = row[2]
        dataArray['title'] = row[3]
        dataArray['organisation'] = row[4]
        fullDataArray.append(dataArray)
    
    response = {}
    response['statusCode'] = 200
    response['body'] = json.dumps(fullDataArray)
    
    return response
