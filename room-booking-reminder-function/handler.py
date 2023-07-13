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
    sql = "SELECT s.device_token, DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(r.starting_time), '+00:00', '+08:00'), '%r'), SUBSTRING_INDEX(u.full_name, ' ', 1) AS first_name, r.room_booking_id, UNIX_TIMESTAMP(NOW()), s.enabled_notification, r.starting_time, u.user_id FROM room_booking AS r JOIN user_info AS u ON r.user_id=u.user_id JOIN user_setting AS s ON u.user_id=s.user_id WHERE (UNIX_TIMESTAMP(NOW()) - r.starting_time) <= 1800 AND UNIX_TIMESTAMP(NOW()) < r.starting_time"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    fullDataArray = []
    userSegmentArray = []

    for row in rows:
        dataArray = collections.OrderedDict()
        dataArray['deviceToken'] = row[0]
        dataArray['startingTime'] = row[1]
        dataArray['firstName'] = row[2]
        dataArray['roomBookingId'] = row[3]
        dataArray['notificationDateTime'] = row[4]
        fullDataArray.append(dataArray)
        if row[5] == 1:
            userSegmentArray.append(messaging.Message(
                notification=messaging.Notification(
                    title='Room Booking Reminder from AP Lib',
                    body='Dear ' + row[2] + ', You have an upcoming room booking at "' + row[1] + '"',
                ),
                token = row[0]
            ))
        notificationId = notificationIdGenerator()
        sqlNotification = "INSERT INTO notification_record VALUES (%s, %s, %s, %s, %s, %s)"
        valNotification = (notificationId, row[4], row[6], row[3], row[7], 0)
        cursor.execute(sqlNotification, valNotification)
        connection.commit()
        
        
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