import requests
from bs4 import BeautifulSoup


def parse_song(artist, song):
    a_list = []
    for i in artist:
        a = "%20".join(i.lower().split(" "))
        a_list.append(a)
    
    s = "%20".join(song.lower().split(" "))

    return a_list[0], s
    
def get_song(artist, song):
    #Function to get the lyrics from the results page given artist and song
    results_url = f"https://www.rentanadviser.com/subtitles/getsubtitle.aspx?artist={artist}&song={song}"
    #print(results_url)
    
    r = requests.get(results_url)
    try:
        soup = BeautifulSoup(r.text, "html.parser")
    except:
        #! Not done yet
        print("No results found")
        lyrics = query_song(artist, song)
        return None
    else:
        #print(soup.prettify())
        lyrics = soup.find(id="ctl00_ContentPlaceHolder1_lbllyrics_simple").text
        
        #process it a little
        lyrics = lyrics.split("[")
        lyrics = {s[0]:s[1] for s in [l.split("]") for l in lyrics[1:]]}
        return lyrics

def query_song(artist, song):
    #Function to query the website for the results page given artist and song when we cant find it right away
    #! in progress
    search = f"{artist}%20{song}"
    query_url = f"https://www.rentanadviser.com/subtitles/subtitles4songs.aspx?q={search}"
    r = requests.get(query_url)
    soup = BeautifulSoup(r.text, "html.parser")

    lyrics = soup.find(id="tablecontainer")
    print(lyrics)
    return lyrics

def main():
    artist = ["beyonce"] #example artist
    song = "formation" #example song
    artist, song = parse_song(artist, song)
    lyrics = get_song(artist, song)
    print(lyrics)


if __name__ == "__main__":
    main()