import discord
from discord.ext import commands
from discord import app_commands
from views.verification import VerificationView
import json

class BotSetupView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Start setup", style=discord.ButtonStyle.green)
    async def start_setup_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open("config.json", 'r') as f:
            config = json.load(f)
            setup_done = config["setup_done"]
            verification_channel_id = config["verification_channel_id"]
            verified_role_id = config["verified_role_id"]

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
        

        try:
            await verification_channel.send("Click the button below to verify.", view=VerificationView(role_id=verified_role_id))
        except discord.Forbidden:
            await interaction.response.send_message(f"❌ Setup failed. I do not have permission to send messages in the verification channel.", ephemeral=True)
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
        await interaction.response.send_message("Click the button below to start the setup.", view=BotSetupView())
 
async def setup(bot: commands.Bot):
    with open("config.json", 'r') as f:
        config = json.load(f)
        verified_role_id = config["verified_role_id"]
    bot.add_view(VerificationView(role_id=verified_role_id))
    await bot.add_cog(BotSetup(bot))