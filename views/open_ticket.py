import discord
import aiosqlite
import json
from components.embeds import LoggingEmbed

class OpenTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.green, custom_id="button:open_ticket", emoji="📩")
    async def open_ticket_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(thinking=True, ephemeral=True)
        conn = await aiosqlite.connect("database.db")
        cur = await conn.cursor()
        await cur.execute("SELECT CHANNELID FROM tickets WHERE USERID = ?", (interaction.user.id,))
        result = await cur.fetchone()
        if result:
            await cur.close()
            await conn.close()
            await interaction.followup.send(f"❌ You cannot create a new ticket since there already is an open one with the channel ID `{result[0]}`.", ephemeral=True)
            return
        with open("config.json", 'r') as f:
            config = json.load(f)
            try:
                ticket_category_id = config["ticket_category_id"]
                ticket_logging_channel_id = config["ticket_logging_channel_id"]
                moderator_role_id = config["moderator_role_id"]
                admin_role_id = config["admin_role_id"]
            except KeyError:
                await cur.close()
                await conn.close()
                await interaction.followup.send(f"❌ Please check if all required config values are set. Please contact an admin.", ephemeral=True)
                return

        ticket_category = interaction.guild.get_channel(ticket_category_id)
        if not ticket_category:
            await cur.close()
            await conn.close()
            await interaction.followup.send(f"❌ The ticket category does not exist. Please contact an admin.", ephemeral=True)
            return
        
        ticket_logging_channel = interaction.guild.get_channel(ticket_logging_channel_id)
        if not ticket_logging_channel:
            await cur.close()
            await conn.close()
            await interaction.followup.send(f"❌ The ticket logging channel does not exist. Please contact an admin.", ephemeral=True)
            return

        mod_role = interaction.guild.get_role(moderator_role_id)
        if not mod_role:
            await cur.close()
            await conn.close()
            await interaction.followup.send(f"❌ The moderator role does not exist. Please contact an admin.", ephemeral=True)
            return
        admin_role = interaction.guild.get_role(admin_role_id)
        if not admin_role:
            await cur.close()
            await conn.close()
            await interaction.followup.send(f"❌ The admin role does not exist. Please contact the server owner.", ephemeral=True)
            return
        ticket_channel = await ticket_category.create_text_channel(name=f"ticket-{interaction.user.id}", overwrites={interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False), interaction.user: discord.PermissionOverwrite(view_channel=True), mod_role: discord.PermissionOverwrite(view_channel=True), admin_role: discord.PermissionOverwrite(view_channel=True)})
        await ticket_channel.send("This is the start of your ticket, please describe your issue. The ticket can be closed by using the </close:1219372148263620701> command.")
        embed = LoggingEmbed(responsible_user=interaction.user, action="Ticket opened", description=f"Ticket created in {ticket_channel.mention}.")
        await ticket_logging_channel.send(embed=embed)
        await cur.execute("INSERT INTO tickets (USERID, CHANNELID) VALUES (?, ?)", (interaction.user.id, ticket_channel.id,))
        await conn.commit()
        await cur.close()
        await conn.close()
        await interaction.followup.send(f"✅ Ticket created: {ticket_channel.mention}.", ephemeral=True)