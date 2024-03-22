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
        
        if before.channel is None or not None and after.channel:
            tempvoice_creation_channel = member.guild.get_channel(tempvoice_creation_channel_id)
            if not tempvoice_creation_channel:
                return
            if not after.channel == tempvoice_creation_channel:
                tempvoice_creation_category = member.guild.get_channel(tempvoice_creation_category_id)
                conn = await aiosqlite.connect("database.db")
                cur = await conn.cursor()
                await cur.execute("SELECT CHANNELID FROM tempvoice")
                result = await cur.fetchall()
                all_channels: list[int] = [row[0] for row in result]
                await cur.close()
                await conn.close()
                reqs = [before.channel is not None, len(before.channel.members) <= 0, before.channel.category == tempvoice_creation_category, before.channel.id in all_channels]
                if all(reqs):
                    if after.channel == tempvoice_creation_channel:
                        conn = await aiosqlite.connect("database.db")
                        cur = await conn.cursor()
                        await before.channel.delete()
                        await cur.execute("DELETE FROM tempvoice")
                        await conn.commit()
                        await cur.close()
                        await conn.close()
                        return
                    conn = await aiosqlite.connect("database.db")
                    cur = await conn.cursor()
                    await before.channel.delete()
                    await cur.execute("DELETE FROM tempvoice")
                    await conn.commit()
                    await cur.close()
                    await conn.close()
                    return
                return
            tempvoice_creation_category = member.guild.get_channel(tempvoice_creation_category_id)
            if not tempvoice_creation_category:
                return
            conn = await aiosqlite.connect("database.db")
            cur = await conn.cursor()
            await cur.execute("SELECT CHANNELID FROM tempvoice")
            result = await cur.fetchall()
            if result:
                all_channels = [row[0] for row in result]
                if before.channel.id in all_channels:
                    await before.channel.delete()
            await cur.close()
            await conn.close()
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
        conn = await aiosqlite.connect("database.db")
        cur = await conn.cursor()
        await cur.execute("SELECT CHANNELID FROM tempvoice")
        result = await cur.fetchall()
        all_channels: list[int] = [row[0] for row in result]
        await cur.close()
        await conn.close()
        reqs = [before.channel is not None, len(before.channel.members) <= 0, before.channel.category == tempvoice_creation_category, before.channel.id in all_channels]
        if all(reqs):
            conn = await aiosqlite.connect("database.db")
            cur = await conn.cursor()
            await before.channel.delete()
            await cur.execute("DELETE FROM tempvoice")
            await conn.commit()
            await cur.close()
            await conn.close()
            return

    @app_commands.command(name="change-name", description="Change the name of your tempvoice channel")
    async def change_name(self, interaction: discord.Interaction, name: str):
        await interaction.response.send_message("this command will change your voice channels name, once implemented")
    
    @app_commands.command(name="max-users", description="Change max users in your tempvoice category")
    async def max_users(self, interaction: discord.Interaction, max_users: int):
        await interaction.response.send_message("this command will change the max users in your tempvoice category, once implemented")

async def setup(bot: commands.Bot):
    await bot.add_cog(Tempvoice(bot))