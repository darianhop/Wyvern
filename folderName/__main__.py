import discord
from folderName.EventsHandler import GoogleCalendar
from folderName.Oauth import discord_token, retrieve_credentials
from folderName.MemberHandler import Member_Handler, guild_ID, MEMBER_ROLE_ID
from folderName.SheetsHandler import Sheets_Handler


class ERPLBot(discord.Client):
    """
    This class represents the core functionality of the ERPL Discord Bot
    """

    async def on_ready(self):
        """
        This function runs when the bot is connected to Discord
        """
        internal_member_Object = Sheets_Handler.__init__()
        await Sheets_Handler.member_list_Sync(self, guild_ID, MEMBER_ROLE_ID, internal_member_Object)
        #Change status
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='4 New Members')) 
        """
        move this (^) to an outside function (in memberhandler), call it there, 
        and update that function whenever someone's role is updated so the discord bot always shows the number of recruits in its activity 
        """
        
        print("Bot initialized")
        from folderName.EventsHandler import GoogleCalendar
        guilds = self.get_guild(id=guild_ID)
        GoogleCalendar.init(guilds) # Comment in to turn on passive events listener
        # GoogleCalendar.initEvents() # Not yet working (Do not comment in, will crash)


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
    # allow mentions
    allowed = discord.AllowedMentions.all()
    # Connects to Discord and runs our bot with the bot's token
    client = ERPLBot(intents=intents,allowed_mentions=allowed)
    client.run(discord_token)
    client2 = Member_Handler(intents=intents)
    client2.run(discord_token)
    client3 = GoogleCalendar(intents=intents)
    client3.run(discord_token)
    client4 = Sheets_Handler(intents=intents)
    client4.run(discord_token)


try:
    main()
except:
    print('Could not start main')
