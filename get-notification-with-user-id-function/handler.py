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
    
    sql = "SELECT notification_id, notification_datetime, description_message, related_reminder_id, message_read FROM notification_record WHERE user_id='" + userId[0] + "' ORDER BY notification_id DESC"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    
    fullDataArray = []
    for row in rows:
        dataArray = collections.OrderedDict()
        dataArray['notificationId'] = row[0]
        dataArray['notificationDateTime'] = row[1]
        dataArray['descriptionMessage'] = row[2]
        dataArray['relatedReminderId'] = row[3]
        dataArray['messageRead'] = row[4]
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