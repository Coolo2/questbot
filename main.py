
import discord, os
from discord.ext import commands, tasks

import datetime

from resources import var
import QuestClient

from discord import app_commands

from bot_commands import zoo_trade
import website
from resources import creatureslister

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

    #await creatureslister.lister(bot)

    #import requests;from resources import shiny_converter;from PIL import Image;channel = await bot.fetch_channel(1026208828976537720)
    #async for message in channel.history(limit=1000): 
    #    if len(message.attachments) == 0: continue
    #    background = Image.open(requests.get(message.attachments[0].url, stream=True).raw);shiny_converter.get_output(background);await bot.get_channel(1026587766739443814).send(content=message.content, file=discord.File("output.gif"))

    await bot.change_presence(activity=discord.Game(name=f"/help | Made for Dash's Lounge"))

@tasks.loop(seconds=30)
async def refreshData():
    # Time out old trades
    client.zoo.getTrades()
    for tradeID in client.zoo.trades:
        trade = client.zoo.Trade(client, tradeID)
        if (datetime.datetime.now() - trade.data.started).total_seconds() > (24 * 60 * 60):
            await trade.getData(bot)
            await trade.end("Timed out")

async def setup_hook():

    await bot.load_extension("cogs.events")
    await bot.load_extension("cogs.quest_commands")
    #await bot.load_extension("cogs.errors")

    #await tree.sync()

    await zoo_trade.load_views(client)

    quart_app : website.quart.Quart = await website.generate_app(bot, client)
    bot.loop.create_task(quart_app.run_task(host=var.host, port=var.port))

bot.setup_hook = setup_hook

bot.run(os.getenv("token"))