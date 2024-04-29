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
            moderator_role_id = config["moderator_role_id"]
            admin_role_id = config["admin_role_id"]
        if not moderator_role_id in [role.id for role in interaction.user.roles] and not admin_role_id in [role.id for role in interaction.user.roles]:
            await interaction.followup.send("❌ You are not an admin or moderator.", ephemeral=True)
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
            moderator_role_id = config["moderator_role_id"]
            admin_role_id = config["admin_role_id"]
        if not moderator_role_id in [role.id for role in interaction.user.roles] and not admin_role_id in [role.id for role in interaction.user.roles]:
            await interaction.followup.send("❌ You are not an admin or moderator.", ephemeral=True)
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
    async def unban(self, interaction: discord.Interaction, user_id: str):
        await interaction.response.defer(thinking=True, ephemeral=True)
        try:
            user_id = int(user_id)
        except:
            await interaction.followup.send("❌ Invalid number.", ephemeral=True)
        with open("config.json", "r") as f:
            config = json.load(f)
            moderation_logging_channel_id = config["moderation_logging_channel_id"]
            moderator_role_id = config["moderator_role_id"]
            admin_role_id = config["admin_role_id"]
        if not moderator_role_id in [role.id for role in interaction.user.roles] and not admin_role_id in [role.id for role in interaction.user.roles]:
            await interaction.followup.send("❌ You are not an admin or moderator.", ephemeral=True)
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
            moderator_role_id = config["moderator_role_id"]
            admin_role_id = config["admin_role_id"]
        if not moderator_role_id in [role.id for role in interaction.user.roles] and not admin_role_id in [role.id for role in interaction.user.roles]:
            await interaction.followup.send("❌ You are not an admin or moderator.", ephemeral=True)
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
        except discord.Forbidden:
            await interaction.followup.send(f"❌ I am not allowed to set a timeout for {member.mention}!", ephemeral=True)
            return
        user_fetched = await interaction.guild.fetch_member(member.id)
        timestamp = discord.utils.format_dt(user_fetched.timed_out_until, 'f')
        embed = LoggingEmbed(responsible_user=interaction.user, action="User timed out", description=f"User {member.mention} has been given a timeout until {timestamp}. Reason: {reason}")
        logging_channel = interaction.guild.get_channel(moderation_logging_channel_id)
        await logging_channel.send(embed=embed)
        await interaction.followup.send(f"✅ {member.mention} has been timed out for {days} days, {hours} hours, {minutes} minutes and {seconds} seconds by {interaction.user.mention}", ephemeral=True)
        return

    @app_commands.command(name="timeout-revoke", description="Revoke a member's timeout")
    async def timeout_revoke(self, interaction: discord.Interaction, member: discord.Member, reason: str=None):
        await interaction.response.defer(thinking=True, ephemeral=True)
        with open("config.json", "r") as f:
            config = json.load(f)
            moderation_logging_channel_id = config["moderation_logging_channel_id"]
            moderator_role_id = config["moderator_role_id"]
            admin_role_id = config["admin_role_id"]
        if not moderator_role_id in [role.id for role in interaction.user.roles] and not admin_role_id in [role.id for role in interaction.user.roles]:
            await interaction.followup.send("❌ You are not an admin or moderator.", ephemeral=True)
            return
        if member.id == interaction.user.id:
            await interaction.followup.send("❌ You cannot revoke your own timeout!", ephemeral=True)
            return
        if member.guild_permissions.moderate_members:
            await interaction.followup.send("❌ You cannot do this, this user is a moderator!", ephemeral=True)
            return
        try:
            await member.timeout(None, reason=reason)
        except discord.Forbidden:
            await interaction.followup.send(f"❌ I am not allowed to revoke a timeout for {member.mention}!", ephemeral=True)
            return
        embed = LoggingEmbed(responsible_user=interaction.user, action="User timeout revoked", description=f"{member.mention}'s timeout has been revoked. Reason: {reason}")
        logging_channel = interaction.guild.get_channel(moderation_logging_channel_id)
        await logging_channel.send(embed=embed)
        await interaction.followup.send(f"✅ {member.mention}'s timeout has been revoked by {interaction.user.mention}", ephemeral=True)

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: discord.Member):
        with open("config.json", "r") as f:
            config = json.load(f)
            moderation_logging_channel_id = config["moderation_logging_channel_id"]
        channel = guild.get_channel(moderation_logging_channel_id)
        if not channel:
            return
        async for entry in guild.audit_logs(action=discord.AuditLogAction.ban, limit = 10):
            if entry.target == user and entry.user != self.bot.user:
                embed = LoggingEmbed(responsible_user=entry.user, action="User banned", description=f"User {user.mention} has been banned. Reason: {entry.reason}")
                await channel.send(embed=embed)
                break
        return
    
    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.User):
        with open("config.json", "r") as f:
            config = json.load(f)
            moderation_logging_channel_id = config["moderation_logging_channel_id"]
        channel = guild.get_channel(moderation_logging_channel_id)
        if not channel:
            return
        async for entry in guild.audit_logs(action=discord.AuditLogAction.unban, limit = 10):
            if entry.target == user and entry.user != self.bot.user:
                embed = LoggingEmbed(responsible_user=entry.user, action="User unbanned", description=f"User {user.mention} has been unbanned.")
                await channel.send(embed=embed)
                break
        return
    
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        with open("config.json", "r") as f:
            config = json.load(f)
            moderation_logging_channel_id = config["moderation_logging_channel_id"]
        channel = member.guild.get_channel(moderation_logging_channel_id)
        if not channel:
            return
        async for entry in member.guild.audit_logs(action=discord.AuditLogAction.kick, limit = 10):
            if entry.target == member and entry.user != self.bot.user:
                now = datetime.datetime.utcnow()
                entry_time = entry.created_at
                if not all([now.year == entry_time.year, now.month == entry_time.month, now.day == entry_time.day, now.hour == entry_time.hour, now.minute == entry_time.minute, now.second - entry_time.second <= 5]):
                    continue
                embed = LoggingEmbed(responsible_user=entry.user, action="User kicked", description=f"User {member.mention} has been kicked. Reason: {entry.reason}")
                await channel.send(embed=embed)
                break
        return
    
    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        with open("config.json", "r") as f:
            config = json.load(f)
            moderation_logging_channel_id = config["moderation_logging_channel_id"]
        channel = after.guild.get_channel(moderation_logging_channel_id)
        if not channel:
            return
        if before.timed_out_until and not after.timed_out_until:
            async for entry in after.guild.audit_logs(action=discord.AuditLogAction.member_update, limit = 10):
                if entry.target == after and entry.user != self.bot.user:
                    if not entry.target.timed_out_until:
                        embed = LoggingEmbed(responsible_user=entry.user, action="User timeout revoked", description=f"{entry.target.mention}'s timeout has been revoked. Reason: {entry.reason}")
                        await channel.send(embed=embed)
                        break
            return
        if not before.timed_out_until and after.timed_out_until:
            async for entry in after.guild.audit_logs(action=discord.AuditLogAction.member_update, limit = 10):
                if entry.target == after and entry.user != self.bot.user:
                    if entry.target.timed_out_until:
                        embed = LoggingEmbed(responsible_user=entry.user, action="User timed out", description=f"User {entry.target.mention} has been given a timeout until {discord.utils.format_dt(entry.target.timed_out_until, 'f')}. Reason: {entry.reason}")
                        await channel.send(embed=embed)
                        break
            return
        
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        with open("config.json", "r") as f:
            config = json.load(f)
            message_logging_channel_id = config["message_logging_channel_id"]
        channel = message.guild.get_channel(message_logging_channel_id)
        if not channel:
            return
        async for entry in message.guild.audit_logs(action=discord.AuditLogAction.message_delete, limit = 10):
            if entry.target == message.author:
                embed = LoggingEmbed(responsible_user=entry.user, action="Message deleted", description=f"Message by {message.author.mention} has been deleted.")
                embed.add_field(name="Message Content", value=message.content if len(message.content) <= 1024 else message.content[:1018] + " [...]", inline=False)
                await channel.send(embed=embed)
                break
        embed = LoggingEmbed(responsible_user=None, action="Message deleted", description=f"Message by {message.author.mention} has been deleted.")
        embed.add_field(name="Message Content", value=message.content if len(message.content) <= 1024 else message.content[:1018] + " [...]", inline=False)
        await channel.send(embed=embed)
        return
    
    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        with open("config.json", "r") as f:
            config = json.load(f)
            message_logging_channel_id = config["message_logging_channel_id"]
        channel = after.guild.get_channel(message_logging_channel_id)
        if not channel:
            return
        embed = LoggingEmbed(responsible_user=before.author, action="Message edited", description=f"[Message]({after.jump_url}) by {before.author.mention} has been edited.")
        embed.add_field(name="Before", value=before.content if len(before.content) <= 1024 else before.content[:1018] + " [...]", inline=False)
        embed.add_field(name="After", value=after.content if len(after.content) <= 1024 else after.content[:1018] + " [...]", inline=False)
        await channel.send(embed=embed)
        return
 
async def setup(bot: commands.Bot):
    await bot.add_cog(NewCog(bot))