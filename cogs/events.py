import discord
from discord.ext import commands

from resources.quests import count, place, voiceChannel, fact, cookie, alex
from resources.quests import message as message_quest

from resources import var
from bot_commands import trade

from discord_components import *


class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):

        if not isinstance(message.channel, discord.DMChannel):
            if not message.author.bot and message.guild.id in var.allowed_guilds:
                
                await count.validate(self.bot, message)
                await place.validate(self.bot, message)
                await message_quest.validate(self.bot, message)
                await fact.validate(self.bot, message)

                await cookie.validate(self.bot, message)
                await alex.validate(self.bot, message)
    
    @commands.Cog.listener() 
    async def on_voice_state_update(self, member, before, after):
        await voiceChannel.validate(self.bot, member, before, after)
    
    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        if interaction.custom_id.startswith("acceptTrade"):
            traded = await trade.acceptTrade(self.bot, interaction.user, interaction.custom_id.split("_")[1])

            if "in return for a" in traded:
                buttonAccept = Button(style=ButtonStyle.green, label="Accept Trade", disabled=True, id=f"acceptTrade_{interaction.custom_id.split('_')[1]}")
                buttonDeny = Button(style=ButtonStyle.red, label="Deny Trade", disabled=True, id=f"denyTrade_{interaction.custom_id.split('_')[1]}")

                await interaction.respond(type=7, components=[buttonAccept, buttonDeny])
                #await interaction.respond(ephemeral=False, content=traded)
            else:
                await interaction.respond(ephemeral=True, content=traded)
        if interaction.custom_id.startswith("denyTrade"):
            traded = await trade.denyTrade(self.bot, interaction.user, interaction.custom_id.split("_")[1])
            await interaction.respond(ephemeral=True, content="Cancelled Trade")


        


def setup(bot):
    bot.add_cog(events(bot))