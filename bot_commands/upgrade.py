import json, discord, random, asyncio
from resources import var, questbot
from datetime import datetime

shinyUpgradeCosts = [None, 20_000, 30_000, 40_000, 50_000, 60_000]
standardUpgradeCosts = [None, 10_000, 15_000, 20_000, 25_000, 30_000]

async def upgrade(bot, ctx, shardProducer):

    if shardProducer == None:
        return await ctx.send(f"> Specify a **shard producer** to upgrade! `{var.prefix}upgrade [shardProducer]`")
    
    user = questbot.User(ctx.author)
    
    user.zoo.getZoo()
    user.zoo.getShardProducers()
    user.economy.loadBal(ctx.guild)

    shardProducer = shardProducer.replace(" ", "_").lower()

    if shardProducer not in user.zoo.shardProducers:
        return await ctx.send(f"> You do not have this shard producer!")
    
    producer = user.zoo.zoo.ShardProducer(
        shardProducer, 
        user.zoo.shardProducers[shardProducer]["birthdate"],  
        user.zoo.shardProducers[shardProducer]["level"],  
        user.zoo.shardProducers[shardProducer]["last_refreshed"]
    )

    if producer.level >= 5:
        return await ctx.send("> This producer is already max level! GG!")
    
    cost = shinyUpgradeCosts[producer.level] if producer.rarity == "shiny" else standardUpgradeCosts[producer.level]

    if user.economy.bank < cost:
        return await ctx.send(f"> You don't have enough money! You have **{user.economy.bank:,d}**{var.currency} but need **{cost:,d}**{var.currency}.")
    
    producer.level += 1
    
    user.zoo.shardProducers[shardProducer] = producer.to_json()
    user.economy.addBal(bank=0-cost)

    user.zoo.saveShardProducers()

    upgradedProducer = user.zoo.zoo.ShardProducer(shardProducer, producer.birthdate,  producer.level,  producer.lastRefreshed)

    embed = discord.Embed(
        title=f"Upgraded your {producer.readableName}", 
        description=f"""Your **{producer.readableName}** was upgraded to level **{producer.level}**, costing you **{cost:,d}**{var.currency}
You will now get **{upgradedProducer.shards}** shards every **{upgradedProducer.hoursForShard}** hours""",
        color=var.embedSuccess
    )
    embed.add_field(name="Balance", value=f"You now have **{user.economy.bank:,d}**{var.currency} in your bank")
    await ctx.send(embeds=[embed])


