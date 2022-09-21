
import discord
from discord.ext import commands
import json

import QuestClient as qc


async def command(client : qc.Client, ctx : commands.Context):

    with open('data/values.json') as f:
        stats = json.load(f)

    sort = dict(sorted(stats.items(), key=lambda item: item[1]["xp"], reverse=True))

    finalString = ""
    counter = 0

    for item in sort:
        counter += 1

        if counter <= 10:

            finalString = finalString + f"\n**{counter}.** <@{item}> - {sort[item]['xp']:,d}"

    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="Full Leaderboard", style=discord.ButtonStyle.url, url=qc.var.address))
    embed = discord.Embed(title="Quest XP Leaderboard", description=finalString, color=qc.var.embed)

    await ctx.send(embed=embed, view=view)