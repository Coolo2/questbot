import json, discord, random, asyncio

from resources import var
import QuestClient as qc

import typing

from discord.ext import commands 
from discord import app_commands

def getCreatureShopEmbed(client : qc.Client):
    zoo = client.zoo

    shopEmbed = discord.Embed(
        title="Today's Creature Crate shop",
        color=var.embed
    )

    crates = ""
    cs : typing.List[qc.classes.Zoo.Crate] = [zoo.crates.creature, zoo.crates.shiny, zoo.crates.collectors]
    for crate in cs:
        crates += f"{crate.emoji}    **{crate.readableName}** ({crate.price:,d}{var.currency})\n{crate.description}.\n\n"

    shopEmbed.add_field(name=f"Creature Crates - /buy crate [crateName]", value=crates, inline=False)

    return shopEmbed

def getQuestXPShopEmbed(client : qc.Client):
    shop = qc.classes.Shop()

    shopEmbed = discord.Embed(
        title="Today's Quest XP shop",
        color=var.embed
    )

    shopEmbed.add_field(name=f"Quest XP - /buy questxp [amount]", value=f"Conversion rate: **1** {qc.var.quest_xp_currency} for **{round(shop.getConversionRate(), 3)}**{var.currency}")

    return shopEmbed

def getItemShopEmbed(client : qc.Client):
    shop = qc.classes.Shop()

    shopEmbed = discord.Embed(
        title="Today's Item Shop",
        color=var.embed
    )

    for item in shop.items.values():
        shopEmbed.add_field(name=f"{item.name} ({var.shards_currency} {item.cost:,d})", value=item.description, inline=False)

    return shopEmbed


async def command_creature(client : qc.Client, ctx : commands.Context):

    return await ctx.send(embed=getCreatureShopEmbed(client))

async def command_quest_xp(client : qc.Client, ctx : commands.Context):

    return await ctx.send(embed=getQuestXPShopEmbed(client))

async def command_items(client : qc.Client, ctx : commands.Context):

    return await ctx.send(embed=getItemShopEmbed(client))
