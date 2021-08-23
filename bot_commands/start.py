import discord, random, aiohttp, json, os, time, datetime, asyncio, json, sys
from discord.ext import commands
from datetime import datetime, timedelta

from resources import questCommons, questData, var
from resources import questCommons as functions

async def start(bot, ctx, questName):

    for quest in questCommons.allQuests:

        if quest.name.lower() == questName.lower():

            name = quest.name
            nameFormatted = quest.name.title().replace("_", " ")
            progress = functions.getProgress(quest.name, ctx.author)

            if progress.started and progress.finished and progress.redeemed: 
                embed = discord.Embed(title="Oops!", 
                    description=f"You have finished the {nameFormatted} quest on tier {progress.tier}! To tier up use **{var.prefix}tier count**",
                    color=var.embedFail
                )
            elif progress.started and progress.finished:
                embed = discord.Embed(title="Oops!", 
                    description=f"You have finished {nameFormatted} on tier {progress.tier}! (Use {var.prefix}redeem to get a reward!)",
                    color=var.embedFail
                )
            elif progress.started:
                embed = discord.Embed(title="Oops!", 
                    description=f"You have already started this quest on tier {progress.tier}!",
                    color=var.embedFail
                )
            else:
                quest.quest.start(ctx.author)

                embed = discord.Embed(
                    title=f"You started {nameFormatted}!", 
                    description=f"Started quest **{nameFormatted}** on tier {progress.tier}! When completed use **{var.prefix}{'quests' if quest not in questCommons.miniQuests else 'miniquests'}**",
                    color=var.embed
                )
                embed.add_field(name="How to complete", value=f"{nameFormatted} quest: {quest.description}")

            await ctx.send(embeds=[embed])