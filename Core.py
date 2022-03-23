import discord
import pickle
from erplbot.club_members import get_members_from_spreadsheet, Name
from erplbot.sheets import GoogleSheets, retrieve_credentials
from erplbot.commands import bot_command

class ERPLBot(discord.Client):
    """
    This class represents the core functionality of the ERPL Discord Bot
    """

    async def on_ready(self):
        """
        This function runs when the bot is connected to Discord
        """
      
    async def on_message(self, message):
        """
        This function runs whenever a message is sent
        """
   
       """
       Bot Commands
       """
       
    async def on_create_project(self, message):
        """
        Create Project Command (Officers Only)
        """
    
    async def on_delete_project(self, message):
        """
        Delete Project Command (Officers Only)
        """
        
   

def main():
    """
    Our "main" function
    """

  


