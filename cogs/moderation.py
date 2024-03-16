import discord
from discord.ext import commands
from discord import app_commands
import datetime
 
class NewCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
 
    @app_commands.command(name="ban", description="Ban a user")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        try:
            await member.ban(reason=reason)
        except:	
            await interaction.response.send_message(f"❌ I am not allowed to ban {member.mention}.", ephemeral=True)
            return
        await interaction.response.send_message(f"✅ Banned {member.mention}. Reason: **{reason}**", ephemeral=True)

    @app_commands.command(name="kick", description="Kick a user")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        try:
            await member.kick(reason=reason)
        except:
            await interaction.response.send_message(f"❌ I am not allowed to kick {member.mention}.", ephemeral=True)
            return
        await interaction.response.send_message(f"✅ Kicked {member.mention}. Reason: **{reason}**", ephemeral=True)

    @app_commands.command(name="unban", description="Unban a user")
    async def unban(self, interaction: discord.Interaction, user_id: int):
        try:
            await interaction.guild.unban(user=discord.Object(id=user_id))
        except:
            await interaction.response.send_message(f"❌ I am not allowed to unban user with ID `{user_id}`.", ephemeral=True)
            return
        await interaction.response.send_message(f"✅ Unbanned user with ID `{user_id}`", ephemeral=True)

    @app_commands.command(name="timeout-set", description="Timeout a member")
    async def timeout_set(self, interaction: discord.Interaction, member: discord.Member, days: app_commands.Range[int, 0, 28]=None, hours: app_commands.Range[int, 0, 672]=None, minutes: app_commands.Range[int, 0, 40320]=None, seconds: app_commands.Range[int, 0, 2419200]=None, reason: str=None):
        if member.id == interaction.user.id:
            await interaction.response.send_message("❌ You cannot time out yourself!", ephemeral=True)
            return
        if member.guild_permissions.moderate_members:
            await interaction.response.send_message("❌ You cannot do this, this user is a moderator!", ephemeral=True)
            return
        if days == None:
            days = 0
        if hours == None:
            hours = 0
        if minutes == None:
            minutes = 0
        if seconds == None:
            seconds = 0
        duration = datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        if duration.total_seconds() > float(2419200):
            await interaction.response.send_message("❌ You cannot set a timeout longer than 28 days!", ephemeral=True)
            return
        if duration.total_seconds() <= 0:
            await interaction.response.send_message("❌ You cannot set a timeout of less than 1 second!", ephemeral=True)
            return
        try:
            await member.timeout(duration, reason=reason)
        except:
            await interaction.response.send_message(f"❌ I am not allowed to set a timeout for {member.mention}!", ephemeral=True)
            return
        await interaction.response.send_message(f"✅ {member.mention} has been timed out for {days} days, {hours} hours, {minutes} minutes and {seconds} seconds by {interaction.user.mention}", ephemeral=True)

    @app_commands.command(name="timeout-revoke", description="Revoke a member's timeout")
    async def timeout_revoke(self, interaction: discord.Interaction, member: discord.Member, reason: str=None):
        if member.id == interaction.user.id:
            await interaction.response.send_message("❌ You cannot revoke your own timeout!", ephemeral=True)
            return
        if member.guild_permissions.moderate_members:
            await interaction.response.send_message("❌ You cannot do this, this user is a moderator!", ephemeral=True)
            return
        try:
            await member.timeout(None, reason=reason)
        except:
            await interaction.response.send_message(f"❌ I am not allowed to revoke a timeout for {member.mention}!", ephemeral=True)
            return
        await interaction.response.send_message(f"✅ {member.mention}'s timeout has been revoked by {interaction.user.mention}", ephemeral=True)
 
async def setup(bot: commands.Bot):
    await bot.add_cog(NewCog(bot))