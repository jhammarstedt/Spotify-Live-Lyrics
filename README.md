<img src=https://www.freepnglogos.com/uploads/spotify-logo-png/spotify-download-logo-30.png align="right" width="100"> 

# Spotify Lyric Generator 
As Spotify only enables live lyrics in the U.S many of us Europeans missed out on a lot of fun karaoke sessions...

Fear not! Fork our repo, connect with your Spotify Account and enjoy real-time lyrics!

## Authors
* Johan Hammarstedt  [<img src =https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png width ="20">](https://github.com/jhammarstedt) 
* Javier García San Vicente  [<img src =https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png width ="20">](https://github.com/https://github.com/Javigsv) 

## Video demo
https://user-images.githubusercontent.com/52280124/138563736-45d96aed-c62b-4b53-b36e-5004d7093ee6.mp4

## Setup
First fork this repository: `$git clone https://github.com/jhammarstedt/Spotify-Lyric-Generator.git`

Install the requirements

`pip install -r requirements.txt`

### Spotify Developer Account
Since our app is still in developer mode, you'll need to have a premium account and create your own app to run it, but fortunately, this is very easy:
1. Go [here](https://developer.spotify.com/dashboard/)
2. Login, accept the conditions to Spotify developers
3. Create an app
4. Get your credentials (Client ID and Client Secret)
5. In the project repo, create a .env file with the following and save:
  ```
  CLIENT_ID = PASTE YOUR ID 
  CLIENT_SECRET = PASTE YOUR SECRET
  ```
 
### Setting up kafka and zookeper
We use Kafka as our data source, which is a distributed, partitioned, replicated commit log service. This
the section presents the steps you need to do to install Kafka on a Linux machine.

If you already have Kafka and zookeeper installed you can skip the first 6 steps, just create the topic lyricgen. If not follow the steps below:
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

10. In another new window start the flask server, then open a browser and type "localhost" and the app should be displayed ("sudo" permits may be needed to init the server):
    
    `python3 server.py`

## Control the occasional Offset
Some songs do not have matching timestamps with the actually played song from Spotify. Therefore, while you run everything, open a new console and run the controls.py:

`python3 controls.py`

Then use the keyboard to control the offset:
* `I` will increase the offset, making the lyrics come later
* `D` will decrease the offset, making the lyrics come earlier 


## Disclaimer
This project is not done in association with Spotify and was made for private use in a school project. Note that not all lyrics will work, as our logic for getting the lyrics is not perfect, some songs are not found. Occasionally the timestamps are not matching with the lyrics due to the wrong version.

Right now the project runs on localhost as the app is not official, so you have to set everything up yourself.

## Credits
* Lyrics from [Rentadviser](https://www.rentanadviser.com/subtitles/subtitles4songs.aspx)

