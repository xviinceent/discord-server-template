import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import aiosqlite
import datetime
import time

start_time = time.time()
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

        conn = await aiosqlite.connect("database.db")
        cur = await conn.cursor()
        await cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tickets (
                USERID INTEGER PRIMARY KEY,
                CHANNELID INTEGER
            )"""
        )
        await cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tempvoice (
                OWNERID INTEGER PRIMARY KEY,
                CHANNELID INTEGER
            )"""
        )
        await conn.commit()
        await cur.close()
        await conn.close()

        await self.tree.sync()

    async def on_ready(self):
        print(f"{self.user} is now online!")

bot = MyBot()

@bot.command()
async def hello(ctx: commands.Context):
    await ctx.reply("Hello, world!")

@bot.command()
async def ping(ctx: commands.Context):
    await ctx.reply(f"🎾 Pong! API Latency: {round(bot.latency * 1000)}ms")

@bot.command()
async def uptime(ctx: commands.Context):
    uptime = str(datetime.timedelta(seconds=int(round(time.time()-start_time))))
    await ctx.reply(f"Uptime: {uptime}")

bot.run(os.getenv("TOKEN"))
