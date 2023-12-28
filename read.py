import os
import json

from files import readJson, writeJson


def get1(): #Getting history from Downloaded Data
    accountData = os.listdir("Spotify Account Data")

    StreamingHistories = [data for data in accountData if "StreamingHistory" in data]
    StreamingHistory = []


    for i in range(len(StreamingHistories)):    
        with open(f'Spotify Account Data/{StreamingHistories[i]}','r') as history:
            data = history.read()
            json_data = json.loads(data)
            StreamingHistory += json_data
    return StreamingHistory

def get2(): #Getting history from history.json
    json_data = readJson('data/history.json')
    StreamingHistory = []
    for data in json_data:
        x = data['artistName']
        if type(x) == str:
            x = (x,)
        elif type(x) == list:

            x = tuple(x)
        newData = {
            'endTime':data['endTime'],
            'artistName':x,
            'trackName': data['trackName'],
            'msPlayed':data['msPlayed'],
            'duration_ms':data['duration_ms'],
                    }
        
        StreamingHistory.append(newData)
        
    return StreamingHistory

def fix():
    print("about to start fixing incomplete artists")
    json_data = readJson('data/history.json')
    dataWithMultipleArtists = [data for data in json_data if len(data['artistName']) > 1] #All entries in history.json where there are multiple artists
    artistsInMultipleArtists = [data['artistName'] for data in json_data if len(data['artistName']) > 1] #All Artists in dataWithMultipleArtists
    artistsInMultipleArtists2 = [] #The previous list would be [['artist1','artist2'],['artist1','artist3']], while this one is ['artist1', 'artist2','artist3']
    for artists in artistsInMultipleArtists:
        for artist in artists:
            if artist not in artistsInMultipleArtists2:
                artistsInMultipleArtists2.append(artist)
    print(artistsInMultipleArtists2)
    for data in json_data:
        artists = data['artistName']
        if len(artists) == 1 and artists[0] in artistsInMultipleArtists2:
            artist = artists[0]
            for otherData in dataWithMultipleArtists:
                if otherData['trackName'] == data['trackName']:
                    if artist in otherData['artistName']:
                        data['artistName'] = otherData['artistName']
                        print("fixed: ", artist,data['trackName'],otherData['artistName'],json_data.index(data))
    
    writeJson('data/history.json',json_data)
    print("finished fixing incomplete artists")