
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
    
    request_id = event['queryStringParameters']['request_id']
    status = event['queryStringParameters']['status']
    
    sql = "UPDATE librarian_registration_request SET request_status=%s WHERE request_id=%s"
    val = (int(status), request_id)
    cursor = connection.cursor()
    cursor.execute(sql, val)
    connection.commit()
    
    if int(status) == 1:
        sql = "SELECT full_name, tp_number, user_email, user_contact_number, school_department_id, user_role_id, user_password FROM librarian_registration_request WHERE request_id=%s"
        val = (request_id)
        cursor = connection.cursor()
        cursor.execute(sql, val)
        rows = cursor.fetchall()
        
        full_name = rows[0][0]
        tp_number = rows[0][1]
        user_email = rows[0][2]
        user_contact_number = rows[0][3]
        school_department_id = rows[0][4]
        user_role_id = rows[0][5]
        user_password = rows[0][6]
        
        user_id = user_id_generator()
        sql = "INSERT INTO user_info (user_id, full_name, tp_number, user_email, user_contact_number, school_department_id, user_role_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (user_id, full_name, tp_number, user_email, user_contact_number, school_department_id, user_role_id)
        cursor = connection.cursor()
        cursor.execute(sql, val)
        connection.commit()
        
        credential_id = credential_id_generator()
        sql = "INSERT INTO credential VALUES (%s, %s, %s, %s)"
        val = (credential_id, tp_number, user_password, user_id)
        cursor = connection.cursor()
        cursor.execute(sql, val)
        connection.commit()
        
        setting_id = setting_id_generator()
        sql = "INSERT INTO user_setting VALUES (%s, %s, %s, %s, %s, %s)"
        val = (setting_id, ' ', ' ', ' ', 0, user_id)
        cursor = connection.cursor()
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

def user_id_generator():
    connection = pymysql.connect(endpoint, user = username, passwd = password, db = database_name)
    cursor = connection.cursor()
    cursor.execute("SELECT user_id FROM user_info ORDER BY user_id DESC LIMIT 1")
    rows = cursor.fetchall()
    cursor.close()
    
    last_id_number = int(str(rows[0])[4:10])
    new_id = "US" + (str(last_id_number + 1).zfill(6))
    
    return new_id
    
def credential_id_generator():
    connection = pymysql.connect(endpoint, user = username, passwd = password, db = database_name)
    cursor = connection.cursor()
    cursor.execute("SELECT credential_id FROM credential ORDER BY credential_id DESC LIMIT 1")
    rows = cursor.fetchall()
    cursor.close()
    
    last_id_number = int(str(rows[0])[4:10])
    new_id = "CR" + (str(last_id_number + 1).zfill(6))
    
    return new_id
    
def setting_id_generator():
    connection = pymysql.connect(endpoint, user = username, passwd = password, db = database_name)
    cursor = connection.cursor()
    cursor.execute("SELECT user_setting_id FROM user_setting ORDER BY user_setting_id DESC LIMIT 1")
    rows = cursor.fetchall()
    cursor.close()
    
    last_id_number = int(str(rows[0][0])[2:8])
    new_id = "UT" + (str(last_id_number + 1).zfill(6))
    
    return new_id
    