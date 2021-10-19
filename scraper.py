import requests
from bs4 import BeautifulSoup

query_url = "https://www.rentanadviser.com/subtitles/subtitles4songs.aspx?"
results_url = "https://www.rentanadviser.com/subtitles/getsubtitle.aspx?artist=Justin%20Bieber&song=Baby%20ft.%20Ludacris"

artist = ["Kanye West"]
song = "Good Morning"

def parse_timestamps(lyrics):
    #function that takes lyrics of a song as a string with format [ss:ms:ms]Text[ss:ms:ms]Text[ss:ms:ms]Text, and returns a list of [time, text]
    lyrics = [lyrics.split("]") for i in lyrics]
    #lyrics = 
    

def parse_song(artist, song):
    a_list = []
    for i in artist:
        a = "%20".join(i.lower().split(" "))
        a_list.append(a)
    
    s = "%20".join(song.lower().split(" "))

    return a_list[0], s
    
def get_song(artist, song):
    #Function to get the lyrics from the results page
    results_url = f"https://www.rentanadviser.com/subtitles/getsubtitle.aspx?artist={artist}&song={song}"
    print(results_url)
    r = requests.get(results_url)
    soup = BeautifulSoup(r.text, "html.parser")

    #print(soup.prettify())
    lyrics = soup.find(id="ctl00_ContentPlaceHolder1_lbllyrics_simple").text
    
    
    print(lyrics)
    
    
    pass

def query_song(artist, song):
    pass
page = requests.get(results_url)

soup = BeautifulSoup(page.content, 'html.parser')

a,s = parse_song(artist, song)
get_song(a,s)