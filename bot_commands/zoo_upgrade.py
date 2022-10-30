import discord

from resources import var
import QuestClient as qc

from discord.ext import commands 

shinyUpgradeCosts = [None, 150_000, 240_000, 500_000, 1_000_000]
standardUpgradeCosts = [None, 50_000, 80_000, 150_000, 300_000]

async def command(client : qc.Client, ctx : commands.Context, producer_name : str):
    
    user = qc.classes.User(client, ctx.author)
    
    await user.economy.loadBal(ctx.guild)

    producer = user.zoo.get_shard_producer(producer_name)

    if not producer:
        raise qc.errors.MildError(f"> You do not have this shard producer!")

    if producer.level >= 5:
        raise qc.errors.MildError("> This producer is already max level! GG!")
    
    cost = shinyUpgradeCosts[producer.level] if producer.rarity == "shiny" else standardUpgradeCosts[producer.level]

    if user.economy.bank < cost:
        raise qc.errors.MildError(f"> You don't have enough money! You have **{user.economy.bank:,d}**{var.currency} but need **{cost:,d}**{var.currency}.")
    
    producer.level += 1
    
    user.zoo.update_shard_producer(producer)
    await user.economy.addBal(bank=0-cost)

    embed = discord.Embed(
        title=f"Upgraded your {producer.name_formatted}", 
        description=f"""Your **{producer.name_formatted}** was upgraded to level **{producer.level}**, costing you **{cost:,d}**{var.currency}
You will now get **{producer.shards}** {qc.var.shards_currency} every **{producer.hours_for_shard}** hours from this creature""",
        color=var.embedSuccess
    )
    embed.add_field(name="Balance", value=f"You now have **{user.economy.bank:,d}**{var.currency} in your bank")
    await ctx.send(embed=embed)
    
