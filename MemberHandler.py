import discord
import os
import pickle
import gspread
import numpy as np
import pygsheets
import pandas as pd
# from erplbot.club_members import get_members_from_spreadsheet, Name
from discord import client, guild
from discord.ext import commands, tasks;
from discord.ext.commands import bot
from pandas import DataFrame
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from Oauth import retrieve_credentials, Google_SPREADSHEET_ID, RANGE
# from __future__ import print_function
import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import asyncio
from SheetsHandler import internal_member_Object, values1

global internal_member_Object
global values1

RECRUIT_ROLE_ID = 946832526075367474
MEMBER_ROLE_ID = 946832420798337054
OFFICER_ROLE_ID = 956395930830114817
PROJECT_ROLE_ID = 956395758200959026
BOT_COMMAND_CHANNEL = 947286454277656587
JOIN_CHANNEL = 956969343994978376
guild_ID = 946831225081958410


class Member_Handler(discord.Client):

    # def initMember():
    #     Member_Handler.initializeMemberHandler.start()

    # def unload(self):
    #     self.initializeMemberHandler.cancel()

    # @tasks.loop(seconds = 20)
    # async def initializeMemberHandler():
    #     # await Member_Handler().on_member_join(None)
    #     # loop = asyncio.new_event_loop()
    #     # tasks = Member_Handler.on_member_join(Member_Handler, Member_Handler.user)
    #     # (loop.run_until_complete(tasks))
    #     # asyncio.to_thread
    #     await Member_Handler.on_member_join(Member_Handler, discord.Member)

    # async def on_member_join(self, member):
    #     """
    #     This function runs whenever a new member joins the server
    #     """
    #     # Ignore our own updates
    #     if member == self.user:
    #         return

    #     print(f"{member.name} joined")
    #     # Give em' the default role
    #     recruit_role = discord.Member.guild.get_role(RECRUIT_ROLE_ID)
    #     # recruit_role = RECRUIT_ROLE_ID # Remove after finished
    #     await member.add_roles(recruit_role, reason ='Member join')
    #     # Create the DM by default
    #     await member.create_dm()
    #     async with member.typing():
    #         # Check as soon as they've joined
    #         await self.update_members(member)
    #         # Add a welcome message/embed here
    #         embed = discord.Embed(
    #             title="*We hope you rocket to success with us!* :rocket: <:ERPL:809226558988484608>",
    #             colour=discord.Colour(0x255c6),
    #             description=f"<@{member.id}> Welcome to **ERPL**! Please read our rules on <#{751973296114761788}>.\r\n If you've paid dues, Please set your nick to the name you filled out in payment of dues...\n *<@{801184786580242552}> should do the rest. This will get you access to project channels.*")
    #         embed.set_thumbnail(url="https://discord.com/assets/748ff0e7b2f1f22adecad8463de25945.svg")
    #         embed.set_author(name="Welcome to the Experimental Rocket Propulsion Lab!")
    #         await member.guild.get_channel(JOIN_CHANNEL).send(embed=embed)

    # async def on_member_leave(self, discord_member):
    #     """
    #     This function runs whenever a new member leaves the server
    #     """

    # async def on_member_update(self, before, after):
    #     """
    #     This function runs whenever a new member updates their own profile, like changing their nickname
    #     """
    #     if before.display_name != after.display_name:
    #         print(f"{before.name} updated to {after.display_name}")
    #         # Ignore our own updates
    #         if after == self.user:
    #             return
    #         # Here we will just call the update_members function
    #         await self.update_members(after.member)

    # async def on_message(self, message):
    #     """
    #     This function runs whenever a message is sent
    #     """

    #     # Ignore our own updates
    #     if message.author == self.user:
    #         return

    #     # Recognize if the message is a DM
    #     if message.content.startswith('/DM'):
    #         msg = 'This Message is send in DM'
    #         await client.send_message(message.author,)

    async def update_member(self, member):
        """
        This function updates the member
        """
        return

    async def member_list_Sync(self):
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

        except HttpError as err:
            print(err.content)

        # Pulls and creates new discord member object
        guild = self.get_guild(guild_ID)
        memberList = guild.members
        discObject = []

        # Creates a varible that verifies if
        # the user has the member role or not
        for member in memberList[1:]:
            if MEMBER_ROLE_ID in list(map(lambda role: role.id, member.roles)):
                pow = 1
            else:
                pow = 0
            discObject.append((member.display_name, pow))

        # Clears out the google-sheets chart before writing
        gc = gspread.service_account()

        sh = gc.open("Copy of MemberDues Sheet")

        worksheet = sh.get_worksheet(1)

        worksheet.clear()

        # Loops through the google-sheets chart while searching
        # and verifying wherther on not the user is a member and has
        # payed dues.

        for lines in discObject:

            name = lines[0].split(" ", 1)
            print(lines[1])
            global internal_member_Object

            # Checks first name, last name, and member role status
            if ((list(filter(lambda person: (person['First'] == name[0]), sheets_member_Object))) and
                    (list(filter(lambda person: (person['Last'] == name[1]), sheets_member_Object)))
                    and lines[1] == 1):
                user_Mark = next(item for item in internal_member_Object if item['First'] == name[0])
                user_Mark['Rolled in Discord'] = 'TRUE'
                user_Mark1 = next(item for item in sheets_member_Object if item['First'] == name[0])
                user_Mark1['Rolled in Discord'] = 'TRUE'

                gc = gspread.service_account()

                sh = gc.open("Copy of MemberDues Sheet")

                worksheet = sh.get_worksheet(1)

                df = pd.DataFrame(sheets_member_Object)

                set_with_dataframe(worksheet, df)

            elif ((list(filter(lambda person: (person['First'] == name[0]), sheets_member_Object))) and
                  (list(filter(lambda person: (person['Last'] == name[1]), sheets_member_Object)))
                  and lines[1] == 0):
                user_Mark2 = next(item for item in internal_member_Object if item['First'] == name[0])
                user_Mark2['Rolled in Discord'] = 'FALSE'
                user_Mark3 = next(item for item in sheets_member_Object if item['First'] == name[0])
                user_Mark3['Rolled in Discord'] = 'FALSE'

                gc = gspread.service_account()

                sh = gc.open("Copy of MemberDues Sheet")

                worksheet = sh.get_worksheet(1)

                df = pd.DataFrame(sheets_member_Object)

                set_with_dataframe(worksheet, df)

            else:
                print('Well....poop...?')

        return