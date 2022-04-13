import os
import discord
import gspread
import pygsheets
import pandas as pd
# from __future__ import print_function
from google.oauth2.credentials import Credentials
from pandas import DataFrame
from gspread_dataframe import get_as_dataframe, set_with_dataframe


from folderName.Oauth import  retrieve_credentials, Google_SPREADSHEET_ID, RANGE, SCOPES
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# global internal_member_Object


class Sheets_Handler():

    def __init__():

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


                internal_member_Object = []

                # print('Date, First name, Last name, bool:')
                for row in values1[1:]:
                    # Print columns A and E, which correspond to indices 0 and 4.
                    # print('%s,%s,%s,%s' % (row[0],row[1],row[2], row[3]))
                    internal_member_Object.append({values1[0][0]: row[0:][0],
                                                values1[0][1]: row[1:][0],
                                                values1[0][2]: row[2:][0],
                                                values1[0][3]: row[3:][0]})
                return internal_member_Object


        except HttpError as err:
            print(err.content)



    async def member_list_Sync(self, guild_ID, MEMBER_ROLE_ID, internal_member_Object):
        """
        This function Syncs the google sheets
        and discord member lists
        """

        # Pulls new google sheets_member_object for comparison

        try:
            creds = retrieve_credentials()
            service = build('sheets', 'v4', credentials=creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=Google_SPREADSHEET_ID,
                                        range=RANGE).execute()
            values2 = result.get('values', [])
            if not values2:
                print('No data found.')
            else:

                sheets_member_Object = []

                for row in values2[1:]:
                    sheets_member_Object.append({values2[0][0]: row[0:][0],
                                                 values2[0][1]: row[1:][0],
                                                 values2[0][2]: row[2:][0],
                                                 values2[0][3]: row[3:][0]})
                    # print(sheets_member_Object,'\n')


        except HttpError as e:
            print(f'Error occured while making sheets_memeber_Object:\n{e}')

        # Pulls and creates new discord member object
        guild = self.get_guild(guild_ID)
        memberList = guild.members
        discObject = []

        # Creates a varible that verifies if
        # the user has the member role or not
        for member in memberList:

            if MEMBER_ROLE_ID in list(map(lambda role: role.id, member.roles)):
                pow = 1
            else:
                pow = 0
            discObject.append((member.display_name, pow))


        # Loops through the google-sheets chart while searching
        # and verifying wherther on not the user is a member and has
        # payed dues.

        for lines in discObject:

            name = lines[0].split(" ", 1)
            # print(lines[1])
            # print(name[0])
            # print(name[1])
            internal_member_Object

            try:
                person = str
                # Checks first name, last name, and member role status
                if ((list(filter(lambda person: person['First'].lower() == name[0].lower() and person['Last'].lower() == name[1].lower(), sheets_member_Object))) and lines[1] == 1):

                    user_Mark = next(item for item in internal_member_Object if item['First'].lower() == name[0].lower() and item['Last'].lower() == name[1].lower())
                    user_Mark['Rolled In Discord'] = 'TRUE'
                    user_Mark1 = next(item for item in sheets_member_Object if item['First'].lower() == name[0].lower() and item['Last'].lower() == name[1].lower())
                    user_Mark1['Rolled In Discord'] = 'TRUE'

                    gc = gspread.service_account()

                    sh = gc.open("Copy of MemberDues Sheet")

                    worksheet = sh.get_worksheet(1)
                    df = pd.DataFrame(sheets_member_Object)
                    set_with_dataframe(worksheet, df)

                elif ((list(filter(lambda person: person['First'].lower() == name[0].lower() and person['Last'].lower() == name[1].lower(), sheets_member_Object))) and lines[1] == 0):
                    
                    user_Mark2 = next(item for item in internal_member_Object if item['First'].lower() == name[0].lower() and item['Last'].lower() == name[1].lower())
                    user_Mark2['Rolled In Discord'] = 'FALSE'
                    user_Mark3 = next(item for item in sheets_member_Object if item['First'].lower() == name[0].lower() and item['Last'].lower() == name[1].lower())
                    user_Mark3['Rolled In Discord'] = 'FALSE'


                    gc = gspread.service_account()

                    sh = gc.open("Copy of MemberDues Sheet")

                    worksheet = sh.get_worksheet(1)
                    df = pd.DataFrame(sheets_member_Object)
                    set_with_dataframe(worksheet, df)

            # else:
            except HttpError as e:
                print(e)
                print(f'Encountered an error while updating the sheets list: \n{e}')

        return
