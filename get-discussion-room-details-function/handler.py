import pymysql
import json
import collections

#configuration
endpoint = 'ap-lib.csbgkjm5xdpr.us-east-1.rds.amazonaws.com';
username = 'admin'
password = 'H4LRH5JLmLKeBvNH'
databaseName = 'ap_lib'


def lambda_handler(event, context):
    connection = pymysql.connect(endpoint, user = username, passwd = password, db = databaseName)
    availability = event['queryStringParameters']['availability']
    notFilter = " != " if availability == '1' else "=" 
    andOrDecisionMaker = " AND " if availability == '1' else " OR "
    filterQueryPart = "discussion_room_id " + notFilter + "''"
    
    cursor = connection.cursor()
    
    # sql = "SELECT * FROM discussion_room WHERE booking_status=" + availability + " ORDER BY discussion_room_id"
    
    sqlBookedId = "SELECT discussion_room_id FROM room_booking WHERE (UNIX_TIMESTAMP(NOW()) BETWEEN starting_time AND starting_time + (duration * 3600))"
    
    cursor.execute(sqlBookedId)
    rowsBookedRoom = cursor.fetchall()
    
    
    for row in rowsBookedRoom:
        filterQueryPart += andOrDecisionMaker + "discussion_room_id" + notFilter + "'" + row[0] + "'"
        
    sql = "SELECT * FROM discussion_room WHERE " + filterQueryPart + " ORDER BY discussion_room_id"
    
    print("--------------------" + sql)
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    
    
    fullDataArray = []
    for row in rows:
        dataArray = collections.OrderedDict()
        dataArray['roomId'] = row[0]
        dataArray['roomName'] = row[1]
        dataArray['capacity'] = row[2]
        dataArray['bookingStatus'] = row[3]
        fullDataArray.append(dataArray)
        
    response = {}
    response['statusCode'] = 200
    response['body'] = json.dumps(fullDataArray)
    
    return response

    
