from __future__ import annotations
import typing

#from bot_commands.miniquests import miniquests
import discord
from discord.ext import commands

import QuestClient as qc
from QuestClient import classes
from QuestClient.classes import CreatureType

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

if typing.TYPE_CHECKING:
    from QuestClient.classes import Quest as QuestFr
    from QuestClient import Client as ClientFr
    from QuestClient import classes as ClassesFr


async def command(client : ClientFr, ctx : commands.Context, page : int = None, oUser : discord.Member = None, filter : str = None):

    accepted = ["golden", "shiny", "standard"]

    if page == None:
        page = 1
    
    if oUser == None:
        oUser = ctx.author
    
    user = classes.User(client, oUser)
    
    all_creatures = reversed(qc.data.creatures)

    if filter == "standard":
        all_creatures = user.zoo.zoo.standard_creatures
    elif filter == "shiny":
        all_creatures = user.zoo.zoo.shiny_creatures
    elif filter == "golden":
        all_creatures = user.zoo.zoo.golden_creatures
    else:
        filter = None

    try:
        page = int(page)
    except:
        raise qc.errors.MildError(f"> Page must be a number. `/zoo list *[{'/'.join(accepted)}] *[user] *[page]`")
    
    ownedUsr = user.zoo.creatures
    ownedUsr = list(sorted(ownedUsr, key=lambda item: ownedUsr.count(item), reverse=True))

    creaturesOld = []
    creatureCount = 0

    for creature in all_creatures:
        if creature in ownedUsr:
            creatureCount += ownedUsr.count(creature)
            creaturesOld.append(f'{creature.emoji} {ownedUsr.count(creature)}x {creature.name_formatted}\n')

    per_page = 15
    creatures = ["".join(creaturesOld[i:i+per_page]) for i in range(0, len(creaturesOld), per_page)]

    if len(creatures) == 0:
        raise qc.errors.MildError(f"> {user.user} has no creatures!")
    if page > len(creatures):
        raise qc.errors.MildError(f"Could not find page `{page}` on {user.user}'s creature list. There are only `{len(creatures)}` pages on {user.user}'s' list.")

    embed = discord.Embed(title=f"{user.user}'s {filter + ' ' if filter else ''}creature list ({creatureCount}x)", description=creatures[page-1], color=qc.var.embed)

    view = qc.paginator.PaginatorView(creatures, embed, page-1, private=ctx.author)

    await ctx.send(embed=embed, view=view)
