import discord
from discord.ext import commands
from discord import app_commands
 
class NewCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
 
    @app_commands.command(name="ban", description="Ban a user")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await member.ban(reason=reason)
        await interaction.response.send_message(f"✅ Banned {member.mention}. Reason: **{reason}**", ephemeral=True)

    @app_commands.command(name="kick", description="Kick a user")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await member.kick(reason=reason)
        await interaction.response.send_message(f"✅ Kicked {member.mention}. Reason: **{reason}**", ephemeral=True)

    @app_commands.command(name="unban", description="Unban a user")
    async def unban(self, interaction: discord.Interaction, user_id: int):
        await interaction.guild.unban(user=discord.Object(id=user_id))
        await interaction.response.send_message(f"✅ Unbanned user with ID `{user_id}`", ephemeral=True)
 
async def setup(bot: commands.Bot):
    await bot.add_cog(NewCog(bot))