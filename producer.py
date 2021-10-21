from kafka import KafkaProducer
from time import sleep
import json
from json import dumps
from decouple import config

import spotipy
from spotipy.oauth2 import SpotifyOAuth

################################
#       CONSTANTS              #
################################

PERIOD = 1

################################
#       AUTHENTIFICATION       #
################################

scope = "user-read-playback-state user-read-playback-position"

# THOSE CAN BE SET AS ENV VARIABLES IN LINUX
CLIENT_ID = config('CLIENT_ID',default='')
CLIENT_SECRET = config('CLIENT_SECRET',default='')
REDIRECT_URI =  'http://localhost/callback'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope))

################################
#       PRODUCER INIT          #
################################

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], 
    value_serializer=lambda x: dumps(x).encode('utf-8'))

################################
#       API REQUEST            #
################################

for e in range(1000): #here we can set the time

    # REQUEST
    results = sp.current_playback()
    print(results)
    try:
        artists = []
        for a in results['item']['artists']:
            artists.append(a['name'])
        data = {
            'status': 'OK',
            'progress_ms': results['progress_ms'],
            'currently_playing_type': results['currently_playing_type'],
            'name': results['item']['name'],
            'artists': artists,
            'id': results['item']['id'],
            'is_playing': results['is_playing']
        }
    except TypeError:
        data = {
            'status': 'NOT PLAYING'
        }
    producer.send('lyricgen', data)
    producer.flush()
    sleep(PERIOD)
