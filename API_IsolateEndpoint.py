import base64
import jwt
import hashlib
import requests
from Crypto.PublicKey import RSA
import time
import json

def create_checksum(http_method, raw_url, headers, request_body):
    string_to_hash = http_method.upper() + '|' + raw_url.lower() + '|' + headers + '|' + request_body    
    base64_string = base64.b64encode(hashlib.sha256(str.encode(string_to_hash)).digest()).decode('utf-8')
    return base64_string    
    
def create_jwt_token(appication_id, api_key, http_method, raw_url, headers, request_body,
                     iat=time.time(), algorithm='HS256', version='V1'):
    checksum = create_checksum(http_method, raw_url, headers, request_body)
    payload = {'appid': appication_id,
               'iat': iat,
               'version': version,
               'checksum': checksum}
    token = jwt.encode(payload, api_key, algorithm=algorithm).decode('utf-8')
    return token

# Use this region to setup the call info of the TMCM server (server url, application id, api key)
use_url_base = 'https://192.168.1.71:443'
use_application_id = '150848F9-A4AA-4F6F-913D-0F261DE95B58'
use_api_key = '4726B2C1-1730-4E2A-9225-D543238058BB'

# This sample is to use host name to isolate the security agent network connection.
print('Using host name to isolate the security agent network connection.')
productAgentAPIPath = '/WebApp/API/AgentResource/ProductAgents'
canonicalRequestHeaders = ''
useQueryString = ''
  
payload = {
  "host_name":"T480SWIN1001",
  "act":"cmd_isolate_agent",
  "allow_multiple_match":True
  }
useRequestBody = json.dumps(payload) 
  
jwt_token = create_jwt_token(use_application_id, use_api_key, 'POST',
                              productAgentAPIPath + useQueryString,
                              canonicalRequestHeaders, useRequestBody, iat=time.time())
 
headers = {'Authorization': 'Bearer ' + jwt_token , 'Content-Type': 'application/json;charset=utf-8'}
r = requests.post(use_url_base + productAgentAPIPath + useQueryString, headers=headers, data=useRequestBody, verify=False)

if r.status_code !=200 and r.status_code!=201:
  print('Not successful, please handle your error')

print(r.status_code)
print(json.dumps(r.json(), indent=4))
