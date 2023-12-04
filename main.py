#!/usr/bin/env python3
from os import path, chdir
from shutil import rmtree

from analyze import analyze, merge
from table import generate
from read import get1,get2
from write import write
from vars import getDownloadedData, useAPI
from cloud import downloadFromDrive,backupToDrive

if useAPI:
    from apicall import get_tracks


def main():
    chdir(__file__.replace('main.py',""))#When run from the command line in some sort of automation like crontab, will change directory to this directory so that all other important files are there
    filePath = path.abspath(__file__)
    fileDir = path.dirname(filePath)#The directory the python file is in

    dataDir = path.join(fileDir, 'Spotify Account Data')


    downloadFromDrive()

    if path.exists(dataDir) and getDownloadedData:
        if not useAPI:
            StreamingHistory = merge(get1(),get2())
        else:
            StreamingHistory = merge(merge(get1(), get_tracks()),get2())
        write(StreamingHistory)
        rmtree(dataDir)
    else:
        if useAPI:
            StreamingHistory = merge(get2(), get_tracks())
        else:
            StreamingHistory = get2()
        write(StreamingHistory)
    
    backupToDrive()    

    

    tableData = analyze(StreamingHistory)
    artistStats = tableData[0]
    trackStats = tableData[2]
    artistHeaders = tableData[1]
    trackHeaders = tableData[3]

    generate(artistStats,artistHeaders,trackStats,trackHeaders)


if __name__ == "__main__":
    main()

