import json
from os import path,listdir
from io import BytesIO
from datetime import datetime,timedelta
from dateutil import parser
from time import time
from pytz import utc

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload




folderName = ''

SCOPES = ['https://www.googleapis.com/auth/drive.file']
global creds 




def credit():
    global creds
    if path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json',SCOPES)

    if not creds or not creds.valid: 
        #Checks if there are valid credentials
        if creds and creds.expired:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('googleapi.json',SCOPES)
            creds = flow.run_local_server(port=5500)
        with open('token.json','w') as token:
            token.write(creds.to_json())




def checkFolder(service,name):
    query = f"mimeType='application/vnd.google-apps.folder' and name='{name}' and trashed=false" 
    #Query that google drive will be filtered by, (mimeType -> must be a folder, name -> must have the specified name, trashed -> cannot be in trash)
    
    response = service.files().list(q=query, spaces='drive',fields='files(id,name)').execute() 
    #returns a list of folders that have the criteria specified

    folders = response.get('files',[]) 
    #If the folder exists, the 'files' will exist in the response dictionary, if not, a [] will be returned, response['files'] not used to avoid error being thrown

    return folders



def checkFile(service,fileName, folderId):
    query = f"mimeType!='application/vnd.google-apps.folder' and name='{fileName}' and parents in '{folderId}'" 
    #Query that google drive will be filter (mimeType -> Cannot be a folder, name -> must have the specified name, parents -> must be in the folder specified)

    response = service.files().list(q=query).execute() 
    #Returns a list of files that have the criteria specified

    files = response.get('files',[]) 
    #If the file exists, the 'files' will exist in the response dictionary, if not a [] will be returned

    return files





def makeFolder(service,name):
    isFolder = checkFolder(service,name)
    if isFolder: 
        #Checks to see if the folder already exists

        return isFolder[0].get('id') 
        #If the folder exists, return the id of the folder

    else:
        file_metadata = {'name':name,'mimeType':'application/vnd.google-apps.folder'}
        file = service.files().create(body=file_metadata, fields='id').execute()
        return file.get('id')



def uploadFile(service, folderId,fileName,filePath, mimeType):
    files = checkFile(service,fileName, folderId)
    media = MediaFileUpload(filePath, mimetype=mimeType)

    if files:
        #If the file already exists
        fileId = files[0].get('id')
        file = service.files().update(fileId=fileId, media_body=media).execute()
        #Updates the file. Google drive doesn't stop multiple uploads from the same name in the same directory, so we need to check if the file exists and if it does we need to update it instead of creating a second one

    else:
        #if the file doesn't exist
        fileMetadata = {
            'name':fileName,
            'parents':[folderId],
        }

        media = MediaFileUpload(filePath,mimetype=mimeType)
        file = service.files().create(body=fileMetadata, media_body=media, fields='id').execute()

    return file.get('id')



def downloadFile(service, fileId, fileName):
    request = service.files().get_media(fileId=fileId)
    fh = BytesIO() #Creates an in-memory binary stream to temporarily store downloaded file content
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%" %int(status.progress() * 100))
    with open(fileName, 'wb') as f:
        fh.seek(0)
        f.write(fh.read())



def getLocalMDate(fileName): #Get the time that a local file was modified
    time =  path.getmtime(fileName)
    return datetime.fromtimestamp(time)

def getRemoteMDate(service, fileId): #Get the time that a remote file was modified
    fileMetaData = service.files().get(fileId=fileId, fields='modifiedTime').execute()
    lastModifiedTime = fileMetaData['modifiedTime']
    readableLastModifiedTime = parser.parse(lastModifiedTime)
    return readableLastModifiedTime





def getId(service,name,mimeType,parentId=None):
    query = f"name='{name}' and mimeType='{mimeType}'"
    if parentId:
        query += f" and '{parentId}' in parents"
    response = service.files().list(q=query, spaces='drive',fields='files(id)').execute()
    files = response.get('files',[])
    if files:
        return files[0].get('id')
    return None

def writeId(folderId, historyJsonId, logsTxtId):
    with open('fileId.json','w') as fileId:
            fileId.write(json.dumps({
                'folderId': folderId,
                'historyJsonId': historyJsonId,
                'logsTxtId': logsTxtId
            }))


def writeAllId(service):
    folderId = getId(service,'unwrappedUserData','application/vnd.google-apps.folder')
    historyJsonId = getId(service,'history.json','application/json',folderId)
    logsTxtId = getId(service,'logs.txt','text/plain',folderId)
    if folderId:
        writeId(folderId,historyJsonId,logsTxtId)
        return True
    return False






def downloadFromDrive():
    global creds
    creds = None
    credit()
    service = build('drive','v3',credentials=creds)

    written = True
    if 'fileId.json' not in listdir(): 
        written = writeAllId(service)
        #If a fileId.json does not exist, create it and write to it

    if written:
        with open('fileId.json','r') as Id:
            x = Id.read()
            if x != "":
                ids = json.loads(x)
            else:
                ids = None
            #If the file exists, but is empty, let ids=None

        if not ids:
            #If the file is empty, write to it
            writeAllId(service)
            with open('fileId.json','r') as Id:
                ids = json.loads(Id.read())
        
        historyJsonId = ids['historyJsonId']
        logsTxtId = ids['logsTxtId']

        d1 = getLocalMDate('history.json') #The time that the local history.json was last modified
        d2 = getRemoteMDate(service,historyJsonId) #The UTC time that the remote history.json was last modified
        localTime = time()

        localDatetime = datetime.fromtimestamp(localTime)
        utcDatetime = datetime.utcfromtimestamp(localTime)
        offset = localDatetime - utcDatetime

        d1 = utc.localize(d1)
        d3 = d2 + offset # The timezone-localized time that the remote history.json was last modified

        if d1 < d3:
            downloadFile(service,historyJsonId,'history.json')
            downloadFile(service,logsTxtId,'logs.txt')

def backupToDrive():
    global creds
    creds = None
    credit()
    service = build('drive','v3',credentials=creds)
    folderId = makeFolder(service,'unwrappedUserData')
    historyJsonId = uploadFile(service,folderId,'history.json','history.json','application/json')
    logsTxtId = uploadFile(service,folderId,'logs.txt','logs.txt','text/plain')
    print(f"Uploaded history.json ({historyJsonId}) and logs.txt ({logsTxtId}) to drive {folderId}")