from http.client import HTTPException
import discord
import os
import pickle
import gspread
from httplib2 import Http
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

global internal_member_Object
global values1
from SheetsHandler import internal_member_Object, values1

WYVERN_ID = 941072154718531594
RECRUIT_ROLE_ID = 946832526075367474
MEMBER_ROLE_ID = 946832420798337054
OFFICER_ROLE_ID = 956395930830114817
PROJECT1_ROLE_ID = 956395758200959026
BOT_COMMAND_CHANNEL = 947286454277656587
JOIN_CHANNEL = 956969343994978376
RULES_INFO_CHANNEL_ID = 960003041178828812
PROJECT_CATEGORY_ID = 947275136900407347
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

    async def member_join(self, member):
        """
        This function runs whenever a new member joins the server
        """
        # Ignore our own updates
        if member == self.user:
            return

        print(f"{member.name} joined")
        # Give em' the default role
        recruit_role = member.guild.get_role(role_id=RECRUIT_ROLE_ID)
        await member.add_roles(recruit_role, reason ='Member join', atomic = True)
        # Create the DM by default
        await member.create_dm()
        async with member.typing():
            # Check as soon as they've joined
            await Member_Handler.update_member(Member_Handler,member)
            # Add a welcome message/embed here
            embed = discord.Embed(
                title="*We hope you rocket to success with us!* :rocket: <:ERPL:809226558988484608>",
                colour=discord.Colour(0x255c6),
                description=f"<@{member.id}> Welcome to **ERPL**! Please read our rules on <#{RULES_INFO_CHANNEL_ID}>.\r\n If you've paid dues, Please set your nick to the name you filled out in payment of dues...\n *<@{WYVERN_ID}> should do the rest. This will get you access to project channels.*")
            embed.set_thumbnail(url="https://discord.com/assets/748ff0e7b2f1f22adecad8463de25945.svg")
            embed.set_author(name="Welcome to the Experimental Rocket Propulsion Lab!")
            await member.guild.get_channel(JOIN_CHANNEL).send(embed=embed)
        # Message member on join with welcome message
        await member.send(f"Hello {member.name}, welcome to *ERPL*!\n Please read our rules on #rules-info & we hope you rocket to success with us. 🚀\n If you've paid dues, Please set your nick to the name you filled out in payment of dues.\n *@Wyvern should do the rest. (if it doesn't work, complain in #join-boost-system )*\n This will get you access to project channels.")


    async def member_leave(self, member):
        """
        This function runs whenever a new member leaves the server
        """
        # Ignore our own updates
        if member == self.user:
            return
        
        print(f"{member.name} left")
        await member.guild.get_channel(JOIN_CHANNEL).send(f"Sorry to see you go {member.name}!")


    async def member_update(self, before, after):
        """
        This function runs whenever a new member updates their own profile, like changing their nickname
        """
        if before.display_name != after.display_name:
            print(f"{before.name} updated to {after.display_name}")
            # Ignore our own updates
            if after == self.user:
                return
            # Here we will just call the update_member function
            await Member_Handler.update_member(Member_Handler,after.member)


    async def message(self, message):
        """
        This function runs whenever a message is sent
        """
        # Ignore our own messages
        if message.author == self.user:
            return
        
        # Check to see if the message is from a DM
        if message.channel.type is discord.ChannelType.private:
            """
            DM Commands (All Members)
            """
            await Member_Handler.existing_projects(self, message)
            guilds = self.get_guild(id=guild_ID)
            try:
                # /Projects Command
                if '/Projects' in message.content:
                    message.author.dm_channel
                    async with message.author.typing():
                        await asyncio.sleep(1)
                        await message.author.send('Grabbing List of Projects')
                        async with message.author.typing():
                            await asyncio.sleep(0.5)
                            await message.author.send(project_list)
                # /join Command                            
                if '/join' in message.content:
                    try:
                        if '/join' == message.content:
                            message.author.dm_channel
                            async with message.author.typing():
                                await asyncio.sleep(1)
                                await message.author.send('Please contact ERFSEDS for additional information.')
                                await message.author.send('Enter Project Name')
                                return
                        for project_name in project_list:
                            if project_name in message.content:
                                message.author.dm_channel
                                async with message.author.typing():
                                    await asyncio.sleep(1)
                                    await message.author.send('Valid project')
                                    await message.author.send(f'Granting {project_name} Role.')
                                    try:
                                        roles = []
                                        roles = guilds.roles
                                        for role_info in roles:
                                            if role_info.name == project_name:
                                                project_role_id=role_info
                                        member_id = message.author.id
                                        member = guilds.get_member(member_id)
                                        # Granting the project role to the member
                                        await member.add_roles(project_role_id)
                                        async with message.author.typing():
                                            await asyncio.sleep(1)
                                            await message.author.send(f'{project_name} Role Granted')

                                    except HTTPException as e:
                                        async with message.author.typing():
                                            await asyncio.sleep(1)
                                            await message.author.send('Something went wrong. Please contact ERFSEDS for additional information.')
                                        print(f"An error occured while interacting with a user through DM: \n{e}")
                                    
                                    return
                        else:
                            async with message.author.typing():
                                await asyncio.sleep(1)
                                await message.author.send('Invalid Project')
                                await message.author.send(project_list)
                                return
                    except HTTPException as e:
                        async with message.author.typing():
                            await asyncio.sleep(1)
                            await message.author.send('Something went wrong. Please contact ERFSEDS for additional information.')
                        print(f"An error occured while interacting with a user through DM: \n{e}")
                # /leave Command
                if '/leave' in message.content:
                    try:
                        if '/leave' == message.content:
                            message.author.dm_channel
                            async with message.author.typing():
                                await asyncio.sleep(1)
                                await message.author.send('Enter Project Name')
                                return
                        for project_name in project_list:
                            if project_name in message.content:
                                message.author.dm_channel
                                async with message.author.typing():
                                    await asyncio.sleep(1)
                                    await message.author.send('Valid project')
                                    await message.author.send(f'Revoking {project_name} Role.')
                                    try:
                                        roles = []
                                        roles = guilds.roles
                                        for role_info in roles:
                                            if role_info.name == project_name:
                                                project_role=role_info
                                        member_id = message.author.id
                                        member = guilds.get_member(member_id)
                                        # Removing the project role from the member
                                        await member.remove_roles(project_role)
                                        async with message.author.typing():
                                            await asyncio.sleep(1)
                                            await message.author.send(f'{project_name} Role Revoked')

                                    except HTTPException as e:
                                        async with message.author.typing():
                                            await asyncio.sleep(1)
                                            await message.author.send('Something went wrong. Please contact ERFSEDS for additional information.')
                                        print(f"An error occured while interacting with a user through DM: \n{e}")
                                    
                                    return
                                    
                        else:
                            async with message.author.typing():
                                await asyncio.sleep(1)
                                await message.author.send('Invalid Project')
                                await message.author.send(project_list)
                                return
                    except:
                        async with message.author.typing():
                            await asyncio.sleep(1)
                            await message.author.send('Something went wrong. Please contact ERFSEDS for additional information.')

            except Exception as e:
                print(f"An exception occured while sending a DM: \n{e}")

        """
        Bot Commands
        """
        # Make sure channel is specified
        if message.channel.id == BOT_COMMAND_CHANNEL:
            """
            Project Commands (Officers Only)
            """
            try:
                if '/CreateProject' in message.content:
                    await message.channel.send('Calling on_create_project function')
                    await self.on_create_project(message)

                if '/DeleteProject' in message.content:
                    await message.channel.send('Calling on_delete_project function')
                    await self.on_delete_project(message)

            except Exception as e:
                await asyncio.sleep(1)
                print(f"An exception occured while creating a new project:\n{e}")
                pass
    
    
    async def update_member(self, member):
        """
        This function updates the member(called when someone joins[implemented], when some updates their nickname[not implemented])
        """
        return


    async def existing_projects(self, message):
        try:
            guilds = self.get_guild(id=guild_ID)
            global project_list
            project_list = []
            
            for discord.guild.TextChannel in guilds.get_channel(PROJECT_CATEGORY_ID).channels:
                project_list.append(discord.guild.TextChannel.name)
                
            
        except HttpError as e:
            print(e)

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
            try:
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

            # else:
            except HttpError as e:
                print(e)
                print('Well....poop...?')

        return