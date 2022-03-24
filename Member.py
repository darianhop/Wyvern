import discord
import pickle
from erplbot.club_members import get_members_from_spreadsheet, Name

class Member(discord.Client):

    async def on_member_join(self, member):
        """
        This function runs whenever a new member joins the server
        """
        # Ignore our own updates
        if member == self.user:
            return
        
        print(f"{member.display_name} joined")
        # Give em' the default role
        recruit_role = member.guild.get_role(RECRUIT_ROLE_ID)
        await member.add_roles(recruit_role, reason='Member join')
        # Create the DM by default
        await member.create_dm()
        async with member.typing():
            # Check as soon as they've joined
            await self.update_members(member)
            # Add a welcome message/embed here
            embed = discord.Embed(
                title="*We hope you rocket to success with us!* :rocket: <:ERPL:809226558988484608>",
                colour=discord.Colour(0x255c6),
                description=f"<@{member.id}> Welcome to **ERPL**! Please read our rules on <#{751973296114761788}>.\r\n If you've paid dues, Please set your nick to the name you filled out in payment of dues...\n *<@{801184786580242552}> should do the rest. This will get you access to project channels.*")
            embed.set_thumbnail(url="https://discord.com/assets/748ff0e7b2f1f22adecad8463de25945.svg")
            embed.set_author(name="Welcome to the Experimental Rocket Propulsion Lab!")
            await member.guild.get_channel(JOIN_CHANNEL).send(embed=embed)
            
    async def on_member_leave(self, discord_member):
        """
        This function runs whenever a new member leaves the server
        """
    
    
    async def on_member_update(self, before, after):
        """
        This function runs whenever a new member updates their own profile, like changing their nickname
        """
        if before.display_name != after.display_name:
            print(f"{before.name} updated to {after.display_name}")
            # Ignore our own updates
            if after == self.user:
                return
            # Here we will just call the update_members function
            await self.update_members(after.member)
            

    async def on_message(self, message):
        """
        This function runs whenever a message is sent
        """
        # Ignore our own updates
        if message.author == self.user:
            return
        
        
    async def update_member(self, member):
        """
        Thhis function updates the member
        """
