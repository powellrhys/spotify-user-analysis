import requests
from dotenv import load_dotenv

import os

def authenticate(client_id, client_secret):

    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    }

    response = requests.post('https://accounts.spotify.com/api/token', data=data)

    access_token = response.json()['access_token']  

    return access_token

def collect_user_data(user_id, access_token):

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer ' + access_token,
        }

    response = requests.get(f'https://api.spotify.com/v1/users/{user_id}', headers=headers)

    return response.json()


load_dotenv()

client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
user_id = os.getenv('user_id')

access_token = authenticate(client_id, client_secret)
r = collect_user_data(user_id, access_token)
print(r)

