import discord

class LoggingEmbed(discord.Embed):
    def __init__(self, responsible_user: discord.Member, action: str, description: str):
        super().__init__(title=action, description=description)

        super().add_field(name="Responsible User", value=responsible_user.mention if responsible_user else "Unknown")