from kafka import KafkaConsumer
#from pyspark.sql import *
from json import loads
import json
from logging import log
from scraper import get_song, query_song
from utils import *
#from pyspark.sql import SparkSession
#from pyspark.sql.types import *
import time
import asyncio

#spark = SparkSession.builder.appName("lyric_gen").getOrCreate()

def forgiving_json_deserializer(v):
    # Now we can access it as json instead!
    try:
        return json.loads(v.decode('utf-8'))
    except json.decoder.JSONDecodeError:
        log.exception('Unable to decode: %s', v)
        return None

def write_to_file(found:bool,lyrics:str="Empty",id:str="Empty",):
    with open('lyrics.txt','r+') as myfile:
        lines = myfile.readlines()
        if not found:
            lines[1] = 'No lyrics found'
        else:
            lines[1] = lyrics
        
        lines[2] = id

        myfile.writelines(lines)
        myfile.close()


consumer = KafkaConsumer(
    'lyricgen',
    value_deserializer= forgiving_json_deserializer,
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest', #Ska denna va latest?
    enable_auto_commit=False, # Stämmer detta?
    group_id=None
    )

previous_line = ''
previous_artist = ''
previous_song = ''
for message in consumer:
    #start_time = time.time()
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
    song_id = message['id']

    if not (artist == previous_artist and song == previous_song):
        print('New song: ' + song + ' by ' + artist)
        #with open('lyrics.txt','w') as myfile:
        #    myfile.write('New song: ' + song + ' by ' + artist)
        lyrics_list = get_song(artist, song)
        
        previous_artist = artist
        previous_song = song
        # try:
            
        # except AttributeError:
        #     print('in here')
        #     lyrics_list = query_song(artist, song)
        #     pass
        #lyrics_df = lyrics2DataFrame(lyrics_dic, spark)
    if lyrics_list is None:
            print('No lyrics found')
            write_to_file(lyrics=song,id=song_id, found = False)
            continue
    #line = search_line_df(timestamp, lyrics_df, fitting_offset=fitting_offset)
    line = search_line_dict(timestamp, lyrics_list)
    #print(line) #here we print the actual line for now
    
    if not line == previous_line: #if the line is the same as the previous line, we don't want to print it
        print(line)
        if line is not "":
            write_to_file(lyrics=line,id=song_id, found = True)
            # with open('lyrics.txt','w') as myfile:
            #     myfile.write(line)

        previous_line = line #update previous line
