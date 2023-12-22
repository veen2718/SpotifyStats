import os
import git
import shutil
from pytz import timezone
from datetime import datetime


from files import readJson, writeJson,setupFiles
from gitcredentials import username, password, repoURL
from analyze import merge


defaultPath = os.path.join(__file__.replace("gitbackup.py",""), 'data')


def initializeRepo(directory=defaultPath):
    if not os.path.isdir(os.path.join(directory, '.git')): #Checks if the directory is already a repo
        print(f"Initializing {directory} as a git repository...")
        repo = git.Repo.init(directory)
    else:
        repo = git.Repo(directory)
    
    if repo.head.ref.name != 'main':
        repo.git.branch('-M', 'main')
        print("added Main branch to repo")

    setRemote(repo)
    return repo



def setRemote(repo, remoteURL=repoURL, remoteName='origin'):
    if remoteName not in repo.remotes:
        remote = repo.create_remote(remoteName, remoteURL)
    else:
        remote = repo.remotes[remoteName]
        remote.set_url(remoteURL)
    print(f"set {remoteName} as remote ")
    return remote


def cloneRepo(remoteURL=repoURL, localDir=defaultPath):
    try:
        # Modify the URL to include authentication credentials
        if 'http://' in remoteURL:
            remoteURL = remoteURL.replace('http://', f'http://{username}:{password}@')
        elif 'https://' in remoteURL:
            remoteURL = remoteURL.replace('https://', f'https://{username}:{password}@')
        print(f"Cloning repository from {remoteURL} into {localDir}")
        repo = git.Repo.clone_from(remoteURL, localDir)
        print("Repository cloned successfully.")
        return repo
    except Exception as e:
        print(f"Error occurred while cloning the repository: {e}")


def pushChanges(repo, remoteName='origin'):
    pdt_zone = timezone("America/Los_Angeles") 
    currentTime = datetime.now(pdt_zone).strftime('%Y-%m-%d %H:%M:%S %Z')

    try:
        repo.git.add(A=True)  # Add all files
        repo.index.commit(f"Backup at {currentTime}")
        print("Added and committed files")
    except Exception as e:
        print(f"Error occurred while adding and committing: {e}")
    try:
        remote = repo.remotes[remoteName]
        remoteURL = remote.url

        if 'http://' in remoteURL:
            remoteURL = remoteURL.replace('http://', f'http://{username}:{password}@')
        elif 'https://' in remoteURL:
            remoteURL = remoteURL.replace('https://', f'https://{username}:{password}@')
        
        remote.set_url(remoteURL)
        print(f"Pushing changes to {remoteName}...")
        print(repo.head.ref.name)
        remote.push()
        print("Changes pushed successfully.")

    except Exception as e:
        print(f"Error occurred while pushing changes: {e}")

def download():
    setupFiles()
    shutil.move('data/history.json','temp/history.json')
    shutil.move('data/logs.json','temp/logs.json')
    shutil.rmtree('data')
    print("moved existing files to temp dir")
    cloneRepo()
    setupFiles()
    for jsonFile in ['history.json', 'logs.json']:
        data1 = readJson(f'data/{jsonFile}')
        data2 = readJson(f'temp/{jsonFile}')
        mergedData = merge(data1, data2)
        writeJson(f'data/{jsonFile}', mergedData)
        print(f"Merged {jsonFile} from remote and local")
        try:
            os.remove(f'temp/{jsonFile}')
        except Exception as e:
            print(f'error removing {jsonFile} from temp: {e}')

def upload():
    Repo = initializeRepo()
    pushChanges(Repo)