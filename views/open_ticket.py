import discord

class OpenTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.green, custom_id="button:open_ticket", emoji="📩")
    async def open_ticket_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("✅ Ticket opened!", ephemeral=True)