
import discord
from discord.ext import commands

import QuestClient as qc
import aiohttp


async def command(client : qc.Client, ctx : commands.Context):
    user = qc.classes.User(client, ctx.author)
    
    lvl = qc.classes.getQuestXPLevel(user.getXP())

    if lvl < 5:
        raise qc.errors.MildError("Get Quest XP level 5 to use this command!")
    
    async with aiohttp.ClientSession() as session:
        async with session.get("https://complimentr.com/api") as r:
            json = await r.json()

            return await ctx.send(json["compliment"].capitalize())