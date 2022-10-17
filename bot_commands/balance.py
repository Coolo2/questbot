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
    
    user = qc.classes.User(client, userO)
    await user.economy.loadBal(ctx.guild)
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

    userquestxp = user.getXP()
    questxplevel = qc.classes.getQuestXPLevel(userquestxp)
    questxp = f"{qc.var.quest_xp_currency}{userquestxp:,d} *(level {questxplevel})*"
    if len(qc.classes.QuestXPLevels) >= questxplevel+1:
        questxp += f"\n{qc.classes.QuestXPLevels[questxplevel+1]-userquestxp:,d} to next level"
    embed.add_field(name="Quest XP", value=questxp)
    embed.add_field(name="Shards", value=f"{qc.var.shards_currency}{user.getShards():,d}")

    await ctx.send(embed=embed)