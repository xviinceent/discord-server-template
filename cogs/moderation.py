import discord
from discord.ext import commands
from discord import app_commands
import datetime
from components.embeds import LoggingEmbed
import json
 
class NewCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
 
    @app_commands.command(name="ban", description="Ban a user")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await interaction.response.defer(thinking=True, ephemeral=True)
        with open("config.json", "r") as f:
            config = json.load(f)
            moderation_logging_channel_id = config["moderation_logging_channel_id"]
        if not interaction.user.guild_permissions.ban_members:
            await interaction.followup.send("❌ You do not have permission to ban members.", ephemeral=True)
            return
        try:
            await member.ban(reason=reason)
        except:	
            await interaction.followup.send(f"❌ I am not allowed to ban {member.mention}.", ephemeral=True)
            return
        embed = LoggingEmbed(responsible_user=interaction.user, action="User banned", description=f"User {member.mention} has been banned. Reason: {reason}")
        logging_channel = interaction.guild.get_channel(moderation_logging_channel_id)
        await logging_channel.send(embed=embed)
        await interaction.followup.send(f"✅ Banned {member.mention}. Reason: **{reason}**", ephemeral=True)

    @app_commands.command(name="kick", description="Kick a user")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await interaction.response.defer(thinking=True, ephemeral=True)
        with open("config.json", "r") as f:
            config = json.load(f)
            moderation_logging_channel_id = config["moderation_logging_channel_id"]
        if not interaction.user.guild_permissions.kick_members:
            await interaction.followup.send("❌ You do not have permission to kick members.", ephemeral=True)
            return
        try:
            await member.kick(reason=reason)
        except:
            await interaction.followup.send(f"❌ I am not allowed to kick {member.mention}.", ephemeral=True)
            return
        embed = LoggingEmbed(responsible_user=interaction.user, action="User kicked", description=f"User {member.mention} has been kicked. Reason: {reason}")
        logging_channel = interaction.guild.get_channel(moderation_logging_channel_id)
        await logging_channel.send(embed=embed)
        await interaction.followup.send(f"✅ Kicked {member.mention}. Reason: **{reason}**", ephemeral=True)

    @app_commands.command(name="unban", description="Unban a user")
    async def unban(self, interaction: discord.Interaction, user_id: int):
        await interaction.response.defer(thinking=True, ephemeral=True)
        with open("config.json", "r") as f:
            config = json.load(f)
            moderation_logging_channel_id = config["moderation_logging_channel_id"]
        if not interaction.user.guild_permissions.ban_members:
            await interaction.followup.send("❌ You do not have permission to unban members.", ephemeral=True)
            return
        try:
            await interaction.guild.unban(user=discord.Object(id=user_id))
        except:
            await interaction.followup.send(f"❌ I am not allowed to unban user with ID `{user_id}`.", ephemeral=True)
            return
        embed = LoggingEmbed(responsible_user=interaction.user, action="User unbanned", description=f"User {self.bot.get_user(user_id).mention} has been unbanned.")
        logging_channel = interaction.guild.get_channel(moderation_logging_channel_id)
        await logging_channel.send(embed=embed)
        await interaction.followup.send(f"✅ Unbanned user with ID `{user_id}`", ephemeral=True)

    @app_commands.command(name="timeout-set", description="Timeout a member")
    async def timeout_set(self, interaction: discord.Interaction, member: discord.Member, days: app_commands.Range[int, 0, 28]=None, hours: app_commands.Range[int, 0, 672]=None, minutes: app_commands.Range[int, 0, 40320]=None, seconds: app_commands.Range[int, 0, 2419200]=None, reason: str=None):
        await interaction.response.defer(thinking=True, ephemeral=True)
        with open("config.json", "r") as f:
            config = json.load(f)
            moderation_logging_channel_id = config["moderation_logging_channel_id"]
        if not interaction.user.guild_permissions.moderate_members:
            await interaction.followup.send("❌ You do not have permission to time out members.", ephemeral=True)
            return
        if member.id == interaction.user.id:
            await interaction.followup.send("❌ You cannot time out yourself!", ephemeral=True)
            return
        if member.guild_permissions.moderate_members:
            await interaction.followup.send("❌ You cannot do this, this user is a moderator!", ephemeral=True)
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
            await interaction.followup.send("❌ You cannot set a timeout longer than 28 days!", ephemeral=True)
            return
        if duration.total_seconds() <= 0:
            await interaction.followup.send("❌ You cannot set a timeout of less than 1 second!", ephemeral=True)
            return
        try:
            await member.timeout(duration, reason=reason)
        except:
            await interaction.followup.send(f"❌ I am not allowed to set a timeout for {member.mention}!", ephemeral=True)
            return
        embed = LoggingEmbed(responsible_user=interaction.user, action="User timed out", description=f"User {member.mention} has been given a timeout. Reason: {reason}")
        logging_channel = interaction.guild.get_channel(moderation_logging_channel_id)
        await logging_channel.send(embed=embed)
        await interaction.followup.send(f"✅ {member.mention} has been timed out for {days} days, {hours} hours, {minutes} minutes and {seconds} seconds by {interaction.user.mention}", ephemeral=True)

    @app_commands.command(name="timeout-revoke", description="Revoke a member's timeout")
    async def timeout_revoke(self, interaction: discord.Interaction, member: discord.Member, reason: str=None):
        await interaction.response.defer(thinking=True, ephemeral=True)
        with open("config.json", "r") as f:
            config = json.load(f)
            moderation_logging_channel_id = config["moderation_logging_channel_id"]
        if not interaction.user.guild_permissions.moderate_members:
            await interaction.followup.send("❌ You do not have permission to remove timeouts from members.", ephemeral=True)
            return
        if member.id == interaction.user.id:
            await interaction.followup.send("❌ You cannot revoke your own timeout!", ephemeral=True)
            return
        if member.guild_permissions.moderate_members:
            await interaction.followup.send("❌ You cannot do this, this user is a moderator!", ephemeral=True)
            return
        try:
            await member.timeout(None, reason=reason)
        except:
            await interaction.followup.send(f"❌ I am not allowed to revoke a timeout for {member.mention}!", ephemeral=True)
            return
        embed = LoggingEmbed(responsible_user=interaction.user, action="User timeout revoked", description=f"{member.mention}'s timeout has been revoked. Reason: {reason}")
        logging_channel = interaction.guild.get_channel(moderation_logging_channel_id)
        await logging_channel.send(embed=embed)
        await interaction.followup.send(f"✅ {member.mention}'s timeout has been revoked by {interaction.user.mention}", ephemeral=True)
 
async def setup(bot: commands.Bot):
    await bot.add_cog(NewCog(bot))