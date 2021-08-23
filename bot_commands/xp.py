import discord, random, aiohttp, json, os, time, datetime, asyncio, json, sys
from discord.ext import commands

from resources import var, globalFunctions

async def xp(bot, ctx, user):

    if user == None:
        user = ctx.author 
    
    ap = "'"

    embed = discord.Embed(title=f'{f"{user.name}{ap}s" if user != ctx.author else "Your"} Quest  XP', 
        description=f"{f'**{user.name}** has' if user != ctx.author else 'You have'} **{globalFunctions.getXP(user):,d}** Quest XP", color=var.embed)

    await ctx.send(embeds=[embed])
