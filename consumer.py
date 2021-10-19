from kafka import KafkaConsumer
from json import loads

consumer = KafkaConsumer(
    'lyricgen',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id=None
    )

for message in consumer:
    message = message.value
    print(message)