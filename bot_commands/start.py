#from bot_commands.miniquests import miniquests
import discord
from discord.ext import commands

import QuestClient as qc

async def command(client : qc.Client, ctx : commands.Context, quest_name : str):

    for quest in client.quest.quests + client.quest.miniquests:

        if quest.name.lower() == quest_name.lower():

            nameFormatted = quest.name.title().replace("_", " ")
            user : discord.Member = ctx.author if hasattr(ctx, "author") else ctx.user
            progress = quest.getProgress(user)

            if progress.started and progress.finished and progress.redeemed: 
                raise qc.errors.MildError(f"You have finished the {nameFormatted} quest on tier {progress.tier}! To tier up use **{qc.var.prefix}tier {quest.name}**")
            elif progress.started and progress.finished:
                raise qc.errors.MildError(f"You have finished {nameFormatted} on tier {progress.tier}! (Use {qc.var.prefix}redeem to get a reward!)")
            elif progress.started:
                raise qc.errors.MildError(f"You have already started this quest on tier {progress.tier}!")
            else:
                quest.start(user)

                embed = discord.Embed(
                    title=f"You started {nameFormatted}!", 
                    description=f"Started quest **{nameFormatted}** on tier {progress.tier}! When completed use **{qc.var.prefix}{'quests' if quest not in client.quest.miniquests else 'miniquests'}**",
                    color=qc.var.embed
                )
                embed.add_field(name="How to complete", value=f"{nameFormatted} quest: {quest.description}")

            send = ctx.response.send_message if isinstance(ctx, discord.Interaction) else ctx.send

            await send(embeds=[embed])