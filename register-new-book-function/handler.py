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
    
    book_id = book_id_generator()
    item_id = item_id_generator()
    barcode = new_barcode_generator()
    title = event['queryStringParameters']['title']
    author = event['queryStringParameters']['author']
    edition = event['queryStringParameters']['edition']
    publication = event['queryStringParameters']['publication']
    year = event['queryStringParameters']['year']
    isbn = event['queryStringParameters']['isbn']
    physical = event['queryStringParameters']['physical']
    subject = event['queryStringParameters']['subject']
    image = event['queryStringParameters']['image']
    summary = event['queryStringParameters']['summary']
    content = event['queryStringParameters']['content']
    
    circulation = event['queryStringParameters']['circulation']
    collection = event['queryStringParameters']['collection']
    library = event['queryStringParameters']['library']
    tag = event['queryStringParameters']['tag']
    call_number = event['queryStringParameters']['call_number']
    coordinate = event['queryStringParameters']['coordinate']
    
    sql = "INSERT INTO book_info VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (book_id, title, author, int(edition), publication, int(year), isbn, physical, summary, content, image, subject)
    cursor.execute(sql, val)
    connection.commit()
    
    sql = "INSERT INTO item_info VALUES (%s, %s, %s, %s, %s, %s, %s, %s, '', %s, %s, %s)"
    val = (item_id, circulation, collection, 1, library, tag, call_number, barcode, coordinate, 'AS001', book_id)
    cursor.execute(sql, val)
    connection.commit()
    
    subject_array = subject.split(',')
    for subject_element in subject_array:
        sql = "INSERT INTO book_subject_info VALUES (%s, %s, %s)"
        book_subject_id = book_subject_id_generator()
        val = (book_subject_id, subject_element, book_id)
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
    

def book_id_generator():
    cursor = connection.cursor()
    cursor.execute("SELECT book_id FROM book_info ORDER BY book_id DESC LIMIT 1")
    rows = cursor.fetchall()
    cursor.close()
    
    last_id_number = int(str(rows[0])[4:10])
    new_id = "BK" + (str(last_id_number + 1).zfill(6))
    
    return new_id

def item_id_generator():
    cursor = connection.cursor()
    cursor.execute("SELECT item_id FROM item_info ORDER BY item_id DESC LIMIT 1")
    rows = cursor.fetchall()
    cursor.close()
    
    last_id_number = int(str(rows[0])[4:10])
    new_id = "IM" + (str(last_id_number + 1).zfill(6))
    
    return new_id
    
def book_subject_id_generator():
    cursor = connection.cursor()
    cursor.execute("SELECT book_subject_id FROM book_subject_info ORDER BY book_subject_id DESC LIMIT 1")
    rows = cursor.fetchall()
    cursor.close()
    
    last_id_number = int(str(rows[0])[4:10])
    new_id = "BS" + (str(last_id_number + 1).zfill(6))
    
    return new_id
    
def new_barcode_generator():
    cursor = connection.cursor()
    cursor.execute("SELECT barcode FROM item_info ORDER BY barcode DESC LIMIT 1")
    rows = cursor.fetchall()
    cursor.close()
    
    last_barcode = int(rows[0][0])
    new_barcode = str(last_barcode + 1).zfill(8)
    
    return new_barcode
    
