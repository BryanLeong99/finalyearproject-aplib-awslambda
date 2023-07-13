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
    
    sql = "SELECT s.subject_name, s.subject_id, x.book_subject_id FROM subject_info AS s JOIN book_subject_info AS x ON s.subject_id=x.subject_id JOIN item_info AS i ON i.book_id=x.book_id WHERE i.barcode='" + barcode + "'"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows_subject = cursor.fetchall()
    
    sql = "SELECT b.book_title, b.book_author, b.edition, b.publication_info, b.isbn, b.physical_description, b.book_id, b.image_url, i.call_number, c.coordinate_code, b.publishing_year, b.content_summary, b.book_content, i.item_id, i.coordinate_id, i.circulation_id, i.collection_id, i.library_id, i.tag_id, i.copy_number, i.availability_status_id, i.barcode FROM book_info AS b JOIN item_info As i ON b.book_id=i.book_id JOIN map_coordinate AS c ON i.coordinate_id=c.coordinate_id WHERE i.barcode='" + barcode + "'"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    
    book_data_array = []
    for row in rows:
        data_array = collections.OrderedDict()
        data_array['title'] = row[0]
        data_array['author'] = row[1]
        data_array['edition'] = row[2]
        data_array['publication'] = row[3]
        data_array['isbn'] = row[4]
        data_array['physical'] = row[5]
        data_array['bookId'] = row[6]
        data_array['image'] = row[7]
        data_array['callNumber'] = row[8]
        data_array['coordinate'] = row[9]
        data_array['year'] = row[10]
        data_array['summary'] = row[11]
        data_array['content'] = row[12]
        data_array['itemId'] = row[13]
        data_array['coordinateId'] = row[14]
        data_array['circulationId'] = row[15]
        data_array['collectionId'] = row[16]
        data_array['libraryId'] = row[17]
        data_array['tagId'] = row[18]
        data_array['copyNumber'] = row[19]
        data_array['availability'] = row[20]
        data_array['barcode'] = row[21]
        book_data_array.append(data_array)
        
    subject_data_array = []
    for row in rows_subject:
        data_array = collections.OrderedDict()
        data_array['subjectName'] = row[0]
        data_array['subjectId'] = row[1]
        data_array['bookSubjectId'] = row[2]
        subject_data_array.append(data_array)
        
    compiled_data = {}
    compiled_data['bookData'] = book_data_array
    compiled_data['subjectData'] = subject_data_array
    
    response = {}
    response['statusCode'] = 200
    response['headers'] = {
        "Access-Control-Allow-Headers" : "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
    }
    response['body'] = json.dumps(compiled_data)
    
    return response