import json, discord, random, asyncio
from discord.ext.commands import MemberConverter
from datetime import datetime

from resources import var, questbot
from discord_components import *

async def trade(bot, ctx, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11):
    
    zoo = questbot.Zoo()
    zoo.getTrades()

    allData = zoo.creatures
    
    converter = MemberConverter()

    if arg2 == None:
        embed = discord.Embed(title="Trade", description="""
`q!trade [user] [yourCreature] [theirCreature]` - Create a new trade to a user (select creature later) and get a tradeID

`q!trade list [inbound/outbound] *[user]` - List trades
        """, color=var.embed)
        try:
            return await ctx.send(embed=embed)
        except:
            return await ctx.send(embeds=[embed])
    
    if arg2 == "list":
        embed = discord.Embed(title="List trades", description="""
`q!trade list inbound *[user]` - List inbound trades
`q!trade list outbound *[user]` - List outbound trades
            """, color=var.embed)
        if arg3 == None:
            return await ctx.send(embed=embed)
        elif arg3 == "outbound":
            what = "from"
        elif arg3 == "inbound":
            what = "to"
        else:
            return await ctx.send(embed=embed)
        
        if arg4 == None:
            user = ctx.author
        else:
            user = await converter.convert(ctx, arg4)

        embed = discord.Embed(
            title="Trade list", 
            color=var.embed
        )
        for tradeID in zoo.trades:
            if zoo.trades[tradeID][what]["user"] == str(user.id):
                embed.add_field(
                    name=f"ID: {tradeID} - From: {bot.get_user(int(zoo.trades[tradeID]['from']['user']))} - To: {bot.get_user(int(zoo.trades[tradeID]['to']['user']))}",
                    value=
                    f"Status: `{'Sent' if 'creature' in zoo.trades[tradeID]['to'] and 'creature' in zoo.trades[tradeID]['from'] else 'Uncomplete'}`" + 
                    f" - Your creature: `{'Unchosen' if 'creature' not in zoo.trades[tradeID]['from'] else zoo.trades[tradeID]['from']['creature'].replace('_', ' ').title()}`" + 
                    f" - Their creature: `{'Unchosen' if 'creature' not in zoo.trades[tradeID]['to'] else zoo.Creature(zoo.trades[tradeID]['to']['creature']).readableName}`",
                    inline=False
                )
        
        return await ctx.send(embed=embed)

    if arg2 == None:
        return await ctx.send(content="> Please choose a user to make a trade request to! (`q!trade [user]`)")
    
    user = await converter.convert(ctx, arg2)

    author = questbot.User(ctx.author)
    otherUser = questbot.User(user)

    if user == ctx.author:
        return await ctx.send("> You can't trade with yourself!")

    yourCreatures = author.zoo.getCreatures()
    theirCreatures = otherUser.zoo.getCreatures()

    yourCreature = ""
    theirCreature = ""

    tradeID = len(zoo.trades) + 1
    
    if arg3.lower() in allData:
        yourCreature = arg3.lower()
        theirCreature = (arg4.lower()
            + ("_" + arg5.lower() if arg5 != None else "")
            + ("_" + arg6.lower() if arg6 != None else "") 
            + ("_" + arg7.lower() if arg7 != None else "")
            + ("_" + arg8.lower() if arg8 != None else "")
        )
    elif str(arg3).lower() + "_" + str(arg4).lower() in allData:
        yourCreature = arg3.lower() + "_" + arg4.lower()
        theirCreature = (arg5.lower()
            + ("_" + arg6.lower() if arg6 != None else "") 
            + ("_" + arg7.lower() if arg7 != None else "")
            + ("_" + arg8.lower() if arg8 != None else "")
            + ("_" + arg9.lower() if arg9 != None else "")
        )
    elif str(arg3).lower() + "_" + str(arg4).lower() + "_" + str(arg5).lower() in allData:
        yourCreature = arg3.lower() + "_" + arg4.lower() + "_" + arg5.lower()
        theirCreature = (arg6.lower()
            + ("_" + arg7.lower() if arg8 != None else "")
            + ("_" + arg8.lower() if arg8 != None else "")
            + ("_" + arg9.lower() if arg9 != None else "")
            + ("_" + arg10.lower() if arg10 != None else "")
        )
    elif str(arg3).lower() + "_" + str(arg4).lower() + "_" + str(arg5).lower() + "_" + str(arg6).lower() in allData:
        yourCreature = arg3.lower() + "_" + arg4.lower() + "_" + arg5.lower() + "_" + arg6.lower()
        theirCreature = (arg7.lower()
            + ("_" + arg8.lower() if arg8 != None else "")
            + ("_" + arg9.lower() if arg9 != None else "")
            + ("_" + arg10.lower() if arg10 != None else "")
            + ("_" + arg11.lower() if arg11 != None else "")
        )
    else:
        return await ctx.send("> Please input a valid creature to give.")
    
    if yourCreature not in yourCreatures:
        return await ctx.send("> Please input a valid creature to give.")
    
    if theirCreature not in allData or theirCreature not in theirCreatures:
        return await ctx.send("> Please input a valid creature to get.")
    
    if theirCreature == yourCreature:
        return await ctx.send("> You cant trade the same creature!")
    
    for trade in zoo.trades:
        if zoo.trades[trade]["from"]["user"] == str(ctx.author.id) and zoo.trades[trade]["from"]["creature"] == yourCreature:
            return await ctx.send("> You are already trading one of this creature (you cant trade the same creature twice at the same time!)")


    message = await ctx.send(f"Loading trade `#{tradeID}` {user.mention}")
    
    try:
        from_message = await ctx.author.send(
            embed=discord.Embed(
                title=f"Sent trade! (#{tradeID})",
                description=f"Created trade to `{user}`!\n{message.jump_url}",
                color=var.embedSuccess
            )
        )
    except:
        pass 
    try:
        to_message = await user.send(
            embed=discord.Embed(
                title=f"You revieved a tradee! (#{tradeID})",
                description=f"You recieved a trade from `{ctx.author}`!\n{message.jump_url}",
                color=var.embed
            )
        )
    except:
        pass

    theirCreature = zoo.Creature(theirCreature)
    yourCreature = zoo.Creature(yourCreature)

    buttonAccept = Button(style=ButtonStyle.green, label="Accept Trade", disabled=False, id=f"acceptTrade_{tradeID}")
    buttonDeny = Button(style=ButtonStyle.red, label="Deny Trade", disabled=False, id=f"denyTrade_{tradeID}")

    embed = discord.Embed(
        title=f"{ctx.author} wants to trade your {theirCreature.emoji} {theirCreature.readableName} for a {yourCreature.emoji} {yourCreature.readableName}!",
        description="Use the reactions to accept or decline. **Both users have to accept.**",
        color=var.embed
    )
    embed.set_footer(text="0/2")
    await message.edit(content=f"{user.mention}", 
        embeds=[embed],
        components=[[buttonAccept], [buttonDeny]]
    )
    
    try:
        tomsg = str(to_message.id)
    except:
        tomsg = "1"
    try:
        frommsg = str(from_message.id)
    except:
        frommsg = "1"

    zoo.addTrade(tradeID, {
            "from": {
                "user":str(ctx.author.id), 
                "creature":yourCreature.name,
                "accepted":False
            }, 
            "to":{
                "user":str(user.id), 
                "creature":theirCreature.name,
                "accepted":False
            }, 
            "data":{
                "channel":str(message.channel.id),
                "message":str(message.id),
                "to_message":tomsg,
                "from_message":frommsg,
                "started":datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
            }
        }
    )

    zoo.saveTrades()

