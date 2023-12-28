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


def log(Length,path='data/logs.json'):
    pdt_zone = pytz.timezone("America/Los_Angeles") 
    currentTime = datetime.now(pdt_zone).strftime('%Y-%m-%d %H:%M:%S %Z')
    if Length > 0:
        messege = f"Added {Length} songs at {currentTime}. Total songs are {len(get2())}"
        oldLogs = readJson(path)
        oldLogs.append({currentTime: messege})
        writeJson(path,oldLogs)
    print(f"Added {Length} songs at {currentTime}. Total songs are {len(get2())}")  



def write(history):
    newHistory = []
    for story in history:
        newStory = {}
        newStory['endTime'] = story['endTime']
        if type(story['artistName']) in [list, tuple]:
            newStory['artistName'] = tuple(story['artistName'])
        if type(story['artistName']) == list:
            print("A list",story['artistName'], newStory['artistName'])
        else:
            newStory['artistName'] = tuple(story['artistName'])
        # newStory['artistName'] = story['artistName']
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

def prune():#Removes duplicate entries, meaning exact time must match, as well as artist and track names
    print("about to start pruning")
    data = readJson('data/history.json')
    prunedData = []
    prunedCount = 0
    for entry in data:
        if entry in prunedData:
            prunedCount += 1
            print(f"pruned: {entry}")
        else:
            prunedData.append(entry)
            
    if prunedCount > 0:
        print(f"Pruned {prunedCount} copies")
        writeJson('data/history.json', prunedData)
        log(prunedCount * -1)

    print("finished prining")