from typing import Tuple
import requests
from bs4 import BeautifulSoup
import asyncio
import time

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
    title = lyrics[0].split("]")[0] #get the title of the song
    print(f"Now playing: {title.replace('(.LRC)','').upper()}")
    lyrics = {s[0]:s[1] for s in [l.split("]") for l in lyrics[1:]]}
    lyrics = lyrics.items() #return it as a touple [(timestamp, lyric)]
    return lyrics

def get_song(artist, song)-> list():
    """Function to get the lyrics from the results page given artist and song"""
    #return query_song(artist, song) #request worked but we song not found
    
    results_url = f"https://www.rentanadviser.com/subtitles/getsubtitle.aspx?artist={artist}&song={song}"
    
    r = requests.get(results_url)
    soup = BeautifulSoup(r.text, "html.parser")
    
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
    
    #! still a bug where it dont find all songs
    
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
        title = cols[0].a.find(text=True).lower()
        link = f"https://www.rentanadviser.com/subtitles/{link}"
        s = song.replace("%20"," ").lower() #remove the %20 from the song to match the title
        a = artist.replace("%20"," ").lower() #remove the %20 from the artist to match the title
        print(f"comparing {s} {a} with {title}")
        if (a in title) and (s in title): #if the artist and song are in the title
            if ("official" in link.lower()): #only want the official version 
                #print("OFFICIAL WAS FOUND") #print it
                return parse_lyrics(BeautifulSoup(requests.get(link).text, "html.parser"))
            else:
                output.append(link) #if we dont find an official we just append it
        else:
            continue
    # if we didnt find any  official we just return the first link through parse_lyrics
    if len(output) == 0:
        print("SONG NOT FOUND IN QUERY") #
        return None 
    else:
        print("OFFICIAL not found,", output[0])
        
        return parse_lyrics(BeautifulSoup(requests.get(output[0]).text, "html.parser")) 

def main():
    start = time.time()
    #testing, we run the function through the consumer instead
    artist = ["busta rhymes"] #example artist
    song = "look over your shoulder" #example song
    artist, song = parse_song(artist, song)
    lyrics = get_song(artist, song)
    #print(lyrics)
    print(f"Time taken: {time.time() - start}")

if __name__ == "__main__":
    main()

    """
    export PYSPARK_PYTHON=python3                                                                                           export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.7-src.zip:$PYTHONPATH                             export PATH=$SPARK_HOME/bin:$SPARK_HOME/python:$PATH
    export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.7-src.zip:$PYTHONPATH                             export PATH=$SPARK_HOME/bin:$SPARK_HOME/python:$PATH
    export PATH=$SPARK_HOME/bin:$SPARK_HOME/python:$PATH
    """