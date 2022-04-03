from __future__ import print_function
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timezone
import os.path
import json

authorize_uri_google = "https://accounts.google.com/o/oauth2/auth"
token_uri_google = "https://oauth2.googleapis.com/token", "auth_provider_x509_cert_url", "https://www.googleapis.com/oauth2/v1/certs"

authorize_uri_discord = "https://discord.com/api/oauth2/authorize?client_id=941072154718531594&permissions=8&redirect_uri=https%3A%2F%2Faccounts.google.com%2Fo%2Foauth2%2Fauth&response_type=code&scope=bot"
token_uri_discord = "https://discord.com/api/oauth2/token"

#callback url specified when the application was defined
callback_uri_google = "urn:ietf:wg:oauth:2.0:oob", "http://localhost"

callback_uri_discord = "https://discord.com/api/oauth2/authorize?client_id=941072154718531594&permissions=8&scope=bot"

#client (application) credentials - discord & google
client_id_google = 'client_secret_317800144070-om88ettpsiutn33kit32knjj9mtpunbg.apps.googleusercontent.com.json'
client_secret_google = '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' #google client secret

client_id_discord = '941072154718531594'
client_secret_discord = 'GJ9Thq9lvkmYtmWaoJF3SMpVlBL8hjMJ'


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/calendar']

# The ID and range of a sample spreadsheet.
Google_SPREADSHEET_ID = '1lucr-jZf4t_KCo3chY4QSQ64yuoxcXh_sBClQqCQZ2U'
RANGE = 'MasterDiscordList!A1:D'

# The ID of a sample calendar
Google_CALENDAR_ID = '19aahr89ga4qhhrj15vskbcfhk@group.calendar.google.com'


# Discord token
if os.path.exists('DiscordToken.json'):
    with open('DiscordToken.json') as f:
        discord_token = json.load(f)
else:
    print('Discord Token File not found')

"""
Shows basic usage of the Sheets API.
Prints values from a sample spreadsheet.
"""
def retrieve_credentials():
    """
    Retrieves the Google OAuth Credentials and refreshes tokens if they are expired
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        expiry = creds.expiry
        now = datetime.utcnow()
    
        # d = datetime.now(tz=timezone.utc)
        # print(expiry, 'expiry time')
        # print(now, 'current time')
        # print(d.tzinfo)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token and now < expiry:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_id_google, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


