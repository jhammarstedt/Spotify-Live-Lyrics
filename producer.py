
from kafka import KafkaProducer
from json import dumps
from time import sleep
import requests

CLIENT_ID = '3be5443f43b14ef587f68864ed10b641'
CLIENT_SECRET = 'a3e2129ee3b8423e98bce7847c4c3a9a'

AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})
# convert the response to JSON
auth_response_data = auth_response.json()
# save the access token
access_token = auth_response_data['access_token']

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}
data = {
    "grant_type": "client_credentials",
    "scope": "user-read-playback-state",
}
response = requests.get('https://api.spotify.com/v1/me/player', headers=headers, data=data)
data = response.content
print(data)

exit()

# Producer part
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], 
    value_serializer=lambda x: dumps(x).encode('utf-8'))

for e in range(10):
    response = requests.get('https://api.spotify.com/v1/markets', headers=headers)
    data = response.json()
    print(data)
    producer.send('numtest', data)
    producer.flush()
    sleep(5)