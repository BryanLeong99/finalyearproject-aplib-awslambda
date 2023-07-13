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
    
    bookingId = bookingIdGenerator()
    startingTime = event['queryStringParameters']['starting_time']
    duration = event['queryStringParameters']['duration']
    numOfPerson = event['queryStringParameters']['num_of_person']
    roomId = event['queryStringParameters']['room_id']
    description = event['queryStringParameters']['description']
    userToken = event['queryStringParameters']['user_token']
    userId = getUserId(userToken)
    checkAvailableSlot = checkIfSlotAvailable(roomId, int(startingTime), int(duration))
    duplicationBooking = checkDuplicationBooking(userId)
    timeLimit = checkTimeLimit(startingTime, duration, roomId)
    
    if (checkAvailableSlot and not duplicationBooking and not timeLimit):
        sql = "INSERT INTO room_booking VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (bookingId, startingTime, int(duration), int(numOfPerson), description, roomId, userId, 0)
        cursor.execute(sql, val)
        connection.commit()
        cursor.close()
    
    dataArray = collections.OrderedDict()
    
    
    if (checkAvailableSlot and not duplicationBooking and not timeLimit):
        dataArray['status'] = 'success'
    elif (duplicationBooking):
        dataArray['status'] = 'duplication found'
    elif (timeLimit):
        dataArray['status'] = 'out of operation'
    else:
        dataArray['status'] = 'slot not available'
    
    dataArray['roomId'] = roomId
    dataArray['bookingId'] = bookingId
    
    response = {}
    response['statusCode'] = 200
    response['headers'] = {
        "Access-Control-Allow-Headers" : "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
    }
    response['body'] = json.dumps(dataArray)
    
    return response
    
    
def bookingIdGenerator():
    cursor = connection.cursor()
    cursor.execute("SELECT room_booking_id FROM room_booking ORDER BY room_booking_id DESC LIMIT 1")
    rows = cursor.fetchall()
    cursor.close()
    
    lastIdNumber = int(str(rows[0])[4:16])
    newId = "RB" + (str(lastIdNumber + 1).zfill(12))
    
    return newId
    
    
def getUserId(userToken):
    cursor = connection.cursor()
    cursor.execute("SELECT user_id FROM authentication_log WHERE authentication_token='" + userToken + "'")
    rows = cursor.fetchall()
    cursor.close()
    
    return rows[0]
    
def checkIfSlotAvailable(roomId, startingTime, duration):
    cursor = connection.cursor()
    cursor.execute("SELECT starting_time, duration FROM room_booking WHERE discussion_room_id='" + roomId + "' AND FROM_UNIXTIME(starting_time, '%Y-%m-%d')=(SELECT DATE_FORMAT(NOW(), '%Y-%m-%d'))" )
    rows = cursor.fetchall()
    cursor.close()
    
    for row in rows:
        if startingTime >= int(row[0]) and startingTime < (int(row[0]) +  row[1] * 3600):
            return False
        elif startingTime <= int(row[0]) and (startingTime + duration * 3600) <= (int(row[0]) +  row[1] * 3600):
            return False
        elif startingTime <= int(row[0]) and (startingTime + duration * 3600) >= (int(row[0]) +  row[1] * 3600):
            return False
        
    return True
    
def checkTimeLimit(startingTime, duration, roomId):
    cursor = connection.cursor()
    endingTime = int(startingTime) + (int(duration) * 3600)
    sql = "SELECT starting_time, ending_time, DATE_FORMAT(FROM_UNIXTIME('" + startingTime + "'), '%H'), DATE_FORMAT(FROM_UNIXTIME('" + str(endingTime) + "'), '%H') FROM discussion_room WHERE discussion_room_id='" + roomId + "'"
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    
    startingTime = int(rows[0][0])
    endingTime = int(rows[0][1])
    bookStartTime = int(rows[0][2])
    bookEndTime = int(rows[0][3])
    
    print(startingTime)
    print(endingTime)
    print(bookStartTime)
    print(bookEndTime)
    
    if ((bookStartTime < endingTime and bookStartTime > startingTime) and (bookEndTime < endingTime and bookEndTime > startingTime)):
        return False
    
    return True
    
    

def checkDuplicationBooking(userId):
    cursor = connection.cursor()
    sql = "SELECT room_booking_id FROM room_booking WHERE user_id='" + userId[0] + "' AND (UNIX_TIMESTAMP(NOW()) < starting_time + (duration * 3600))"
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    
    if len(rows) == 0:
        return False
    
    return True
    