from analyze import analyze, merge
from table import generate
from read import get1,get2
from write import write
from vars import getDownloadedData
from apicall import get_tracks
from os import path
from shutil import rmtree

def main():

    filePath = path.abspath(__file__)
    fileDir = path.dirname(filePath)#The directory the python file is in

    dataDir = path.join(fileDir, 'Spotify Account Data')
    if path.exists(dataDir) and getDownloadedData:
        StreamingHistory = merge(merge(get1(), get_tracks()),get2())
        write(StreamingHistory)
        rmtree(dataDir)
    else:
        StreamingHistory = merge(get2(), get_tracks())
        write(StreamingHistory)
    
        

    

    tableData = analyze(StreamingHistory)
    artistStats = tableData[0]
    trackStats = tableData[2]
    artistHeaders = tableData[1]
    trackHeaders = tableData[3]

    generate(artistStats,artistHeaders,trackStats,trackHeaders)


if __name__ == "__main__":
    main()

