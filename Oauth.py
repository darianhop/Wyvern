from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

authorize_uri_google = "https://accounts.google.com/o/oauth2/auth"
token_uri_google = "https://oauth2.googleapis.com/token", "auth_provider_x509_cert_url", "https://www.googleapis.com/oauth2/v1/certs"

authorize_uri_discord = ""
token_uri_discord = ""

#callback url specified when the application was defined
callback_uri_google = "urn:ietf:wg:oauth:2.0:oob", "http://localhost"

callback_uri_discord = "https://discord.com/api/oauth2/authorize?client_id=941072154718531594&permissions=8&scope=bot"

test_api_url_google = "<<the URL of the API you want to call, along with any parameters, goes here>>"
test_api_url_discord = "<<the URL of the API you want to call, along with any parameters, goes here>>"

#client (application) credentials - discord & google
client_id_google = 'client_secret_317800144070-om88ettpsiutn33kit32knjj9mtpunbg.apps.googleusercontent.com.json'
client_secret_google = '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' #google client secret?

client_id_discord = ''
client_secret_discord = ''


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/calendar.events.readonly']

# The ID and range of a sample spreadsheet.
Google_SPREADSHEET_ID = '1lucr-jZf4t_KCo3chY4QSQ64yuoxcXh_sBClQqCQZ2U'
RANGE = 'MasterDiscordList!A1:D20'



"""
Shows basic usage of the Sheets API.
Prints values from a sample spreadsheet.
"""
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret_317800144070-om88ettpsiutn33kit32knjj9mtpunbg.apps.googleusercontent.com.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

try:
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=Google_SPREADSHEET_ID,
                                range=RANGE).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')


        member_object = []

        #print('Date, First name, Last name, bool:')
        for row in values[1:]:
            # Print columns A and E, which correspond to indices 0 and 4.
            #print('%s,%s,%s,%s' % (row[0],row[1],row[2], row[3]))
            member_object.append({values[0][0]:row[0:][0],
                                  values[0][1]:row[1:][0],
                                  values[0][2]:row[2:][0],
                                  values[0][3]:row[3:][0]})


    print(member_object)

except HttpError as err:
    print(err)