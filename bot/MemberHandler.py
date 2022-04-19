from http.client import HTTPException
from urllib.error import HTTPError
import discord
from googleapiclient.errors import HttpError
import asyncio
from .SheetsHandler import Sheets_Handler, query_names


BOT_ID = 941072154718531594
RECRUIT_ROLE_ID = 946832526075367474
MEMBER_ROLE_ID = 946832420798337054
PROJECT_LEAD_ROLE_ID = 956395758200959026
OFFICER_ROLE_ID = 956395930830114817
REMINDER_CHANNEL_ID = 947286490973634640
BOT_COMMAND_CHANNEL_ID = 947286454277656587
JOIN_CHANNEL_ID = 956969343994978376
RULES_INFO_CHANNEL_ID = 960003041178828812
PROJECT_CATEGORY_ID = 947275136900407347
guild_ID = 946831225081958410


# # ERPL temp ids

# BOT_ID = 801184786580242552                       #ERPLBot
# RECRUIT_ROLE_ID = 962178982869086210
# MEMBER_ROLE_ID = 962178982869086211
# PROJECT_LEAD_ROLE_ID = 962178982869086212
# OFFICER_ROLE_ID = 962178982869086213
# REMINDER_CHANNEL_ID = 962178983078797390          #reminders
# BOT_COMMAND_CHANNEL_ID = 962178983078797389       #officer-chat
# JOIN_CHANNEL_ID = 962178983573721150              #join-boost
# RULES_INFO_CHANNEL_ID = 962178983078797387        #rules-info
# PROJECT_CATEGORY_ID = 962178983078797391
# guild_ID = 962178982575505499                     #ERPL Discord Guild


