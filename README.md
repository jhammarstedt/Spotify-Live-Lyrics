# Spotify-lyric-Generator

## MVP/POC
1. Explore the spotify API - how to make calls (ADD LINK)
2. Explore the Kafka rest framework : How do we make API calls using kafka [LINK](https://www.instaclustr.com/making-api-requests-with-the-kafka-rest-proxy/)
3. Connect the framework to Spotify - Make spotify calls - General and private calls (non user based or private that requires access)
4. Output the timestamp from kafka
5. Input to python script that has the lyric API
6. call the lyric script and get the lyric given the timestamp 

When done:
1. Add database to store the lyrics and timestamps
2. Make a UI that displays the stuff
3. Try to make the cool translations on songs using gtranslate or similar

    

## setup
Start zookeeper: 

`$KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties`


Start kafka server
`$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties`

Create our topic
$KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1
--topic lyricgen

Then run the producer
`python3 producer.py`

and the consumer 

`python3 consumer.py`

## Approach
### Scraping
Try to get the regular name and artist and make a call to rentadviser
