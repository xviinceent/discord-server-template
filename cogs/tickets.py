import discord
from discord.ext import commands
from discord import app_commands
from views.close_ticket import CloseTicketView
 
class Tickets(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="close", description="Close a ticket")
    async def close(self, interaction: discord.Interaction):
        await interaction.response.send_message("Are you sure you want to close this ticket?", view=CloseTicketView(), ephemeral=True)
 
async def setup(bot: commands.Bot):
    await bot.add_cog(Tickets(bot))