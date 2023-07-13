var crypto = require('crypto');
var mysql = require('mysql');
const NodeRSA = require('node-rsa');
    
const privateKey = '-----BEGIN PRIVATE KEY-----\n' +
    'MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCDzm1Q83/7eJee\n' + 
    'b2gycEJMcKMSA0udCKzrHZtxT9/EqE19jHIjgA7n6QNrKkbHDbGBU43RicCLSXwW\n' +
    'tiuHNoKG/sGSDmRCg1gHGJ+6bROlA4Dvg+rUvkU3ql2bj5+8P8CnC2vPfIBhcxKg\n' +
    'tjG5irFHH3sG1QWZWT33OKjPu7avHhZ1MsRNQOsO7BEuYyxpK19SRZV44TqxW8DF\n' +
    'TLv6BbAOxM9YrZiSYP+aOujTkvA4ZMQ5RQptEhXE0JfYEAcODtfEnUp009yZrst+\n' +
    '/y1PLjuxYZHbLnYljxH6fhlIluSYdmEX2bdUJUqFYxyxoaAiRc+XhCraX+UHqGtr\n' +
    '6vDltErnAgMBAAECggEBAIOholaX95aChpj5lcvZhLymOJUCqX74bQiZluWA6W6S\n' +
    'zmC15D9D4p8EfB+IJwsfx8fqU9WRhrMT/lMIN0xfyddbkKF2sfYjCcR8ePhLerTv\n' +
    'XNLWoa05IBNJlxaGRvZPjOzGYTLjmaq4qz/I9LvhoM3wyIK4N1FAaLv+38gmJXmY\n' +
    'TM8QZ8Fb5GSPLhDtT0Qakes9dJRu0rxJlaBYz+jemEw7DxvWm9asgyO/EpYQYsop\n' + 
    '0mBrRo1CQVc1202L9wBO+VlzNh9xtIbgI3QiuSF1joXXr6icft4wa5KZ1ShvRuwO\n' +
    'WxlTnigzLJgZVTedNNW5Cd23VRjP9KNXfIAZ+q6xjVECgYEA76R7R9MJIZAMvKIm\n' +
    'Ulv1waWuOP2IhR4wOZBfR+RKHbU8400uUmNFguBnJX+fe8ePgIbcAEodDUsX27ag\n' +
    'DOAr+EGPNWit2XITPgpVU8vU0VP7i7zXIohWX4jz+Ocg2aWIfpTQsRqMoTrbOMwB\n' +
    '564wyy6y41NdVL9GfqbB5ap0WHUCgYEAjM2dOtZnG6QEPFH96La4ubIx3pEookGR\n' + 
    'y6X8/wy8C1dZ1Tju0frJj2PWqfhLsTq0eCPJeY/azxD4WPy6YKAHPhJlrOaBie5N\n' + 
    'ovOcUbOK6wM3hP6qiBYqCcHZs1qRSr8HK9n9hOBTVzWu9bSo2RIcOz573AS/wGM+\n' + 
    '0yL2E1NLymsCgYBeBplgWwswIgb9VFnY4sAQVOOA9OlF4cxmKaFY4de6xEu5m6Tb\n' +
    'Kpwxd77A1cxLksdZVJCphGrVtmsMCCHQK3zVEVQRTps3wCyQoRlNoaJE58DA2T1I\n' +
    'DVpmbaPcO0OGYg6mK9meQ559/EvbgyAUOSJn9lC2JRVvlQUh2GgnprOzqQKBgCoB\n' +
    'IPmvgnz1dioEj8m/0OXc6hGqnkOhafwl3Y683tBHU85POLe9qCm1sBFuuC38BGCe\n' +
    '1HkGWFFTj7MEWhl/RAnZdSmabmSWieSl5ilddYDcqdBsJLWKXyogAXEHALcau+ny\n' +
    'EzZzsYkfw70bExAG3hMydcLSS935/YEBOgXT4JVXAoGBAJeNuzxXVkT7WOceKxM/\n' + 
    'MwzoWKzf5t/7EZjp+MmgW/LB8SU9UmfWoW/gGHPrQ2SXcXQkCfVGLqglY3KRmDyr\n' +
    'Nu5TeTj79ab3FLiSdElgHP5HyI4Opv7zmGmZVlvNkJQk2VjTIsx3JQ7OSPDrY3jw\n' +
    'IIg+FOqvS6YROFoi8W0A4OIu\n' + 
    '-----END PRIVATE KEY-----';
    
