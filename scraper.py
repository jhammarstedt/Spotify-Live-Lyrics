import requests
from bs4 import BeautifulSoup
import time
import re
from utils import write_to_file


def parse_song(artist, song):
    """
    Function that parses the song for it to be used in the get_song function

    Args:
        artist: the artist of the song
        song: the song name
    """
    a_list = []
    for i in artist:
        a = "%20".join(i.lower().split(" "))
        a_list.append(a)

    s = "%20".join(song.lower().split(" "))

    return a_list[0], s


def parse_lyrics(soup_object):
    """
    Function to find the lyrics from the soup object and clean it
    Args:
        soup_object: the soup object of the results page
    """
    lyrics = soup_object.find(
        id="ctl00_ContentPlaceHolder1_lbllyrics_simple").text

    # process it a little
    # clean up the lyrics from format [time] lyrics [time] lyrics
    lyrics = lyrics.split("[")
    title = lyrics[0].split("]")[0]  # get the title of the song
    title = title.replace("(.LRC)", "")
    write_to_file(title=title)  # write title

    print(f"Now playing: {title.upper()}")
    lyrics = {s[0]: s[1] for s in [l.split("]") for l in lyrics[1:]]}
    lyrics = lyrics.items()  # return it as a touple [(timestamp, lyric)]
    return lyrics


def get_song(artist, song, query_only=True) -> list():
    """
    Function to get the lyrics from the website given the artist and song

    Makes a query to the website and returns then tries to find the best matching lyrics


    Args:
        artist: the artist of the song
        song: the song name
        query_only: if we only want to query the website instead of trying to find the lyrics right away, more stable results
    """
    if query_only:

        return query_song(artist, song)
    else:
        # if we dont want to query the website we just try to find the lyrics right away, faster but less accurate
        results_url = f"https://www.rentanadviser.com/subtitles/getsubtitle.aspx?artist={artist}&song={song}"

        r = requests.get(results_url)
        soup = BeautifulSoup(r.text, "html.parser")

        if r.status_code == 404:
            return None  # request failed
        elif "error" in soup.b.text.lower():
            # request worked but we song not found
            return query_song(artist, song)
        else:
            return parse_lyrics(soup)  # song found


def query_song(artist, song):
    """
    Function to query the website for the results page given 
    artist and song when we cant find it right away

    Args:
        artist: the artist of the song
        song: the song name



    """

    search = f"{artist}%20{song}"  # the search query
    # the query url
    query_url = f"https://www.rentanadviser.com/subtitles/subtitles4songs.aspx?q={search}"
    r = requests.get(query_url)

    if r.status_code == 404:
        return None  # request failed

    soup = BeautifulSoup(r.text, "html.parser")

    """Rentadviser keeps all queries in a table which we can access with the below code"""
    table = soup.find("table")
    rows = table.find_all('tr')
    output = []
    for row in rows:
        cols = row.find_all('td')
        cols = [x for x in cols]
        link = cols[0].a['href']
        title = cols[0].a.find(text=True).lower()
        link = f"https://www.rentanadviser.com/subtitles/{link}"
        # remove the %20 from the song to match the title
        s = song.replace("%20", " ").lower()
        # remove the %20 from the artist to match the title
        a = artist.replace("%20", " ").lower()

        """
        
        Note: Query logic is not perfect, sometimes it will return the wrong song but works in many cases
            Any suggestions are welcome
            
        """
        if (a in title):  # if the artist are in the title
            find = "\s+(\(?fe?a?t.*\)?)"  # regex to drop all the ft feat etc
            title_clean = re.sub(find, "", title)  # remove the ft feat etc
            s_clean = re.sub(find, "", s)  # remove the ft feat etc
            # if the song is in the title or the link description (trying to avoid the above mentioned error)
            if (s_clean in title_clean or s in link):
                if ("audio" in title):  # only want the official version
                    return parse_lyrics(BeautifulSoup(requests.get(link).text, "html.parser"))
                elif ("official" in title):  # only want the official version

                    return parse_lyrics(BeautifulSoup(requests.get(link).text, "html.parser"))
                else:
                    # if we dont find an official we just append it
                    output.append(link)
        else:
            continue
    # if we didnt find any  official we just return the first link through parse_lyrics
    if len(output) == 0:
        print("SONG NOT FOUND IN QUERY")
        return None
    else:
        print("OFFICIAL not found,", output[0])

        return parse_lyrics(BeautifulSoup(requests.get(output[0]).text, "html.parser"))

    """
    Main not used, simply for testing
    def main():
    start = time.time()
    
    # testing, we run the function through the consumer instead
    artist = ["Justin bieber"]  # example artist
    song = "baby"  # example song
    artist, song = parse_song(artist, song)
    lyrics = get_song(artist, song)
    # print(lyrics)
    print(f"Time taken: {time.time() - start}")


if __name__ == "__main__":
    main()
    """
