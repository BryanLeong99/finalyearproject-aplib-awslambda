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
    
    requestId = illRequestIdGenerator()
    requestDateTime = event['queryStringParameters']['date_time']
    email = event['queryStringParameters']['email']
    contactNumber = event['queryStringParameters']['contact_number']
    title = event['queryStringParameters']['title']
    author = event['queryStringParameters']['author']
    year = event['queryStringParameters']['year']
    city = event['queryStringParameters']['city']
    publisher = event['queryStringParameters']['publisher']
    edition = event['queryStringParameters']['edition']
    isbn = event['queryStringParameters']['isbn']
    callNumber = event['queryStringParameters']['call_number']
    organisation = event['queryStringParameters']['organisation']
    userToken = event['queryStringParameters']['user_token']
    userId = getUserId(userToken)
    statusRecordId = illStatusRecordIdGenerator()
    
    cursor = connection.cursor()
    
    sqlIllRequest = "INSERT INTO ill_request VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    valIllRequest = (requestId, requestDateTime, email, contactNumber, title, author, year, city, publisher, int(edition), isbn, callNumber, organisation, userId)
    cursor.execute(sqlIllRequest, valIllRequest)
    connection.commit()
    
    sqlStatusRecord = "INSERT INTO ill_status_record VALUES (%s, %s, %s, %s)"
    valStatusRecord = (statusRecordId, requestDateTime, 'IS001', requestId)
    cursor.execute(sqlStatusRecord, valStatusRecord)
    connection.commit()
    
    dataArray = collections.OrderedDict()
    dataArray['status'] = "success"
    
    response = {}
    response['statusCode'] = 200
    response['body'] = json.dumps(dataArray)
    
    return response
    
    
    
def illRequestIdGenerator():
    connection = pymysql.connect(endpoint, user = username, passwd = password, db = databaseName)
    cursor = connection.cursor()
    cursor.execute("SELECT ill_request_id FROM ill_request ORDER BY ill_request_id DESC LIMIT 1")
    rows = cursor.fetchall()
    cursor.close()
    
    lastIdNumber = int(str(rows[0])[4:10])
    newId = "IR" + (str(lastIdNumber + 1).zfill(6))
    
    return newId
    

def illStatusRecordIdGenerator():
    connection = pymysql.connect(endpoint, user = username, passwd = password, db = databaseName)
    cursor = connection.cursor()
    cursor.execute("SELECT ill_status_record_id FROM ill_status_record ORDER BY ill_status_record_id DESC LIMIT 1")
    rows = cursor.fetchall()
    cursor.close()
    
    lastIdNumber = int(str(rows[0])[4:16])
    newId = "IL" + (str(lastIdNumber + 1).zfill(12))
    
    return newId

    
    
def getUserId(userToken):
    connection = pymysql.connect(endpoint, user = username, passwd = password, db = databaseName)
    cursor = connection.cursor()
    cursor.execute("SELECT user_id FROM authentication_log WHERE authentication_token='" + userToken + "'")
    rows = cursor.fetchall()
    cursor.close()
    
    return rows[0]