from urllib.parse import urlencode
from dotenv import load_dotenv
import pandas as pd
import webbrowser
import requests
import base64
import os

load_dotenv()

# Load in application secrets
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')

def authenticate(client_id, client_secret):

    # Configure request headers
    auth_headers = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": "http://localhost:7777/callback",
        "scope": "user-top-read, user-read-email"
    }

    # Open authentication portal
    webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))

    # Input authentication code
    code = input('Return Auth Code: ')       
    encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")

    # Configuire request headers
    token_headers = {
        "Authorization": "Basic " + encoded_credentials,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Configure request parameters
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:7777/callback"
    }

    # Send authentication request
    r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)

    # Collect access_token
    token = r.json()["access_token"]

    return token

def call_user_top_data(access_token, time_range, type):
        
    # Configure request headers
    user_headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }

    # Configure request parameters
    user_params = {
        "limit": 50,
        "time_range": time_range
    }

    # Send GET request
    response = requests.get(f"https://api.spotify.com/v1/me/top/{type}", 
                                        params=user_params, headers=user_headers).json()

    return response

def collect_user_top_track_data(access_token, time_range):

    # Collect track request response
    user_tracks_response = call_user_top_data(access_token, time_range, 'tracks')

    # Collect top data
    data = []
    for i in user_tracks_response['items']:
        artist = i['album']['artists'][0]['name']
        image_url = i['album']['images'][0]['url']
        song_name = i['album']['name']

        metadata = [song_name, artist, image_url]
        data.append(metadata)

    # Write dataframe to local storage
    df = pd.DataFrame(data=data, columns=['song_name', 'artist', 'image_url'])
    df.to_csv(f'data/top_song_data_{time_range}.csv')

def collect_user_top_artist_data(access_token, time_range):

    # Collect track request response
    user_artists_response = call_user_top_data(access_token, time_range, 'artists')

    # Collect top data
    data = []
    for i in user_artists_response['items']:
        artist = i['name']
        image_url = i['images'][0]['url']

        metadata = [artist, image_url]
        data.append(metadata)

    # Write dataframe to local storage
    df = pd.DataFrame(data=data, columns=['artist', 'image_url'])
    df.to_csv(f'data/top_artist_data_{time_range}.csv')

if __name__ == "__main__":
    # Get access token
    token = authenticate(client_id, client_secret)

    # Collect top artist and song data
    for i in ['short_term', 'medium_term', 'long_term']:
        collect_user_top_track_data(token, i)
        collect_user_top_artist_data(token, i)
