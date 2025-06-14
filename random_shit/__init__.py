import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_youtube():
    key = ""

    flow = InstalledAppFlow

    return build(API_SERVICE_NAME, API_VERSION, credentials=key)

print(get_youtube())
