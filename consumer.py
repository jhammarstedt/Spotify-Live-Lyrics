from kafka import KafkaConsumer
from pyspark.sql import *
from json import loads
import json
from logging import log
from scraper import get_song
from utils import *
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import time

spark = SparkSession.builder.appName("lyric_gen").getOrCreate()

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
    start_time = time.time()
    '''
    with open('config.json', 'r') as f:
        config  = json.load(f)
    f.close()
    fitting_offset = config['offset']
    '''

    message = message.value

    if message['status'] == 'NOT PLAYING':
        print('No song being played')
        continue

    song = message['name']
    artist = message['artists'][0]
    timestamp = message['progress_ms']

    if not (artist == previous_artist and song == previous_song):
        lyrics_dic = get_song(artist, song)
        #lyrics_df = lyrics2DataFrame(lyrics_dic, spark)

    #line = search_line_df(timestamp, lyrics_df, fitting_offset=fitting_offset)
    line = search_line_dict(timestamp, lyrics_dic)
    if not line == previous_line:
        print(line)
        previous_line = line

    end_time = time.time()

    print(end_time - start_time)

    #add artist