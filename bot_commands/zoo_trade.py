#from bot_commands.miniquests import miniquests
import discord
from discord.ext import commands

import QuestClient as qc
from QuestClient import classes

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

import datetime

async def get_accept_view(client : qc.Client, zoo : qc.classes.Zoo, tradeID : int) -> discord.ui.View:

    view = discord.ui.View(timeout=None)

    class AcceptButton(discord.ui.Button):
        def __init__(self, client : qc.Client, zoo : qc.classes.Zoo, tradeID : int):
            self.client = client 
            self.zoo = zoo 
            self.trade_id = tradeID

            super().__init__(label="Accept Trade", style=discord.ButtonStyle.green, emoji="✅", custom_id=f"accept_trade_{self.trade_id}")
        
        async def callback(self, interaction : discord.Interaction):
            trade = self.zoo.Trade(self.client, self.trade_id)
            await trade.getData(self.client.bot)

            if trade.fromUser == interaction.user:
                trade.fromData.accepted = True
            elif interaction.user == trade.toUser:
                trade.toData.accepted = True
            else:
                return await interaction.response.send_message("You are not involved with this trade", ephemeral=True)
            
            msg = interaction.message

            msg.embeds[0].set_footer(text=("2" if trade.toData.accepted and trade.fromData.accepted else ("1" if (trade.toData.accepted or trade.fromData.accepted) else "0")) + "/2")
            trade.saveData()
            await interaction.response.edit_message(embed=msg.embeds[0])
            

            if trade.toData.accepted and trade.fromData.accepted:
                trade.toUserClass.zoo.creatures
                trade.fromUserClass.zoo.creatures

                trade.toUserClass.zoo.addCreature(trade.fromData.creature)
                trade.fromUserClass.zoo.addCreature(trade.toData.creature)

                trade.toUserClass.zoo.removeCreature(trade.toData.creature)
                trade.fromUserClass.zoo.removeCreature(trade.fromData.creature)

                await trade.end("Trade Completed")
                await trade.channel.send(f'> `{trade.fromUser}` got `{trade.toUser}`\'s {trade.toData.creature.name_formatted} in return for a {trade.fromData.creature.name_formatted}')

                for item in self.view.children:
                    item.disabled = True 

                await interaction.message.edit(view=self.view)
        
    class DenyButton(discord.ui.Button):
        def __init__(self, client : qc.Client, zoo : qc.classes.Zoo, tradeID : int):
            self.client = client 
            self.zoo = zoo 
            self.trade_id = tradeID

            super().__init__(label="Deny Trade", style=discord.ButtonStyle.red, emoji="❌", custom_id=f"deny_trade_{self.trade_id}")
        
        async def callback(self, interaction : discord.Interaction):
            trade = self.zoo.Trade(self.client, self.trade_id)
            await trade.getData(self.client.bot)

            if interaction.user != trade.fromUser and interaction.user != trade.toUser:
                return 
            
            await interaction.response.send_message("Trade cancelled successfully", ephemeral=True)
            
            await trade.end("Trade cancelled.")

            for item in self.view.children:
                item.disabled = True 

            await interaction.message.edit(view=self.view)
    


    view.add_item(AcceptButton(client, zoo, tradeID))
    view.add_item(DenyButton(client, zoo, tradeID))

    return view
                
                
        
        

            

