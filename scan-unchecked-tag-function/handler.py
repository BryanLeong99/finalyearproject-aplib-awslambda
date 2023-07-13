import pymysql
import json
import collections
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

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
    
    tag_array = []
    tag_array = event['queryStringParameters']['barcode'].split(",")
    
    print(event['queryStringParameters']['barcode'])
    print(tag_array)
    
    filtered_tag_array = []
    
    cursor = connection.cursor()
    
    for tag in tag_array:
        print(tag)
        sql = "SELECT barcode FROM item_info WHERE rfid_tag=%s"
        val = (tag)
        cursor.execute(sql, val)
        rows = cursor.fetchall()
        
        if (len(rows) > 0):
            filtered_tag_array.append(tag)
    
    unchecked_tag_array = []
    
    for tag in filtered_tag_array:
        print(tag)
        sql = "SELECT l.loan_record_id FROM loan_record AS l JOIN item_info AS i ON l.item_id=i.item_id WHERE i.rfid_tag=%s AND (l.return_datetime=' ' OR l.return_datetime='')"
        val = (tag)
        cursor.execute(sql, val)
        rows = cursor.fetchall()
        
        if (len(rows) == 0):
            unchecked_tag_array.append(tag)
            
    
    data_array = collections.OrderedDict()
    
    if (len(unchecked_tag_array) > 0):
        data_array['status'] = 'found'
            
    else:
        data_array['status'] = 'not found'
        
        payload = {
          "state": {
            "desired": {
              "welcome": "aws-iot",
              "on": False
            }
          }
        }
        
        my_shadow_client.publish("$aws/things/my_pi/shadow/update", json.dumps(payload), 1)
        
        time.sleep(5)
            
        payload = {
          "state": {
            "desired": {
              "welcome": "aws-iot",
              "on": True
            }
          }
        }
            
        my_shadow_client.publish("$aws/things/my_pi/shadow/update", json.dumps(payload), 1)
        
        
        sql = "UPDATE visit_limit SET current_total=current_total - 1 WHERE visit_limit_id=%s"
        val = ('VI01')
        cursor.execute(sql, val)
        connection.commit()
        
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

    