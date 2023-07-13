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
    
    barcode = event['queryStringParameters']['barcode']
    rfid_tag = event['queryStringParameters']['rfid_tag']
    
    data_array = collections.OrderedDict()
    
    sql = "SELECT item_id FROM item_info WHERE barcode=%s"
    val = (barcode)
    cursor.execute(sql, val)
    rows = cursor.fetchall()
    
    sql = "SELECT item_id FROM item_info WHERE rfid_tag=%s"
    val = (rfid_tag)
    cursor.execute(sql, val)
    rows_tag = cursor.fetchall()
    
    if (len(rows) > 0 and len(rows_tag) == 0):
        sql = "UPDATE item_info SET rfid_tag=%s WHERE item_id=%s"
        val = (rfid_tag, rows[0][0])
        cursor.execute(sql, val)
        connection.commit()
        
        data_array['status'] = 'success'
    elif (len(rows_tag) > 0):
        data_array['status'] = 'duplicated'
    else:
        data_array['status'] = 'not found'
        
    
    
    response = {}
    response['statusCode'] = 200
    response['headers'] = {
        "Access-Control-Allow-Headers" : "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
    }
    response['body'] = json.dumps(data_array)
    
    return response
    
    