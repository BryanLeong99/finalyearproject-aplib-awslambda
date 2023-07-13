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
    
    barcode = event['queryStringParameters']['barcode']
    
    sql = "SELECT i.item_id, b.book_title, b.book_author, b.image_url, t.tag_name, a.availability_status_name FROM book_info AS b JOIN item_info AS i ON b.book_id=i.book_id JOIN material_tag AS t ON i.tag_id=t.tag_id JOIN availability_status AS a ON i.availability_status_id=a.availability_status_id WHERE i.barcode LIKE '%" + barcode + "%' ORDER BY i.item_id LIMIT 1"
    
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    
    full_data_array = []
    for row in rows:
        data_array = collections.OrderedDict()
        data_array['itemId'] = row[0]
        data_array['bookTitle'] = row[1]
        data_array['bookAuthor'] = row[2]
        data_array['imageUrl'] = row[3]
        data_array['tag'] = row[4]
        data_array['availabilityStatus'] = row[5]
        full_data_array.append(data_array)
        
    response = {}
    response['statusCode'] = 200
    response['body'] = json.dumps(full_data_array)
    
    return response
    
    
    