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
    user_token = event['queryStringParameters']['user_token']
    user_id = get_user_id(user_token)
    item_id = event['queryStringParameters']['item_id']
    loan_datetime = event['queryStringParameters']['loan_datetime']
    due_datetime = event['queryStringParameters']['due_datetime']
    tag = event['queryStringParameters']['tag']
    loan_record_id = loan_record_id_generator()
    
    if (check_loan_limit(user_id[0]) and check_role_availability(user_id[0], tag) and check_outstanding_fine(user_id[0])):
        sql = "INSERT INTO loan_record VALUES(%s, %s, %s, %s, %s, %s, %s)"
        val = (loan_record_id, loan_datetime, ' ', due_datetime, 1, item_id, user_id)
        cursor = connection.cursor()
        cursor.execute(sql, val)
        connection.commit()
        
        sqlUpdateItem = "UPDATE item_info SET availability_status_id='AS002' WHERE item_id='" + item_id + "'"
        cursor.execute(sqlUpdateItem)
        connection.commit()
        
        cursor.close()
        
    data_array = collections.OrderedDict()
    
    if (check_loan_limit(user_id[0]) and check_role_availability(user_id[0], tag) and check_outstanding_fine(user_id[0])):
        data_array['status'] = 'success'
    elif (not check_loan_limit(user_id[0])):
        data_array['status'] = 'exceed limit'
    elif (not check_outstanding_fine(user_id[0])):
        data_array['status'] = 'outstanding fine'
    else:
        data_array['status'] = 'role not available'
    
    response = {}
    response['statusCode'] = 200
    response['body'] = json.dumps(data_array)
    
    return response



def loan_record_id_generator():
    connection = pymysql.connect(endpoint, user = username, passwd = password, db = database_name)
    cursor = connection.cursor()
    cursor.execute("SELECT loan_record_id FROM loan_record ORDER BY loan_record_id DESC LIMIT 1")
    rows = cursor.fetchall()
    cursor.close()
    
    last_id_number = int(str(rows[0])[4:16])
    new_id = "LR" + (str(last_id_number + 1).zfill(12))
    
    return new_id
    
def check_loan_limit(user_id):
    connection = pymysql.connect(endpoint, user = username, passwd = password, db = database_name)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(loan_record_id) FROM loan_record WHERE user_id='" + user_id + "' AND return_datetime=' '")
    rows = cursor.fetchall()
    
    cursor.execute("SELECT r.loan_limit FROM user_role AS r JOIN user_info AS u ON r.user_role_id=u.user_role_id WHERE u.user_id='" + user_id + "'")
    rowsLimit = cursor.fetchall()
    cursor.close()
    
    # return true if the limit is not reached
    return rows < rowsLimit

def check_role_availability(user_id, tag):
    if (tag == "Green"):
        connection = pymysql.connect(endpoint, user = username, passwd = password, db = database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT r.role_name FROM user_role AS r JOIN user_info AS u On r.user_role_id=u.user_role_id WHERE u.user_id='" + user_id + "'")
        rows = cursor.fetchall()
        cursor.close()
        
        if (rows[0][0] != "Full-time Academic Staff" or rows[0][0] != "Part-time Academic Staff"):
            return False
        else: 
            return True
    
    else:
        return True
        
def check_outstanding_fine(user_id):
        connection = pymysql.connect(endpoint, user = username, passwd = password, db = database_name)
        cursor = connection.cursor()
        sql = "SELECT amount FROM fine_record WHERE user_id=%s AND paid=0"
        val = (user_id)
        cursor.execute(sql, val)
        rows = cursor.fetchall()
        cursor.close()
        
        # return true if there is no outstanding fine
        if (len(rows) > 0):
            return False
        else: 
            return True


        
def get_user_id(user_token):
    #connection
    connection = pymysql.connect(endpoint, user = username, passwd = password, db = database_name)
    cursor = connection.cursor()
    cursor.execute("SELECT user_id FROM authentication_log WHERE authentication_token='" + user_token + "'")
    rows = cursor.fetchall()
    cursor.close()
    
    return rows[0]
