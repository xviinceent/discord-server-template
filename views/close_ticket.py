import discord
import aiosqlite
import json
import asyncio
from components.embeds import LoggingEmbed

class CloseTicketView(discord.ui.View):
    
    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.green, custom_id="button:close_ticket", emoji="❌")
    async def close_ticket_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(thinking=True, ephemeral=True)
        conn = await aiosqlite.connect("database.db")
        cur = await conn.cursor()
        await cur.execute("SELECT USERID FROM tickets WHERE CHANNELID = ?", (interaction.channel.id,))
        result = await cur.fetchone()
        if not result:
            await cur.close()
            await conn.close()
            await interaction.followup.send("❌ This is not a ticket channel.", ephemeral=True)
            return
        
        with open("config.json", 'r') as f:
            config = json.load(f)
            try:
                mod_role_id = config["moderator_role_id"]
                admin_role_id = config["admin_role_id"]
                ticket_logging_channel_id = config["ticket_logging_channel_id"]
            except KeyError:
                await cur.close()
                await conn.close()
                await interaction.followup.send("❌ Please check if all required config values are set. Please contact an admin.", ephemeral=True)
                return
        
        ticket_user = interaction.guild.get_member(result[0])
        mod_role = interaction.guild.get_role(mod_role_id)
        admin_role = interaction.guild.get_role(admin_role_id)
        ticket_logging_channel = interaction.guild.get_channel(ticket_logging_channel_id)
        checks = [mod_role in interaction.user.roles, admin_role in interaction.user.roles, interaction.user == interaction.guild.owner]

        if not any(checks) and result[0] != interaction.user.id:
            await cur.close()
            await conn.close()
            await interaction.followup.send("❌ You do not have permission to close this ticket.", ephemeral=True)
            return
        
        await cur.execute("DELETE FROM tickets WHERE CHANNELID = ?", (interaction.channel.id,))
        await conn.commit()
        await cur.close()
        await conn.close()
        embed = LoggingEmbed(responsible_user=interaction.user, action="Ticket closed", description=f"Ticket by user {ticket_user.mention} has been closed.")
        await ticket_logging_channel.send(embed=embed)
        await interaction.followup.send("✅ Ticket closed successfully. Channel will be deleted in 3 seconds.", ephemeral=True)
        await asyncio.sleep(3)
        await interaction.channel.delete()