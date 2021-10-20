from kafka import KafkaConsumer
from json import loads
import json
from logging import log
from scraper import get_song

def time2ms(time):
    
    time = time.split(':')
    minutes = float(time[0])
    seconds = float(time[1])

    ms = (minutes * 60 + seconds) * 1000

    return ms

def search_line(timestamp, lyrics_dic):

    keys = list(lyrics_dic.keys())

    current_time = list(filter(lambda time: time2ms(time) > timestamp, keys))[0]

    return lyrics_dic[current_time]    

def forgiving_json_deserializer(v):
    # Now we can access it as json instead!
    try:
        return json.loads(v.decode('utf-8'))
    except json.decoder.JSONDecodeError:
        log.exception('Unable to decode: %s', v)
        return None

consumer = KafkaConsumer(
    'lyricgen',
    value_deserializer= forgiving_json_deserializer,
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id=None
    )

previous_line = ''
previous_artist = ''
previous_song = ''
for message in consumer:

    message = message.value
    #print(message)
    #print(message)
    song = message['name']
    artist = message['artists'][0]
    timestamp = message['progress_ms']

    #print(song, artist, timestamp)

    if not (artist == previous_artist and song == previous_song):
        lyrics_dic = get_song(artist, song)

    line = search_line(timestamp, lyrics_dic)
    if not line == previous_line:
        print(line)
        previous_line = line

    #add artist