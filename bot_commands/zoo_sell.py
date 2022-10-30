import json, discord, random, asyncio

from resources import var
import QuestClient as qc

import typing

from discord.ext import commands 
from discord import app_commands
import datetime


async def command(client : qc.Client, ctx : commands.Context, creature_name : str):

    user = qc.classes.User(client, ctx.author)
    
    creature = user.zoo.zoo.get_creature(creature_name)
    
    validate = user.zoo.has_creature((creature.name if creature else None) or creature_name)
    if validate.valid == False:
        return await ctx.send(content=f"> {validate.message} Check your list of creatures with `/zoo list`")

    user.zoo.removeCreature(creature)

    await user.economy.addBal(bank=creature.sell_price, guild=ctx.guild)

    client.zoo.getTrades()

    for trade in client.zoo.trades:
        t = client.zoo.Trade(client, trade)

        await t.getData(client.bot)

        if t.fromData.creature == creature and int(t.fromUser.id) == ctx.author.id and creature not in user.zoo.creatures:
            await t.end(f"The trade initiator sold their **{creature.name_formatted}**!")
        
        if t.toData.creature == creature.name and int(t.toUser.id) == ctx.author.id and creature not in user.zoo.creatures:
            await t.end(f"The trade target sold their **{creature.name_formatted}**!")

    embed = discord.Embed(title="Creature sold", description=f"A **{creature.emoji} {creature.name_formatted}** was sold for **{creature.sell_price:,d}** {var.currency}\n\nThe money was added to your bank", color=var.embed)
    await ctx.send(embed=embed)
    
