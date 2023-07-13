import pymysql
import json
import collections

#configuration
endpoint = 'ap-lib.csbgkjm5xdpr.us-east-1.rds.amazonaws.com';
username = 'admin'
password = 'H4LRH5JLmLKeBvNH'
databaseName = 'ap_lib'

#connection
connection = pymysql.connect(endpoint, user = username, passwd = password, db = databaseName)

def lambda_handler(event, context):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM school_department")
    
    rows = cursor.fetchall()
    cursor.close()
    
    fullDataArray = []
    
    for row in rows:
        dataArray = collections.OrderedDict()
        dataArray['schoolDepartmentId'] = row[0]
        dataArray['schoolDepartmentName'] = row[1]
        fullDataArray.append(dataArray)
        
    response = {}
    response['statusCode'] = 200
    response['body'] = json.dumps(fullDataArray)
    
    return response
    

