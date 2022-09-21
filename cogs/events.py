import discord
from discord.ext import commands

from QuestClient.quests import count

from resources import var

import QuestClient as qc

class events(commands.Cog):
    def __init__(self, bot, client : qc.Client):
        self.bot = bot
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, message : discord.Message):

        if not isinstance(message.channel, discord.DMChannel):
            if not message.author.bot and message.guild.id in var.allowed_guilds_raw:

                quests = ["count", "ping_dino", "message", "greetings"]

                for quest in self.client.quest.quests + self.client.quest.miniquests:
                    if quest.name in quests:
                        await quest.validate(self.client, message)
    
    @commands.Cog.listener() 
    async def on_voice_state_update(self, member : discord.Member, before : discord.VoiceState, after : discord.VoiceState):

        if not member.bot and member.guild.id in var.allowed_guilds_raw:
            quests = ["voice_channel"]

            for quest in self.client.quest.quests + self.client.quest.miniquests:
                if quest.name in quests:

                    await quest.validate(self.client, member, before, after)


async def setup(bot):
    await bot.add_cog(events(bot, bot.client))