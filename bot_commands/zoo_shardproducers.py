import json, discord, random, asyncio

from resources import var
import QuestClient as qc

import typing

from discord.ext import commands 
from discord import app_commands
import datetime


async def command(client : qc.Client, ctx : commands.Context, userO : discord.User, page : int):

    if page == None:
        page = 1

    if userO == None:
        userO = ctx.author
    
    user = qc.classes.User(client, userO)

    shinyProd : typing.List[qc.classes.ShardProducer] = []
    standardProd : typing.List[qc.classes.ShardProducer] = [] 
    perHour = 0

    for producer in user.zoo.shard_producers:
        if producer.rarity == "shiny":
            shinyProd.append(producer)
        else:
            standardProd.append(producer)

        perHour += producer.shards / producer.hours_for_shard    

    shinyProd = list(sorted(shinyProd, key=lambda item: item.level, reverse=True))
    standardProd = list(sorted(standardProd, key=lambda item: item.level, reverse=True))
    shardProducers : typing.List[qc.classes.ShardProducer] = shinyProd + standardProd
    
    perHour = round(perHour, 2)
    if len(shardProducers) == 0:
        return await ctx.send(f"> `{user.user}` has no shard producers.")
    
    if page > len(shardProducers):
        return await ctx.send(f"> That page doesn't exist! `{user.user}`'s shard producer collection has **{len(shardProducers)}** pages.")
    
    description_full = ""

    for producer in shardProducers:
        description_full += f"""
{producer.emoji} **{producer.name_formatted}** (Age: {(datetime.datetime.now() - producer.birthdate).days} days)
{'👑 ' if producer.level == 5 else ''}Level {producer.level} - {producer.shards} {qc.var.shards_currency} every {producer.hours_for_shard} hours
_ _"""

    description_split = description_full.split("\n")
    per_page = 12
    shard_producers_pages = ["\n".join(description_split[i:i+per_page]) for i in range(0, len(description_split), per_page)]

    embed = discord.Embed(title=f"{user.user}'s Shard Producers ({perHour}/h)", description=shard_producers_pages[page-1], color=var.embed)

    view = qc.paginator.PaginatorView(shard_producers_pages, embed, private=ctx.author)

    await ctx.send(embed=embed, view=view)
    
