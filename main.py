from analyze import analyze
from table import generate
from read import get1,get2
from write import write
from vars import getDownloadedData

from os import path

def main():

    filePath = path.abspath(__file__)
    fileDir = path.dirname(filePath)#The directory the python file is in

    dataDir = path.join(fileDir, 'Spotify Account Data')
    if path.exists(dataDir) and getDownloadedData:
        StreamingHistory = get1()
        write(StreamingHistory)
    else:
        StreamingHistory = get2()
    
        

    

    tableData = analyze(StreamingHistory)
    artistStats = tableData[0]
    trackStats = tableData[2]
    artistHeaders = tableData[1]
    trackHeaders = tableData[3]

    generate(artistStats,artistHeaders,trackStats,trackHeaders)


if __name__ == "__main__":
    main()

