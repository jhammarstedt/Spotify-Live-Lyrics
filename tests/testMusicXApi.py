import requests

API_KEY = '17c71e9f8e5cae220b9373bdfca550e2'


#q_artist=justin%20bieber&page_size=3&page=1&s_track_rating=desc&apikey=17c71e9f8e5cae220b9373bdfca550e2

SEARCH_URL = 'https://api.musixmatch.com/ws/1.1/track.search'

# POST
response = requests.get(SEARCH_URL, {
    'q_track': 'What would I change it to (feat. Aluna)',
    "page_size": '1',
    'page': '1',
    'apikey': API_KEY
})
# save the access token
print(response.content)

data = response.json()

print(data['message']['body']['track_list'][0]['track'].keys())

track_id = data['message']['body']['track_list'][0]['track']['track_id']
has_subtitles = data['message']['body']['track_list'][0]['track']['has_subtitles']
has_lyrics = data['message']['body']['track_list'][0]['track']['has_lyrics']

print(track_id, has_subtitles, has_lyrics)


SUBTITLES_URL = 'https://api.musixmatch.com/ws/1.1/track.subtitle.get'

# POST
response = requests.get(SUBTITLES_URL, {
    'commontrack_id': str(track_id),
    'apikey': API_KEY
})

data = response.json()

print(data)