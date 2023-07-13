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
    
    book_id = event['queryStringParameters']['book_id']
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
    
    sql = "UPDATE book_info SET book_title=%s, book_author=%s, edition=%s, publication_info=%s, publishing_year=%s, isbn=%s, physical_description=%s, content_summary=%s, book_content=%s, image_url=%s, subject_id=%s WHERE book_id=%s"
    val = (title, author, int(edition), publication, int(year), isbn, physical, summary, content, image, subject, book_id)
    # cursor = connection.cursor()
    cursor.execute(sql, val)
    connection.commit()
    
    sql = "DELETE FROM book_subject_info WHERE book_id=%s"
    val = (book_id)
    # cursor = connection.cursor()
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
    
    response = {}
    response['statusCode'] = 200
    response['headers'] = {
        "Access-Control-Allow-Headers" : "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
    }
    response['body'] = json.dumps(data_array)
    
    return response
    
def book_subject_id_generator():
    cursor = connection.cursor()
    cursor.execute("SELECT book_subject_id FROM book_subject_info ORDER BY book_subject_id DESC LIMIT 1")
    rows = cursor.fetchall()
    cursor.close()
    
    last_id_number = int(str(rows[0])[4:10])
    new_id = "BS" + (str(last_id_number + 1).zfill(6))
    
    return new_id
    