import discord, os
from discord.ext import commands
from discord_components import *

from resources import var

from website import backend

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(commands.when_mentioned_or(var.prefix, var.prefix.title(), var.prefix.upper()), case_insensitive=True, intents=intents)

@bot.event
async def on_ready():
    print(bot.user.name + " Online")
    DiscordComponents(bot)
    

    await bot.change_presence(activity=discord.Game(name=f"{var.prefix}help | Made for Dash's Lounge"))

bot.load_extension("cogs.events")
bot.load_extension("cogs.quest_commands")
#bot.load_extension("cogs.errorHandling")

backend.webserver_run(bot)
print("\n\n")

bot.run(os.getenv("token"))