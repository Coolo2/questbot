import json, discord, random, asyncio
from discord.ext.commands import MemberConverter
from resources import var


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

async def command_list(bot, ctx, arg1, arg2, arg3):
    converter = MemberConverter()
    ctx.bot = bot

    page = 1
    creatureType = None
    user = None

    if arg1 == None:
        user = arg1
    elif arg2 == None:
        try:
            user = await converter.convert(ctx, arg1)
        except:
            if arg1.lower() == "shiny" or arg1.lower() == "standard":
                creatureType = arg1.lower()
            else:
                page = arg1
    elif arg3 == None:
        if arg1.lower() == "shiny" or arg1.lower() == "standard":
            creatureType = arg1.lower()
            try:
                user = await converter.convert(ctx, arg2)
            except:
                page = arg2
        else:
            page = arg2
            try:
                user = await converter.convert(ctx, arg1)
            except:
                page = arg1
                user = await converter.convert(ctx, arg2)
    else:
        creatureType = arg1.lower()
        page = arg3
        try:
            user = await converter.convert(ctx, arg2)
        except:
            page = arg2
            user = await converter.convert(ctx, arg3)
    
    if not str(page).isnumeric():
        return await ctx.send(f"> Invalid argument order. `{var.prefix}list *[shiny/standard] *[user] *[page]`")

    with open("resources/zoo/creatures.json", encoding="utf8") as f:
        data = json.load(f) 
    with open("data/zoo/ownedCreatures.json") as f:
        owned = json.load(f) 
    
    if user == None:
        user = ctx.author
    
    allData = {}

    if creatureType == "standard":
        allData.update(data["common"])
        allData.update(data["very_common"])
    elif creatureType == "shiny":
        allData.update(data["rare"])
    else:
        creatureType = None
        allData.update(data["rare"])
        allData.update(data["common"])
        allData.update(data["very_common"])

    try:
        page = int(page)
    except:
        return await ctx.send(content="> Page must be a number. `q!list *[shiny/standard] *[user] *[page]`")
    
    ownedUsr = owned[str(user.id)] if str(user.id) in owned else []

    creaturesOld = []
    creatureCount = 0

    for creature in allData:
        if creature in ownedUsr:
            creatureCount += ownedUsr.count(creature)
            creaturesOld.append(f'{allData[creature]["emoji"]} {ownedUsr.count(creature)}x {creature.replace("_", " ").title()}\n')

    creatures = list(chunks(creaturesOld, 15))

    embedFail = discord.Embed(title="Uh Oh!", description=f"Could not find page `{page}` on {user}'s creature list. There are only `{len(creatures)}` pages on {user}'s' list.", color=0xFF0000)

    if len(creatures) == 0:
        return await ctx.send(f"> {user} has no creatures!")
    if page > len(creatures):
        try:
            return await ctx.send(embed=embedFail)
        except:
            return await ctx.send(embeds=[embedFail])

    embed = discord.Embed(title=f"{user}'s {creatureType + ' ' if creatureType else ''}creature list ({creatureCount}x)", description=["".join(creature_list) for creature_list in creatures][page-1], color=var.embed)

    embed.set_footer(text=f"Page {page}/{len(creatures)}" + (f"  -  Use \"q!list {creatureType + ' ' if creatureType else ''}{page+1 if page != len(creatures) else 1}{f' {user.name}' if user != ctx.author else ''}\" to see the next page." if len(creatures) != 1 else ""))

    await ctx.send(embeds=[embed])