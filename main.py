#!/usr/bin/env python3
from os import path, chdir
from shutil import rmtree
from sys import exit

from analyze import analyze, merge
from table import generate
from read import get1,get2
from write import write, log, fix, prune
from vars import getDownloadedData, useAPI,useGithubBackup
from files import setupFiles
from gitbackup import download, upload

if useAPI:
    from apicall import get_tracks

def main():
    chdir(__file__.replace('main.py',""))#When run from the command line in some sort of automation like crontab, will change directory to this directory so that all other important files are there
    filePath = path.abspath(__file__)
    fileDir = path.dirname(filePath)#The directory the python file is in

    dataDir = path.join(fileDir, 'Spotify Account Data')


    if useGithubBackup:
        setupFiles()
        download()

    data1 = []
    data2 = []
    data3 = []

    if path.exists(dataDir) and getDownloadedData:
        print("about to get data from Spotify Account Data Folder")
        data1 = get1()
        print("got data from Spotify Account Data Folder")
        print("about to delete Spotify Account Data Folder")
        rmtree(dataDir)
        print("Deleted Spotify account Data folder")

    if useAPI:
        print("About to get data from Spotify API")
        data2 = get_tracks()
        print("Got data from spotify API")

    print("About to get data from history.json")
    data3 = get2()
    print("Got data from history.json")

    size0 = len(data3)

    merged1 = merge(data1,data2)
    StreamingHistory = merge(merged1,data3)

    print("About to write streaming history to history.json")
    write(StreamingHistory)
    print("Wrote to history.json")
    fix()
    prune()

    sizef = len(get2())
    difference = sizef-size0
    log(difference)

    if useGithubBackup:
        upload()


    tableData = analyze(StreamingHistory)
    artistStats = tableData[0]
    trackStats = tableData[2]
    artistHeaders = tableData[1]
    trackHeaders = tableData[3]

    generate(artistStats,artistHeaders,trackStats,trackHeaders)


if __name__ == "__main__":
    main()

