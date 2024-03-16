import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all(),
            status=discord.Status.online,
            activity=discord.Game("with the server")
        )

    async def setup_hook(self):
        for f in os.listdir("./cogs"):
            if f.endswith(".py"):
                await self.load_extension("cogs." + f[:-3])
        print("Successfully loaded all extensions!")
        await self.tree.sync()

    async def on_ready(self):
        print(f"{self.user} is now online!")

bot = MyBot()

bot.run(os.getenv("TOKEN"))