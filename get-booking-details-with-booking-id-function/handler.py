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
    bookingId = event['queryStringParameters']['booking_id']
    notificationId = event['queryStringParameters']['notification_id']
    
    sql = "SELECT b.starting_time, b.duration, b.num_of_person, b.booking_description, b.discussion_room_id, r.room_name FROM room_booking AS b JOIN discussion_room AS r ON b.discussion_room_id=r.discussion_room_id WHERE b.room_booking_id='" + bookingId + "'"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    sqlUpdate = "UPDATE notification_record SET message_read=1 WHERE notification_id='" + notificationId + "'"
    cursor.execute(sqlUpdate)
    connection.commit()
    
    cursor.close()
    
    fullDataArray = []
    for row in rows:
        dataArray = collections.OrderedDict()
        dataArray['startingTime'] = row[0]
        dataArray['duration'] = row[1]
        dataArray['numOfPerson'] = row[2]
        dataArray['description'] = row[3]
        dataArray['roomId'] = row[4]
        dataArray['roomName'] = row[5]
        fullDataArray.append(dataArray)
        
    response = {}
    response['statusCode'] = 200
    response['body'] = json.dumps(fullDataArray)
    
    return response