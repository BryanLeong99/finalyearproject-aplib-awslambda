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
    
    roomId = event['queryStringParameters']['room_id']
    
    cursor = connection.cursor()
    
    sql = "SELECT r.room_booking_id, r.starting_time, r.duration, u.full_name FROM room_booking AS r JOIN user_info AS u ON r.user_id=u.user_id WHERE FROM_UNIXTIME(r.starting_time, '%Y-%m-%d')=(SELECT DATE_FORMAT(NOW(), '%Y-%m-%d')) AND r.discussion_room_id='" + roomId + "' ORDER BY r.starting_time"    
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    
    fullDataArray = []
    for row in rows:
        dataArray = collections.OrderedDict()
        dataArray['roomBookingId'] = row[0]
        dataArray['startingTime'] = row[1]
        dataArray['duration'] = row[2]
        dataArray['bookingUserFullName'] = row[3]
        fullDataArray.append(dataArray)
        
    response = {}
    response['statusCode'] = 200
    response['body'] = json.dumps(fullDataArray)
    
    return response


