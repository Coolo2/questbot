import json, discord, random, asyncio

from resources import var
import QuestClient as qc

import typing

from discord.ext import commands 
from discord import app_commands
import datetime


async def command(client : qc.Client, ctx : commands.Context, creature : str):

    user = qc.classes.User(ctx.author)
    
    user.zoo.getCreatures()
    user.zoo.getZoo()
    user.zoo.getShardProducers()

    creature = creature.replace(" ", "_").lower()

    if not user.zoo.zoo.validateCreatureExists(creature).valid:
        raise qc.errors.MildError("> This creature does not exist!")

    if user.zoo.creatures.count(creature) < 5:
        raise qc.errors.MildError(f"> You do not have 5 of this creature! You need 5 of the same creature to merge (you currently have {user.zoo.creatures.count(creature)}).")
    
    if creature in user.zoo.shardProducers:
        raise qc.errors.MildError("> You already have a shard producer of this creature!")

    user.zoo.removeCreature(creature, 5)
    user.zoo.shardProducers[creature] = {
        "birthdate":datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"), 
        "last_refreshed":datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"),
        "level":1
    }

    creatureClass = user.zoo.zoo.Creature(creature)

    embed = discord.Embed(
        title=f"Merged 5 {creatureClass.emoji} {creatureClass.readableName}s",
        description=f"[x5 | Creature {creatureClass.emoji}]   **----->**   [x1 | Shard Producer {creatureClass.emoji}]",
        color=var.embedSuccess
    )
    embed.set_footer(text=f"You now have {user.zoo.creatures.count(creature)} {creatureClass.readableName}s")

    await ctx.send(embed=embed)

    user.zoo.saveCreatures()
    user.zoo.saveShardProducers()
    
