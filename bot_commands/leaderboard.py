import discord, random, aiohttp, json, os, time, datetime, asyncio, json, sys
from discord.ext import commands

from resources import var
from discord_components import *

async def leaderboard(bot, ctx):
    with open('data/values.json') as f:
        stats = json.load(f)

    sort = dict(sorted(stats.items(), key=lambda item: item[1]["xp"], reverse=True))

    finalString = ""
    counter = 0

    for item in sort:
        counter += 1

        if counter <= 10:

            finalString = finalString + f"\n**{counter}.** <@{item}> - {sort[item]['xp']:,d}"

    button = Button(style=5, label="Full Leaderboard", url=var.address)
    embed = discord.Embed(title="Quest XP Leaderboard", description=finalString, color=var.embed)

    await ctx.send(embeds=[embed], components=[button])