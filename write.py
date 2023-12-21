from datetime import datetime
import json
import pytz

from read import get2
from files import readJson, writeJson

def parse_time(data,time='endTime'):
    try:
        return datetime.strptime(data[time], '%Y-%m-%d %H:%M:%S')
    except:
        return datetime.strptime(data[time], '%Y-%m-%d %H:%M')


def log(length,path='data/logs.json'):
    pdt_zone = pytz.timezone("America/Los_Angeles") 
    currentTime = datetime.now(pdt_zone).strftime('%Y-%m-%d %H:%M:%S %Z')
    if length > 0:
        messege = f"Added {length} songs at {currentTime}. Total songs are {len(get2())}"
        oldLogs = readJson(path)
        oldLogs.append({currentTime: messege})
        writeJson(path,oldLogs)
    print(f"Added {length} songs at {currentTime}. Total songs are {len(get2())}")  



def write(history):
    newHistory = []
    for story in history:
        newStory = {}
        newStory['endTime'] = story['endTime']
        newStory['artistName'] = story['artistName']
        newStory['trackName'] = story['trackName']
        if 'msPlayed' in story:
            newStory['msPlayed'] = story['msPlayed']
        else:
            newStory['msPlayed'] = None
        if 'duration_ms' in story:
            newStory['duration_ms'] = story['duration_ms']
        else:
            newStory['duration_ms'] = None

        newHistory.append(newStory)
    
    sortedHistory = sorted(newHistory, key=parse_time)
    print("About to write to history.json")
    writeJson('data/history.json', sortedHistory)
    print("Written to history.json")


