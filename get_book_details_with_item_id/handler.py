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
    itemId = event['queryStringParameters']['item_id']
    
    cursor = connection.cursor()
    
    sql = "SELECT s.subject_name, s.subject_id FROM subject_info AS s JOIN book_subject_info AS x ON s.subject_id=x.subject_id JOIN item_info AS i ON i.book_id=x.book_id WHERE i.item_id='" + itemId + "'"
    cursor.execute(sql)
    rowsSubject = cursor.fetchall()
    
    print(rowsSubject)
    
    
    sql = "SELECT DISTINCT b.book_title, b.book_author, a.availability_status_name, b.publication_info, b.isbn, b.physical_description, c.circulation_name, o.collection_name, i.copy_number, l.library_name, i.call_number, b.content_summary, b.book_content, i.coordinate_id FROM book_info AS b JOIN item_info AS i ON b.book_id=i.book_id JOIN circulation_info AS c ON c.circulation_id=i.circulation_id JOIN collection_info AS o ON o.collection_id=i.collection_id JOIN library_info AS l ON l.library_id=i.library_id JOIN availability_status AS a ON a.availability_status_id=i.availability_status_id JOIN book_subject_info AS x ON x.book_id=b.book_id JOIN subject_info AS s ON s.subject_id=x.subject_id WHERE i.item_id='" + itemId + "'"                                                                  
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    sql = "SELECT coordinate_code, x_coordinate, y_coordinate FROM map_coordinate WHERE coordinate_id='" + rows[0][13] + "'"
    cursor.execute(sql)
    rowsCoordinate = cursor.fetchall()
    
    cursor.close()
    
    fullDataArray = []
    fullSubjectArray = []
    
    print(rows)
    
    for row in rows:
        dataArray = collections.OrderedDict()
        dataArray['bookTitle'] = row[0]
        dataArray['bookAuthor'] = row[1]
        dataArray['availabilityStatusName'] = row[2]
        dataArray['publicationInfo'] = row[3]
        dataArray['isbn'] = row[4]
        dataArray['physicalDescription'] = row[5]
        dataArray['circulationName'] = row[6]
        dataArray['collectionName'] = row[7]
        dataArray['copyNumber'] = row[8]
        dataArray['libraryName'] = row[9]
        dataArray['callNumber'] = row[10]
        dataArray['contentSummary'] = row[11]
        dataArray['bookContent'] = row[12]
        dataArray['coordinateCode'] = ' ' if (len(rowsCoordinate) == 0) else rowsCoordinate[0][0]
        dataArray['xCoordinate'] = 0 if (len(rowsCoordinate) == 0) else rowsCoordinate[0][1]
        dataArray['yCoordinate'] = 0 if (len(rowsCoordinate) == 0) else rowsCoordinate[0][2]

        fullDataArray.append(dataArray)
    
    for row in rowsSubject:
        dataArray = collections.OrderedDict()
        dataArray['subjectId'] = row[1]
        dataArray['subjectName'] = row[0]

        fullSubjectArray.append(dataArray)
    
    compiledData = {}
    compiledData['bookDetails'] = fullDataArray
    compiledData['subjects'] = fullSubjectArray
        
    response = {}
    response['statusCode'] = 200
    response['body'] = json.dumps(compiledData)
    print(response)
    
    return response

