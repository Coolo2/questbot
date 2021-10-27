import json, discord, random, asyncio

from resources import var, UB, questbot

async def buy(bot, ctx, crateType):

    user = questbot.User(ctx.author)
    user.zoo.getCreatures()
    user.zoo.getZoo()

    if crateType == None:
        embed = discord.Embed(title="Crate shop", color=var.embed)

        for crate in [user.zoo.zoo.crates.creature, user.zoo.zoo.crates.shiny, user.zoo.zoo.crates.collectors]:

            embed.add_field(
                name=f"{crate.emoji}  {crate.readableName} - {var.prefix}buy {crate.name}", value=f"{crate.description}. **({crate.price:,d}{var.currency})**", inline=False)

        return await ctx.send(embeds=[embed])


    if crateType == "creature":
        crate = user.zoo.zoo.crates.creature  
        creature = crate.getCreature()
    if crateType == "shiny":
        crate = user.zoo.zoo.crates.shiny
        creature = crate.getCreature()
    
    if crateType == "collectors":
        crate = user.zoo.zoo.crates.collectors
        creature = crate.getCreature()
        
        if crate.calculatePerc(75):

            if str(ctx.author.id) in user.zoo.creatures:
                while creature.name in user.zoo.creatures[str(ctx.author.id)]:
                    creature = crate.getCreature()

    user.economy.loadBal(ctx.guild)

    if user.economy.bank < crate.cost:
        embed = discord.Embed(title="Uh oh!", description=f'You do not have enough money ({crate.cost:,d}) **in bank** for this crate!', color=var.embedFail)
        return await ctx.send(embeds=[embed])

    user.zoo.addCreature(creature.name)
    user.zoo.saveUser()
    user.economy.addBal(bank=0-crate.cost)
    
    amount = user.zoo.creatures.count(creature.name)

    embed = discord.Embed(title=f"Here's your {crate.name.title()} Crate!", description=f'**1x** {creature.emoji} {creature.readableName}\n\n{"**New creature!** " if amount == 1 else ""}You now have {amount} {creature.readableName}{"" if amount == 1 else "s"}', color=crate.color)

    embed.set_thumbnail(url=crate.icon)
    embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
    
    return await ctx.send(embeds=[embed])