#from bot_commands.miniquests import miniquests
import discord
from discord.ext import commands

import QuestClient as qc
from QuestClient import classes

async def command(client : qc.Client, ctx : commands.Context, user : discord.User = None):

    if user == None:
        user = ctx.author 
    
    u = classes.User(client, user)

    embed = discord.Embed(title="Your active items:", description=f"See and buy items with `{client.var.prefix}shop items`", color=client.var.embed)

    for item in u.item.items:
        desc = item.description 
        if item.lasts:
            timestamp = round((item.active_since + item.lasts).timestamp())
            desc += f"\nExpires <t:{timestamp}:f> (<t:{timestamp}:R>)"

        embed.add_field(name=item.name, value=desc, inline=False)
    
    await ctx.send(embed=embed)
    
