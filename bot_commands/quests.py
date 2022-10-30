
import discord
from discord.ext import commands

import QuestClient as qc

async def command(client : qc.Client, ctx : commands.Context, member : discord.Member = None):

    if member == None:
        member = ctx.author  
    
    embed = discord.Embed(title="Here are {}'s quests".format(member.display_name), description=f"`To see miniquests use /zoo miniquests`", color=qc.var.embed)

    for quest in client.quest.quests:

        progress = quest.getProgress(member)

        if progress.started and progress.finished and progress.redeemed: 
            response = f"{qc.var.completionEmoji} You have completed the **{quest.name_formatted}** quest{f' in tier {progress.tier}' if quest.tiers > 1 else ''}!"
            response = response + (f' To start the next tier use **/tier {quest.name}**!' if quest.tiers > 1 and progress.tier < quest.tiers else '')
        elif progress.started and progress.finished:
            response=f"You haven't redeemed the reward for the {quest.name_formatted} quest{f' in tier {progress.tier}' if quest.tiers > 1 else ''}! Use **/zoo redeem {quest.name}**!"
        elif progress.started:
            response=f"You haven't finished the quest{f' in tier {progress.tier}' if quest.tiers > 1 else ''}! ({progress.value}/{quest.required[progress.tier]})"
        else:
            response = f"You havent started this quest{f' in tier {progress.tier}' if quest.tiers > 1 else ''} yet! Use **/zoo start {quest.name}**"

        embed.add_field(name=quest.name_formatted, value=response, inline=False)
    
    await ctx.send(embed=embed)