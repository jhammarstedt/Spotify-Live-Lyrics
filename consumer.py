from kafka import KafkaConsumer
#from pyspark.sql import *
from json import loads
import json
from logging import log
from scraper import get_song, query_song
from utils import *

"""
from pyspark.sql import SparkSession
from pyspark.sql.types import *
spark = SparkSession.builder.appName("lyric_gen").getOrCreate()
"""


def forgiving_json_deserializer(v):
    """Make kafka process json data

    Args:
        v  :data from kafka

    Returns:
        json object readable by kafka
    """
    try:
        return json.loads(v.decode('utf-8'))
    except json.decoder.JSONDecodeError:
        log.exception('Unable to decode: %s', v)
        return None


write_to_file(reset=True)

# Set our consumer
consumer = KafkaConsumer(
    'lyricgen',
    value_deserializer=forgiving_json_deserializer,
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',   
    enable_auto_commit=False,  # Stämmer detta?
    group_id=None
)

# When changing song we need to check if we have a new song and reset offset
previous_line = ''
previous_artist = ''
previous_song = ''
for message in consumer:
    with open('config.json', 'r') as f:
        config = json.load(f)
    f.close()
    fitting_offset = config['offset']

    message = message.value

    if message['status'] == 'NOT PLAYING':
        print('No song being played')
        continue

    song = message['name']
    artist = message['artists'][0]
    timestamp = message['progress_ms']
    song_id = message['id']

    if not (artist == previous_artist and song == previous_song):

        print('New song: ' + song + ' by ' + artist)
        reset_offset()
        print('Reset offset')
        lyrics_list = get_song(artist, song)

        previous_artist = artist
        previous_song = song
        """
        Spark things we removed: 
        # try:
            
        # except AttributeError:
        #     print('in here')
        #     lyrics_list = query_song(artist, song)
        #     pass
        #lyrics_df = lyrics2DataFrame(lyrics_dic, spark)
        """
    if lyrics_list is None:
        print('No lyrics found')
        write_to_file(lyrics=song, id=song_id, found=False)
        continue
    #line = search_line_df(timestamp, lyrics_df, fitting_offset=fitting_offset)
    line = search_line_dict(timestamp, lyrics_list,
                            fitting_offset=fitting_offset)

    if not line == previous_line:  # if the line is the same as the previous line, we don't want to print it
        print(line)
        if line is not "":
            write_to_file(lyrics=line, id=song_id, found=True)

        previous_line = line  # update previous line
