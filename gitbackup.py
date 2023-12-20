import os
import git
from getpass import getpass
from gitcredentials import username, password, repoURL


def initializeRepo(directory):
    if not os.path.isdir(os.path.join(directory, '.git')): #Checks if the directory is already a repo
        print(f"Initializing {directory} as a git repository...")
        repo = git.Repo.init(directory)
    else:
        repo = git.Repo(directory)
    return repo


def setRemote(repo, remoteURL, remoteName='origin'):
    if remoteName not in repo.remotes:
        remote = repo.create_remote(remoteName, remoteURL)
    else:
        remote = repo.remotes[remoteName]
        remote.set_url(remoteURL)
    return remote


def clone_repo(remoteURL, localDir):
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
    try:
        remote = repo.remotes[remoteName]
        remoteURL = remote.url

        if 'http://' in remoteURL:
            remoteURL = remoteURL.replace('http://', f'http://{username}:{password}@')
        elif 'https://' in remoteURL:
            remoteURL = remoteURL.replace('https://', f'https://{username}:{password}@')
        
        remote.set_url(remoteURL)
        print(f"Pushing changes to {remoteName}...")
        remote.push()
        print("Changes pushed successfully.")

    except Exception as e:
        print(f"Error occurred while pushing changes: {e}")