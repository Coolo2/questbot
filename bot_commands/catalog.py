import json, discord, random, asyncio
from discord.ext.commands import MemberConverter
from resources import var, questbot


async def catalog(bot, ctx, section = None, page = 1):

    user = questbot.User(ctx.author)
    user.zoo.getCreatures()
    user.zoo.getZoo()
    
    ownedUsr = user.zoo.creatures
    
    if section == None or section.lower() not in ["standard", "shiny"]:
        embed = discord.Embed(title="Catalog", description=f"""
        Standard creatures: `{var.prefix}catalog standard`
        Shiny creatures: `{var.prefix}catalog shiny`
        """, color=var.embed)

        return await ctx.send(embeds=[embed])

    section = section.lower()    
    data = user.zoo.zoo.creaturesRaw

    if section == "shiny":
        creatureList = data["rare"]

    else:
        data["very_common"].update(data["common"])
        creatureList = data["very_common"]
    
    if page == 2:
        pageAdd = 60
        page=2
    else:
        pageAdd = 0
        page=1

    amount = 0 

    for creature in set(ownedUsr):
        if creature in creatureList:
            amount += 1

    embed = discord.Embed(title=f"{section.title()} catalog (page {page})", description=f"""
{''.join([creatureList[creature]['emoji'] if creature in ownedUsr else "<:__:827565769709191248>" for creature in creatureList][0+pageAdd:12+pageAdd])}
{''.join([creatureList[creature]['emoji'] if creature in ownedUsr else "<:__:827565769709191248>" for creature in creatureList][12+pageAdd:24+pageAdd])}
{''.join([creatureList[creature]['emoji'] if creature in ownedUsr else "<:__:827565769709191248>" for creature in creatureList][24+pageAdd:36+pageAdd])}
{''.join([creatureList[creature]['emoji'] if creature in ownedUsr else "<:__:827565769709191248>" for creature in creatureList][36+pageAdd:48+pageAdd])}
{''.join([creatureList[creature]['emoji'] if creature in ownedUsr else "<:__:827565769709191248>" for creature in creatureList][48+pageAdd:60+pageAdd])}
{amount}/120 different {section} creatures collected
        """, color=var.embed)

    embed.set_footer(text=f"Page {page}/2  -  Use {var.prefix}catalog {section} {1 if page == 2 else 2} to move to the next page.")

    return await ctx.send(embeds=[embed])