#from bot_commands.miniquests import miniquests
import discord
from discord.ext import commands

import QuestClient as qc
from QuestClient import classes

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


async def command(client : qc.Client, ctx : commands.Context, page : int = None, oUser : discord.Member = None, filter : str = None):

    accepted = ["golden", "shiny", "standard"]

    if page == None:
        page = 1
    
    if oUser == None:
        oUser = ctx.author
    
    user = classes.User(oUser)
    user.zoo.creatures
    user.zoo.getZoo()
    
    allData = {}

    if filter == "standard":
        allData.update(user.zoo.zoo.creaturesRaw["common"])
        allData.update(user.zoo.zoo.creaturesRaw["very_common"])
    elif filter == "shiny":
        allData.update(user.zoo.zoo.creaturesRaw["rare"])
    elif filter == "golden":
        allData.update(user.zoo.zoo.creaturesRaw["golden"])
    else:
        filter = None
        allData.update(user.zoo.zoo.creaturesRaw["golden"])
        allData.update(user.zoo.zoo.creaturesRaw["rare"])
        allData.update(user.zoo.zoo.creaturesRaw["common"])
        allData.update(user.zoo.zoo.creaturesRaw["very_common"])

    try:
        page = int(page)
    except:
        raise qc.errors.MildError(f"> Page must be a number. `{client.var.prefix}list *[{'/'.join(accepted)}] *[user] *[page]`")
    
    ownedUsr = user.zoo.creatures

    ownedUsr = list(sorted(ownedUsr, key=lambda item: ownedUsr.count(item), reverse=True))

    creaturesOld = []
    creatureCount = 0

    for creature in allData:
        if creature in ownedUsr:
            creatureCount += ownedUsr.count(creature)
            creaturesOld.append(f'{allData[creature]["emoji"]} {ownedUsr.count(creature)}x {creature.replace("_", " ").title()}\n')

    per_page = 15
    creatures = ["".join(creaturesOld[i:i+per_page]) for i in range(0, len(creaturesOld), per_page)]

    if len(creatures) == 0:
        raise qc.errors.MildError(f"> {user.user} has no creatures!")
    if page > len(creatures):
        raise qc.errors.MildError(f"Could not find page `{page}` on {user.user}'s creature list. There are only `{len(creatures)}` pages on {user.user}'s' list.")

    embed = discord.Embed(title=f"{user.user}'s {filter + ' ' if filter else ''}creature list ({creatureCount}x)", description=creatures[page-1], color=qc.var.embed)

    view = qc.paginator.PaginatorView(creatures, embed, page-1)

    await ctx.send(embed=embed, view=view)
