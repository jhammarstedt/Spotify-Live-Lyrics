<img src=https://www.freepnglogos.com/uploads/spotify-logo-png/spotify-download-logo-30.png align="right" width="100"> 

# Spotioke 
As Spotify only enables live lyrics in the U.S many of us Europeans missed out on a lot of fun kareoke sessions... Fear not, Spotioke is the Spotify Kareoke mashup you need! 

## Authors
* Johan Hammarstedt  [<img src =https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png width ="20">](https://github.com/jhammarstedt) 
* Javier García San Vicente  [<img src =https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png width ="20">](https://github.com/https://github.com/Javigsv) 

## Setup
Since our app is still in developer mode, you'll need to create your own app to run it. 


If you already have kafka and zookeeper installed you can skip the first 6 steps, just create the topic lyricgen. If not follow the steps below:


Download and install kafka and zookeeper:
### Installing Kafka

We use Kafka as our data source, which is a distributed, partitioned, replicated commit log service. This
section presents the steps you need to do to install Kafka on a Linux machine.
<details> 
  <summary>Kafka & Zookeeper Setup</summary>
 1. Download Kafka 2.0.0: https://archive.apache.org/dist/kafka/2.0.0/kafka 2.11-2.0.0.tgz
2. Set the following environment variables.
    * `$export KAFKA_HOME="/path/to/the/kafka/folder"` 
    * `$export PATH=$KAFKA_HOME/bin:$PATH`

3. Kafka uses ZooKeeper to maintain the configuration information, so you need to first start a ZooKeeper
server if you do not already have one.

    `$KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties`

4. Start the Kafka server.

`$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties`

5. Then, create a topic. A topic is a category or feed name to which messages are published. Add the following line to create the topic 'lyricgen' which will be used for communication between producer and consumer.

    `$KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1
--topic lyricgen`

6. To see the list of topics you can run the following command.

    `$KAFKA_HOME/bin/kafka-topics.sh --list --zookeeper localhost:2181`
</details>

7. Run the producer
    `python3 producer.py`

8. On the first run you need to give the app authentication to use your account, 

9. In a new window start the consumer: 
    `python3 consumer.py`

10. In another new window start the flask server, then open a browser and type "localhost" and the app should be displayed:
    `python3 server.py`


## Video demo


## Disclaimer


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

    


## Approach
### Scraping
Try to get the regular name and artist and make a call to rentadviser

### UI
https://codepen.io/rachsmith/pen/oGEMbz
