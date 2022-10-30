import json, discord, random, asyncio

from resources import var
import QuestClient as qc

import typing

from discord.ext import commands 
from discord import app_commands
import datetime

def is_emoji(s):
    emojis = "😘◼️" # add more emojis here
    count = 0
    for emoji in emojis:
        count += s.count(emoji)
        if count > 1:
            return False
    return bool(count)

async def command(client : qc.Client, ctx : commands.Context, creature_name : str):

    user = qc.classes.User(client, ctx.author)
    
    creature = user.zoo.zoo.get_creature(creature_name)
    
    validate = user.zoo.has_creature((creature.name if creature else None) or creature_name)
    if validate.valid == False:
        return await ctx.send(content=f"> {validate.message} Check your list of creatures with `/zoo list`")
    
    url = None
    
    if len(creature.emoji) == 1:
        un = '{:X}'.format(ord(creature.emoji)).lower()
        url = f"https://twemoji.maxcdn.com/v/14.0.2/72x72/{un}.png"
    else:
        url = client.bot.get_emoji(int(creature.emoji.split(":")[2].split(">")[0])).url
    
    embed = discord.Embed(title=f"Your {creature.name_formatted} ({creature.category})", color=var.embed)
    
    embed.set_image(url=url)
    await ctx.send(embed=embed)
    
