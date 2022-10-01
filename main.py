
import discord, os
from discord.ext import commands, tasks

import datetime

from resources import var
from website import backend
import QuestClient

from discord import app_commands

from bot_commands import zoo_trade

intents = discord.Intents.all()

bot : discord.client.Client = commands.Bot(commands.when_mentioned_or(var.prefix, var.prefix.title(), var.prefix.upper()), case_insensitive=True, intents=intents)
client = QuestClient.Client(bot)

bot.client = client
bot.remove_command("help")

tree : app_commands.CommandTree = bot.tree

@bot.event
async def on_ready():
    print(bot.user.name + " Online")

    refreshData.start()

    await client.initialise_ub()
    
    await bot.change_presence(activity=discord.Game(name=f"{var.prefix}help | Made for Dash's Lounge"))

@tasks.loop(seconds=30)
async def refreshData():
    # Time out old trades
    zoo = client.get_zoo()
    zoo.getTrades()
    for tradeID in zoo.trades:
        trade = zoo.Trade(tradeID)
        if (datetime.datetime.now() - trade.data.started).total_seconds() > (24 * 60 * 60):
            await trade.getData(bot)
            await trade.end("Timed out")

async def setup_hook():

    await bot.load_extension("cogs.events")
    await bot.load_extension("cogs.quest_commands")
    await bot.load_extension("cogs.errors")

    #await tree.sync()

    await zoo_trade.load_views(client)

bot.setup_hook = setup_hook

backend.webserver_run(bot)
print("\n\n")

bot.run(os.getenv("token"))