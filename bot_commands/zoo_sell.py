import json, discord, random, asyncio

from resources import var
import QuestClient as qc

import typing

from discord.ext import commands 
from discord import app_commands
import datetime


async def command(client : qc.Client, ctx : commands.Context, creature : str):

    user = qc.classes.User(client, ctx.author)
    
    user.zoo.creatures
    user.zoo.getZoo()
    
    creatureName = creature.replace(" ", "_").lower()
    
    validate = user.zoo.validateCreature(creatureName)
    if validate.valid == False:
        return await ctx.send(content=f"> {validate.message} Check your list of creatures with `{var.prefix}list`")
    
    creature : qc.classes.Zoo.Creature = user.zoo.zoo.Creature(creatureName)

    user.zoo.removeCreature(creature.name)
    user.zoo.saveCreatures()

    sellPrice = creature.sellPrice

    await user.economy.addBal(bank=sellPrice, guild=ctx.guild)

    zoo = client.get_zoo()
    zoo.getTrades()

    for trade in zoo.trades:
        t = zoo.Trade(client, trade)

        await t.getData(client.bot)

        if t.fromData.creature == creature.name and int(t.fromUser.id) == ctx.author.id and creature.name not in user.zoo.creatures:
            await t.end(f"The trade initiator sold their **{creature.name}**!")
        
        if t.toData.creature == creature.name and int(t.toUser.id) == ctx.author.id and creature.name not in user.zoo.creatures:
            await t.end(f"The trade target sold their **{creature.name}**!")

    embed = discord.Embed(title="Creature sold", description=f"A **{creature.emoji} {creature.readableName}** was sold for **{sellPrice:,d}** {var.currency}\n\nThe money was added to your bank", color=var.embed)
    await ctx.send(embed=embed)
    
