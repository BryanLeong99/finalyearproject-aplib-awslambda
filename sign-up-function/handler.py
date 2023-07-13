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
    userId = userIdGenerator()
    fullName = event['queryStringParameters']['fullName']
    tpNumber = event['queryStringParameters']['tpNumber']
    userEmail = event['queryStringParameters']['email']
    userContactNumber = event['queryStringParameters']['contactNumber']
    schoolDepartmentId = event['queryStringParameters']['schoolDepartment']
    userRole = event['queryStringParameters']['userRole']
    password = event['queryStringParameters']['password']

    
    if userRole == 'RL004':
        requestId = requestIdGenerator()
        sql = "INSERT INTO librarian_registration_request VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, UNIX_TIMESTAMP(NOW()))"
        val = (requestId, fullName, tpNumber, userEmail, userContactNumber, schoolDepartmentId, userRole, password, 0)
        cursor.execute(sql, val)
        connection.commit()
        
    else:
        sql = "INSERT INTO user_info (user_id, full_name, tp_number, user_email, user_contact_number, school_department_id, user_role_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (userId, fullName, tpNumber, userEmail, userContactNumber, schoolDepartmentId, userRole)
        cursor.execute(sql, val)
        connection.commit()
        
        rows = cursor.fetchall()
        
        credentialId = credentialIdGenerator();
        sqlCredential = "INSERT INTO credential VALUES (%s, %s, %s, %s)"
        valCredential = (credentialId, tpNumber, password, userId)
        cursor.execute(sqlCredential, valCredential)
        connection.commit()
        
        settingId = settingIdGenerator()
        sqlSetting = "INSERT INTO user_setting VALUES (%s, %s, %s, %s, %s, %s)"
        valSetting = (settingId, ' ', ' ', ' ', 0, userId)
        cursor.execute(sqlSetting, valSetting)
        connection.commit()

    
    cursor.close()
    
    dataArray = collections.OrderedDict()
    dataArray['status'] = "success"
    
    response = {}
    response['statusCode'] = 200
    response['body'] = json.dumps(dataArray)
    
    return response

def userIdGenerator():
    cursor = connection.cursor()
    cursor.execute("SELECT user_id FROM user_info ORDER BY user_id DESC LIMIT 1")
    rows = cursor.fetchall()
    cursor.close()
    
    lastIdNumber = int(str(rows[0])[4:10])
    newId = "US" + (str(lastIdNumber + 1).zfill(6))
    
    return newId
    
def requestIdGenerator():
    cursor = connection.cursor()
    cursor.execute("SELECT request_id FROM librarian_registration_request ORDER BY request_id DESC LIMIT 1")
    rows = cursor.fetchall()
    cursor.close()
    
    lastIdNumber = int(str(rows[0])[4:10])
    newId = "RR" + (str(lastIdNumber + 1).zfill(6))
    
    return newId

def credentialIdGenerator():
    cursor = connection.cursor()
    cursor.execute("SELECT credential_id FROM credential ORDER BY credential_id DESC LIMIT 1")
    rows = cursor.fetchall()
    cursor.close()
    
    lastIdNumber = int(str(rows[0])[4:10])
    newId = "CR" + (str(lastIdNumber + 1).zfill(6))
    
    return newId
    
def settingIdGenerator():
    cursor = connection.cursor()
    cursor.execute("SELECT user_setting_id FROM user_setting ORDER BY user_setting_id DESC LIMIT 1")
    rows = cursor.fetchall()
    cursor.close()
    
    lastIdNumber = int(str(rows[0][0])[2:8])
    newId = "UT" + (str(lastIdNumber + 1).zfill(6))
    
    return newId