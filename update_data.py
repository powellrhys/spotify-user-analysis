import requests
from urllib.parse import urlencode
import base64
import webbrowser
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')

def authenticate(client_id, client_secret):

    auth_headers = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": "http://localhost:7777/callback",
        "scope": "user-top-read, user-read-email"
    }

    webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))

    code = input('Return Auth Code: ')
                
    encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")

    token_headers = {
        "Authorization": "Basic " + encoded_credentials,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:7777/callback"
    }

    r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)

    token = r.json()["access_token"]

    return token

def collect_user_track_data(access_token, time_range):

    user_headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }

    user_params = {
        "limit": 50,
        "time_range": time_range
    }

    user_tracks_response = requests.get(f"https://api.spotify.com/v1/me/top/tracks", 
                                        params=user_params, headers=user_headers).json()

    data = []
    
    for i in user_tracks_response['items']:
        artist = i['album']['artists'][0]['name']
        image_url = i['album']['images'][0]['url']
        song_name = i['album']['name']

        metadata = [song_name, artist, image_url]
        data.append(metadata)

    df = pd.DataFrame(data=data, columns=['song_name', 'artist', 'image_url'])
    df.to_csv(f'data/song_data_{time_range}.csv')


if __name__ == "__main__":
    token = authenticate(client_id, client_secret)

    for i in ['short_term', 'medium_term', 'long_term']:
        user_tracks_response = collect_user_track_data(token, i)