const privateKey2 = '-----BEGIN PRIVATE KEY-----\n' +
    'MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCDzm1Q83/7eJee\n' + 
    'b2gycEJMcKMSA0udCKzrHZtxT9/EqE19jHIjgA7n6QNrKkbHDbGBU43RicCLSXwW\n' +
    'tiuHNoKG/sGSDmRCg1gHGJ+6bROlA4Dvg+rUvkU3ql2bj5+8P8CnC2vPfIBhcxKg\n' +
    'tjG5irFHH3sG1QWZWT33OKjPu7avHhZ1MsRNQOsO7BEuYyxpK19SRZV44TqxW8DF\n' +
    'TLv6BbAOxM9YrZiSYP+aOujTkvA4ZMQ5RQptEhXE0JfYEAcODtfEnUp009yZrst+\n' +
    '/y1PLjuxYZHbLnYljxH6fhlIluSYdmEX2bdUJUqFYxyxoaAiRc+XhCraX+UHqGtr\n' +
    '6vDltErnAgMBAAECggEBAIOholaX95aChpj5lcvZhLymOJUCqX74bQiZluWA6W6S\n' +
    'zmC15D9D4p8EfB+IJwsfx8fqU9WRhrMT/lMIN0xfyddbkKF2sfYjCcR8ePhLerTv\n' +
    'XNLWoa05IBNJlxaGRvZPjOzGYTLjmaq4qz/I9LvhoM3wyIK4N1FAaLv+38gmJXmY\n' +
    'TM8QZ8Fb5GSPLhDtT0Qakes9dJRu0rxJlaBYz+jemEw7DxvWm9asgyO/EpYQYsop\n' + 
    '0mBrRo1CQVc1202L9wBO+VlzNh9xtIbgI3QiuSF1joXXr6icft4wa5KZ1ShvRuwO\n' +
    'WxlTnigzLJgZVTedNNW5Cd23VRjP9KNXfIAZ+q6xjVECgYEA76R7R9MJIZAMvKIm\n' +
    'Ulv1waWuOP2IhR4wOZBfR+RKHbU8400uUmNFguBnJX+fe8ePgIbcAEodDUsX27ag\n' +
    'DOAr+EGPNWit2XITPgpVU8vU0VP7i7zXIohWX4jz+Ocg2aWIfpTQsRqMoTrbOMwB\n' +
    '564wyy6y41NdVL9GfqbB5ap0WHUCgYEAjM2dOtZnG6QEPFH96La4ubIx3pEookGR\n' + 
    'y6X8/wy8C1dZ1Tju0frJj2PWqfhLsTq0eCPJeY/azxD4WPy6YKAHPhJlrOaBie5N\n' + 
    'ovOcUbOK6wM3hP6qiBYqCcHZs1qRSr8HK9n9hOBTVzWu9bSo2RIcOz573AS/wGM+\n' + 
    '0yL2E1NLymsCgYBeBplgWwswIgb9VFnY4sAQVOOA9OlF4cxmKaFY4de6xEu5m6Tb\n' +
    'Kpwxd77A1cxLksdZVJCphGrVtmsMCCHQK3zVEVQRTps3wCyQoRlNoaJE58DA2T1I\n' +
    'DVpmbaPcO0OGYg6mK9meQ559/EvbgyAUOSJn9lC2JRVvlQUh2GgnprOzqQKBgCoB\n' +
    'IPmvgnz1dioEj8m/0OXc6hGqnkOhafwl3Y683tBHU85POLe9qCm1sBFuuC38BGCe\n' +
    '1HkGWFFTj7MEWhl/RAnZdSmabmSWieSl5ilddYDcqdBsJLWKXyogAXEHALcau+ny\n' +
    'EzZzsYkfw70bExAG3hMydcLSS935/YEBOgXT4JVXAoGBAJeNuzxXVkT7WOceKxM/\n' + 
    'MwzoWKzf5t/7EZjp+MmgW/LB8SU9UmfWoW/gGHPrQ2SXcXQkCfVGLqglY3KRmDyr\n' +
    'Nu5TeTj79ab3FLiSdElgHP5HyI4Opv7zmGmZVlvNkJQk2VjTIsx3JQ7OSPDrY3jw\n' +
    'IIg+FOqvS6YROFoi8W0A4OIu\n' + 
    '-----END PRIVATE KEY-----';
    

    const nodeRsa = new NodeRSA(privateKey);
    
const connection = mysql.createConnection({
    host: "ap-lib.csbgkjm5xdpr.us-east-1.rds.amazonaws.com",
    user: "admin",
    password: "H4LRH5JLmLKeBvNH",
    database: "ap_lib",
});

