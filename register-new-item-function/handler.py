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
    
    item_id = item_id_generator()
    barcode = new_barcode_generator()
    book_id = event['queryStringParameters']['book_id']
    circulation = event['queryStringParameters']['circulation']
    collection = event['queryStringParameters']['collection']
    library = event['queryStringParameters']['library']
    tag = event['queryStringParameters']['tag']
    call_number = event['queryStringParameters']['call_number']
    coordinate = event['queryStringParameters']['coordinate']
    copy = event['queryStringParameters']['copy']
    
    sql = "INSERT INTO item_info VALUES (%s, %s, %s, %s, %s, %s, %s, %s, '', %s, %s, %s)"
    val = (item_id, circulation, collection, int(copy), library, tag, call_number, barcode, coordinate, 'AS001', book_id)
    cursor.execute(sql, val)
    connection.commit()
    cursor.close()
    
    data_array = collections.OrderedDict()
    data_array['status'] = 'success'
    data_array['barcode'] = barcode
    
    response = {}
    response['statusCode'] = 200
    response['headers'] = {
        "Access-Control-Allow-Headers" : "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
    }
    response['body'] = json.dumps(data_array)
    
    return response


def item_id_generator():
    cursor = connection.cursor()
    cursor.execute("SELECT item_id FROM item_info ORDER BY item_id DESC LIMIT 1")
    rows = cursor.fetchall()
    cursor.close()
    
    last_id_number = int(str(rows[0])[4:10])
    new_id = "IM" + (str(last_id_number + 1).zfill(6))
    
    return new_id

def new_barcode_generator():
    cursor = connection.cursor()
    cursor.execute("SELECT barcode FROM item_info ORDER BY barcode DESC LIMIT 1")
    rows = cursor.fetchall()
    cursor.close()
    
    last_barcode = int(rows[0][0])
    new_barcode = str(last_barcode + 1).zfill(8)
    
    return new_barcode