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
    
    sql = "SELECT l.loan_record_id, l.user_id, t.fine_amount FROM loan_record AS l JOIN item_info AS i ON l.item_id=i.item_id JOIN material_tag AS t ON i.tag_id=t.tag_id WHERE l.due_date < UNIX_TIMESTAMP(NOW()) AND (l.return_datetime='' OR l.return_datetime=' ')"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    
    for row in rows:
        fine_record_id = fine_record_id_generator()

        sql = "INSERT INTO fine_record VALUES (%s, UNIX_TIMESTAMP(NOW()), %s, %s, %s, %s)"
        val = (fine_record_id, row[2], 0, row[0], row[1])
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
    
    
        
def fine_record_id_generator():
    #connection
    connection = pymysql.connect(endpoint, user = username, passwd = password, db = database_name)
    cursor = connection.cursor()
    cursor.execute("SELECT fine_record_id FROM fine_record ORDER BY fine_record_id DESC LIMIT 1")
    rows = cursor.fetchall()
    cursor.close()
    
    last_id_number = int(str(rows[0])[4:16])
    new_id = "FR" + (str(last_id_number + 1).zfill(12))
    
    return new_id
        
    
