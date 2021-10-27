import discord, random, aiohttp, json, os, time, datetime, asyncio, json, sys
from discord.ext import commands
from datetime import datetime, timedelta

from resources import questCommons, questData, var, questbot
from resources import questCommons as functions

from discord_components import *

from bot_commands import tier

async def redeem(bot, ctx, questName, extra=None):

    for quest in questCommons.allQuests:

        if quest.name.lower() == questName.lower():

            name = quest.name
            progress = functions.getProgress(quest.name, ctx.author)
            user = ctx.author

            if progress.started and progress.finished and progress.redeemed: 
                embed = discord.Embed(title="Oops!", description=f"You have already redeemed the {name} quest tier {progress.tier}! To tier up use **{var.prefix}tier {name}**", color=var.embedFail)
            elif progress.started and progress.finished:
                
                multiplier = await functions.useMultiplier(user)

                functions.setProgress(name, user, [True, True, True])

                reward = quest.reward[progress.tier]

                userClass = questbot.User(ctx.author)
                economyUser = userClass.economy
                economyUser.addBal(bank=reward.stars * multiplier)

                if reward.xp != 0:
                    userClass.addXP(reward.xp * multiplier)
                
                embed = discord.Embed(
                    title=f"You redeemed {name.replace('_', ' ').title()}!", 
                    description=f"You redeemed this quest, which gave you {f'**{reward.stars}** stars' if reward.stars != 0 else ''}{' and ' if reward.stars != 0 and reward.xp != 0 else ''}{f'**{reward.xp}** Quest XP' if reward.xp != 0 else ''}! {f'Use **{var.prefix}tier {name}** to tier up!' if quest.tiers > 1 and progress.tier < quest.tiers else ''}",
                    color=var.embedSuccess
                )
                
            elif progress.started:
                embed = discord.Embed(title="Oops!", description=f"You haven't completed this quest on tier {progress.tier}!", color=var.embedFail)
            else:
                embed = discord.Embed(title="Oops!", description=f"You havent started this quest on tier {progress.tier} yet! Use **{var.prefix}start {name}**", color=var.embedFail)
            

            if quest.tiers > 1 and embed.color.value == var.embedSuccess:
                
                button = Button(style=ButtonStyle.blue, label="Tier Up!", disabled=False, id="tierButton")

                if extra != None:
                    msg = await ctx.send(content=extra, embeds=[embed], components=[button])
                else:
                    msg = await ctx.send(embeds=[embed], components=[button])
                button.set_disabled(True)
                button.set_style(3)

                try:
                    async def wait_loop():
                        res = await bot.wait_for("button_click", timeout= 30, check = lambda i: i.custom_id == "tierButton")

                        if res.user == ctx.author:
                            await res.respond(type=7, components=[button])
                            await tier.tier(bot, ctx, name)
                        else:
                            await res.send("Nice try... You aren't the right person!")
                            await wait_loop()
                    await wait_loop()

                except asyncio.TimeoutError:
                    await msg.edit(components=[button])

            else:
                if extra != None:
                    await ctx.send(content=extra, embeds=[embed])
                else:
                    await ctx.send(embeds=[embed])

