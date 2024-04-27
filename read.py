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

