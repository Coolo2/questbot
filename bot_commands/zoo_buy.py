#from bot_commands.miniquests import miniquests
import discord
from discord.ext import commands

import QuestClient as qc
from QuestClient import classes

from discord import app_commands

from bot_commands import zoo_list
from QuestClient.quests import creature as creatureQuest

class CheckoutView(discord.ui.View):

    def __init__(self, client : qc.Client, user : qc.classes.User, shop : qc.classes.Shop, amount : int):

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
            embed = discord.Embed(title="Uh oh!", description=f'You do not have enough money ({cost:,d}) **in bank** for this amount of quest xp!', color=qc.var.embedFail)
            return await interaction.response.edit_message(embed=embed)

        self.user.economy.addBal(bank=0-cost)
        self.user.addXP(self.amount)

        embed = discord.Embed(
            title="Successfully purchased",
            description=f"Successfully purchased **{self.amount:,d}** Quest XP for **{cost:,d}**{qc.var.currency}",
            color=qc.var.embedSuccess
        )

        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="Cancel Purchase", style=discord.ButtonStyle.red)
    async def cancel_button(self, interaction : discord.Interaction, button : discord.ui.Button):

        if interaction.user.id != self.user.user.id:
            return await interaction.response.send_message("You are not the correct customer!", ephemeral=True)

        for item in self.children:
            item.disabled = True 
        
        await interaction.response.edit_message(view=self)


async def crate(client : qc.Client, ctx : commands.Context, crate_type : str, cog):

    user = qc.classes.User(ctx.author)
    user.zoo.getCreatures()
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

    user.economy.loadBal(ctx.guild)

    if user.economy.bank < crate.cost:
        embed = discord.Embed(title="Uh oh!", description=f'You do not have enough money ({crate.cost:,d}) **in bank** for this crate!', color=qc.var.embedFail)
        return await ctx.send(embeds=[embed])

    user.zoo.addCreature(creature.name)
    user.zoo.saveCreatures()
    user.economy.addBal(bank=0-crate.cost)
    
    amount = user.zoo.creatures.count(creature.name)

    embed = discord.Embed(title=f"Here's your {crate.name.title()} Crate!", description=f'**1x** {creature.emoji} {creature.readableName}\n\n{"**New creature!** " if amount == 1 else ""}You now have {amount} {creature.readableName}{"" if amount == 1 else "s"}', color=crate.color)

    embed.set_thumbnail(url=crate.icon)
    embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar.url)

    view = discord.ui.View()
    button = discord.ui.Button(label="See creature list", emoji="📃")
    async def response(interaction : discord.Interaction):
        await zoo_list.command(client, ctx)
    button.callback = response
    view.add_item(button)

    await creatureQuest.quest.check(client, ctx.author)
    
    return await ctx.send(embeds=[embed], view=view)

async def quest_xp(client : qc.Client, ctx : commands.Context, amount : int):

    user = qc.classes.User(ctx.author)
    shop = qc.classes.Shop()
    user.economy.loadBal(ctx.guild)
    
    starsPerXP = shop.getConversionRate()
    cost = round(amount * starsPerXP)

    view = CheckoutView(client, user, shop, amount)

    embed = discord.Embed(
        title="Checkout", 
        description=f"This purchase will cost **{cost:,d}**{qc.var.currency}. Continue?",
        color=qc.var.embed
    )

    await ctx.send(embed=embed, view=view)