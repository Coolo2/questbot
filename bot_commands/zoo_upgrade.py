import discord

from resources import var
import QuestClient as qc

from discord.ext import commands 

shinyUpgradeCosts = [None, 150_000, 240_000, 500_000, 1_000_000]
standardUpgradeCosts = [None, 50_000, 80_000, 150_000, 300_000]

async def command(client : qc.Client, ctx : commands.Context, producer : str):
    
    user = qc.classes.User(client, ctx.author)
    
    user.zoo.getZoo()
    user.zoo.getShardProducers()
    await user.economy.loadBal(ctx.guild)

    shardProducer = producer.replace(" ", "_").lower()

    if shardProducer not in user.zoo.shardProducers:
        raise qc.errors.MildError(f"> You do not have this shard producer!")
    
    producer : qc.classes.Zoo.ShardProducer = user.zoo.zoo.ShardProducer(
        shardProducer, 
        user.zoo.shardProducers[shardProducer]["birthdate"],  
        user.zoo.shardProducers[shardProducer]["level"],  
        user.zoo.shardProducers[shardProducer]["last_refreshed"]
    )

    if producer.level >= 5:
        raise qc.errors.MildError("> This producer is already max level! GG!")
    
    cost = shinyUpgradeCosts[producer.level] if producer.rarity == "shiny" else standardUpgradeCosts[producer.level]

    if user.economy.bank < cost:
        raise qc.errors.MildError(f"> You don't have enough money! You have **{user.economy.bank:,d}**{var.currency} but need **{cost:,d}**{var.currency}.")
    
    producer.level += 1
    
    user.zoo.shardProducers[shardProducer] = producer.to_json()
    await user.economy.addBal(bank=0-cost)

    user.zoo.saveShardProducers()

    upgradedProducer = user.zoo.zoo.ShardProducer(shardProducer, producer.birthdate,  producer.level,  producer.lastRefreshed)

    embed = discord.Embed(
        title=f"Upgraded your {producer.readableName}", 
        description=f"""Your **{producer.readableName}** was upgraded to level **{producer.level}**, costing you **{cost:,d}**{var.currency}
You will now get **{upgradedProducer.shards}** {qc.var.shards_currency} every **{upgradedProducer.hoursForShard}** hours""",
        color=var.embedSuccess
    )
    embed.add_field(name="Balance", value=f"You now have **{user.economy.bank:,d}**{var.currency} in your bank")
    await ctx.send(embed=embed)
    
