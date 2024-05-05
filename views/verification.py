import discord

class VerificationView(discord.ui.View):
    def __init__(self, role_id: int = None):
        super().__init__(timeout=None)
        self.verified_role_id = role_id 

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.green, custom_id="button:verify", emoji="✅")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.verified_role_id is None:
            await interaction.response.send_message("Failed to verify. Please contact an admin.", ephemeral=True)
            return
        role = interaction.guild.get_role(self.verified_role_id)
        if not role:
            await interaction.response.send_message(f"Failed to verify. Please check if the role with the ID `{self.verified_role_id}` exists or contact an admin.", ephemeral=True)
            return
        if role in interaction.user.roles:
            await interaction.response.send_message("You are already verified.", ephemeral=True)
            return
        await interaction.user.add_roles(role)
        await interaction.response.send_message("You are now verified!", ephemeral=True)