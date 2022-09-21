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
                tier = progress.tier

                if int(tier) >= quest.tiers:
                    return await ctx.send(embeds=[discord.Embed(color=qc.var.embed, title="GG!", description="You have fully completed this quest! GG!")])

                quest.tierUp(user)

                view = discord.ui.View(timeout=None)

                class button(discord.ui.Button):

                    def __init__(self, client : qc.Client, quest):
                        self.quest = quest
                        self.client = client

                        super().__init__(style=discord.ButtonStyle.blurple, label="Start Next Tier")

                    async def callback(self, interaction: discord.Interaction):

                        tree : app_commands.CommandTree = client.bot.tree

                        if interaction.user.id != user.id:
                            return await interaction.response.send_message("You are not the initiator.", ephemeral=True)
                        
                        self.disabled = True

                        class FakeCog():
                            def __init__(self, client : qc.Client):
                                self.client = client 
                                self.bot = client.bot

                        await tree.get_command("start")._callback(FakeCog(self.client), interaction, self.quest.name)

                view.add_item(button(client=client, quest=quest))

                send = ctx.response.send_message if isinstance(ctx, discord.Interaction) else ctx.send

                await send(
                    embed=discord.Embed(
                        color=qc.var.embedSuccess, 
                        title="Tiered up!", 
                        description=f"You have been tiered up to tier {tier+1}! Use **{qc.var.prefix}start {quest.name}** to begin tier " + str(int(tier) + 1) + "!"
                    ),
                    view=view
                )

            elif progress.started and progress.finished:
                raise qc.errors.MildError("You haven't redeemed this quest yet! Please redeem it before tiering up!")
            elif progress.started:
                raise qc.errors.MildError("You haven't completed this quest yet! Please complete it and redeem it before tiering up!")
            else:
                raise qc.errors.MildError("You haven't started this quest yet! Please start, complete and redeem the quest before tiering up!")