exports.handler = async (event) => {
    var username = event['queryStringParameters']['username'];
    var password = event['queryStringParameters']['password'];
    var deviceToken = event['queryStringParameters']['device_token'];
    var buildOs = event['queryStringParameters']['build_os'];
    var deviceName = event['queryStringParameters']['device_name'];
    // var username = '';
    
    var status;
    var authenticationToken = generateToken(username);
    var roleName;

    nodeRsa.setOptions({encryptionScheme: 'pkcs1', padding: crypto.constants.RSA_PKCS1_PADDING});

    var queryResult = await authenticateCredential(username);
    
    console.log("Password: " + password);
    console.log(queryResult);
    
    
    var decryptedInputPassword = 'test';
    
    if (deviceToken != '') {
        decryptedInputPassword = crypto.privateDecrypt({key: privateKey, passphrase: '', padding: crypto.constants.RSA_NO_PADDING}, Buffer.from(password, 'base64'));
    } else {
        // decryptedInputPassword = nodeRsa.decrypt(password, 'utf8');
        decryptedInputPassword = crypto.privateDecrypt({key: privateKey, passphrase: '', padding: crypto.constants.RSA_PKCS1_PADDING}, Buffer.from(password, 'base64'));
        console.log("testing" + decryptedInputPassword.length);
    }
    
    console.log('decryptedInputPassword: ' + decryptedInputPassword);
    
    var inputPasswordHash = removePadding(decryptedInputPassword);
    
    console.log('inputPasswordHash: ' + inputPasswordHash);
    
    var storedPasswordHash = "";
    var userId = "";
    
    if (queryResult.length != 0) {
        var decryptedStoredPassword = crypto.privateDecrypt({key: privateKey, passphrase: '', padding: crypto.constants.RSA_NO_PADDING}, Buffer.from(queryResult[0]['user_password'], 'base64'));
        storedPasswordHash = removePadding(decryptedStoredPassword);
        userId = queryResult[0]['user_id'];
        var tokenExecutor = await saveToken(authenticationToken, userId);
        if (deviceToken != '') {
            var deviceTokenExecutor = await saveDeviceToken(deviceToken, buildOs, deviceName, userId);
        }
    }
    
    console.log("Input password hash: " + inputPasswordHash);
    
    
    if (deviceToken == '' && queryResult.length != 0) {
        if (decryptedInputPassword == storedPasswordHash && queryResult.length != 0 && queryResult[0]['role_name'] == 'Library Staff') {
            status = "success";
            roleName = queryResult[0]['role_name'];
            authenticationToken = authenticationToken;
            console.log("success lo");
        } else {
            status = "fail";
            roleName = "none";
            authenticationToken = "none";
            console.log("fail lo");
        }
    } else if (inputPasswordHash == storedPasswordHash && queryResult.length != 0) {
        status = "success";
        roleName = queryResult[0]['role_name'];
        authenticationToken = authenticationToken;
        console.log("success lo");
    } else {
        status = "fail";
        roleName = "none";
        authenticationToken = "none";
        console.log("fail lo");
    }
    
    
    var responseBody = {
        authenticationToken: authenticationToken,
        status: status,
        roleName: roleName,
    };
    
    console.log(responseBody);
    
    // TODO implement
    const response = {
        statusCode: 200,
        headers: {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        body: JSON.stringify(responseBody)
    };
    return response;
};

function removePadding(decryptedText) {
    var hexString = decryptedText.toString('hex');
    
    var originalText = Buffer.from(hexString.substring(hexString.lastIndexOf('00') + 2, 512), 'hex').toString();
    
    return originalText;
}

function generateToken(username) {
    const epochSeconds = Math.round(Date.now() / 1000);
    var tokenGenerated = epochSeconds + username.toLowerCase();
    
    return tokenGenerated;
}

function authenticateCredential(username) {
    return new Promise((resolve, reject) => {
        
        const sql = mysql.format("SELECT c.user_password, c.user_id, u.user_role_id, r.role_name FROM credential AS c JOIN user_info AS u ON c.user_id=u.user_id JOIN user_role AS r ON u.user_role_id=r.user_role_id WHERE username=?", [username]);
        
        connection.query(sql, function(err, results) {
            
            if (err) {
                return reject(err);
            }
            
            resolve(results);
           
          });
    });
}

async function saveToken(tokenGenerated, userId) {
    var authenticationLogId = await authenticationLogIdGenerator();
    return new Promise((resolve, reject) => {
       const sql = mysql.format("INSERT INTO authentication_log VALUES (?, ?, ?, ?)", [authenticationLogId, tokenGenerated, userId, Math.round(Date.now() / 1000)])
       console.log(sql);
       
       connection.query(sql, (err, results) => {
           if (err) {
               return reject(err);
           }
           
           resolve(results);
       });
    });
}

async function saveDeviceToken(deviceToken, buildOs, deviceName, userId) {
    return new Promise((resolve, reject) => {
       const sql = mysql.format("UPDATE user_setting SET device_token=?, device_build_os=?, device_name=?, enabled_notification=1 WHERE user_id=?", [deviceToken, buildOs, deviceName, userId])
       console.log(sql);
       
       connection.query(sql, (err, results) => {
           if (err) {
               return reject(err);
           }
           
           resolve(results);
       });
    });
}

async function authenticationLogIdGenerator() {
    var lastAuthenticationLog = await getLastAuthenticationLog();
    var lastAuthenticationIdNumber = parseInt(lastAuthenticationLog[0]['authentication_log_id'].substring(2, 14));
    var newAuthenticationIdNumber = lastAuthenticationIdNumber + 1;
    var newAuthenticationLogId = "AL" + newAuthenticationIdNumber.toString().padStart(12, "0");
    
    return newAuthenticationLogId;
}

function getLastAuthenticationLog() {
    return new Promise((resolve, reject) => {
        
        const sql = mysql.format("SELECT authentication_log_id FROM authentication_log ORDER BY authentication_log_id DESC LIMIT 1");
        
        connection.query(sql, function(err, results) {
            
            if (err) {
                return reject(err);
            }
            
            resolve(results);
           
          });
    });
}
