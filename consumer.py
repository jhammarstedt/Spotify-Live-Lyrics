from kafka import KafkaConsumer
from json import loads
import json
from logging import log

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
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id=None
    )

for message in consumer:
    #here we run our stuff
    message = message.value
    print(message)
    #print("TEST",message["progress_ms"])
    name = message["name"]
    timestamp = message["progress_ms"]
    #add artist