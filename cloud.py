import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from os.path import *

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def backup_drive():
    creds = None
    