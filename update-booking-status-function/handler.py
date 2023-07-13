import pymysql
import json
import collections
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
    
    booking_id = event['queryStringParameters']['booking_id']
    access_param = event['queryStringParameters']['access']
    access = 1 if access_param == 'true' else 0
    
    print(access_param)
    print(event['queryStringParameters']['access'])
    print(access)
    
    sql = "UPDATE room_booking SET accessed=%s WHERE room_booking_id=%s"
    val = (access, booking_id)
    cursor = connection.cursor()
    cursor.execute(sql, val)
    connection.commit()
    
    cursor.close()
    
    if (access == 1):
        payLoadTest = {
          "state": {
            "desired": {
              "welcome": "aws-iot",
              "on": True
            }
          }
        }
        
        my_shadow_client.publish("$aws/things/my_arduino/shadow/update", json.dumps(payLoadTest), 1)
    
    else:
        payLoadTest = {
          "state": {
            "desired": {
              "welcome": "aws-iot",
              "on": False
            }
          }
        }
        
        my_shadow_client.publish("$aws/things/my_arduino/shadow/update", json.dumps(payLoadTest), 1)
    

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
    
    