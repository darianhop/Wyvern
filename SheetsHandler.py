import os
import discord
import gspread
import pygsheets
import pandas as pd
# from __future__ import print_function
from google.oauth2.credentials import Credentials
from pandas import DataFrame
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from Oauth import  retrieve_credentials, Google_SPREADSHEET_ID, RANGE, SCOPES
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# def create_internal_member_object():

try:
    global values1
    creds = retrieve_credentials()
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=Google_SPREADSHEET_ID,
                                range=RANGE).execute()
    values1 = result.get('values', [])

    if not values1:
        print('No data found.')
    else:



        global internal_member_Object

        internal_member_Object = []

        # print('Date, First name, Last name, bool:')
        for row in values1[1:]:
            # Print columns A and E, which correspond to indices 0 and 4.
            # print('%s,%s,%s,%s' % (row[0],row[1],row[2], row[3]))
            internal_member_Object.append({values1[0][0]: row[0:][0],
                                         values1[0][1]: row[1:][0],
                                         values1[0][2]: row[2:][0],
                                         values1[0][3]: row[3:][0]})
            # print(values[0][0],values[1][1])
            # print(row[0:][0],row[1:][0],row[2:][0],row[3:][0])
        # print(internal_member_Object)

except HttpError as err:
    print(err.content)
