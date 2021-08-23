import json, discord, random, asyncio

from resources import var, UB

async def buy(bot, ctx, crateType):
    with open("resources/zoo/creatures.json", encoding="utf8") as f:
        data = json.load(f) 
    with open("data/zoo/ownedCreatures.json") as f:
        owned = json.load(f) 

    if crateType == None:
        embed = discord.Embed(title="Crate shop", color=var.embed)

        embed.add_field(
            name="<:Creature_Crate:822858246666584094>  Creature Crate - q!buy creature", value=f"5% chance of a shiny creature. Get 1 random creature. **(1,000{var.currency})**", 
            inline=False)
        
        embed.add_field(
            name="<:Shiny_Creature_Crate:822858260709244929>  Shiny Creature Crate - q!buy shiny", value=f"75% chance of a shiny creature. Get 1 random creature. **(10,000{var.currency})**", 
            inline=False)
        
        embed.add_field(
            name="<:Collectors_Creature_Crate:822858278219546634>  Collectors Creature Crate - q!buy collectors", value=f"75% chance of a creature that you do not have. **(25,000{var.currency})**", 
            inline=False)

        return await ctx.send(embeds=[embed])


    if crateType == "creature":
        cost = 1000

        is_shiny = True if random.randint(1, 100) <= 20 else False
        is_common = True if random.randint(1, 3) == 2 else False 
        
        if is_shiny is True:
            choice = random.choice(list(data["rare"]))
            key = "rare"
        else:
            if is_common is True:
                choice = random.choice(list(data["common"]))
                key = "common"
            else:
                choice = random.choice(list(data["very_common"]))
                key = "very_common"
    
    if crateType == "shiny":
        cost = 10_000

        is_shiny = True if random.randint(1, 100) <= 75 else False
        is_common = True if random.randint(1, 3) == 2 else False 
        
        if is_shiny is True:
            choice = random.choice(list(data["rare"]))
            key = "rare"
        else:
            if is_common is True:
                choice = random.choice(list(data["common"]))
                key = "common"
            else:
                choice = random.choice(list(data["very_common"]))
                key = "very_common"

    if crateType == "collectors":
        cost = 25_000

        is_shiny = True if random.randint(1, 100) <= 75 else False
        is_common = True if random.randint(1, 3) == 2 else False 
        
        if is_shiny is True:
            choice = random.choice(list(data["rare"]))
            key = "rare"
        else:
            if is_common is True:
                choice = random.choice(list(data["common"]))
                key = "common"
            else:
                choice = random.choice(list(data["very_common"]))
                key = "very_common"
        
        if random.randint(1, 100) <= 75:

            if str(ctx.author.id) in owned:
                while choice in owned[str(ctx.author.id)]:
                    is_shiny = True if random.randint(1, 2) == 2 else False
                    is_common = True if random.randint(1, 3) == 2 else False 
                    
                    if is_shiny is True:
                        choice = random.choice(list(data["rare"]))
                        key = "rare"
                    else:
                        if is_common is True:
                            choice = random.choice(list(data["common"]))
                            key = "common"
                        else:
                            choice = random.choice(list(data["very_common"]))
                            key = "very_common"

    economyUser = UB.EconomyUser(ctx.guild, ctx.author)
    economyUser.loadBal()

    bal = economyUser.bank

    if bal < cost:
        embed = discord.Embed(title="Uh oh!", description=f'You do not have enough money ({cost:,d}) **in bank** for this crate!', color=0xFF0000)
        
        return await ctx.send(embeds=[embed])

    economyUser.addBal(bank=0-cost)
    
    if str(ctx.author.id) not in owned:
        owned[str(ctx.author.id)] = []
    owned[str(ctx.author.id)].append(choice)

    
    with open("data/zoo/ownedCreatures.json", "w") as f:
        json.dump(owned, f, indent=4) 
    
    amount = owned[str(ctx.author.id)].count(choice)

    embed = discord.Embed(title="Here's your Creature Crate!", description=f'**1x** {data[key][choice]["emoji"]} {choice.replace("_", " ").title()}\n\n{"**New creature!** " if amount == 1 else ""}You now have {amount} {choice.replace("_", " ").title()}{"" if amount == 1 else "s"}', color=0x808080)

    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/821774449459855423/822857982672240730/Creature_Crate.png")
    embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
    
    return await ctx.send(embeds=[embed])