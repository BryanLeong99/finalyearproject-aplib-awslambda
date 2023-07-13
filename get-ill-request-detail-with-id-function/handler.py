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
    
    sql = "SELECT u.full_name, u.tp_number, s.school_department_name, i.email, i.contact_number, i.resource_title, i.resource_author, i.publishing_year, i.publishing_city, i.publisher, i.edition, i.isbn, i.call_number, i.organisation, i.request_datetime FROM ill_request AS i JOIN user_info AS u ON i.user_id=u.user_id JOIN school_department AS s ON u.school_department_id=s.school_department_id WHERE i.ill_request_id=%s"                               
    val = (request_id)
    cursor = connection.cursor()
    cursor.execute(sql, val)
    rows = cursor.fetchall()
    cursor.close()
    
    full_data_array = []
    
    for row in rows:
        data_array = collections.OrderedDict()
        data_array['name'] = row[0]
        data_array['tpNumber'] = row[1]
        data_array['school'] = row[2]
        data_array['email'] = row[3]
        data_array['contactNumber'] = row[4]
        data_array['title'] = row[5]
        data_array['author'] = row[6]
        data_array['year'] = row[7]
        data_array['city'] = row[8]
        data_array['publisher'] = row[9]
        data_array['edition'] = row[10]
        data_array['isbn'] = row[11]
        data_array['callNumber'] = row[12]
        data_array['organisation'] = row[13]
        data_array['date'] = row[14]
        full_data_array.append(data_array)
        
    response = {}
    response['statusCode'] = 200
    response['headers'] = {
        "Access-Control-Allow-Headers" : "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
    }
    response['body'] = json.dumps(full_data_array)
    
    return response