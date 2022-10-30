import json, discord, random, asyncio

from resources import var
import QuestClient as qc

import typing

from discord.ext import commands 
from discord import app_commands
import datetime


async def command(client : qc.Client, ctx : commands.Context, creature_name : str):

    user = qc.classes.User(client, ctx.author)
    
    if not user.zoo.zoo.validateCreatureExists(creature_name).valid:
        raise qc.errors.MildError("> This creature does not exist!")

    creature = user.zoo.zoo.get_creature(creature_name)

    if user.zoo.creatures.count(creature) < 5:
        raise qc.errors.MildError(f"> You do not have 5 of this creature! You need 5 of the same creature to merge (you currently have {user.zoo.creatures.count(creature)}).")
    
    if user.zoo.get_shard_producer(creature.name):
        raise qc.errors.MildError("> You already have a shard producer of this creature!")

    user.zoo.removeCreature(creature, 5)
    user.zoo.add_shard_producer(creature)


    embed = discord.Embed(
        title=f"Merged 5 {creature.emoji} {creature.name_formatted}s",
        description=f"[x5 {creature.emoji} Creature]   **----->**   [x1 {creature.emoji} Shard Producer]",
        color=var.embedSuccess
    )
    embed.set_footer(text=f"You now have {user.zoo.creatures.count(creature)} {creature.name_formatted} creatures")

    await ctx.send(embed=embed)
    
