import json, discord, random, asyncio

from resources import var
import QuestClient as qc

import typing

from discord.ext import commands 
from discord import app_commands

def getShopEmbed(client : qc.Client):
    zoo = client.get_zoo()
    shop = qc.classes.Shop()

    shopEmbed = discord.Embed(
        title="Today's shop",
        color=var.embed
    )

    crates = ""
    cs : typing.List[qc.classes.Zoo.Crate] = [zoo.crates.creature, zoo.crates.shiny, zoo.crates.collectors]
    for crate in cs:
        crates += f"{crate.emoji}    **{crate.readableName}** ({crate.price:,d}{var.currency})\n{crate.description}.\n\n"

    shopEmbed.add_field(name=f"Creature Crates - {var.prefix}buy crate [crateName]", value=crates, inline=False)
    shopEmbed.add_field(name=f"Quest XP - {var.prefix}buy questxp [amount]", value=f"Conversion rate: **1** Quest XP for **{round(shop.getConversionRate(), 3)}**{var.currency}")

    return shopEmbed


async def command(client : qc.Client, ctx : commands.Context):

    return await ctx.send(embed=getShopEmbed(client))
