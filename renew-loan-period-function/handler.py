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
    
    loan_record_id = event['queryStringParameters']['loan_record_id']
    new_loan_record_id = loan_record_id_generator()
    
    print(loan_record_id)
    
    sql_old_record = "SELECT UNIX_TIMESTAMP(NOW()), loan_datetime, due_date, renew, item_id, user_id FROM loan_record WHERE loan_record_id='" + loan_record_id + "'"
    cursor = connection.cursor()
    cursor.execute(sql_old_record)
    rows = cursor.fetchall()

    current_time = rows[0][0]
    duration = int(rows[0][2]) - int(rows[0][1])
    new_due_date = int(current_time) + duration
    renew_increment = rows[0][3] + 1
    
    sql_update = "UPDATE loan_record SET return_datetime=%s WHERE loan_record_id=%s"
    val_update = (current_time, loan_record_id)
    cursor.execute(sql_update, val_update)
    connection.commit()
    
    sql_insert = "INSERT INTO loan_record VALUES(%s, %s, %s, %s, %s, %s, %s)"
    val_insert = (new_loan_record_id, current_time, ' ', str(new_due_date), renew_increment, rows[0][4], rows[0][5])
    cursor.execute(sql_insert, val_insert)
    connection.commit()
    
    cursor.close()
    
    full_data_array = []
    
    data_array = collections.OrderedDict()
    data_array['status'] = 'success'
    data_array['loanDateTime'] = str(current_time)
    data_array['dueDate'] = str(new_due_date)
    
    full_data_array.append(data_array)
    
    response = {}
    response['statusCode'] = 200
    response['body'] = json.dumps(full_data_array)
    
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