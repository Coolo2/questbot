import discord, random, aiohttp, json, os, time, datetime, asyncio, json, sys
from discord.ext import commands

from resources import var, questbot

def make_ordinal(n):
    n = int(n)
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix

async def balance(bot, ctx, user):

    if user == None:
        user = ctx.author 
    
    user = questbot.User(user)
    user.economy.loadBal(ctx.guild)
    user.zoo.refreshProducers()
    
    ap = "'"

    embed = discord.Embed(
        title=f'{f"{user.user.name}{ap}s" if user != ctx.author else "Your"} balances', 
        description=f"Star leaderboard rank: {make_ordinal(user.economy.rank)}",
        color=var.embed
    )

    embed.add_field(name="Cash", value=f"{var.currency}{user.economy.cash:,d}")
    embed.add_field(name="Bank", value=f"{var.currency}{user.economy.bank:,d}")
    embed.add_field(name="Total", value=f"{var.currency}{user.economy.total:,d}")

    embed.add_field(name="Quest XP", value=f"{user.getXP():,d}")
    embed.add_field(name="Shards", value=f"{user.getShards():,d}")

    await ctx.send(embeds=[embed])
