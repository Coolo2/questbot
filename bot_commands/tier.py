import discord, random, aiohttp, json, os, time, datetime, asyncio, json, sys
from discord.ext import commands
from datetime import datetime, timedelta

from resources import questCommons, questData, var, UB, globalFunctions
from resources import questCommons as functions

from discord_components import *

from bot_commands import start

async def tier(bot, ctx, questName):

    for quest in questCommons.allQuests:

        if quest.name.lower() == questName.lower():

            name = quest.name
            progress = functions.getProgress(quest.name, ctx.author)
            user = ctx.author

            if progress.started and progress.finished and progress.redeemed: 
                tier = progress.tier

                if int(tier) >= quest.tiers:
                    return await ctx.send(embeds=[discord.Embed(color=var.embed, title="GG!", description="You have fully completed this quest! GG!")])

                quest.quest.tierUp(user)


                button = Button(style=ButtonStyle.blue, label="Start Next Tier", disabled=False, id="startButton")

                msg = await ctx.send(embeds=[discord.Embed(color=var.embedSuccess, title="Tiered up!", description=f"You have been tiered up to tier {tier+1}! Use **{var.prefix}start {name}** to begin tier " + str(int(tier) + 1) + "!")], components=[button])
                button.set_disabled(True)
                button.set_style(3)

                try:
                    async def wait_loop():
                        res = await bot.wait_for("button_click", timeout= 30, check = lambda i: i.custom_id == "startButton")

                        if res.user == ctx.author:
                            await res.respond(type=7, components=[button])
                            await start.start(bot, ctx, name)
                        else:
                            await res.send("Nice try... You aren't the right person!")
                            await wait_loop()
                    await wait_loop()

                except asyncio.TimeoutError:
                    await msg.edit(components=[button])

            elif progress.started and progress.finished:
                await ctx.send(embeds=[discord.Embed(color=var.embedFail, title="Oops!", description="You haven't redeemed this quest yet! Please redeem it before tiering up!")])
            elif progress.started:
                await ctx.send(embeds=[discord.Embed(color=var.embedFail, title="Oops!", description="You haven't completed this quest yet! Please complete it and redeem it before tiering up!")])
            else:
                await ctx.send(embeds=[discord.Embed(color=var.embedFail, title="Oops!", description="You haven't started this quest yet! Please start, complete and redeem the quest before tiering up!")])
            


