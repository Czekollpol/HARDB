import discord
from discord.ext import commands
import os

TOKEN = os.getenv("DISCORD_TOKEN")

STAFF_ROLE_ID = 1468284972006641755
CATEGORY_ID = 1486389862193168535

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ===================== MODAL =====================

class TicketModal(discord.ui.Modal, title="Formularz Rekrutacyjny"):

    imie = discord.ui.TextInput(label="Imię i nazwisko (IC)")
    uid = discord.ui.TextInput(label="UID")
    wiek = discord.ui.TextInput(label="Wiek OOC")
    powod = discord.ui.TextInput(
        label="Dlaczego chcesz dołączyć?",
        style=discord.TextStyle.paragraph
    )

    async def on_submit(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            ),
        }

        if STAFF_ROLE_ID:
            role = guild.get_role(STAFF_ROLE_ID)
            overwrites[role] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            )

        channel = await guild.create_text_channel(
            name=f"ticket-{user.name}",
            category=discord.Object(id=CATEGORY_ID) if CATEGORY_ID else None,
            overwrites=overwrites
        )

        embed = discord.Embed(
            title="📋 Nowe zgłoszenie",
            color=discord.Color.blue()
        )

        embed.add_field(name="Imię i nazwisko", value=self.imie, inline=False)
        embed.add_field(name="UID", value=self.uid, inline=False)
        embed.add_field(name="Wiek OOC", value=self.wiek, inline=False)
        embed.add_field(name="Powód", value=self.powod, inline=False)
        embed.set_footer(text=f"Autor: {user}")

        await channel.send(embed=embed)

        await interaction.response.send_message(
            f"✅ Ticket utworzony: {channel.mention}",
            ephemeral=True
        )


# ===================== BUTTON =====================

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Otwórz ticket",
        style=discord.ButtonStyle.green
    )
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TicketModal())


# ===================== /TICKETY =====================

@bot.tree.command(name="tickety", description="Panel ticketów")
async def tickety(interaction: discord.Interaction):

    embed = discord.Embed(
        title="🎫 System Ticketów HAZARD",
        description=(
            "Witaj w systemie ticketów HAZARD!\n\n"
            "Kliknij przycisk poniżej, aby otworzyć nowy ticket i złożyć wniosek o rangę.\n\n"
            "**Instrukcje:**\n"
            "• Wypełnij formularz\n"
            "• Podaj prawdziwe dane\n"
            "• Czekaj na odpowiedź administracji\n\n"
            "**Uwaga:** Fałszywe informacje = odrzucenie."
        ),
        color=discord.Color.green()
    )

    await interaction.response.send_message(embed=embed, view=TicketView())


# ===================== ACCEPT =====================

@bot.tree.command(name="accept", description="Akceptuj rekrutację")
async def accept(
    interaction: discord.Interaction,
    user: discord.Member,
    stanowisko: str,
    imie_nazwisko: str,
    uid: str
):

    embed = discord.Embed(
        title="✅ Rekrutacja zaakceptowana",
        color=discord.Color.green()
    )

    embed.add_field(name="Stanowisko", value=stanowisko, inline=False)
    embed.add_field(name="Imię i nazwisko", value=imie_nazwisko, inline=False)
    embed.add_field(name="UID", value=uid, inline=False)

    embed.add_field(
        name="Nick do ustawienia",
        value=f"`{stanowisko} | {imie_nazwisko} | {uid}`",
        inline=False
    )

    try:
        await user.send(embed=embed)
    except:
        await interaction.response.send_message(
            "❌ Nie mogę wysłać DM do użytkownika",
            ephemeral=True
        )
        return

    await interaction.response.send_message(
        "✅ Wysłano akceptację",
        ephemeral=True
    )


# ===================== DENY =====================

@bot.tree.command(name="deny", description="Odrzuć rekrutację")
async def deny(interaction: discord.Interaction, user: discord.Member):

    embed = discord.Embed(
        title="❌ Rekrutacja odrzucona",
        description="Możesz spróbować ponownie za 24h.",
        color=discord.Color.red()
    )

    try:
        await user.send(embed=embed)
    except:
        await interaction.response.send_message(
            "❌ Nie mogę wysłać DM do użytkownika",
            ephemeral=True
        )
        return

    await interaction.response.send_message(
        "❌ Odrzucono zgłoszenie",
        ephemeral=True
    )


# ===================== READY =====================

@bot.event
async def on_ready():
    print(f"Zalogowano jako {bot.user}")
    await bot.tree.sync()


bot.run(TOKEN)
    await bot.tree.sync()


bot.run(TOKEN)
