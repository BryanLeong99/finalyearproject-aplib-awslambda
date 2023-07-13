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
    loanId = event['queryStringParameters']['loan_id']
    notificationId = event['queryStringParameters']['notification_id']

    sql = "SELECT i.item_id, b.book_title, b.book_author, a.loan_datetime, a.due_date, b.image_url FROM loan_record AS a JOIN item_info As i ON a.item_id=i.item_id JOIN book_info AS b ON i.book_id=b.book_id WHERE a.loan_record_id='" + loanId + "'"  
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    sqlUpdate = "UPDATE notification_record SET message_read=1 WHERE notification_id='" + notificationId + "'"
    cursor.execute(sqlUpdate)
    connection.commit()
    
    cursor.close()
    
    fullDataArray = []
    for row in rows:
        dataArray = collections.OrderedDict()
        dataArray['itemId'] = row[0]
        dataArray['bookTitle'] = row[1]
        dataArray['bookAuthor'] = row[2]
        dataArray['loanDateTime'] = row[3]
        dataArray['dueDate'] = row[4]
        dataArray['imageUrl'] = row[5]
        fullDataArray.append(dataArray)
        
    response = {}
    response['statusCode'] = 200
    response['body'] = json.dumps(fullDataArray)
    
    return response