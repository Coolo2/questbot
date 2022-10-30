
import discord
from discord.ext import commands

import QuestClient as qc

async def command(client : qc.Client, ctx : commands.Context, quest_name : str):
    
    for quest in client.quest.quests + client.quest.miniquests:

        if quest.name.lower() == quest_name.lower():

            embed = discord.Embed(title=f"Quest info: {quest.name_formatted}", description=quest.description, color=qc.var.embed)
            
            if quest.tiers > 1:
                tiers = ""
                for i, tier in enumerate(quest.required):
                    if i != 0:
                        tiers += f"**Tier {i}:** {tier} {quest.amountType}\n"
                embed.add_field(name="Tiers", value=tiers)
            
            rewards = ""
            for i, reward in enumerate(quest.reward):
                if i != 0:
                    rewards += f"**Tier {i}:** {reward.name_emoji}\n"
            embed.add_field(name="Rewards", value=rewards, inline=False)

            
            return await ctx.send(embed=embed)
    
    raise qc.errors.MildError("You did not specify a valid quest")