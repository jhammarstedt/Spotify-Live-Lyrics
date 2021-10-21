from typing import Tuple
import requests
from bs4 import BeautifulSoup
import asyncio


def parse_song(artist, song):
    a_list = []
    for i in artist:
        a = "%20".join(i.lower().split(" "))
        a_list.append(a)
    
    s = "%20".join(song.lower().split(" "))

    return a_list[0], s

def parse_lyrics(soup_object):
    """Function to find the lyrics from the soup object and clean it"""
    lyrics = soup_object.find(id="ctl00_ContentPlaceHolder1_lbllyrics_simple").text
    
    #process it a little
    lyrics = lyrics.split("[") #clean up the lyrics from format [time] lyrics [time] lyrics
    lyrics = {s[0]:s[1] for s in [l.split("]") for l in lyrics[1:]]}
    lyrics = lyrics.items() #return it as a touple [(timestamp, lyric)]
    return lyrics

def get_song(artist, song)-> list():
    """Function to get the lyrics from the results page given artist and song"""
    results_url = f"https://www.rentanadviser.com/subtitles/getsubtitle.aspx?artist={artist}&song={song}"
    
    r = requests.get(results_url)
    soup = BeautifulSoup(r.text, "html.parser")
    #! just need to catch when this dont work
    if r.status_code == 404:
        return None #request failed
    elif "error" in soup.b.text.lower(): 
        return query_song(artist, song) #request worked but we song not found
    else:
        return parse_lyrics(soup) #song found
    

        

def query_song(artist, song):
    """
    Function to query the website for the results page given 
    artist and song when we cant find it right away
    """
    search = f"{artist}%20{song}"
    query_url = f"https://www.rentanadviser.com/subtitles/subtitles4songs.aspx?q={search}"
    r = requests.get(query_url)
    soup = BeautifulSoup(r.text, "html.parser")

    table = soup.find("table")
    rows = table.find_all('tr')
    output = []
    for row in rows:
        cols=row.find_all('td')
        cols=[x for x in cols]
        link = cols[0].a['href']
        link = f"https://www.rentanadviser.com/subtitles/{link}"
        if "official" in link.lower(): #only want the official version 
            return parse_lyrics(BeautifulSoup(requests.get(link).text, "html.parser"))
        else:
            output.append(link) #if we dont find an official we just append it
    
    # if we didnt find any  official we just return the first link through parse_lyrics

    return parse_lyrics(BeautifulSoup(requests.get(link).text, "html.parser"))

def main():
    #testing, we run the function through the consumer instead
    artist = ["ed sheeran"] #example artist
    song = "shape of you" #example song
    artist, song = parse_song(artist, song)
    lyrics = get_song(artist, song)
    print(lyrics)


if __name__ == "__main__":
    main()

    """
    export PYSPARK_PYTHON=python3                                                                                           export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.7-src.zip:$PYTHONPATH                             export PATH=$SPARK_HOME/bin:$SPARK_HOME/python:$PATH
    export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.7-src.zip:$PYTHONPATH                             export PATH=$SPARK_HOME/bin:$SPARK_HOME/python:$PATH
    export PATH=$SPARK_HOME/bin:$SPARK_HOME/python:$PATH
    """