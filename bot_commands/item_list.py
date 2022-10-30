
import discord
from discord.ext import commands

import QuestClient as qc
from QuestClient import classes

import typing

async def command(client : qc.Client, ctx : commands.Context, user : discord.User = None):

    if user == None:
        user = ctx.author 
    
    u = classes.User(client, user)

    embed = discord.Embed(title="Your active items:", description=f"See and buy items with `/shop items`", color=client.var.embed)

    item_names : typing.List[str] = [i.name for i in u.item.items]
    active_items : typing.List[str] = [i.name for i in u.item.items if i.active]
    passed = []

    for item in u.item.items:
        if item.name in passed:
            continue
        passed.append(item.name)

        desc = item.description 
        item_count = item_names.count(item.name)
        active = item.name in active_items

        if item.lasts and active:
            timestamp = round((item.active + item.lasts).timestamp())
            desc += f"\nExpires <t:{timestamp}:f> (<t:{timestamp}:R>)"
        
        active_str = ""
        if active:
            active_str = f"1x Active : "
        active_str += f"{item_count - (1 if active else 0)}x Inactive"

        embed.add_field(name=f"{item.name} ({active_str})", value=desc, inline=False)
    
    await ctx.send(embed=embed)
    