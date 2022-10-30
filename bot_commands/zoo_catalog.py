#from bot_commands.miniquests import miniquests
import discord
from discord.ext import commands

import QuestClient as qc
from QuestClient.classes import CreatureType

async def command(client : qc.Client, ctx : commands.Context, section : str, userO : discord.User):

    if userO == None:
        userO = ctx.author

    user = qc.classes.User(client, userO)
    
    ownedUsr = user.zoo.creatures

    section = section.lower()

    creatureList = user.zoo.zoo.standard_creatures
    if section == "shiny":
        creatureList = user.zoo.zoo.shiny_creatures
    elif section == "golden":
        creatureList = user.zoo.zoo.golden_creatures

    description = ""
    for i, creature in enumerate(creatureList):
        description += creature.emoji if creature in ownedUsr else "<:__:827565769709191248>"
        if (i+1) % 12 == 0:
            description += "\n"
    
    split = description.split("\n")

    amount = 0
    for creature in set(ownedUsr):
        if creature in creatureList: amount += 1
    
    per_page = 5
    catalog_pages = ["\n".join(split[i:i+per_page]) for i in range(0, len(split), per_page)]

    embed = discord.Embed(title=f"{section.title()} catalog", description=catalog_pages[0], color=qc.var.embed)
    embed.set_footer(text=f"{amount}/{len(creatureList)} different {section} creatures collected")

    view = qc.paginator.PaginatorView(catalog_pages, embed, private=ctx.author)

    return await ctx.send(embed=embed, view=view)

