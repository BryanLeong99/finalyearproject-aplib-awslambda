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
    
    cursor = connection.cursor()
    
    sql = "SELECT u.full_name, u.tp_number, u.user_email, u.user_contact_number, s.school_department_name, r.role_name, u.school_department_id FROM user_info AS u JOIN school_department AS s ON u.school_department_id=s.school_department_id JOIN user_role AS r ON u.user_role_id=r.user_role_id WHERE u.user_id='" + userId[0] + "'"
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    
    fullDataArray = []
    for row in rows:
        dataArray = collections.OrderedDict()
        dataArray['fullName'] = row[0]
        dataArray['tpNumber'] = row[1]
        dataArray['email'] = row[2]
        dataArray['contactNumber'] = row[3]
        dataArray['department'] = row[4]
        dataArray['role'] = row[5]
        dataArray['departmentId'] = row[6]
        fullDataArray.append(dataArray)
        
    response = {}
    response['statusCode'] = 200
    response['headers'] = {
        "Access-Control-Allow-Headers" : "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
    }
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