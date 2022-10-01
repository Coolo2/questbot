#from bot_commands.miniquests import miniquests
import discord
from discord.ext import commands

import QuestClient as qc

from discord import app_commands

async def command(client : qc.Client, ctx : commands.Context, quest_name : str):

    for quest in client.quest.quests + client.quest.miniquests:

        if quest.name.lower() == quest_name.lower():
            
            user : discord.Member = ctx.author if hasattr(ctx, "author") else ctx.user
            progress = quest.getProgress(user)
            

            if progress.started and progress.finished and progress.redeemed: 
                embed = discord.Embed(title="Oops!", description=f"You have already redeemed the {quest.name} quest tier {progress.tier}! To tier up use **{qc.var.prefix}tier {quest.name}**", color=qc.var.embedFail)
            elif progress.started and progress.finished:
                
                #multiplier = await client.quest.useMultiplier(user)
                userClass = qc.classes.User(client, user)
                multiplier = 1
                if userClass.item.has_item(name="double_cherry"):
                    multiplier = 2
                    userClass.item.remove_item("double_cherry")

                quest.setProgress(user, [True, True, True])

                reward = quest.reward[progress.tier]

                economyUser = userClass.economy
                await economyUser.addBal(bank=reward.stars * multiplier, guild=ctx.guild)

                if reward.xp != 0:
                    userClass.addXP(reward.xp * multiplier)
                
                embed = discord.Embed(
                    title=f"You redeemed {quest.name.replace('_', ' ').title()}!", 
                    description=f"You redeemed this quest, which gave you {f'**{reward.stars*multiplier:,d}** stars' if reward.stars != 0 else ''}{' and ' if reward.stars != 0 and reward.xp != 0 else ''}{f'**{reward.xp*multiplier:,d}** Quest XP' if reward.xp != 0 else ''}! {f'Use **{qc.var.prefix}tier {quest.name}** to tier up!' if quest.tiers > 1 and progress.tier < quest.tiers else ''}",
                    color=qc.var.embedSuccess
                )
                
            elif progress.started:
                embed = discord.Embed(title="Oops!", description=f"You haven't completed this quest on tier {progress.tier}!", color=qc.var.embedFail)
            else:
                embed = discord.Embed(title="Oops!", description=f"You havent started this quest on tier {progress.tier} yet! Use **{qc.var.prefix}start {quest.name}**", color=qc.var.embedFail)
            

            if quest.tiers > 1 and embed.color.value == qc.var.embedSuccess:

                view = discord.ui.View(timeout=None)

                class button(discord.ui.Button):

                    def __init__(self, client : qc.Client, quest):
                        self.quest = quest
                        self.client = client

                        super().__init__(style=discord.ButtonStyle.blurple, label="Tier Up")

                    async def callback(self, interaction: discord.Interaction):

                        tree : app_commands.CommandTree = client.bot.tree

                        if interaction.user.id != user.id:
                            return await interaction.response.send_message("You are not the initiator.", ephemeral=True)
                        
                        self.disabled = True

                        class FakeCog():
                            def __init__(self, client : qc.Client):
                                self.client = client 
                                self.bot = client.bot

                        await tree.get_command("tier")._callback(FakeCog(self.client), interaction, self.quest.name)

                view.add_item(button(client=client, quest=quest))


                return await ctx.send(embed=embed, view=view)
            await ctx.send(embed=embed)