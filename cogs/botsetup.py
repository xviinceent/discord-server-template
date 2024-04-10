import discord
from discord.ext import commands
from discord import app_commands

from views.verification import VerificationView
from views.open_ticket import OpenTicketView

import json

class BotSetupView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Start setup", style=discord.ButtonStyle.green)
    async def start_setup_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.guild.owner:
            await interaction.response.send_message("❌ Only the server owner can use this button.", ephemeral=True)
            return
        bot_user = interaction.guild.get_member(interaction.client.user.id)
        if bot_user.top_role.id > interaction.guild.roles[-1].id:
            await interaction.response.send_message("❌ Please make sure I have the highest role in the server.", ephemeral=True)
            return
        with open("config.json", 'r') as f:
            config = json.load(f)
            try:
                setup_done = config["setup_done"]
            except:
                setup_done = None
            try:
                verification_channel_id = config["verification_channel_id"]
                verified_role_id = config["verified_role_id"]
                moderator_role_id = config["moderator_role_id"]
                admin_role_id = config["admin_role_id"]
                ticket_opening_channel_id = config["ticket_opening_channel_id"]
                ticket_category_id = config["ticket_category_id"]
                tempvoice_creation_channel_id = config["tempvoice_creation_channel_id"]
                tempvoice_creation_category_id = config["tempvoice_creation_category_id"]
                ticket_logging_channel_id = config["ticket_logging_channel_id"]
            except KeyError:
                await interaction.response.send_message(f"❌ Setup failed. Please contact an admin.", ephemeral=True)
                return

        if setup_done or setup_done is not None:
            await interaction.response.send_message(f"❌ Already set up.", ephemeral=True)
            return
        
        verification_channel = interaction.guild.get_channel(verification_channel_id)
        if not verification_channel:
            await interaction.response.send_message(f"❌ Setup failed. Please check if the channel with the ID `{verification_channel_id}` exists.", ephemeral=True)
            return
        
        verified_role = interaction.guild.get_role(verified_role_id)
        if not verified_role:
            await interaction.response.send_message(f"❌ Setup failed. Please check if the role with the ID `{verified_role_id}` exists.", ephemeral=True)
            return
        
        mod_role = interaction.guild.get_role(moderator_role_id)
        if not mod_role:
            await interaction.response.send_message(f"❌ Setup failed. Please check if the role with the ID `{moderator_role_id}` exists.", ephemeral=True)
            return
        
        admin_role = interaction.guild.get_role(admin_role_id)
        if not admin_role:
            await interaction.response.send_message(f"❌ Setup failed. Please check if the role with the ID `{admin_role_id}` exists.", ephemeral=True)
            return
        
        ticket_opening_channel = interaction.guild.get_channel(ticket_opening_channel_id)
        if not ticket_opening_channel:
            await interaction.response.send_message(f"❌ Setup failed. Please check if the channel with the ID `{ticket_opening_channel_id}` exists.", ephemeral=True)
            return
        
        ticket_category = interaction.guild.get_channel(ticket_category_id)
        if not ticket_category:
            await interaction.response.send_message(f"❌ Setup failed. Please check if the category with the ID `{ticket_category_id}` exists.", ephemeral=True)
            return
        
        tempvoice_creation_channel = interaction.guild.get_channel(tempvoice_creation_channel_id)
        if not tempvoice_creation_channel:
            await interaction.response.send_message(f"❌ Setup failed. Please check if the channel with the ID `{tempvoice_creation_channel_id}` exists.", ephemeral=True)
            return
        
        tempvoice_creation_category = interaction.guild.get_channel(tempvoice_creation_category_id)
        if not tempvoice_creation_category:
            await interaction.response.send_message(f"❌ Setup failed. Please check if the category with the ID `{tempvoice_creation_category_id}` exists.", ephemeral=True)
            return
        
        ticket_logging_channel = interaction.guild.get_channel(ticket_logging_channel_id)
        if not ticket_logging_channel:
            await interaction.response.send_message(f"❌ Setup failed. Please check if the channel with the ID `{ticket_logging_channel_id}` exists.", ephemeral=True)
            return


        try:
            await verification_channel.send("Click the button below to verify.", view=VerificationView(role_id=verified_role_id))
        except discord.Forbidden:
            await interaction.response.send_message(f"❌ Setup failed. I do not have permission to send messages in the verification channel ({verification_channel.mention}).", ephemeral=True)
            return
        
        try:
            await ticket_opening_channel.send("Click the button below to open a ticket.", view=OpenTicketView())
        except discord.Forbidden:
            await interaction.response.send_message(f"❌ Setup failed. I do not have permission to send messages in the ticket opening channel ({ticket_opening_channel.mention}).", ephemeral=True)
            return
        

        with open("config.json", 'w') as f:
            config["setup_done"] = True
            json.dump(config, f)
        await interaction.response.send_message(f"✅ Setup successful.", ephemeral=True)
 
class BotSetup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
 
    @app_commands.command(name="setup", description="Setup the bot.")
    async def setup_bot(self, interaction: discord.Interaction):
        if interaction.user != interaction.guild.owner:
            await interaction.response.send_message("❌ Only the server owner can use this command.", ephemeral=True)
            return
        await interaction.response.send_message("Click the button below to start the setup.", view=BotSetupView())
 
async def setup(bot: commands.Bot):
    with open("config.json", 'r') as f:
        config = json.load(f)
        verified_role_id = config["verified_role_id"]
    bot.add_view(VerificationView(role_id=verified_role_id))
    bot.add_view(OpenTicketView())
    await bot.add_cog(BotSetup(bot))