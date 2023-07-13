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
    initialIndex = event['queryStringParameters']['initial_index']
    keyword = event['queryStringParameters']['keyword']
    collectionType = event['queryStringParameters']['collection']
    minYear = event['queryStringParameters']['min_year']
    maxYear = event['queryStringParameters']['max_year']
    subject = event['queryStringParameters']['subject']
    availability = event['queryStringParameters']['availability']
    sort = event['queryStringParameters']['sort']
    
    collectionQueryPart = "" if collectionType == "none" else " AND i.collection_id='" + collectionType + "'"
    
    minYearQueryPart = "" if minYear == "none" else " AND b.publishing_year>=" + minYear
    
    maxYearQueryPart = "" if maxYear == "none" else " AND b.publishing_year<=" + maxYear
    
    subjectQueryPart = "" if subject == "none" else " AND b.subject_id LIKE '%" + subject + "%'"
    
    availabilityStatus = "" if availability == "none" else availability
    availabilityQueryPart = " AND i.availability_status_id='AS001'" if availabilityStatus == "1" else "" if availabilityStatus == "" else " AND (i.availability_status_id='AS002' OR i.availability_status_id='AS003')"
    
    sortSplit = sort.split("-")
    sortQuery = "" if sort == "none" else " ORDER BY " + sortSplit[0] + " " + sortSplit[1]
    
    cursor = connection.cursor()
    
    if initialIndex == "0":
        sql = "SELECT DISTINCT i.item_id, b.book_title, b.book_author, c.collection_name, b.edition, b.publishing_year, a.availability_status_name, l.library_name, i.call_number, b.image_url FROM book_info AS b " + "JOIN item_info AS i ON b.book_id=i.book_id " + "JOIN collection_info AS c on i.collection_id=c.collection_id JOIN availability_status AS a ON a.availability_status_id=i.availability_status_id JOIN library_info AS l ON l.library_id=i.library_id JOIN book_subject_info AS x ON x.book_id=b.book_id JOIN subject_info AS s ON s.subject_id=x.subject_id" + " WHERE (s.subject_name LIKE '%" + keyword + "%')" + availabilityQueryPart + collectionQueryPart + minYearQueryPart + maxYearQueryPart + subjectQueryPart   
        cursor.execute(sql)
        rowForCounting = cursor.fetchall()
    
    sql = "SELECT DISTINCT i.item_id, b.book_title, b.book_author, c.collection_name, b.edition, b.publishing_year, a.availability_status_name, l.library_name, i.call_number, b.image_url FROM book_info AS b " + "JOIN item_info AS i ON b.book_id=i.book_id " + "JOIN collection_info AS c on i.collection_id=c.collection_id JOIN availability_status AS a ON a.availability_status_id=i.availability_status_id JOIN library_info AS l ON l.library_id=i.library_id JOIN book_subject_info AS x ON x.book_id=b.book_id JOIN subject_info AS s ON s.subject_id=x.subject_id" + " WHERE (s.subject_name LIKE '%" + keyword + "%')" + availabilityQueryPart + collectionQueryPart + minYearQueryPart + maxYearQueryPart + subjectQueryPart + sortQuery +" LIMIT " + initialIndex + ", 5"                                                                  
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    cursor.close()
    
    fullDataArray = []
    for row in rows:
        dataArray = collections.OrderedDict()
        dataArray['result_found'] = str(len(rowForCounting)) if initialIndex == "0" else "0"
        dataArray['itemId'] = row[0]
        dataArray['bookTitle'] = row[1]
        dataArray['bookAuthor'] = row[2]
        dataArray['collectionName'] = row[3]
        dataArray['edition'] = str(row[4])
        dataArray['publishingYear'] = str(row[5])
        dataArray['availabilityStatus'] = row[6]
        dataArray['libraryName'] = row[7]
        dataArray['callNumber'] = row[8]
        dataArray['imageUrl'] = row[9]
        fullDataArray.append(dataArray)
        
    response = {}
    response['statusCode'] = 200
    response['body'] = json.dumps(fullDataArray)
    print(response)
    
    return response
