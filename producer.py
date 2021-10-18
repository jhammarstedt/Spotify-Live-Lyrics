
from kafka import KafkaProducer
from time import sleep
import json
from json import dumps

import spotipy
from spotipy.oauth2 import SpotifyOAuth

################################
#       CONSTANTS              #
################################

PERIOD = 1

################################
#       AUTHENTIFICATION       #
################################

scope = "user-read-playback-state"

# THOSE CAN BE SET AS ENV VARIABLES IN LINUX
CLIENT_ID = '3be5443f43b14ef587f68864ed10b641'
CLIENT_SECRET = 'a3e2129ee3b8423e98bce7847c4c3a9a'
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

for e in range(10):

    # REQUEST
    results = sp.current_playback()

    relevant = {
        'progress_ms': results['progress_ms'],
        'currently_playing_type': results['currently_playing_type'],
        'name': results['item']['name'],
        'id': results['item']['id']
    }

    producer.send('numtest', relevant)
    producer.flush()
    sleep(PERIOD)
