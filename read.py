import os
import json

def get():
    accountData = os.listdir("Spotify Account Data")

    StreamingHistories = [data for data in accountData if "StreamingHistory" in data]
    StreamingHistory = []


    for i in range(len(StreamingHistories)):    
        with open(f'Spotify Account Data/{StreamingHistories[i]}','r') as history:
            data = history.read()
            json_data = json.loads(data)
            StreamingHistory += json_data
    return StreamingHistory