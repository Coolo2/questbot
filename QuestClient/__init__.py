
from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from QuestClient import Client as ClFr

from discord.ext import commands
import json

from QuestClient import classes, errors, data
from QuestClient.components import paginator, autocompletes
from resources import var
from discord import client

import aiohttp

from QuestClient.quests import count, ping_dino, greetings, message, voice_channel, creature, money_maker

miniquests : typing.List[classes.Quest] = [
    ping_dino.quest,
    greetings.quest,
    voice_channel.quest
]

quests : typing.List[classes.Quest] = [
    count.quest,
    message.quest,
    creature.quest,
    money_maker.quest
]

class QuestClient():
    
    def __init__(self, client : ClFr):

        self.client = client

        self.miniquests : typing.List[classes.Quest] = miniquests
        self.quests : typing.List[classes.Quest] = quests

        

    async def useMultiplier(self, user):
        multiplier = 1

        with open("data/multipliers.json") as f:
            m = json.load(f)

        if str(user.id) in m:
            await user.send(f"Your {m[str(user.id)]}X quest reward power up was used!")
            multiplier = m[str(user.id)]
            del m[str(user.id)]
        
        with open('data/multipliers.json', 'w') as f:
            json.dump(m, f, indent=4)  
        
        return multiplier
    
    

class Client():

    def __init__(self, bot : typing.Union[client.Client, commands.Bot]):

        self.bot = bot 
        self.var = var

        self.quest = QuestClient(self)

        self.eco_totals : dict = {}

        self.__zoo_hold : classes.Zoo = None
    
    
    @property 
    def zoo(self):
        if not self.__zoo_hold:
            self.__zoo_hold = classes.Zoo()
            
        return self.__zoo_hold
    
    async def initialise_ub(self):
        guild = self.bot.get_guild(var.allowed_guilds[0].id)

        for member in [m for m in guild.members if not m.bot]:
            ub_member = classes.User(self, member)
            await ub_member.economy.loadBal(guild)
            self.eco_totals[str(member.id)] = ub_member.economy.total




            #async with aiohttp.ClientSession() as session:
            #    async with session.get(var.UBbase + f"/guilds/{var.allowed_guilds[0].id}/user/{member.id}", headers=var.UBheaders) as r:
            #        data = await r.json()
            #        for user in data:
            #            self.eco_totals[user["user_id"]] = user["total"]


