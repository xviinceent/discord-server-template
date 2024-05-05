import discord
from discord.ext import commands
from discord import app_commands
import json
import aiosqlite
 
class Autorole(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
 
    @commands.group(name="autorole", invoke_without_command=True)
    async def autorole(self, ctx: commands.Context):
        await ctx.reply("Use `!autorole add [role]` to add an autorole and `!autorole remove [role]` to remove an autorole. These commands are only available to moderators and admins.")

    @autorole.command()
    async def add(self, ctx: commands.Context, role: discord.Role):
        with open("config.json", "r") as f:
            config = json.load(f)
            moderator_role_id = config["moderator_role_id"]
            admin_role_id = config["admin_role_id"]

        if not moderator_role_id in [role.id for role in ctx.author.roles] and not admin_role_id in [role.id for role in ctx.author.roles]:
            await ctx.reply("You are not an admin or moderator.")
            return
        
        if role.position >= ctx.me.top_role.position:
            await ctx.reply("I am not allowed to add this role.")
            return
        
        with open("autoroles.json", "r") as f:
            data = json.load(f)
            autorole_list = data["list"]
        if role.id in autorole_list:
            await ctx.reply("This role is already in the autorole list.")
            return
        autorole_list.append(role.id)
        with open("autoroles.json", "w") as f:
            json.dump(data, f)
        await ctx.reply(f"Successfully added {role.mention} to the autorole list!", allowed_mentions=discord.AllowedMentions.none())
    
    @autorole.command()
    async def remove(self, ctx: commands.Context, role: discord.Role):
        with open("config.json", "r") as f:
            config = json.load(f)
            moderator_role_id = config["moderator_role_id"]
            admin_role_id = config["admin_role_id"]

        if not moderator_role_id in [role.id for role in ctx.author.roles] and not admin_role_id in [role.id for role in ctx.author.roles]:
            await ctx.reply("You are not an admin or moderator.")
            return
        
        if role.position >= ctx.me.top_role.position:
            await ctx.reply("I am not allowed to remove this role.")
            return
        
        with open("autoroles.json", "r") as f:
            data = json.load(f)
            autorole_list = data["list"]
        if role.id not in autorole_list:
            await ctx.reply("This role is not in the autorole list.")
            return
        autorole_list.remove(role.id)
        with open("autoroles.json", "w") as f:
            json.dump(data, f)
        await ctx.reply(f"Successfully removed {role.mention} from the autorole list!", allowed_mentions=discord.AllowedMentions.none())

    
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        with open("autoroles.json", "r") as f:
            data = json.load(f)
            autorole_list = data["list"]
        for role_id in autorole_list:
            role = member.guild.get_role(role_id)
            await member.add_roles(role)
 
async def setup(bot: commands.Bot):
    await bot.add_cog(Autorole(bot))