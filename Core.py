from Oauth import discord_token, retrieve_credentials
from MemberHandler import Member_Handler,\
     JOIN_CHANNEL, BOT_COMMAND_CHANNEL, guild_ID,\
     OFFICER_ROLE_ID, PROJECT_ROLE_ID, MEMBER_ROLE_ID, RECRUIT_ROLE_ID
import discord
import asyncio
# from erplbot.club_members import get_members_from_spreadsheet, Name
# from erplbot.commands import bot_command

class ERPLBot(discord.Client):
    """
    This class represents the core functionality of the ERPL Discord Bot
    """

    async def on_ready(self):
        """
        This function runs when the bot is co5nnected to Discord
        """
        await Member_Handler.member_list_Sync(self)
        #Change status
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='4 New Members'))
        print("Bot initialized")
        from EventsHandler import GoogleCalendar
        GoogleCalendar.init() # Comment in to turn on passive events listener
        # GoogleCalendar.initEvents() # Not yet working (Do not comment in, will crash)


    async def on_member_join(self, member):
        """
        This function runs whenever a new member joins the server
        """
        # Ignore our own updates
        if member == self.user:
            return

        print(f"{member.name} joined")
        # Give em' the default role
        recruit_role = member.guild.get_role(role_id=RECRUIT_ROLE_ID)
        # recruit_role = RECRUIT_ROLE_ID # Remove after finished
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
                description=f"<@{member.id}> Welcome to **ERPL**! Please read our rules on <#{960003041178828812}>.\r\n If you've paid dues, Please set your nick to the name you filled out in payment of dues...\n *<@{941072154718531594}> should do the rest. This will get you access to project channels.*")
            embed.set_thumbnail(url="https://discord.com/assets/748ff0e7b2f1f22adecad8463de25945.svg")
            embed.set_author(name="Welcome to the Experimental Rocket Propulsion Lab!")
            await member.guild.get_channel(JOIN_CHANNEL).send(embed=embed)
        # Message member on join with welcome message
        await member.send(f"Hello {member.name}, welcome to *ERPL*!\n Please read our rules on #rules-info & we hope you rocket to success with us. 🚀\n If you've paid dues, Please set your nick to the name you filled out in payment of dues.\n *@ERPLDiscordBot should do the rest. (if it doesn't work, complain in #join-boost-system )*\n This will get you access to project channels.")

        
    async def on_member_leave(self, member):
        """
        This function runs whenever a new member leaves the server
        """
        # Ignore our own updates
        if member == self.user:
            return
        
        print(f"{member.name} left")
        await member.guild.get_channel(JOIN_CHANNEL).send(f"Sorry to see you go {member.name}!")
    
    
    async def on_member_update(self, before, after):
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


    async def on_create_project(self, message):
        """
        Create Project Command (Officers Only)
        """
        await message.channel.send('on_create_project function called')
        # Check to make sure the person sending the message has officer role
        if OFFICER_ROLE_ID in list(map(lambda role: role.id, message.author.roles)):
            # Attempt to split and save the project name
            await message.channel.send('Officer Role confirmed')
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
                    await message.channel.send(e)
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
        
        # Check to see if the message is from a DM
        if message.channel.type is discord.ChannelType.private:
            """
            DM Commands (All Members)
            """
            try:
                if '/Projects' in message.content:
                    message.author.dm_channel
                    async with message.author.typing():
                        await asyncio.sleep(1)
                        await message.author.send('Grabbing List of Projects')

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
                print(f"An exception occured while creating a new project:\n{e}")

"""
    async def calendarEmbed(self, member):
        embed = discord.Embed(
            title='*LB-130 Calenar',
            color=discord.Colour(0x255c6),
            description="Desc",
        )
        from EventsHandler import REMINDER_ID
        await member.guild.get_channel(REMINDER_ID).send(embed=embed)
"""

def main():
    """
    Our "main" function
    """
    # # Reads our Google API credentials before starting the bot
    # creds = retrieve_credentials()
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


try:
    main()
except:
    print('Could not start main')
