import pymysql
import json
import collections

import firebase_admin
from firebase_admin import messaging
from firebase_admin import credentials

#configuration
endpoint = 'ap-lib.csbgkjm5xdpr.us-east-1.rds.amazonaws.com';
username = 'admin'
password = 'H4LRH5JLmLKeBvNH'
databaseName = 'ap_lib' 

cred = credentials.Certificate('ap-lib-firebase-adminsdk-kroav-71b4e95715.json')

firebase_admin.initialize_app(cred)

def lambda_handler(event, context):
    
    #connection
    connection = pymysql.connect(endpoint, user = username, passwd = password, db = databaseName)
    sql = "SELECT s.device_token, b.book_title, SUBSTRING_INDEX(u.full_name, ' ', 1) AS first_name, l.loan_record_id, UNIX_TIMESTAMP(NOW()), s.enabled_notification, s.user_id FROM loan_record AS l JOIN item_info AS i ON l.item_id=i.item_id JOIN book_info AS b ON i.book_id=b.book_id JOIN user_info AS u ON l.user_id=u.user_id JOIN user_setting AS s ON l.user_id=s.user_id WHERE (DATEDIFF(FROM_UNIXTIME(l.due_date), NOW())=3 OR DATEDIFF(FROM_UNIXTIME(l.due_date), NOW())=1) AND l.return_datetime=' ' AND UNIX_TIMESTAMP(NOW()) < l.due_date"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    fullDataArray = []
    userSegmentArray = []

    for row in rows:
        dataArray = collections.OrderedDict()
        dataArray['deviceToken'] = row[0]
        dataArray['bookTitle'] = row[1]
        dataArray['firstName'] = row[2]
        dataArray['loanRecordId'] = row[3]
        dataArray['notificationDateTime'] = row[4]
        fullDataArray.append(dataArray)
        
        if row[5] == 1:
            # add a notification object 
            userSegmentArray.append(messaging.Message(
                notification=messaging.Notification(
                    title='Due Date Reminder from AP Lib',
                    body='Dear ' + row[2] + ', you have an upcoming loaning due date for the book title of "' + row[1] + '"',
                ),
                token = row[0]
            ))
        notificationId = notificationIdGenerator()
        sqlNotification = "INSERT INTO notification_record VALUES (%s, %s, %s, %s, %s, %s)"
        valNotification = (notificationId, row[4], row[1], row[3], row[6], 0)
        cursor.execute(sqlNotification, valNotification)
        connection.commit()
        
    # send notification
    response = messaging.send_all(userSegmentArray)
    print('Successfully sent message:', response)
    
    cursor.close()
        
    response = {}
    response['statusCode'] = 200
    response['body'] = json.dumps(fullDataArray)
    
    print(response)
    
    return response

def notificationIdGenerator():
    connection = pymysql.connect(endpoint, user = username, passwd = password, db = databaseName)
    cursor = connection.cursor()
    cursor.execute("SELECT notification_id FROM notification_record ORDER BY notification_id DESC LIMIT 1")
    rows = cursor.fetchall()
    cursor.close()
    
    lastIdNumber = int(str(rows[0])[4:16])
    newId = "NT" + (str(lastIdNumber + 1).zfill(12))
    
    return newId
