#!/usr/bin/env python3
from os import path, chdir
from shutil import rmtree
from sys import exit

from analyze import analyze, merge
from table import generate
from read import get1,get2
from write import write, log
from vars import getDownloadedData, useAPI, usePushbullet
from cloud import downloadFromDrive,backupToDrive

if useAPI:
    from apicall import get_tracks

if usePushbullet:
    from notify import notify

def main(continueAnyways=False):
    chdir(__file__.replace('main.py',""))#When run from the command line in some sort of automation like crontab, will change directory to this directory so that all other important files are there
    filePath = path.abspath(__file__)
    fileDir = path.dirname(filePath)#The directory the python file is in

    dataDir = path.join(fileDir, 'Spotify Account Data')

    
    if path.exists(dataDir) and getDownloadedData:
        if not useAPI:
            StreamingHistory,length = merge(get1(),get2(),True)
        else:
            StreamingHistory,length = merge(merge(get1(), get_tracks()),get2(),True)
        if(StreamingHistory == get2() and not continueAnyways):
            try:
                print("program halted as nothing to write")
                exit()#Exits program to avoid overuse API calls if there are no changes
            except Exception as e:
                print(f"This error is expected to occur, program halted as nothing to write: {e}")
        else:
            print("Continuing flow")
            try:
                downloadFromDrive()
            except Exception as e:
                print(f"An error occured: {e}")
                notify(f"An error occured in Unwrapped: {e}. You may need to sign in again to google for the application to function correctly.")
            log(length)
            write(StreamingHistory)
        

        write(StreamingHistory)
        rmtree(dataDir)
    else:
        if useAPI:
            StreamingHistory, length = merge(get2(), get_tracks(),True)
        else:
            StreamingHistory = get2()
        
        if(StreamingHistory == get2() and not continueAnyways):
            try:
                print("program halted as nothing to write")
                exit()#Exits program to avoid overuse API calls if there are no changes
               
            except Exception as e:
                print(f"This error is expected to occur, program halted as nothing to write: {e}")
        else:
            print("Continuing flow")
            try:
                downloadFromDrive()
            except Exception as e:
                print(f"An error occured: {e}")
                notify(f"An error occured in Unwrapped: {e}. You may need to sign in again to google for the application to function correctly.")
            log(length)
            write(StreamingHistory)
        
    try:
        backupToDrive() 
    except Exception as e:
        print(f"An error occured: {e}")
       

    

    tableData = analyze(StreamingHistory)
    artistStats = tableData[0]
    trackStats = tableData[2]
    artistHeaders = tableData[1]
    trackHeaders = tableData[3]

    generate(artistStats,artistHeaders,trackStats,trackHeaders)


if __name__ == "__main__":
    main()

