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

class BalanceView(discord.ui.View):
    def __init__(self, client : qc.Client):
        self.client = client 
        super().__init__(timeout=None)
    
    @discord.ui.button(label="View Quest XP levels", emoji="📊")
    async def _quest_xp_levels(self, interaction : discord.Interaction, button : discord.ui.Button):

        levels = len(qc.classes.QuestXPLevels)
        description_full = ""

        for i in range(levels-1):
            reward = qc.data.levels[i]

            if reward:
                if reward.stars:
                    description_full += qc.var.currency
                if reward.shards:
                    description_full += qc.var.shards_currency
                if reward.role:
                    description_full += "👷"
                if reward.crate:
                    description_full += "<:Shiny_Creature_Crate:822858260709244929>"
                if reward.badge:
                    description_full += "<:QuestIII:1032021193034846298>"
                if reward.command:
                    description_full += "💬"
            else:
                description_full += "⛔"

            description_full += f" **{i+1}.** {reward.name if reward else 'No reward'} (`{qc.classes.QuestXPLevels[i]:,d} XP`)\n"
        
        description_split = description_full.split("\n")
        per_page = 15
        catalog_pages = ["\n".join(description_split[i:i+per_page]) for i in range(0, len(description_split), per_page)]

        embed = discord.Embed(color=qc.var.embed, title="Quest XP Levels", description=catalog_pages[0])
        
        view = qc.paginator.PaginatorView(catalog_pages, embed, private=interaction.user)

        return await interaction.response.send_message(embed=view.embed, view=view)


async def command(client : qc.Client, ctx : commands.Context, userO : discord.User = None):

    if userO == None:
        userO = ctx.author 
    
    user = qc.classes.User(client, userO)
    await user.economy.loadBal(ctx.guild)
    user.zoo.refresh_shard_producers()
    
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

    await ctx.send(embed=embed, view=BalanceView(client))