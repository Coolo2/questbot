import discord
from discord.ext import commands

from resources.quests import count, place, voiceChannel, fact, cookie, alex
from resources.quests import message as message_quest

from resources import var


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

        


def setup(bot):
    bot.add_cog(events(bot))