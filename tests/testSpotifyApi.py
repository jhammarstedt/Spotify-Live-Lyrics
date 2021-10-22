import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

scope = "user-read-playback-state"

# THOSE CAN BE SET AS ENV VARIABLES IN LINUX
CLIENT_ID = '3be5443f43b14ef587f68864ed10b641'
CLIENT_SECRET = 'a3e2129ee3b8423e98bce7847c4c3a9a'
REDIRECT_URI =  'http://localhost/callback'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope))

results = sp.current_playback()
with open('results.json','w') as file:
    json_result = json.dump(results, file)
print(json_result)


'''
import requests

CLIENT_ID = '3be5443f43b14ef587f68864ed10b641'
CLIENT_SECRET = 'a3e2129ee3b8423e98bce7847c4c3a9a'

#AUTH_URL = 'https://accounts.spotify.com/api/token'
AUTH_URL = 'https://accounts.spotify.com/authorize'

# POST
auth_response = requests.redirect(AUTH_URL, {
    'grant_type': 'client_credentials',
    "scope": "user-read-private",
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET
})
# save the access token
print(auth_response.content)
access_token = auth_response.json()['access_token']

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

response = requests.get('https://api.spotify.com/v1/me/player', headers=headers)
data = response.content
print(data)
'''