async def outOfTime(bot, tradeID):
    pass

async def acceptTrade(bot, user, tradeID):
    
    zoo = questbot.Zoo() 
    zoo.getTrades()

    if str(tradeID) in zoo.trades:

        trade = zoo.Trade(tradeID)
        await trade.getData(bot)

        if trade.fromUser == user:
            trade.fromData.accepted = True
        elif user == trade.toUser:
            trade.toData.accepted = True
        else:
            return "You are not involved with this trade"

        embed = discord.Embed(
            title=f"{trade.fromUser} wants to trade your {zoo.Creature(trade.toData.creature).emoji} {zoo.Creature(trade.toData.creature).readableName} for a {zoo.Creature(trade.fromData.creature).emoji} {zoo.Creature(trade.fromData.creature).readableName}!",
            description="Use the reactions to accept or decline. **Both users have to accept.**",
            color=var.embed
        )

        embed.set_footer(text=("2" if trade.toData.accepted and trade.fromData.accepted else ("1" if (trade.toData.accepted or trade.fromData.accepted) else "0")) + "/2")
        await trade.message.edit(content=f"{trade.toUser.mention}", embed=embed)

        if trade.toData.accepted and trade.fromData.accepted:
            trade.toUserClass.zoo.getCreatures()
            trade.fromUserClass.zoo.getCreatures()

            trade.toUserClass.zoo.addCreature(trade.fromData.creature)
            trade.fromUserClass.zoo.addCreature(trade.toData.creature)

            trade.toUserClass.zoo.removeCreature(trade.toData.creature)
            trade.fromUserClass.zoo.removeCreature(trade.fromData.creature)

            trade.toUserClass.zoo.saveUser()
            trade.fromUserClass.zoo.saveUser()

            await trade.end("Trade Completed")
            await trade.channel.send(f'> `{trade.fromUser}` got `{trade.toUser}`\'s {zoo.Creature(trade.toData.creature).readableName} in return for a {zoo.Creature(trade.fromData.creature).readableName}')
            return "in return for a"

        trade.saveData()
        return "Your vote was added to the trade"

async def denyTrade(bot, user, tradeID):
    zoo = questbot.Zoo() 
    zoo.getTrades()

    if str(tradeID) in zoo.trades:

        trade = zoo.Trade(tradeID)
        await trade.getData(bot)

        if user != trade.fromUser and user != trade.toUser:
            return 
        
        await trade.end("Trade cancelled.")