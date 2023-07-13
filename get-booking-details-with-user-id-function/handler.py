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
    
    cursor = connection.cursor()
    
    userToken = event['queryStringParameters']['user_token']
    userId = getUserId(userToken)
    
    sql = "SELECT r.room_booking_id, r.starting_time, r.duration, r.num_of_person, r.booking_description, r.discussion_room_id, d.room_name, r.accessed FROM room_booking AS r JOIN discussion_room AS d ON r.discussion_room_id=d.discussion_room_id WHERE r.user_id='" + userId[0] + "' AND (UNIX_TIMESTAMP(NOW()) < r.starting_time + (r.duration * 3600) + 900)"
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    
    fullDataArray = []
    
    for row in rows:
        dataArray = collections.OrderedDict()
        dataArray['bookingId'] = row[0]
        dataArray['startingTime'] = row[1]
        dataArray['duration'] = row[2]
        dataArray['numOfPerson'] = row[3]
        dataArray['description'] = row[4]
        dataArray['roomId'] = row[5]
        dataArray['room'] = row[6]
        dataArray['accessed'] = row[7]
        fullDataArray.append(dataArray)
    
    response = {}
    response['statusCode'] = 200
    response['body'] = json.dumps(fullDataArray)
    
    return response
    

def getUserId(userToken):
    connection = pymysql.connect(endpoint, user = username, passwd = password, db = databaseName)
    cursor = connection.cursor()
    cursor.execute("SELECT user_id FROM authentication_log WHERE authentication_token='" + userToken + "'")
    rows = cursor.fetchall()
    cursor.close()
    
    return rows[0]