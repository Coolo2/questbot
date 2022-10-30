
import discord
from discord.ext import commands

import QuestClient as qc
from QuestClient import classes

async def command(client : qc.Client, ctx : commands.Context, item : str):
    
    u = classes.User(client, ctx.author)
    shop = qc.classes.Shop()

    if not u.item.has_item(name=item):
        raise qc.errors.MildError("You do not have one of these creatures. Buy one at the **/shop item** shop")
    
    if u.item.has_item(name=item, active=True):
        raise qc.errors.MildError("You already have one of these items active. See when it runs out with **/item list**")
    
    item : classes.Shop.Item = shop.items[item]

    u.item.activate_item(item)

    return await ctx.send(embed=discord.Embed(color=qc.var.embedSuccess, title="Activated item!", description=f"Successfully activated a **{item.name}**!\n\n{item.name}: {item.description}"))
    