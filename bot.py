import discord, os
from discord.ext import commands, tasks
from discord_components import *

import datetime

from resources import var, questbot

from website import backend

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(commands.when_mentioned_or(var.prefix, var.prefix.title(), var.prefix.upper()), case_insensitive=True, intents=intents)

bot.remove_command("help")

@bot.event
async def on_ready():
    print(bot.user.name + " Online")
    DiscordComponents(bot)

    refreshData.start()
    
    await bot.change_presence(activity=discord.Game(name=f"{var.prefix}help | Made for Dash's Lounge"))

@tasks.loop(seconds=30)
async def refreshData():
    zoo = questbot.Zoo()
    zoo.getTrades()
    for tradeID in zoo.trades:
        trade = zoo.Trade(tradeID)
        if (datetime.datetime.now() - trade.data.started).total_seconds() > (24 * 60 * 60):
            await trade.getData(bot)
            await trade.end("Timed out")

bot.load_extension("cogs.events")
bot.load_extension("cogs.quest_commands")
#bot.load_extension("cogs.errorHandling")

backend.webserver_run(bot)
print("\n\n")

bot.run(os.getenv("token"))