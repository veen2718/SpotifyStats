from vars import mMin, sortBy


def merge(a, b):
    newList = []
    for item in b:
        if item not in a:
            newList.append(item)
    print(f"Merged Succesfully adding {len(newList)} items")
    return a + newList
    

def analyze(StreamingHistory):
    statsArtists = {}
    statsTracks = {}
    for data in StreamingHistory:
        artistName = data['artistName']
        if data['msPlayed']:
            mPlayed = data['msPlayed']/60000
        elif data['duration_ms']:
            mPlayed = data['duration_ms']/60000
        trackName = data['trackName']
        count = 0
        if mPlayed >= mMin:
            count = 1
        if artistName != 'Unknown Artist':
        #storing data for artists
            if artistName in statsArtists:
                oldCount = statsArtists[artistName][0]
                oldM = statsArtists[artistName][1]
                statsArtists[artistName] = [oldCount + count, oldM + mPlayed]
            else:
                statsArtists[artistName] = [count, mPlayed]

            #storing data for tracks
            key = (trackName, artistName)
            #print(key)
            if key in statsTracks:
                oldCount = statsTracks[key][0]
                oldM = statsTracks[key][1]
                statsTracks[key] = [oldCount + count, oldM + mPlayed]
            else:
                statsTracks[key] = [count, mPlayed]
        #print(key,statsTracks[key])

    #Organizing Arist data

    sortedStats = sorted(statsArtists.items(),key=lambda x:x[1][sortBy], reverse=True)
    sortedStats2 = [[item[0],item[1][0],item[1][1]] for item in sortedStats]



    sumCount = sum([item[1] for item in sortedStats2])
    sumM = sum([item[2] for item in sortedStats2])
    print(sumCount)
    sortedStats3 = [[i+1,item[0],item[1],round(item[2],4),f'{round((100*item[1])/sumCount,2)}%',f'{round((100*item[2])/sumM,4)}%'] for i,item in enumerate(sortedStats2)]

    headersArtists = ["","Artist","Times played","Minutes played for","Percent of total plays","Percent of total Minutes"]

    finalStatsArtists = [headersArtists]+[[0,"Total",sumCount,round(sumM,2),"100%","100%"]] + sortedStats3






    #Organizing Track Data
    sortedStats = sorted(statsTracks.items(),key=lambda x:x[1][sortBy], reverse=True)
    sortedStats2 = [[i+1,item[0][0], item[0][1],item[1][0],round(item[1][1],2)] for i,item in enumerate(sortedStats)]

    sumCount = sum([item[3] for item in sortedStats2])
    sumM = sum([item[4] for item in sortedStats2])

    headersTracks = ["","Track","Artist","Times played","Minutes played for"]
    finalStatsTracks = [headersTracks]+[[0,"Total","Total",sumCount,round(sumM,2)]] + sortedStats2

    return [finalStatsArtists, headersArtists,finalStatsTracks,headersTracks]


