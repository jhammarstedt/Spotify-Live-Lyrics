import json


def time2ms(time):
    """Converting the time to milliseconds

    Args:
        time

    Returns:
        time in milliseconds
    """
    time = time.split(':')
    minutes = float(time[0])
    seconds = float(time[1])

    ms = int((minutes * 60 + seconds) * 1000)

    return ms


# )title:str="Empty",lyrics:str="Empty",id:str="Empty",):
def write_to_file(found: bool = True, reset=False, **kwargs):
    """Writes from the consumer to the file which will be read by the server and displayed on the website

    Args:
        found (bool, optional): If the lyrics was found or not. Defaults to True.
        reset (bool, optional): If the app is restared we set default values for loading screen. Defaults to False.
        **kwargs: The arguments which will be written to the file
            Can be:
                * lyrics
                * title
                * id
    """
    info = {}
    with open('lyrics.json', 'r') as f:
        info = json.load(f)

    if reset:  # at the start we want to reset the file
        info["data"]["title"] = "By Johan Hammarstedt & Javier Garcia San Vicente "
        info["data"]["lyrics"] = "The Spotify Kareoke Special \n\n Play a song to start!"
        info["data"]["id"] = "Empty"
    else:
        if "title" in kwargs:
            info["data"]["title"] = kwargs["title"]
            info["data"]["lyrics"] = "Loading..."

        else:
            if not found:
                info["data"]["lyrics"] = "Not Found"
            else:
                info["data"]["lyrics"] = kwargs["lyrics"]

            info["data"]["id"] = kwargs["id"]

    with open('lyrics.json', "w") as myfile:
        json.dump(info, myfile)


def search_line_dict(timestamp, lyrics_list, fitting_offset=0, anticipation=1):
    """Search for the line in the lyrics_list

    Args:
        timestamp ([type]): [description]
        lyrics_list ([type]): [description]
        fitting_offset (int, optional): If controls are used to change the offset. Defaults to 0.
        anticipation (int, optional): [description]. Defaults to 1.

    Returns:
        Timestamp that matches the lyrics
    """
    lyrics_dic = {}
    for k, v in lyrics_list:
        lyrics_dic[k] = v

    keys = list(lyrics_dic.keys())

    fitting_offset *= 1000
    anticipation *= 1000

    filtered_time = list(filter(lambda time: time2ms(time) + fitting_offset >
                         timestamp and time2ms(time) + fitting_offset - anticipation < timestamp, keys))

    if not filtered_time:
        return ''

    current_time = filtered_time[0]
    # print("TIME",current_time)
    return lyrics_dic[current_time]


def search_line_df(timestamp, lyrics_df, fitting_offset=0, anticipation=6, delay=-1):
    """[summary]

    Args:
        timestamp ([type]): [description]
        lyrics_df ([type]): [description]
        fitting_offset (int, optional): [description]. Defaults to 0.
        anticipation (int, optional): [description]. Defaults to 6.
        delay (int, optional): [description]. Defaults to -1.

    Returns:
        [type]: [description]
    """
    # Convert to ms
    fitting_offset *= 1000
    anticipation *= 1000
    delay *= 1000

    lower_bound = timestamp - fitting_offset - delay
    upper_bound = timestamp - fitting_offset - delay + anticipation

    lyrics_df = lyrics_df.filter(lyrics_df['Timestamp'] > lower_bound)

    lyrics_df = lyrics_df.filter(lyrics_df['Timestamp'] < upper_bound)

    if lyrics_df.rdd.isEmpty():
        return ''

    return lyrics_df.collect()[0][1]


def lyrics2DataFrame(lyrics, spark):
    """
    Convert lyrics to dataframe, not used since spark was not implemented in the final version
    """
    columns = ['Timestamp', 'Line']

    rdd = spark.sparkContext.parallelize(lyrics.items())

    rdd_ms = rdd.map(lambda x: (time2ms(x[0]), x[1]))

    dataframe = spark.createDataFrame(rdd_ms, columns)

    dataframe = dataframe.filter(~dataframe['Line'].contains('RentAnAdviser'))

    return dataframe


def reset_offset():
    """Resets offset to 0 given new songs"""
    
    with open('config.json', 'w') as f:
        json.dump({"offset": 0.0}, f)  # reseting the offset
