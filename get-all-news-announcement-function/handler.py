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
    
    sql = "SELECT n.news_announcement_id, n.news_announcement_title, n.news_announcement_url, n.image_url, n.created_date, u.full_name FROM news_announcement AS n JOIN user_info AS u ON n.user_id=u.user_id"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    
    full_data_array = []
    for row in rows:
        data_array = collections.OrderedDict()
        data_array['newsAnnouncementId'] = row[0]
        data_array['newsAnnouncementTitle'] = row[1]
        data_array['newsAnnouncementUrl'] = row[2]
        data_array['imageUrl'] = row[3]
        data_array['createdDate'] = row[4]
        data_array['author'] = row[5]
        full_data_array.append(data_array)
        
    response = {}
    response['statusCode'] = 200
    response['body'] = json.dumps(full_data_array)
    
    return response