import pymysql
import json
import collections

#configuration
endpoint = 'ap-lib.csbgkjm5xdpr.us-east-1.rds.amazonaws.com';
username = 'admin'
password = 'H4LRH5JLmLKeBvNH'
database_name = 'ap_lib'

def lambda_handler(event, context):
    #connection
    connection = pymysql.connect(endpoint, user = username, passwd = password, db = database_name)
    
    sql = "SELECT b.starting_time, b.duration, b.num_of_person, b.booking_description, r.room_name, u.full_name FROM room_booking AS b JOIN discussion_room AS r ON b.discussion_room_id=r.discussion_room_id JOIN user_info AS u ON b.user_id=u.user_id WHERE b.starting_time > UNIX_TIMESTAMP(NOW())"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    
    full_data_array = []
    
    for row in rows:
        data_array = collections.OrderedDict()
        data_array['time'] = row[0]
        data_array['duration'] = row[1]
        data_array['person'] = row[2]
        data_array['description'] = row[3]
        data_array['room'] = row[4]
        data_array['name'] = row[5]
        full_data_array.append(data_array)
        
    response = {}
    response['statusCode'] = 200
    response['headers'] = {
        "Access-Control-Allow-Headers" : "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
    }
    response['body'] = json.dumps(full_data_array)
    
    return response

