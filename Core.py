import discord
import pickle
# from erplbot.club_members import get_members_from_spreadsheet, Name
from Oauth import creds, discord_creds
# from erplbot.commands import bot_command

class ERPLBot(discord.Client):
    """
    This class represents the core functionality of the ERPL Discord Bot
    """

    async def on_ready(self):
        """
        This function runs when the bot is connected to Discord
        """
      

    async def on_create_project(self, message):
        """
        Create Project Command (Officers Only)
        """
        # Check to make sure the person sending the message has officer role
        if OFFICER_ROLE_ID in list(map(lambda role: role.id, message.author.roles)):
            # Attempt to split and save the project name
            try:
                if len(message.content.split(' '))<2:
                    await message.author.send("Project name is empty")
                projectName = message.content.split(' ')[1]
                print(len(message.content.split(' ')))
                if len(message.content.split(' ')) >=3:
                    subChatBool = message.content.split(' ')[3]
                else:
                    subChatBool = True
                # Get category, names, and channels
                for category in message.guild.categories:
                    if category.name == "Projects":
                        print(category.channels)
                        # Check to make sure the channel/project/role does not already exist 
                        if projectName in [channel.name for channel in category.channels]:
                            await message.author.create_dm()
                            async with message.author.typing():
                                await message.author.send(f"The project, {projectName}, already exists!")
                        elif projectName in [role.name for role in message.guild.roles]:
                            await message.author.create_dm()
                            async with message.author.typing():
                                await message.author.send(f"The role, {projectName}, already exists!")
                        else:
                            # Get the new project lead
                            newProjectLead = message.guild.get_member_named(message.content.split(' ')[2])
                            print(f"Project lead: {newProjectLead}")
                            # Create the Project role
                            projectRole = await message.guild.create_role(name=projectName, reason=f'Project creation by {message.author}')
                            # Create the project channel
                            projectChannel = await message.guild.create_text_channel(name=projectName,category=category)
                            await projectChannel.set_permissions(newProjectLead, manage_channels=True, manage_permissions=True, manage_webhooks=True, read_message_history=True, reason=f'Project creation by {message.author}')
                            await projectChannel.set_permissions(projectRole, view_channel=True, read_messages=True, send_messages=True, add_reactions=True, attach_files=True, embed_links=True, read_message_history=True, reason=f'Project creation by {message.author}')
                            
                            if subChatBool:
                                print(f"Subchat: {subChatBool}")
                                # Setup Sub-chat category & channel
                                
                                # Assign Permissions to category

                            # Give new project lead roles & alert them
                            await newProjectLead.add_roles(message.guild.get_role(PROJECT_ROLE_ID), reason=f'Project creation by {message.author}')
                            await newProjectLead.add_roles(projectRole, reason=f'Project creation by {message.author}')
                            await newProjectLead.send(f"Project {projectName} created by {message.author}!") 
                            # Send a message back to confirm creation
                            await message.channel.send(f"Project {projectName} created!")
            
            except Exception as e:
                print(f"User entry failed: {message.content} \n {e}")
                await message.author.create_dm()
                async with message.author.typing():
                    await message.author.send("***Error creating the project...***\nPlease use the format: `/CreateProject projectName projectLeadUsername true/false` \n Where ProjectName is the name of the project, projectLeadUsername is the username (not nick) of the new project lead, and the boolean is whether sub-chats are created (default:true)")
        else:
            print(f'Name Taken: {name}')

    
    async def on_delete_project(self, message):
        """
        Delete Project Command (Officers Only)
        """
        # Check to make sure the person sending the message has officer role
        if OFFICER_ROLE_ID in list(map(lambda role: role.id, message.author.roles)):
            # Attempt to split and save the project name
            try:
                if len(message.content.split(' '))<2:
                    await message.author.send("Project name is empty")
                projectName = message.content.split(' ')[1].lower()
                # Get category, names, and channels
                for category in message.guild.categories:
                    if category.name == "Projects":
                        # Check to make sure the channel/project already exists 
                        if projectName in [channel.name for channel in category.channels]:
                            for channel in category.channels:
                                if channel.name == projectName:
                                    # Locate the Project Lead and remove them

                                    # Hide Old Project Channel
                                    await channel.set_permissions(message.guild.get_role(MEMBER_ROLE_ID), view_channel=False, read_messages=False, send_messages=False, reason=f'Project Deleted by {message.author}')
                                    await channel.set_permissions(message.guild.get_role(RECRUIT_ROLE_ID), view_channel=False, read_messages=False, send_messages=False, reason=f'Project Deleted by {message.author}')
                                    await channel.set_permissions(message.guild.get_role(PROJECT_ROLE_ID), view_channel=False, read_messages=False, send_messages=False, reason=f'Project Deleted by {message.author}')
                                    await channel.set_permissions(message.guild.get_role(OFFICER_ROLE_ID), view_channel=False, read_messages=False, send_messages=False, reason=f'Project Deleted by {message.author}')
                                    # Loop through categories to locate sub-chats
                                    for category in message.guild.categories:
                                        if category.name == projectName+" sub-chats":
                                            await category.set_permissions(message.guild.get_role(PROJECT_ROLE_ID), view_channel=False, read_messages=False, send_messages=False,reason='Project Deleted')
                                            await category.set_permissions(message.guild.get_role(OFFICER_ROLE_ID), view_channel=False, read_messages=False, send_messages=False,reason='Project Deleted')
                                    # Delete Role (not tested, as i couldnt get the /deleteproject to work)
                                    for projectRole in message.guild.roles:
                                        if projectRole.name == projectName:
                                            await projectRole.delete(reason=f'Project Deleted by {message.author}')
                                    # Send a message back to confirm deletion
                                    await message.channel.send(f"Project {projectName} deleted!")
                        else:
                            await message.author.create_dm()
                            async with message.author.typing():
                                await message.author.send(f"The project, {projectName}, doesn't exist!")
            
            except Exception as e:
                print(f"User entry failed: {message.content} \n {e}")
                await message.author.create_dm()
                async with message.author.typing():
                    await message.author.send("***Error deleting the project...***\nPlease use the format: `/DeleteProject projectName` \n Where ProjectName is the name of the project")


    async def on_message(self, message):
        """
        This function runs whenever a message is sent
        """
        # Ignore our own messages
        if message.author == self.user:
            return
        
        """
        Bot Commands
        """
        # Make sure channel is specified
        if message.channel == message.guild.get_channel(BOT_COMMAND_CHANNEL):
            """
            Create Project Command (Officers Only)
            """
            try:
                if '/CreateProject' in message.content:
                    on_create_project(self,message)

                if '/DeleteProject' in message.content:
                    on_delete_project(self,message)
                         
            except Exception as e:
                print(f"An exception occured while creating a new project:\n{e}")


def main():
    """
    Our "main" function
    """
    global creds
    # Reads our Google API credentials before starting the bot
    # creds = retrieve_credentials()
    # Sets up our intents as a Discord Bot
    intents = discord.Intents.default()
    intents.members = True
    # allow mentions
    allowed = discord.AllowedMentions.all()
    # Connects to Discord and runs our bot with the bot's token
    client = ERPLBot(intents=intents,allowed_mentions=allowed)
    client.run(discord_creds)

main()
  