async def trade(client : qc.Client, ctx : commands.Context, user : discord.User, your_creature_name : str, their_creature_name : str):

    zoo = client.zoo
    zoo.getTrades()

    author = qc.classes.User(client, ctx.author)
    otherUser = qc.classes.User(client, user)

    if user == ctx.author:
        raise qc.errors.MildError("> You can't trade with yourself!")

    your_creatures = author.zoo.creatures
    their_creatures = otherUser.zoo.creatures

    your_creature = zoo.get_creature(your_creature_name)
    their_creature = zoo.get_creature(their_creature_name)

    tradeID = len(zoo.trades) + 1
    
    
    if your_creature not in your_creatures:
        raise qc.errors.MildError("> You do not own this creature.")
    
    if their_creature not in zoo.creatures or their_creature not in their_creatures:
        raise qc.errors.MildError("> They do not own this creature.")
    
    if their_creature == your_creature:
        raise qc.errors.MildError("> You cant trade the same creature!")
    
    for trade in zoo.trades:
        if zoo.trades[trade]["from"]["user"] == str(ctx.author.id) and zoo.trades[trade]["from"]["creature"] == your_creature:
            raise qc.errors.MildError("> You are already trading one of this creature (you cant trade the same creature twice at the same time!)")


    message = await ctx.send(f"Loading trade `#{tradeID}` {user.mention}")
    
    try:
        from_message = await ctx.author.send(
            embed=discord.Embed(
                title=f"Sent trade! (#{tradeID})",
                description=f"Created trade to `{user}`!\n{message.jump_url}",
                color=qc.var.embedSuccess
            )
        )
    except:
        pass 
    try:
        to_message = await user.send(
            embed=discord.Embed(
                title=f"You revieved a trade! (#{tradeID})",
                description=f"You recieved a trade from `{ctx.author}`!\n{message.jump_url}",
                color=qc.var.embed
            )
        )
    except:
        pass

    embed = discord.Embed(
        title=f"{ctx.author} wants to trade your {their_creature.emoji} {their_creature.name_formatted} for a {your_creature.emoji} {your_creature.name_formatted}!",
        description="Use the reactions to accept or decline. **Both users have to accept.**",
        color=qc.var.embed
    )
    embed.set_footer(text="0/2")

    view = await get_accept_view(client, zoo, tradeID)

    await message.edit(
        content=f"{user.mention}", 
        embed=embed,
        view=view
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
                "creature":your_creature.name,
                "accepted":False
            }, 
            "to":{
                "user":str(user.id), 
                "creature":their_creature.name,
                "accepted":False
            }, 
            "data":{
                "channel":str(message.channel.id),
                "message":str(message.id),
                "to_message":tomsg,
                "from_message":frommsg,
                "started":datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
            }
        }
    )

    zoo.saveTrades()

async def trade_list(client : qc.Client, ctx : commands.Context, bound : str, user : discord.User):

    zoo = client.zoo
    zoo.getTrades()

    if bound == "outbound":
        what = "from"
    elif bound == "inbound":
        what = "to"
    
    if user == None:
        user = ctx.author

    embed = discord.Embed(
        title="Trade list", 
        color=qc.var.embed
    )
    for tradeID in zoo.trades:
        if zoo.trades[tradeID][what]["user"] == str(user.id):

            trade_from_user : discord.User = client.bot.get_user(int(zoo.trades[tradeID]['from']['user']))
            trade_to_user : discord.User = client.bot.get_user(int(zoo.trades[tradeID]['yo']['user']))

            embed.add_field(
                name=f"ID: {tradeID} - From: {trade_from_user} - To: {trade_to_user}",
                value=
                f"Status: `{'Sent' if 'creature' in zoo.trades[tradeID]['to'] and 'creature' in zoo.trades[tradeID]['from'] else 'Uncomplete'}`" + 
                f" - Your creature: `{'Unchosen' if 'creature' not in zoo.trades[tradeID]['from'] else zoo.trades[tradeID]['from']['creature'].replace('_', ' ').title()}`" + 
                f" - Their creature: `{'Unchosen' if 'creature' not in zoo.trades[tradeID]['to'] else zoo.get_creature(zoo.trades[tradeID]['to']['creature']).name_formatted}`",
                inline=False
            )
    
    return await ctx.send(embed=embed)

async def load_views(client : qc.Client):

    client.zoo.getTrades()

    for trade_id, trade in client.zoo.trades.items():
        view = await get_accept_view(client, client.zoo, int(trade_id))

        client.bot.add_view(view, message_id=int(trade["data"]["message"]))
