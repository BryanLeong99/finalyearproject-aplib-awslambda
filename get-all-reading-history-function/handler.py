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
    userToken = event['queryStringParameters']['user_token']
    userId = getUserId(userToken)
    
    sql = "SELECT i.item_id, b.book_title, b.book_author, l.loan_datetime, l.return_datetime, b.image_url, l.loan_record_id FROM loan_record AS l JOIN item_info As i ON l.item_id=i.item_id JOIN book_info AS b ON i.book_id=b.book_id WHERE l.user_id='" + userId[0] + "' ORDER BY l.loan_record_id DESC"  
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    
    fullDataArray = []
    for row in rows:
        dataArray = collections.OrderedDict()
        dataArray['itemId'] = row[0]
        dataArray['bookTitle'] = row[1]
        dataArray['bookAuthor'] = row[2]
        dataArray['loanDateTime'] = row[3]
        dataArray['returnDateTime'] = row[4]
        dataArray['imageUrl'] = row[5]
        dataArray['loanRecordId'] = row[6]
        fullDataArray.append(dataArray)
        
    response = {}
    response['statusCode'] = 200
    response['body'] = json.dumps(fullDataArray)
    
    return response
    
    
def getUserId(userToken):
    #connection
    connection = pymysql.connect(endpoint, user = username, passwd = password, db = databaseName)
    cursor = connection.cursor()
    cursor.execute("SELECT user_id FROM authentication_log WHERE authentication_token='" + userToken + "'")
    rows = cursor.fetchall()
    cursor.close()
    
    return rows[0]