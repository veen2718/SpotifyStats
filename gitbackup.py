import os
import git
from getpass import getpass

def setupGit():
    username = input("Enter your github username: ")
    password = getpass("Enter your github password: ")
    path = '/data/'
