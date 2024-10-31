# Imports
import requests
from requests.auth import HTTPBasicAuth
import base64

# Variables
URL = 'http://dev.web.local'
REQUEST_RETRIES = 3
WAIT_FOR_RETRY = 1
USERNAME = 'cisco'
PASSWORD = '1234QWer'

## Send request
def send_request(url, data, headers):
    tries = 0
    while True:
        tries += 1
        try:
            response = requests.post(url=url, json=data, headers=headers)
            # Everything ok? 
            if response:
                return response.json()

            # Raise HTTP error if occurs
            response.raise_for_status() 
                    
        # Network timeout, should we retry? 
        except requests.ConnectTimeout:
            if tries < REQUEST_RETRIES:
                continue
            else:
                raise
            
# Encode string to base64
def to_base64(s):
    return base64.b64encode(s.encode('utf8')).decode('utf8')

## Basic auth
def basic_auth():
    url = URL + '/login'
    creds = to_base64(f'{USERNAME}:{PASSWORD}')
    headers = {'Authorization': f'Basic {creds}'}
    response = send_request(url, None, headers)
    print(response)
    return response.get('key')

## API Key auth
def invoke_info_v1(api_key, name):
    url = URL + '/v1/info'
    data = {'name': name}
    headers = {'x-api-key': api_key}
    response = send_request(url, data, headers)
    print(response)
    return response.get('bearer_token')
 
## Bearer token
def invoke_info_v2(bearer_token, name):
    url = URL + '/v2/info'
    data = {'name': name}
    headers = {'Authorization': f'Bearer {bearer_token}'}
    response = send_request(url, data, headers)
    print(response)

if __name__ == '__main__':
    print('Basic Auth')
    api_key = basic_auth()

    print('------------------------------------------')

    print('API Key Auth')
    bearer_token = invoke_info_v1(api_key, 'World!')

    print('------------------------------------------')

    print('Bearer Token Auth')
    invoke_info_v2(bearer_token, 'World!')