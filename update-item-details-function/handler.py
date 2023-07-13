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
    
    item_id = event['queryStringParameters']['item_id']
    circulation = event['queryStringParameters']['circulation']
    collection = event['queryStringParameters']['collection']
    library = event['queryStringParameters']['library']
    tag = event['queryStringParameters']['tag']
    call_number = event['queryStringParameters']['call_number']
    coordinate = event['queryStringParameters']['coordinate']
    availability = event['queryStringParameters']['availability']
    copy = event['queryStringParameters']['copy']
    
    sql = "UPDATE item_info SET circulation_id=%s, collection_id=%s, copy_number=%s, library_id=%s, tag_id=%s, call_number=%s, coordinate_id=%s, availability_status_id=%s WHERE item_id=%s"
    val = (circulation, collection, int(copy), library, tag, call_number, coordinate, availability, item_id)
    cursor = connection.cursor()
    cursor.execute(sql, val)
    connection.commit()
    
    cursor.close()
    
    data_array = collections.OrderedDict()
    data_array['status'] = 'success'
    
    response = {}
    response['statusCode'] = 200
    response['headers'] = {
        "Access-Control-Allow-Headers" : "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
    }
    response['body'] = json.dumps(data_array)
    
    return response