class Member_Handler(discord.Client):
    
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
            try:
                await Member_Handler.update_member(Member_Handler,member)
            except:
                pass
            # Add a welcome message/embed here
            embed = discord.Embed(
                title="*We hope you rocket to success with us!* :rocket: <:ERPL:809226558988484608>",
                colour=discord.Colour(0x255c6),
                description=f"<@{member.id}> Welcome to **ERPL**! Please read our rules on <#{RULES_INFO_CHANNEL_ID}>.\r\n If you've paid dues, Please set your nick to the name you filled out in payment of dues...\n *<@{BOT_ID}> should do the rest. This will get you access to project channels.*")
            embed.set_thumbnail(url="https://discord.com/assets/748ff0e7b2f1f22adecad8463de25945.svg")
            embed.set_author(name="Welcome to the Experimental Rocket Propulsion Lab!")
            await member.guild.get_channel(JOIN_CHANNEL_ID).send(embed=embed)
            # Message member on join with welcome message
            DM_embed=discord.Embed(title="Please read our rules on #rules-info & we hope you rocket to success with us. 🚀", 
                                colour=discord.Colour(0x255c6),
                                description="If you've paid dues, Please set your nick to the name you filled out in payment of dues. *@ERPL Bot should do the rest. (if it doesn't work, complain in #join-boost-system )*"
                                )
            DM_embed.set_author(name=f"Hello {member.name}, welcome to ERPL!")
            DM_embed.add_field(name="DM Commads", value="The following commands are to be used in DM to join and leave projects.", inline=False)
            DM_embed.add_field(name="/Projects", value="Lists the current projects.", inline=False)
            DM_embed.add_field(name="/join {Project Name}", value="Grants you the role for that project so you can stay informed!", inline=False)
            DM_embed.add_field(name="/leave {Project Name}", value="Revokes that project's role from you, they'll be sad to see you go.", inline=True)
            DM_embed.add_field(name="/Help", value="Sends this message again in case you've misplaced it.")
            await member.send(embed=DM_embed)

        """    
        # await member.send(f"Hello {member.name}, welcome to *ERPL*!\
        # \n Please read our rules on #rules-info & we hope you rocket to success with us. 🚀\
        # \n If you've paid dues, Please set your nick to the name you filled out in payment of dues.\
        # \n *@Wyvern should do the rest. (if it doesn't work, complain in #join-boost-system )*\
        # \n======\
        # \nCommands\
        # \n======\
        # \n <#/join> This will get you access to project channels.")
        """

    async def member_leave(self, member):
        """
        This function runs whenever a member leaves the server
        """
        # Ignore our own updates
        if member == self.user:
            pass
        
        print(f"{member.name} left")
        await member.guild.get_channel(JOIN_CHANNEL_ID).send(f"Sorry to see you go {member.name}!")

    async def member_update(self, before, after):
        """
        This function runs whenever a member updates their own profile, like changing their nickname
        """
        guilds = self.get_guild(id=guild_ID)

        if before.display_name != after.display_name:
            print(f"{before.name} updated to {after.display_name}")
            # Ignore our own updates
            if after == self.user:
             return

            desired_state = True
            # Here we will just call the update_member function
            if await Member_Handler.update_member(self, after.display_name, desired_state) == True:

                recruit_role = guilds.get_role(role_id=RECRUIT_ROLE_ID)
                await after.remove_roles(recruit_role, reason='Member join', atomic=True)

                member_role = guilds.get_role(role_id=MEMBER_ROLE_ID)
                await after.add_roles(member_role, reason='Member join', atomic=True)
                internal_member_Object = Sheets_Handler.__init__()
                await Sheets_Handler.member_list_Sync(self, guild_ID, MEMBER_ROLE_ID, internal_member_Object)

            return

    async def message(self, message):
        """
        This function runs whenever a message is sent
        """
        # Collect list of existing projects
        await Member_Handler.existing_projects(self, message)
        # Pass the guild info
        guilds = self.get_guild(id=guild_ID)
        
        # Ignore our own messages
        if message.author == self.user:
            return

        # Check to see if the message is from a DM
        if message.channel.type is discord.ChannelType.private:
            """
            DM Commands (All Members)
            """
            try:
                # /Help Command
                if '/Help' or '/help' in message.content:
                    message.author.dm_channel
                    async with message.author.typing():
                        await asyncio.sleep(1)
                        DM_embed=discord.Embed(title="Please read our rules on #rules-info & we hope you rocket to success with us. 🚀", 
                                colour=discord.Colour(0x255c6),
                                description="If you've paid dues, Please set your nick to the name you filled out in payment of dues. *@ERPL Bot should do the rest. (if it doesn't work, complain in #join-boost-system )*"
                                            )
                        DM_embed.set_author(name=f"Hello {message.author}, welcome to ERPL!")
                        DM_embed.add_field(name="DM Commads", value="The following commands are to be used in DM to join and leave projects.", inline=False)
                        DM_embed.add_field(name="/Projects", value="Lists the current projects.", inline=False)
                        DM_embed.add_field(name="/join {Project Name}", value="Grants you the role for that project so you can stay informed!", inline=False)
                        DM_embed.add_field(name="/leave {Project Name}", value="Revokes that project's role from you, they'll be sad to see you go.", inline=True)
                        DM_embed.add_field(name="/Help", value="Sends this message again in case you've misplaced it.")
                        await message.author.send(embed=DM_embed)


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
                        # If message only says '/join'
                        if '/join' == message.content:
                            message.author.dm_channel
                            async with message.author.typing():
                                await asyncio.sleep(1)
                                await message.author.send('Please contact ERFSEDS for additional information.')
                                await message.author.send('Enter Project Name')
                                return
                        # Check to see if message contains the name of an existing project
                        for project_name in project_list:
                            # If the message has the name of a project
                            if project_name in message.content:
                                message.author.dm_channel
                                async with message.author.typing():
                                    await asyncio.sleep(1)
                                    await message.author.send('Valid project')
                                    await message.author.send(f'Granting {project_name} Role.')
                                    # Search the guild for the role associated with the designated project, and grant the member that role
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
                                    # Exception if one occurs
                                    except HTTPException as e:
                                        async with message.author.typing():
                                            await asyncio.sleep(1)
                                            await message.author.send('Something went wrong. Please contact ERFSEDS for additional information.')
                                        print(f"An error occured while interacting with a user through DM: \n{e}")
                                    return
                        # Catch all for any misspellings
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
                        # If message only says '/leave'
                        if '/leave' == message.content:
                            message.author.dm_channel
                            async with message.author.typing():
                                await asyncio.sleep(1)
                                await message.author.send('Enter Project Name')
                                return
                        # Check to see if message contains the name of an existing project
                        for project_name in project_list:
                            # If the message has the name of a project
                            if project_name in message.content:
                                message.author.dm_channel
                                async with message.author.typing():
                                    await asyncio.sleep(1)
                                    await message.author.send('Valid project')
                                    await message.author.send(f'Revoking {project_name} Role.')
                                    # Search the guild for the role associated with the designated project, and revoke the role from that member
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
                        # Catch all for any misspellings         
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
            # Error message for DM
            except Exception as e:
                print(f"An exception occured while sending a DM: \n{e}")
            # End of DM Section
        
        
        """
        Bot Commands
        """
        # Make sure channel is specified
        if message.channel.id == BOT_COMMAND_CHANNEL_ID:
            """
            Project Commands (Officers Only)
            """
            try:
                # /CreateProject {projectName} {Project Lead} Command
                if '/CreateProject' in message.content:
                    # Check to make sure the person sending the message has officer role
                    if guilds.get_role(OFFICER_ROLE_ID) in message.author.roles:
                        await Member_Handler.create_project(self, message, guilds)
                        await message.channel.send(f'Text Channel and Role {projectName} Created')
                
                # /DeleteProject {projectName} Command
                if '/DeleteProject' in message.content:
                    await Member_Handler.delete_project(self, message, guilds)
            # Exception if one occurs
            except Exception as e:
                print(f"An exception occured while creating a new project:\n{e}")
                pass 
            """
            Name Query Sheets
            """
            try:
                if '/QueryNames' in message.content:
                    # Query the names in sheets
                    query_names(message.content)
                    # Make an embed listing all matches
            except Exception as e:
                print(f"An exception occured while creating querying names:\n{e}")
                pass 
            """
            Dectalk
            """
            try:
                if '/Dectalk' in message.content:
                    dectalk(self,message)
            except Exception as e:
                print(f"An exception occured while creating querying names:\n{e}")
                pass 
    
    async def create_project(self, message, guilds):
        """
        Create Project Command (Officers Only) /CreateProject {projectName} {ProjectLead}
        """
        # Attempt to split and save the project name
        await message.channel.send('Officer Role confirmed')
        try:
            if len(message.content.split(' '))<2:
                await message.author.send("Project name is empty")
            global projectName
            projectName = message.content.split(' ')[1]
            print(len(message.content.split(' ')))
            # Get the new project lead
            newProjectLead = message.guild.get_member_named(message.content.split(' ')[2])
            if len(message.content.split(' ')) >=3:
                subChatBool = message.content.split(' ')[3]
            else:
                subChatBool = True
            # Get category, names, and channels
            await Member_Handler.existing_projects(self, message)
            for projects in project_list:
                if projectName  not in project_list:
                    #create channel
                    await discord.TextChannel.clone(guilds.get_channel(project_id_list[0]),name=projectName)
                    # Gather the list of the existing roles
                    await Member_Handler.existing_roles(self)
                    for roles in roles_list:
                        if projectName not in roles_name_list:
                            # If role of that name does not exist, make one
                            await guilds.create_role(name=projectName)
                            # for role in guilds.roles:
                            #     if role.name == projectName:
                            #         perms = discord.Permissions()
                            #         perms.update(create_instant_invite = False, change_nickname = False, read_messages = True, read_message_history = True, connect = True, speak = True, send_messages = False)
                            #         await role.edit(reason = None, colour = discord.Colour.orange(), permissions=perms)
                    # Give the project lead the role
                    project_lead_role = guilds.get_role(role_id=PROJECT_LEAD_ROLE_ID)
                    await newProjectLead.add_roles(project_lead_role)
                    return
        # Exception if one occurs  
        except HttpError as e:
            print(f"User entry failed: {message.content} \n {e}")
            await message.author.create_dm()
            async with message.author.typing():
                await message.author.send("***Error creating the project...***\nPlease use the format: `/CreateProject projectName projectLeadUsername true/false` \n Where ProjectName is the name of the project, projectLeadUsername is the username (not nick) of the new project lead, and the boolean is whether sub-chats are created (default:true)")
                await message.channel.send(e)
        else:
            try:
                print(f'Name Taken: {projectName}')
            except:
                pass

    async def archive_project(self, message, guilds):
        """
        Not Working
        Archive Project Command (Officers Only) /ArchiveProject
        """
        # Attempt to split and save the project name
        await message.channel.send('Officer Role confirmed')
        try:
            if len(message.content.split(' '))<2:
                await message.author.send("Project name is empty")
            global projectName
            projectName = message.content.split(' ')[1]
            print(len(message.content.split(' ')))
            if len(message.content.split(' ')) >=3:
                subChatBool = message.content.split(' ')[3]
            else:
                subChatBool = True
            # Get category, names, and channels
            await Member_Handler.existing_projects(self, message)
            for projects in project_list:
                # Verify channel and role exist
                if projectName in project_list:
                    for channel in project_list:
                        if projectName == guilds.get_channel(project_list):
                            channel = project_id_list
                    # Locate the Project Lead and remove them

                    # Hide Old Project Channel
                    await channel.set_permissions(message.guild.get_role(MEMBER_ROLE_ID), view_channel=False, read_messages=False, send_messages=False, reason=f'Project Deleted by {message.author}')
                    await channel.set_permissions(message.guild.get_role(RECRUIT_ROLE_ID), view_channel=False, read_messages=False, send_messages=False, reason=f'Project Deleted by {message.author}')
                    await channel.set_permissions(message.guild.get_role(PROJECT_LEAD_ROLE_ID), view_channel=False, read_messages=False, send_messages=False, reason=f'Project Deleted by {message.author}')
                    await channel.set_permissions(message.guild.get_role(OFFICER_ROLE_ID), view_channel=False, read_messages=False, send_messages=False, reason=f'Project Deleted by {message.author}')
                    # Loop through categories to locate sub-chats
                    for category in message.guild.categories:
                        if category.name == projectName+" sub-chats":
                            await category.set_permissions(message.guild.get_role(PROJECT_LEAD_ROLE_ID), view_channel=False, read_messages=False, send_messages=False,reason='Project Deleted')
                            await category.set_permissions(message.guild.get_role(OFFICER_ROLE_ID), view_channel=False, read_messages=False, send_messages=False,reason='Project Deleted')
                    # Delete Role (not tested, as i couldnt get the /deleteproject to work) Mee too
                    for projectRole in message.guild.roles:
                        if projectRole.name == projectName:
                            await projectRole.delete(reason=f'Project Deleted by {message.author}')
                    # Send a message back to confirm deletion
                    await message.channel.send(f"Project {projectName} deleted!")

                else:
                    await message.author.create_dm()
                    async with message.author.typing():
                        await message.author.send(f"The project, {projectName}, doesn't exist!")
            
                   
        except HTTPError as e:
            print(f"User entry failed: {message.content} \n {e}")
            await message.author.create_dm()
            async with message.author.typing():
                await message.author.send("***Error deleting the project...***\nPlease use the format: `/DeleteProject projectName` \n Where ProjectName is the name of the project")

    # async def on_delete_project(self, message):
    #     """
    #     Delete Project Command (Officers Only)
    #     """
    #     # Check to make sure the person sending the message has officer role
    #     if OFFICER_ROLE_ID in list(map(lambda role: role.id, message.author.roles)):
    #         # Attempt to split and save the project name
    #         try:
    #             if len(message.content.split(' '))<2:
    #                 await message.author.send("Project name is empty")
    #             projectName = message.content.split(' ')[1].lower()
    #             # Get category, names, and channels
    #             for category in message.guild.categories:
    #                 if category.name == "Projects":
    #                     # Check to make sure the channel/project already exists
    #                     if projectName in [channel.name for channel in category.channels]:
    #                         for channel in category.channels:
    #                             if channel.name == projectName:
    #                                 # Locate the Project Lead and remove them

    #                                 # Hide Old Project Channel
    #                                 await channel.set_permissions(message.guild.get_role(MEMBER_ROLE_ID), view_channel=False, read_messages=False, send_messages=False, reason=f'Project Deleted by {message.author}')
    #                                 await channel.set_permissions(message.guild.get_role(RECRUIT_ROLE_ID), view_channel=False, read_messages=False, send_messages=False, reason=f'Project Deleted by {message.author}')
    #                                 await channel.set_permissions(message.guild.get_role(PROJECT1_ROLE_ID), view_channel=False, read_messages=False, send_messages=False, reason=f'Project Deleted by {message.author}')
    #                                 await channel.set_permissions(message.guild.get_role(OFFICER_ROLE_ID), view_channel=False, read_messages=False, send_messages=False, reason=f'Project Deleted by {message.author}')
    #                                 # Loop through categories to locate sub-chats
    #                                 for category in message.guild.categories:
    #                                     if category.name == projectName+" sub-chats":
    #                                         await category.set_permissions(message.guild.get_role(PROJECT1_ROLE_ID), view_channel=False, read_messages=False, send_messages=False,reason='Project Deleted')
    #                                         await category.set_permissions(message.guild.get_role(OFFICER_ROLE_ID), view_channel=False, read_messages=False, send_messages=False,reason='Project Deleted')
    #                                 # Delete Role (not tested, as i couldnt get the /deleteproject to work)
    #                                 for projectRole in message.guild.roles:
    #                                     if projectRole.name == projectName:
    #                                         await projectRole.delete(reason=f'Project Deleted by {message.author}')
    #                                 # Send a message back to confirm deletion
    #                                 await message.channel.send(f"Project {projectName} deleted!")
    #                     else:
    #                         await message.author.create_dm()
    #                         async with message.author.typing():
    #                             await message.author.send(f"The project, {projectName}, doesn't exist!")

    #         except Exception as e:
    #             print(f"User entry failed: {message.content} \n {e}")
    #             await message.author.create_dm()
    #             async with message.author.typing():
    #                 await message.author.send("***Error deleting the project...***\nPlease use the format: `/DeleteProject projectName` \n Where ProjectName is the name of the project")
        return

    async def update_member(self, after, desired_state):
        """
        This function updates the member(called when someone joins[implemented], when some updates their nickname[not implemented])
        """
        internal_member_Object = Sheets_Handler.__init__()
        # If exists,
        # and the currently filled boolean is opposite disired_state,
        # set the boolean to what was passed,
        # call and return true.
        # Else false.
        global guilds
        guilds = self.get_guild(id=guild_ID)
        #
        # print(after)
        name = after.split(" ",1)
        # print(name[0])
        # print(name[1])
        # print('Before')
        # print(internal_member_Object)
        try:
            if ((list(filter(lambda person: person['First'].lower() == name[0].lower() and person['Last'].lower() == name[1].lower() and person['Rolled In Discord'] != str(desired_state).upper(), internal_member_Object)))):

                    role_Mark = next(item for item in internal_member_Object if item['First'].lower() == name[0].lower() and item['Last'].lower() == name[1].lower() and item['Rolled In Discord'] != str(desired_state).upper())
                    role_Mark['Rolled In Discord'] = 'TRUE'

                    update_member_role = True
                    # print('After')
                    # print('\n\n\n\n',internal_member_Object)
                    # print(update_member_role)

            else:
                    print("There is a user with this name already, not granting member role for security reasons. \ne.g. So all discord users cant have one name to get access to avoid paying dues.")
                    update_member_role = False
                    # print('After')
                    # print('\n\n\n\n',internal_member_Object)
                    # print(update_member_role)

        except HttpError as e:
            print(e)

        return update_member_role

    async def existing_projects(self, message):
        try:
            guilds = self.get_guild(id=guild_ID)
            global project_list
            project_list = []
            global project_id_list
            project_id_list = []
            
            for discord.guild.TextChannel in guilds.get_channel(PROJECT_CATEGORY_ID).channels:
                project_list.append(discord.guild.TextChannel.name)
                project_id_list.append(discord.guild.TextChannel.id)
            return project_list, project_id_list
        except HttpError as e:
            print(e)
            pass

    async def existing_roles(self):
        try:
            guilds = self.get_guild(id=guild_ID)
            global roles_list
            roles_list = []
            global roles_name_list
            roles_name_list = []
            global role_ids
            role_ids =[]
            
            for discord.guild.Role in guilds.roles:
                # roles_list.append(discord.guild.Role)
                roles_name_list.append(discord.guild.Role.name)
                role_ids.append(discord.guild.Role.id)
            return roles_list, roles_name_list, role_ids
        except HTTPError as e:
            print(e)
            pass



