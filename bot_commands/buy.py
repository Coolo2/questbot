import json, discord, random, asyncio

from resources import var,questbot
from discord_components import *

async def checkout(bot, ctx, bank=0, shards=0, questxp=0):

    if bank != 0:
        readable = f"**{bank:,d}**{var.currency}"
    elif shards != 0:
        readable = f"**{shards:,d}** shards"
    elif questxp != 0:
        readable = f"**{questxp:,d}** Quest XP"

    embed = discord.Embed(
        title="Checkout", 
        description=f"This purchase will cost {readable}. Continue?",
        color=var.embed
    )

    buttonConfirm = Button(style=ButtonStyle.green, label="Purchase", disabled=False, id="purchaseConfirm")
    buttonDeny = Button(style=ButtonStyle.red, label="Cancel", disabled=False, id="purchaseCancel")

    msg = await ctx.send(embeds=[embed], components=[buttonConfirm, buttonDeny])
    buttonConfirm.set_disabled(True)
    buttonDeny.set_disabled(True)

    try:
        async def wait_loop():
            res = await bot.wait_for("button_click", timeout= 30, check = lambda i: i.custom_id in ["purchaseConfirm", "purchaseCancel"])

            if res.user == ctx.author:
                await res.respond(type=7, components=[buttonConfirm, buttonDeny])
                if res.custom_id == "purchaseConfirm":
                    return True
                else:
                    return False
            else:
                await res.send("Nice try... You aren't the right person!")
                await wait_loop()
        final = {"msg":msg, "result":await wait_loop()}

    except asyncio.TimeoutError:
        await msg.edit(components=[buttonConfirm, buttonDeny])
        final = {"msg":msg, "result":False}
    
    return final

async def crate(bot, ctx, crateType):

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
    user.zoo.saveCreatures()
    user.economy.addBal(bank=0-crate.cost)
    
    amount = user.zoo.creatures.count(creature.name)

    embed = discord.Embed(title=f"Here's your {crate.name.title()} Crate!", description=f'**1x** {creature.emoji} {creature.readableName}\n\n{"**New creature!** " if amount == 1 else ""}You now have {amount} {creature.readableName}{"" if amount == 1 else "s"}', color=crate.color)

    embed.set_thumbnail(url=crate.icon)
    embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
    
    return await ctx.send(embeds=[embed])

async def questxp(bot, ctx, amount):
    try:
        amount = int(amount)
    except TypeError:
        return await ctx.send(f"> Quest XP amount must be an integer! `{var.prefix}buy questxp [amount]`")
    if amount < 1:
        return await ctx.send(f"> Quest XP amount must be an integer above 1! `{var.prefix}buy questxp [amount]`")

    user = questbot.User(ctx.author)
    user.economy.loadBal(ctx.guild)
    
    starsPerXP = 2.5 
    cost = round(amount * starsPerXP)

    result = await checkout(bot, ctx, bank=cost)

    if result["result"] == True:
        msg = result["msg"]

        if user.economy.bank < cost:
            embed = discord.Embed(title="Uh oh!", description=f'You do not have enough money ({cost:,d}) **in bank** for this amount of quest xp!', color=var.embedFail)
            return await msg.edit(embeds=[embed], components=[])

        user.economy.addBal(bank=0-cost)
        user.addXP(amount)

        embed = discord.Embed(
            title="Successfully purchased",
            description=f"Successfully purchased **{amount:,d}** Quest XP for **{cost:,d}**{var.currency}",
            color=var.embedSuccess
        )

        await msg.edit(embeds=[embed], components=[])

    


