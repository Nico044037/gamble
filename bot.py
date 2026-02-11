import discord
from discord.ext import commands
import asyncio
import random
import os

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

player_numbers = {}
coins = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

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

@bot.command()
async def balance(ctx):
    bal = coins.get(ctx.author.id, 0)
    await ctx.send(f"💰 You have {bal} coins.")

bot.run(os.getenv("TOKEN"))
