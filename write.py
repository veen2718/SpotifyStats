from datetime import datetime
import json

def parse_time(data,time='endTime'):
    try:
        return datetime.strptime(data[time], '%Y-%m-%d %H:%M:%S')
    except:
        return datetime.strptime(data[time], '%Y-%m-%d %H:%M')

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
    with open('history.json','w') as historyjson:
        json.dump(sortedHistory, historyjson,indent=4)
    print("Written to history.json")


