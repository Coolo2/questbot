import json, discord, random, asyncio

from resources import var, questbot

async def sell(bot, ctx, creature):
    
    user = questbot.User(ctx.author)
    
    user.zoo.getCreatures()
    user.zoo.getZoo()

    embedNone = discord.Embed(title="Sell a creature", color=var.embed)
    embedNone.add_field(name="Sell Prices", value=f"""
Shiny Creatures: **1,000** - **3,000** {var.currency}
Standard Creatures: **100** - **300** {var.currency}""")
    embedNone.add_field(name="Usage", value=f"{var.prefix}sell [creature name]", inline=False)

    if creature == None:
        return await ctx.send(embeds=[embedNone])
    
    creatureName = creature.replace(" ", "_").lower()
    
    validate = user.zoo.validateCreature(creatureName)
    if validate.valid == False:
        return await ctx.send(content=f"> {validate.message} Check your list of creatures with `q!list`")
    
    creature = user.zoo.zoo.Creature(creatureName)

    user.zoo.removeCreature(creature.name)
    user.zoo.saveUser()

    sellPrice = creature.sellPrice

    user.economy.addBal(bank=sellPrice, guild=ctx.guild)

    embed = discord.Embed(title="Creature sold", description=f"A **{creature.emoji} {creature.readableName}** was sold for **{sellPrice:,d}** {var.currency}\n\nThe money was added to your bank", color=var.embed)
    await ctx.send(embeds=[embed])