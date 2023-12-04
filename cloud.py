import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload

from os import path,listdir


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
    writeId(folderId,historyJsonId,logsTxtId)







def downloadFromDrive():
    global creds
    creds = None
    credit()
    service = build('drive','v3',credentials=creds)


    if 'fileId.json' not in listdir(): 
        writeAllId(service)
        #If a fileId.json does not exist, create it and write to it

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
    


    

def backupToDrive():
    global creds
    creds = None
    credit()
    service = build('drive','v3',credentials=creds)
    folderId = makeFolder(service,'unwrappedUserData')
    historyJsonId = uploadFile(service,folderId,'history.json','history.json','application/json')
    logsTxtId = uploadFile(service,folderId,'logs.txt','logs.txt','text/plain')
    print(f"Uploaded history.json ({historyJsonId}) and logs.txt ({logsTxtId}) to drive {folderId}")



downloadFromDrive()