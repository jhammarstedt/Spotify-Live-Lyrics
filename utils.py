import json

def time2ms(time):
    
    time = time.split(':')
    minutes = float(time[0])
    seconds = float(time[1])

    ms = int((minutes * 60 + seconds) * 1000)

    return ms

def write_to_file(found:bool=True,reset=False,**kwargs): #)title:str="Empty",lyrics:str="Empty",id:str="Empty",):
    info = {}
    with open('lyrics.json', 'r') as f:
        info = json.load(f)


    if reset: #at the start we want to reset the file
        info["data"]["title"] =  "By Johan Hammarstedt & Javier Garcia San Vicente "
        info["data"]["lyrics"] =  "The Spotify Kareoke Special \n\n Play a song to start!"
        info["data"]["id"] =  "Empty"
    else:
        if "title" in kwargs:
            info["data"]["title"] =  kwargs["title"]
            info["data"]["lyrics"] =  "Loading..."

        else:
            if not found:
                info["data"]["lyrics"] = "Not Found"
            else:
                info["data"]["lyrics"] = kwargs["lyrics"]

            info["data"]["id"] = kwargs["id"]

    with open('lyrics.json',"w") as myfile:  
        json.dump(info, myfile)
   

def search_line_dict(timestamp, lyrics_list, fitting_offset=0, anticipation=1):

    lyrics_dic = {}
    for k,v in lyrics_list:
        lyrics_dic[k] = v

    keys = list(lyrics_dic.keys())

    fitting_offset *= 1000
    anticipation *= 1000

    filtered_time = list(filter(lambda time: time2ms(time) + fitting_offset > timestamp and time2ms(time) + fitting_offset - anticipation < timestamp, keys))


    if not filtered_time:
        return ''

    current_time = filtered_time[0]
    #print("TIME",current_time)
    return lyrics_dic[current_time]    


def search_line_df(timestamp, lyrics_df, fitting_offset=0, anticipation=6, delay = -1):

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

    columns = ['Timestamp', 'Line']

    rdd = spark.sparkContext.parallelize(lyrics.items())

    rdd_ms = rdd.map(lambda x: (time2ms(x[0]), x[1]))

    dataframe = spark.createDataFrame(rdd_ms, columns)

    dataframe = dataframe.filter(~dataframe['Line'].contains('RentAnAdviser'))

    return dataframe
