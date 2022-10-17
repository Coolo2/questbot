from __future__ import annotations
import typing

#from bot_commands.miniquests import miniquests
import discord
from discord.ext import commands

import QuestClient as qc
from QuestClient import classes

from discord import app_commands

from bot_commands import zoo_list
from QuestClient.quests import creature as creatureQuest

import datetime

if typing.TYPE_CHECKING:
    from QuestClient.classes import Quest as QuestFr
    from QuestClient import Client as ClientFr
    from QuestClient import classes as ClassesFr

class CheckoutView(discord.ui.View):

    def __init__(self, client : ClientFr, user : qc.classes.User, shop : qc.classes.Shop, amount : int):

        self.client = client 
        self.user = user 
        self.shop = shop
        self.amount = amount

        super().__init__(timeout=None)
    
    @discord.ui.button(label="Confirm Purchase", style=discord.ButtonStyle.green)
    async def confirm_button(self, interaction : discord.Interaction, button : discord.ui.Button):
        
        if interaction.user.id != self.user.user.id:
            return await interaction.response.send_message("You are not the correct customer!", ephemeral=True)
        
        starsPerXP = self.shop.getConversionRate()
        cost = round(self.amount * starsPerXP)

        for item in self.children:
            item.disabled = True
        
        if self.user.economy.bank < cost:
            embed = discord.Embed(title="Uh oh!", description=f'You do not have enough money ({cost:,d}) **in bank** for this amount of Quest XP!', color=qc.var.embedFail)
            return await interaction.response.edit_message(embed=embed)

        await self.user.economy.addBal(bank=0-cost)
        

        embed = discord.Embed(
            title="Successfully purchased",
            description=f"Successfully purchased **{self.amount:,d} {qc.var.quest_xp_currency}** for **{cost:,d}**{qc.var.currency}",
            color=qc.var.embedSuccess
        )

        await interaction.response.edit_message(embed=embed, view=self)

        await self.user.addQuestXP(self.amount, channel=interaction.channel)
    
    @discord.ui.button(label="Cancel Purchase", style=discord.ButtonStyle.red)
    async def cancel_button(self, interaction : discord.Interaction, button : discord.ui.Button):

        if interaction.user.id != self.user.user.id:
            return await interaction.response.send_message("You are not the correct customer!", ephemeral=True)

        for item in self.children:
            item.disabled = True 
        
        await interaction.response.edit_message(view=self)


async def crate(client : qc.Client, ctx : commands.Context, crate_type : str, cog):

    user = qc.classes.User(client, ctx.author)
    user.zoo.getZoo()

    if crate_type == None:
        embed = discord.Embed(title="Crate shop", color=qc.var.embed)

        for crate in [user.zoo.zoo.crates.creature, user.zoo.zoo.crates.shiny, user.zoo.zoo.crates.collectors]:

            embed.add_field(
                name=f"{crate.emoji}  {crate.readableName} - {qc.var.prefix}buy {crate.name}", value=f"{crate.description}. **({crate.price:,d}{qc.var.currency})**", inline=False)

        return await ctx.send(embeds=[embed])


    if crate_type == "creature":
        crate = user.zoo.zoo.crates.creature  
        creature = crate.getCreature()
    if crate_type == "shiny":
        crate = user.zoo.zoo.crates.shiny
        creature = crate.getCreature()
    
    if crate_type == "collectors":
        crate = user.zoo.zoo.crates.collectors
        creature = crate.getCreature()
        
        if crate.calculatePerc(75):

            if str(ctx.author.id) in user.zoo.creatures:
                while creature.name in user.zoo.creatures[str(ctx.author.id)]:
                    creature = crate.getCreature()

    await user.economy.loadBal(ctx.guild)

    if user.economy.bank < crate.cost:
        embed = discord.Embed(title="Uh oh!", description=f'You do not have enough money ({crate.cost:,d}) **in bank** for this crate!', color=qc.var.embedFail)
        return await ctx.send(embeds=[embed])

    user.zoo.addCreature(creature.name)
    user.zoo.saveCreatures()
    await user.economy.addBal(bank=0-crate.cost)
    
    amount = user.zoo.creatures.count(creature.name)

    embed = discord.Embed(title=f"Here's your {crate.name.title()} Crate!", description=f'**1x** {creature.emoji} {creature.readableName}\n\n{"**New creature!** " if amount == 1 else ""}You now have {amount} {creature.readableName}{"" if amount == 1 else "s"}', color=crate.color)

    embed.set_thumbnail(url=crate.icon)
    embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar.url)

    view = discord.ui.View()
    button = discord.ui.Button(label="See creature list", emoji="📃")
    async def response(interaction : discord.Interaction):
        if interaction.user != ctx.author:
            return
        await zoo_list.command(client, ctx)
    button.callback = response
    view.add_item(button)

    await creatureQuest.quest.check(client, ctx.author)
    
    return await ctx.send(embeds=[embed], view=view)

async def quest_xp(client : qc.Client, ctx : commands.Context, amount : int):

    user = qc.classes.User(client, ctx.author)
    shop = qc.classes.Shop()
    await user.economy.loadBal(ctx.guild)
    
    starsPerXP = shop.getConversionRate()
    cost = round(amount * starsPerXP)

    view = CheckoutView(client, user, shop, amount)

    embed = discord.Embed(
        title="Checkout", 
        description=f"This purchase will cost **{cost:,d}**{qc.var.currency}. Continue?",
        color=qc.var.embed
    )

    await ctx.send(embed=embed, view=view)

async def item(client : qc.Client, ctx : commands.Context, item : str):

    item = item.lower().replace(" ", "_")

    user = qc.classes.User(client, ctx.author)
    shop = qc.classes.Shop()
    
    user.zoo.refreshProducers()
    shards : int = user.getShards()

    user.item.refresh_items()

    item : classes.Shop.Item = shop.items[item]

    if shards < item.cost:
        raise qc.errors.MildError(f"You do not have enough shards ({item.cost:,d}) **in your bank** to purchase this item.")

    for i in user.item.items:
        if i.name == item.name:
            if i.lasts:
                ends_at_relative = f"<t:{round((i.active_since + i.lasts).timestamp())}:f>"

            raise qc.errors.MildError(f"You already have a {i.name} active. {f'Wait till this item runs out on {ends_at_relative}' if i.lasts else ''}")

    new_item = user.item.buy_item(item)
    
    desc = f"Successfully purchased a **{item.name}** for **{item.cost} {qc.var.shards_currency}**!"

    if item.lasts:
        ends_at_relative = f"<t:{round((item.active_since + new_item.lasts).timestamp())}:f>"
        desc += f" This item will last until {ends_at_relative}"

    embed = discord.Embed(title=f"Successfully bought {item.name}", description=desc, color=client.var.embedSuccess)
    await ctx.send(embed=embed)
    
    
    