#!/usr/bin/env python3
from os import path, chdir
from shutil import rmtree
from sys import exit

from analyze import analyze, merge
from table import generate
from read import get1,get2
from write import write, log
from vars import getDownloadedData, useAPI
from files import setupFiles
from gitbackup import download, upload

if useAPI:
    from apicall import get_tracks

from notify import notify

def main():
    chdir(__file__.replace('main.py',""))#When run from the command line in some sort of automation like crontab, will change directory to this directory so that all other important files are there
    filePath = path.abspath(__file__)
    fileDir = path.dirname(filePath)#The directory the python file is in

    dataDir = path.join(fileDir, 'Spotify Account Data')

    setupFiles()

    download()

    if path.exists(dataDir) and getDownloadedData:
        
        if not useAPI:
            print("about to get data from Spotify Account Data folder and history.json")
            StreamingHistory,length = merge(get1(),get2(),True)
            print("got data from Spotify Account Data folder and history.json")
        else:
            print("about to get data from Spotify Account Data folder, Spotify API and history.json")
            StreamingHistory,length = merge(merge(get1(), get_tracks()),get2(),True)
            print("got data from Spotify Account Data folder, Spotify API and history.json")

        print("Continuing flow")
        log(length)
        write(StreamingHistory)
    

        write(StreamingHistory)
        rmtree(dataDir)
    else:
        if useAPI:
            print("about to get data from Spotify API and history.json")            
            StreamingHistory, length = merge(get2(), get_tracks(),True)
            print("got data from Spotify API and history.json")
        else:
            print("about to get data from history.json")
            StreamingHistory = get2()
            print("got data from history.json")
        
        log(length)
        print("about to write data to history.json")
        write(StreamingHistory)
        print("wrote data to history.json")

    upload()

    

    tableData = analyze(StreamingHistory)
    artistStats = tableData[0]
    trackStats = tableData[2]
    artistHeaders = tableData[1]
    trackHeaders = tableData[3]

    generate(artistStats,artistHeaders,trackStats,trackHeaders)


if __name__ == "__main__":
    main()

