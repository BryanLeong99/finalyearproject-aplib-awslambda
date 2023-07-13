import pymysql
import json
import collections
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from datetime import datetime

#configuration
endpoint = 'ap-lib.csbgkjm5xdpr.us-east-1.rds.amazonaws.com';
username = 'admin'
password = 'H4LRH5JLmLKeBvNH'
database_name = 'ap_lib'

my_shadow_client = AWSIoTMQTTClient("my_client")
my_shadow_client.configureEndpoint("az655a0dlvx64-ats.iot.us-east-1.amazonaws.com", 8883)
my_shadow_client.configureCredentials("AmazonRootCA1.pem", "private.pem.key", "certificate.pem.crt")
my_shadow_client.configureConnectDisconnectTimeout(10) # 10 seconds
my_shadow_client.configureMQTTOperationTimeout(5) # 5 seconds

my_shadow_client.connect()

def lambda_handler(event, context):
    #connection
    connection = pymysql.connect(endpoint, user = username, passwd = password, db = database_name)
    
    qr = event['queryStringParameters']['qr']
    qr_text = ""
    tp_or_ap = "";
    
    if qr[0:2] == 'aa':
        qr_text = qr[2:len(qr)]
        tp_or_ap = "ap"
    else:
        qr_text = qr
        tp_or_ap = "tp"
        
    qr_copy_1 = qr_text
    qr_copy_2 = qr_text
    qr_copy_3 = qr_text
    
    qr_part_1 = qr_copy_1[0:10]
    qr_part_2 = qr_copy_2[16:22]
    qr_part_3 = qr_copy_3[22:len(qr_text)]
    
    authentication_token  = qr_part_1 + tp_or_ap + qr_part_2
    time_stamp = qr_part_3
    
    sql = "SELECT UNIX_TIMESTAMP(NOW()), user_id FROM authentication_log WHERE authentication_token=%s"
    val = (authentication_token)
    cursor = connection.cursor()
    cursor.execute(sql, val)
    rows = cursor.fetchall()
    
    sql = "SELECT total_limit, current_total FROM visit_limit"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows_limit = cursor.fetchall()
    
    current_limit = rows_limit[0][0]
    current_total = rows_limit[0][1]
    
    user_id = ""
    current_time = ""
    data_array = collections.OrderedDict()
    sat_closing_datetime = datetime.strptime(datetime.now().strftime("%x") + " 20:00:00", '%m/%d/%y %H:%M:%S')
    current_time = datetime.now()
    
    print(data_array)
    if (int(current_limit) - int(current_total) > 0):
        if (len(rows) > 0):
            current_time = rows[0][0]
            user_id = rows[0][1]
            if ((current_time - int(time_stamp)) <= 60):
                data_array['status'] = 'found'
                
                payLoadTest = {
                  "state": {
                    "desired": {
                      "welcome": "aws-iot",
                      "on": False
                    }
                  }
                }
                
                # my_shadow_client.publish("$aws/things/my_pi/shadow/name/my_pi_shadow/update", json.dumps(payLoadTest), 1)
                my_shadow_client.publish("$aws/things/my_pi/shadow/update", json.dumps(payLoadTest), 1)
                
                time.sleep(5)
                
                payLoadTest = {
                  "state": {
                    "desired": {
                      "welcome": "aws-iot",
                      "on": True
                    }
                  }
                }
                
                my_shadow_client.publish("$aws/things/my_pi/shadow/update", json.dumps(payLoadTest), 1)
                
                visit_log_id = visit_log_id_generator()
                sql = "INSERT INTO visit_log VALUES (%s, UNIX_TIMESTAMP(NOW()), %s)"
                val = (visit_log_id, user_id)
                cursor.execute(sql, val)
                connection.commit()
                
                sql = "SELECT visit_stat_id, total_visit FROM visit_stat WHERE FROM_UNIXTIME(stat_date, '%Y-%m-%d')=(SELECT DATE_FORMAT(NOW(), '%Y-%m-%d'));"
                cursor.execute(sql)
                rows = cursor.fetchall()
                
                if (len(rows) > 0):
                    visit_stat_id = rows[0][0]
                    new_total_visit = rows[0][1] + 1
                    sql = "UPDATE visit_stat SET total_visit=%s WHERE visit_stat_id=%s"
                    val = (new_total_visit, visit_stat_id)
                    cursor.execute(sql, val)
                    connection.commit()
                else:
                    visit_stat_id = visit_stat_id_generator()
                    sql = "INSERT INTO visit_stat VALUES (%s, %s, %s)"
                    val = (visit_stat_id, str(current_time), 1)
                    cursor.execute(sql, val)
                    connection.commit()
                
                sql = "SELECT current_total FROM visit_limit"
                cursor.execute(sql)
                rows = cursor.fetchall()
                
                new_total = rows[0][0] + 1
                sql = "UPDATE visit_limit SET current_total=%s"
                val = (new_total)
                cursor.execute(sql, val)
                connection.commit()
                    
                    
            else:
                data_array['status'] = 'not found'
        else: 
            data_array['status'] = 'not found'
    else:
        data_array['status'] = 'not found'
        
    cursor.close()
        
    response = {}
    response['statusCode'] = 200
    response['headers'] = {
        "Access-Control-Allow-Headers" : "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
    }
    response['body'] = json.dumps(data_array)
    
    return response
    

def visit_log_id_generator():
    connection = pymysql.connect(endpoint, user = username, passwd = password, db = database_name)
    cursor = connection.cursor()
    cursor.execute("SELECT visit_log_id FROM visit_log ORDER BY visit_log_id DESC LIMIT 1")
    rows = cursor.fetchall()
    cursor.close()
    
    last_id_number = int(str(rows[0])[4:20])
    new_id = "VL" + (str(last_id_number + 1).zfill(16))
    
    return new_id
    
def visit_stat_id_generator():
    connection = pymysql.connect(endpoint, user = username, passwd = password, db = database_name)
    cursor = connection.cursor()
    cursor.execute("SELECT visit_stat_id FROM visit_stat ORDER BY visit_stat_id DESC LIMIT 1")
    rows = cursor.fetchall()
    cursor.close()
    
    last_id_number = int(str(rows[0])[4:10])
    new_id = "VS" + (str(last_id_number + 1).zfill(6))
    
    return new_id
    
    