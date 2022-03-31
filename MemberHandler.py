import discord
import pickle
# from erplbot.club_members import get_members_from_spreadsheet, Name
from discord import client, guild
from discord.ext import commands, tasks; from discord.ext.commands import bot

from Oauth import  retrieve_credentials, Google_SPREADSHEET_ID, RANGE
#from __future__ import print_function
import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import asyncio



RECRUIT_ROLE_ID = 946832526075367474
MEMBER_ROLE_ID = 946832420798337054
OFFICER_ROLE_ID = 956395930830114817
PROJECT_ROLE_ID = 956395758200959026
BOT_COMMAND_CHANNEL = 947286454277656587
JOIN_CHANNEL = 956969343994978376
guild_ID = 946831225081958410

def __str__(self):
    return ""
def iterateDictionary2(key_name, some_list):
    for d in some_list:
        print(d[key_name])
class Name:
    """
    Represents a person's name. First and Last
    """

    def __init__(self, first=None, last=None):
        """
        Creates a new Name instance with the optional values
        """
        self.first = first
        self.last = last

    @staticmethod
    def from_str(s):
        """
        Creates a new Name object from the given string.
        Will only populate the first name if that is the only one given
        """
        name = Name()

        # Split the string by spaces
        name_split = s.split(' ')

        name.first = name_split[0]

        # If their name has more than one word, like a name, store that too
        if len(name_split) > 1:
            name.last = name_split[1]

        return name

    def __eq__(self, other):
        """
        Overrides the == operator for this type
        """
        return self.first == other.first and self.last == other.last

    def __repr__(self):
        """
        The internal function called by Python when trying to print this type
        """
        return f'{self.first} {self.last}'



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

    def iterateDictionary2(key_name, some_list):
        for d in some_list:
            print(d[key_name])

    async def member_list_Sync(self):
        """
        This function Syncs the google sheets
        and discord member lists
        """
        discord_member_object = []
        # Pull new google sheets member_object
        try:
            creds = retrieve_credentials()
            service = build('sheets', 'v4', credentials=creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=Google_SPREADSHEET_ID,
                                        range=RANGE).execute()
            values = result.get('values', [])

            if not values:
                print('No data found.')
            else:

                member_object = []

                # print('Date, First name, Last name, bool:')
                for row in values[1:]:
                    # Print columns A and E, which correspond to indices 0 and 4.
                    # print('%s,%s,%s,%s' % (row[0],row[1],row[2], row[3]))
                    member_object.append({values[0][0]: row[0:][0],
                                          values[0][1]: row[1:][0],
                                          values[0][2]: row[2:][0],
                                          values[0][3]: row[3:][0]})
                    #print(row[1:][0],row[2:][0])
                print(member_object)

        except HttpError as err:
            print(err.content)

        #obtain guild members
        guild = self.get_guild(guild_ID)
        memberList = guild.members
        print(memberList)

        discord_member_object = [dict() for i in range(4)]
        #print(discord_member_object)

        #discord_member_object
        # X = bool
        #
        # for row2 in memberList[1:]:
        #  name = str(row2)
        #  name = name[:-5]
        #  name = name.split(" ", 1)
        #  print(name[0])
        #  # iterateDictionary2('First',member_object)
        #  list_of_all_values = [value for x in member_object
        #                        for value in x.values()]
        #  if name[0] in list_of_all_values:
        #    #print(row[1:][0])
        #    print("First name: Match")
        #    X=True
        #    if name[1] in list_of_all_values:
        #        print("Last name: Match")
        #  else:
        #    print("nope not the same")
        #    X=False
        #    print(X)
        # print(row2)
        # print(X)
        # print("{} {}".format(row[1:][0], row[2:][0]))




        return