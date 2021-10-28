import json, discord, random, asyncio

from resources import var,questbot

from bot_commands import buy

def getShopEmbed():
    zoo = questbot.Zoo()
    shop = questbot.Shop()

    shopEmbed = discord.Embed(
        title="Today's shop",
        color=var.embed
    )

    crates = ""
    for crate in [zoo.crates.creature, zoo.crates.shiny, zoo.crates.collectors]:
        crates += f"{crate.emoji}    **{crate.readableName}** ({crate.price:,d}{var.currency})\n{crate.description}.\n\n"

    shopEmbed.add_field(name=f"Creature Crates - {var.prefix}buy crate [crateName]", value=crates, inline=False)
    shopEmbed.add_field(name=f"Quest XP - {var.prefix}buy questxp [amount]", value=f"Conversion rate: **1** Quest XP for **{round(shop.getConversionRate(), 3)}**{var.currency}")

    return shopEmbed


async def shop(bot, ctx, category, item):

    
    

    if category == None or item == None:
        return await ctx.send(embed=getShopEmbed())
    
    if category.lower() == "crate":
        return await buy.crate(bot, ctx, item)
    if category.lower() in ["xp", "questxp"]:
        return await buy.questxp(bot, ctx, item)
