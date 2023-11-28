import os
import json


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
    with open('history.json','r') as history:
        json_data = json.loads(history.read())
        StreamingHistory = []
        for data in json_data:
            newData = {
                'endTime':data['endTime'],
                'artistName':data['artistName'],
                'trackName': data['trackName']
                       }
            if data['msPlayed'] == None:
                newData['msPlayed'] == data['duration_ms']
            else:
                newData['msPlayed'] = data['msPlayed']
            StreamingHistory.append(newData)
        
        return StreamingHistory