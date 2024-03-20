import discord
from discord.ext import commands
from discord import app_commands
import aiosqlite
import json
 
class Tempvoice(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
 
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        with open("config.json", "r") as f:
            config = json.load(f)
            try:
                tempvoice_creation_channel_id = config["tempvoice_creation_channel_id"]
                tempvoice_creation_category_id = config["tempvoice_creation_category_id"]
            except KeyError:
                return
            
        if before.channel is None and after.channel:
            tempvoice_creation_channel = member.guild.get_channel(tempvoice_creation_channel_id)
            if not tempvoice_creation_channel:
                return
            if not after.channel == tempvoice_creation_channel:
                return
            tempvoice_creation_category = member.guild.get_channel(tempvoice_creation_category_id)
            if not tempvoice_creation_category:
                return
            new_tempvoice = await tempvoice_creation_category.create_voice_channel(name=member.id)
            await member.move_to(new_tempvoice)
            conn = await aiosqlite.connect("database.db")
            cur = await conn.cursor()
            try:
                await cur.execute("INSERT INTO tempvoice (OWNERID, CHANNELID) VALUES (?, ?)", (member.id, new_tempvoice.id,))
            except:
                await cur.execute("UPDATE tempvoice SET CHANNELID = ? WHERE OWNERID = ?", (new_tempvoice.id, member.id,))
            await conn.commit()
            await cur.close()
            await conn.close()
            return
        tempvoice_creation_category = member.guild.get_channel(tempvoice_creation_category_id)
        reqs = [before.channel is not None, after.channel is None, len(before.channel.members) <= 0, before.channel.category == tempvoice_creation_category]
        if all(reqs):
            conn = await aiosqlite.connect("database.db")
            cur = await conn.cursor()
            await before.channel.delete()
            await cur.execute("DELETE FROM tempvoice WHERE OWNERID = ?", (member.id,))
            await conn.commit()
            await cur.close()
            await conn.close()
            return

async def setup(bot: commands.Bot):
    await bot.add_cog(Tempvoice(bot))