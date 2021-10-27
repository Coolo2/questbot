import json, discord, random, asyncio

from discord.ext.commands.errors import MemberNotFound
from resources import var, questbot
from discord.ext.commands import MemberConverter
from datetime import datetime

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

async def shardproducers(bot, ctx, arg1, arg2):

    converter = MemberConverter()
    user = None

    try:
        user = await converter.convert(ctx, arg1)
        if arg2 != None and arg2.isdigit():
            page = int(arg2)
        else:
            page = 1
    except:
        try:
            user = await converter.convert(ctx, arg2)
        except:
            pass 
        if arg1 and arg1.isdigit():
            page = int(arg1)
        else:
            page = 1

    if user == None:
        user = ctx.author
    
    user = questbot.User(user)
    
    user.zoo.refreshProducers()

    shardProducers = [] 
    shinyProd = []
    standardProd = [] 
    perHour = 0

    for shardProducerName in user.zoo.shardProducers:
        producer = user.zoo.zoo.ShardProducer(shardProducerName, 
                user.zoo.shardProducers[shardProducerName]["birthdate"],
                user.zoo.shardProducers[shardProducerName]["level"],
                user.zoo.shardProducers[shardProducerName]["last_refreshed"]
            )
        if producer.rarity == "shiny":
            shinyProd.append(producer)
        else:
            standardProd.append(producer)

        perHour += producer.shards / producer.hoursForShard    

    shinyProd = list(sorted(shinyProd, key=lambda item: item.level, reverse=True))
    standardProd = list(sorted(standardProd, key=lambda item: item.level, reverse=True))
    shardProducers = shinyProd + standardProd
    
    perHour = round(perHour, 2)
    shardProducers = list(chunks(shardProducers, 5))

    if len(shardProducers) == 0:
        return await ctx.send(f"> `{user.user}` has no shard producers.")
    
    if page > len(shardProducers):
        return await ctx.send(f"> That page doesn't exist! `{user.user}`'s shard producer collection has **{len(shardProducers)}** pages.")
    
    result = ""

    for producer in shardProducers[page-1]:
        result += f"""
[{producer.rarity.title()}] {producer.emoji} **{producer.readableName}** (Age: {(datetime.now() - producer.birthdate).days} days)
**Level {producer.level}** - {producer.shards} shard{'' if producer.shards == 1 else 's'} every {producer.hoursForShard} hours
_ _"""

    embed = discord.Embed(title=f"{user.user}'s Shard Producers ({perHour}/h)", description=result, color=var.embed)
    embed.set_footer(
        text=
        f"Page {page}/{len(shardProducers)}" + (f" - Use \"{var.prefix}shardproducers {page+1}{' '+user.user.name if user.user != ctx.author else ''}\" to see the next page" if page != len(shardProducers) else ""))

    await ctx.send(embeds=[embed])

