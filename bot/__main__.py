from urllib.error import HTTPError
import discord
# from .EventsHandler import GoogleCalendar
from .Oauth import discord_token, retrieve_credentials
from .MemberHandler import Member_Handler, guild_ID, MEMBER_ROLE_ID
from .SheetsHandler import Sheets_Handler


class ERPLBot(discord.Client):
    """
    This class represents the core functionality of the ERPL Discord Bot
    """

    async def on_ready(self):
        """
        This function runs when the bot is connected to Discord
        """
        internal_member_Object = Sheets_Handler.__init__() #Grab the member list
        #Change status
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='4 New Members')) 
        """
        move this (^) to an outside function (in memberhandler), call it there, and update that function whenever someone's role is updated so the discord bot always shows the number of recruits in its activity 
        """
        
        from .EventsHandler import GoogleCalendar
        guilds = self.get_guild(id=guild_ID)
        GoogleCalendar.init(guilds) # Comment in to turn on passive events listener
        # GoogleCalendar.initEvents() # Not yet working (Do not comment in, will crash)
        print("Bot initialized") #success?
        await Sheets_Handler.member_list_Sync(self, guild_ID, MEMBER_ROLE_ID, internal_member_Object) #Do this last because otherwise we ratelimit

    async def on_member_join(self, member):
        await Member_Handler.member_join(self, member)
        
        
    async def on_member_leave(self, member):
        await Member_Handler.member_leave(self, member)
        
    
    async def on_member_update(self, before, after):
        await Member_Handler.member_update(self, before, after)

    async def on_message(self, message):
       await Member_Handler.message(self, message)
    

def main():
    """
    Our "main" function
    """
    # # Reads our Google API credentials before starting the bot
    creds = retrieve_credentials()
    # Sets up our intents as a Discord Bot
    intents = discord.Intents.default()
    intents.members = True
    # Connects to Discord and runs our bot with the bot's token
    client = ERPLBot(intents=intents)
    client.run(discord_token)
    client2 = Member_Handler(intents=intents)
    client2.run(discord_token)


try:
    main()
except HTTPError as e:
    print(f'Could not start main:\n{e}')
