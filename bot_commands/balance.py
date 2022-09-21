#from bot_commands.miniquests import miniquests
import discord
from discord.ext import commands

import QuestClient as qc

def make_ordinal(n):
    n = int(n)
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix


async def command(client : qc.Client, ctx : commands.Context, userO : discord.User = None):

    if userO == None:
        userO = ctx.author 
    
    user = qc.classes.User(userO)
    user.economy.loadBal(ctx.guild)
    user.zoo.refreshProducers()
    
    ap = "'"

    embed = discord.Embed(
        title=f'{f"{user.user.name}{ap}s" if user != ctx.author else "Your"} balances', 
        description=f"Star leaderboard rank: {make_ordinal(user.economy.rank)}",
        color=qc.var.embed
    )

    embed.add_field(name="Cash", value=f"{qc.var.currency}{user.economy.cash:,d}")
    embed.add_field(name="Bank", value=f"{qc.var.currency}{user.economy.bank:,d}")
    embed.add_field(name="Total", value=f"{qc.var.currency}{user.economy.total:,d}")

    embed.add_field(name="Quest XP", value=f"{user.getXP():,d}")
    embed.add_field(name="Shards", value=f"{user.getShards():,d}")

    await ctx.send(embed=embed)