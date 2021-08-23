from bot_commands.miniquests import miniquests
import discord, random, aiohttp, json, os, time, datetime, asyncio, json, sys
from discord.ext import commands
from datetime import datetime, timedelta

from resources import questCommons, questData, var
from resources import questCommons as functions

async def quests(bot, ctx, member = None):

    if member == None:
        member = ctx.author  
    
    embed = discord.Embed(title="Here are {}'s quests".format(member.display_name), color=var.embed)

    for quest in questCommons.allQuests:

        if quest not in questCommons.miniQuests:

            name = quest.name
            nameFormatted = quest.name.title().replace("_", " ")

            progress = functions.getProgress(name, member)

            if progress.started and progress.finished and progress.redeemed: 
                response = f"{var.completionEmoji} You have completed the **{nameFormatted}** quest{f' in tier {progress.tier}' if quest.tiers > 1 else ''}!"
                response = response + (f' To start the next tier use **{var.prefix}tier {name}**!' if quest.tiers > 1 and progress.tier < quest.tiers else '')
            elif progress.started and progress.finished:
                response=f"You haven't redeemed the reward for the {nameFormatted} quest{f' in tier {progress.tier}' if quest.tiers > 1 else ''}! Use **{var.prefix}redeem {name}**!"
            elif progress.started:
                response=f"You haven't finished the quest{f' in tier {progress.tier}' if quest.tiers > 1 else ''}! ({progress.value}/{quest.required[progress.tier]})"
            else:
                response = f"You havent started this quest{f' in tier {progress.tier}' if quest.tiers > 1 else ''} yet! Use **{var.prefix}start {name}**"
    
            embed.add_field(name=nameFormatted, value=response, inline=False)
    embed.add_field(name="Quests", value= f"`To see miniquests use {var.prefix}miniquests`", inline=False)
    
    await ctx.send(embeds=[embed])