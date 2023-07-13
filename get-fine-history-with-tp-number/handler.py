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
    
    tp_number = event['queryStringParameters']['tp_number']
    
    sql = "SELECT f.fine_record_id, f.fine_datetime, f.amount, b.book_title FROM fine_record AS f JOIN loan_record AS l ON f.loan_record_id=l.loan_record_id JOIN item_info AS i ON l.item_id=i.item_id JOIN book_info AS b ON i.book_id=b.book_id JOIN user_info AS u ON f.user_id=u.user_id WHERE f.paid=%s AND u.tp_number=%s ORDER BY f.fine_record_id"
    val = (0, tp_number)
    cursor = connection.cursor()
    cursor.execute(sql, val)
    rows = cursor.fetchall()
    cursor.close()
    
    full_data_array = []
    for row in rows:
        data_array = collections.OrderedDict()
        data_array['fineRecordId'] = row[0]
        data_array['date'] = int(row[1])
        data_array['amount'] = row[2]
        data_array['title'] = row[3]
        full_data_array.append(data_array)
    
    response = {}
    response['statusCode'] = 200
    response['headers'] = {
        "Access-Control-Allow-Headers" : "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
    }
    response['body'] = json.dumps(full_data_array)
    
    return response;

