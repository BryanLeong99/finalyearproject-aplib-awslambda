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
    paid = event['queryStringParameters']['paid']
    userId = getUserId(userToken)

    sql = "SELECT f.fine_record_id, f.fine_datetime, f.amount, b.book_title FROM fine_record AS f JOIN loan_record AS l ON f.loan_record_id=l.loan_record_id JOIN item_info AS i ON l.item_id=i.item_id JOIN book_info AS b ON i.book_id=b.book_id WHERE f.paid=" + paid + " AND f.user_id='" + userId[0] + "' ORDER BY f.fine_record_id DESC"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    
    fullDataArray = []
    for row in rows:
        dataArray = collections.OrderedDict()
        dataArray['recordId'] = row[0]
        dataArray['fineDateTime'] = row[1]
        dataArray['amount'] = row[2]
        dataArray['description'] = ''
        dataArray['bookTitle'] = row[3]
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