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
    password = event['queryStringParameters']['newPassword']
    contactDetails = event['queryStringParameters']['contactDetails']
    print(contactDetails)
    method = event['queryStringParameters']['method']
    userId = retriveUserId(contactDetails, method)
    
    cursor = connection.cursor()
    sqlCredential = "UPDATE credential SET user_password=%s WHERE user_id=%s"
    varCredential = (password, userId)
    cursor.execute(sqlCredential, varCredential)
    connection.commit()
    cursor.close()
    
    dataArray = collections.OrderedDict()
    dataArray['status'] = "success"
    
    response = {}
    response['statusCode'] = 200
    response['body'] = json.dumps(dataArray)
    
    return response
    
def retriveUserId(contactDetails, method):
    cursor = connection.cursor()
    if method == "phone":
        sql = "SELECT user_id FROM user_info WHERE user_contact_number=" + contactDetails
        cursor.execute(sql)
        rows = cursor.fetchall()
        print("test1")
        print(rows)
        cursor.close()
        return rows[0]
    elif method == "email":
        sql = "SELECT user_id FROM user_info WHERE user_email='" + contactDetails + "'"
        cursor.execute(sql)
        rows = cursor.fetchall()
        print("test2")
        print(rows)
        cursor.close()
        return rows[0]
    else:
        sql = "SELECT user_id FROM authentication_log WHERE authentication_token='" + contactDetails + "'"
        cursor.execute(sql)
        rows = cursor.fetchall()
        print("test3")
        print(rows)
        cursor.close()
        return rows[0]
    
    

    

