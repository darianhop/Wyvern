import os
from google import Create_Service
import pandas as pd

CLIENT_SECRET_FILE = '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'
API_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

spreadsheet_id = '1lucr-jZf4t_KCo3chY4QSQ64yuoxcXh_sBClQqCQZ2U'



"""
BatchGet test
"""
valueRanges_body = [
    'MasterDiscordList!A1:D20'

    ]

response = service.spreadsheets().values().batchGet(
    spreadsheetId=spreadsheet_id,
    majorDimension='ROWS',
    ranges=valueRanges_body
).execute()
print(response.keys())
print(response['valueRanges'])

dataset = {}
for item in response['valueRanges']:
    dataset[item['range']] = item ['values']

    print(dataset["'MasterDiscordList'!A1:D20"])

    df = {}
    for indx, k in enumerate(dataset):
        columns = dataset [k][0]
        data = dataset[k][1:]
        df[indx] = pd.DataFrame(data, columns=columns)
