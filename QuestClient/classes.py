from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from QuestClient.classes import Quest as QuestFr
    from QuestClient import Client as ClientFr

import re
from discord.client import Coro
from resources import var
import discord
import json, requests, random
from datetime import datetime, timedelta

import typing
from discord import app_commands


class Validator():

    def __init__(self, valid, message=""):

        self.valid = valid 
        self.message = message 

class Zoo():

    class Crate():
        def __init__(self, zoo, name, description, color, icon, emoji, cost, shinyPercentage):
            self.zoo = zoo
            self.name = name 
            self.description = description
            self.cost = cost 
            self.color = color 
            self.icon = icon 
            self.emoji = emoji
            self.shinyPercentage = shinyPercentage

            self.readableName = name.replace("_", " ").title()
            self.price = cost
        
        def calculatePerc(self, percentage):
            return True if random.randint(1, 100) <= percentage else False
        
        def getCreature(self) -> Zoo.Creature:
            is_shiny = self.calculatePerc(self.shinyPercentage)
            is_common = self.calculatePerc(63)
            is_golden = self.calculatePerc(100)

            if self.name == "collectors" and is_golden:
                key = random.choice(list(self.zoo.creaturesRaw["golden"]))
                return self.zoo.Creature(key, self.zoo.creaturesRaw["golden"][key])
            elif is_shiny:
                key = random.choice(list(self.zoo.creaturesRaw["rare"]))
                return self.zoo.Creature(key, self.zoo.creaturesRaw["rare"][key])
            elif is_common:
                key = random.choice(list(self.zoo.creaturesRaw["common"]))
                return self.zoo.Creature(key, self.zoo.creaturesRaw["common"][key])
            else:
                key = random.choice(list(self.zoo.creaturesRaw["very_common"]))
                return self.zoo.Creature(key, self.zoo.creaturesRaw["very_common"][key])

    class Creature():
        def __init__(self, name, data=None):
            zoo = Zoo()

            self.name = name 
            self.readableName = name.replace("_", " ").title()

            if data == None:
                data = zoo.creatures[name]

            self.emoji = data["emoji"]
            self.rarity = "golden" if name in zoo.creaturesRaw["golden"] else "rare" if name in zoo.creaturesRaw["rare"] else "common" if name in zoo.creaturesRaw else "very_common"

            if self.rarity in ["common", "very_common"]:
                self.sellPrice = random.randint(100, 300)
            elif self.rarity in ["rare"]:
                self.sellPrice = random.randint(1000, 3000)
            else:
                self.sellPrice = random.randint(10000, 50000)
    
    class ShardProducer():
        def __init__(self, name, birthday, level, lastRefreshed):
            zoo = Zoo()

            self.name = name 
            self.readableName = name.replace("_", " ").title()

            self.birthdate = datetime.strptime(birthday, "%d-%b-%Y (%H:%M:%S.%f)") if type(birthday) == str else birthday 
            self.lastRefreshed = datetime.strptime(lastRefreshed, "%d-%b-%Y (%H:%M:%S.%f)") if type(lastRefreshed) == str else lastRefreshed 
            self.level = level

            data = zoo.creatures[name]

            self.emoji = data["emoji"]
            self.rarity = "shiny" if name in zoo.creaturesRaw["rare"] or name in zoo.creaturesRaw["golden"] else "standard"

            self.hoursForShard = [None, 24, 18, 15, 12, 8][int(self.level)]

            if self.rarity == "shiny":
                self.shards = 5
            else:
                self.shards = 1
            
        def to_json(self):
            return {
                "birthdate":self.birthdate.strftime("%d-%b-%Y (%H:%M:%S.%f)"),
                "last_refreshed":self.lastRefreshed.strftime("%d-%b-%Y (%H:%M:%S.%f)"),
                "level":int(self.level)
            }
            
    class Crates():

        def __init__(self, zoo : Zoo):

            self.zoo = zoo

            self.creature : zoo.Crate = zoo.Crate(
                zoo, 
                "creature", 
                "5% chance of a shiny creature. Get 1 random creature",
                0x808080, 
                "https://cdn.discordapp.com/attachments/821774449459855423/822857982672240730/Creature_Crate.png", 
                "<:Creature_Crate:822858246666584094>", 
                1000, 
                5
            )
            
            self.shiny = zoo.Crate(
                zoo, 
                "shiny", 
                "75% chance of a shiny creature. Get 1 random creature",
                0x926505, 
                "https://cdn.discordapp.com/attachments/821774449459855423/822858013157228544/Shiny_Creature_Crate.png", 
                "<:Shiny_Creature_Crate:822858260709244929>", 
                10_000, 
                75
            )

            self.collectors = zoo.Crate(
                zoo, 
                "collectors",
                "75% chance of a creature that you do not have, 1% chance of a golden creature",
                0x7F0C13, 
                "https://cdn.discordapp.com/attachments/821774449459855423/822858046644289578/Collectors_Creature_Crate.png", 
                "<:Collectors_Creature_Crate:822858278219546634>", 
                25_000, 
                75
            )
        
    class Trade():

        class FromTo():
            def __init__(self, user, creature, accepted=False):
                self.userID = user 
                self.creature : str = creature 
                self.accepted = accepted
        
        class Data():
            def __init__(self, channel, message, to_message, from_message, started):
                self.channelID = channel 
                self.messageID = message 
                self.to_messageID = to_message
                self.from_messageID = from_message
                self.started = datetime.strptime(started, "%d-%b-%Y (%H:%M:%S.%f)")

        def __init__(self, id):
            with open("data/zoo/creatureTrades.json") as f:
                data = json.load(f)

            self.id = id
            id = str(id)
            self.fromData = self.FromTo(data[id]["from"]["user"], data[id]["from"]["creature"], data[id]["from"]["accepted"])
            self.toData = self.FromTo(data[id]["to"]["user"], data[id]["to"]["creature"], data[id]["to"]["accepted"])
            self.data = self.Data(data[id]["data"]["channel"], data[id]["data"]["message"], data[id]["data"]["to_message"], data[id]["data"]["from_message"], data[id]["data"]["started"])
            self.raw = data
        
        def saveData(self):

            with open("data/zoo/creatureTrades.json") as f:
                data = json.load(f)

            data[str(self.id)] = {
                "from": {
                    "user":str(self.fromData.userID), 
                    "creature":self.fromData.creature,
                    "accepted":self.fromData.accepted
                }, 
                "to":{
                    "user":str(self.toData.userID), 
                    "creature":self.toData.creature,
                    "accepted":self.toData.accepted
                }, 
                "data":{
                    "channel":str(self.data.channelID),
                    "message":str(self.data.messageID),
                    "to_message":str(self.data.to_messageID),
                    "from_message":str(self.data.from_messageID),
                    "started":self.data.started.strftime("%d-%b-%Y (%H:%M:%S.%f)")
                }
            }

            with open("data/zoo/creatureTrades.json", "w") as f:
                data = json.dump(data, f)
        
        async def end(self, reason=None):
            with open("data/zoo/creatureTrades.json") as f:
                data = json.load(f)
            del data[str(self.id)]
            with open("data/zoo/creatureTrades.json", "w") as f:
                data = json.dump(data, f)
            
            if reason != None:
                

                embed = discord.Embed(
                    title=f"~~{self.fromUser} wants to trade your {Zoo().Creature(self.toData.creature).emoji} {Zoo().Creature(self.toData.creature).readableName} for a {Zoo().Creature(self.fromData.creature).emoji} {Zoo().Creature(self.fromData.creature).readableName}!~~",
                    description=f"~~Use the reactions to accept or decline. **Both users have to accept.**~~\n\n{reason}",
                    color=var.embed
                )
                embed.set_footer(text=("2" if self.toData.accepted and self.fromData.accepted else ("1" if (self.toData.accepted or self.fromData.accepted) else "0")) + "/2")
                await self.message.edit(content=reason, embed=embed)
                try:
                    await self.fromUserMessage.edit(
                        embed=discord.Embed(
                            title=f"~~Sent trade! (#{self.id})~~",
                            description=f"~~Created trade to `{self.toUser}`!\n{self.message.jump_url}~~\n\n{reason}",
                            color=var.embedSuccess
                        )
                    )
                    await self.fromUserChannel.send(f"> Trade `#{self.id}` ended with reason: {reason}")
                except:
                    pass
                try:
                    await self.toUserMessage.edit(
                        embed=discord.Embed(
                            title=f"~~You revieved a trade! (#{self.id})~~",
                            description=f"~~You recieved a trade from `{self.fromUser}`!\n{self.message.jump_url}~~\n\n{reason}",
                            color=var.embed
                        )
                    )
                    await self.toUserChannel.send(f"> Trade `#{self.id}` ended with reason: {reason}")
                except:
                    pass
        
        async def getData(self, bot):

            self.fromUser : discord.User = bot.get_user(int(self.fromData.userID))
            self.toUser : discord.User = bot.get_user(int(self.toData.userID))

            self.fromUserClass = User(self.fromUser)
            self.toUserClass = User(self.toUser)

            self.channel : discord.TextChannel = bot.get_channel(int(self.data.channelID))
            self.message = await self.channel.fetch_message(int(self.data.messageID))

            self.fromUserChannel = None 
            self.fromUserMessage = None
            self.toUserChannel = None 
            self.toUserMessage = None

            for dmChannel in bot.private_channels:
                if dmChannel.recipient == self.fromUser:
                    self.fromUserChannel = dmChannel 
                    self.fromUserMessage = await dmChannel.fetch_message(int(self.data.from_messageID))
                
                if dmChannel.recipient == self.toUser:
                    self.toUserChannel = dmChannel 
                    self.toUserMessage = await dmChannel.fetch_message(int(self.data.to_messageID))
            
            return self

    def __init__(self):

        with open("resources/zoo/creatures.json", encoding="utf8") as f:
            data = json.load(f) 
        
        allData = {}

        allData.update(data["golden"])
        allData.update(data["rare"])
        allData.update(data["common"])
        allData.update(data["very_common"])
        
        self.creaturesRaw = data
        self.creatures = allData 
        self.creatureList = list(self.creatures)

        self.crates = self.Crates(self)
        
        self.trades : dict = None 
    
    def getTrades(self):
        with open("data/zoo/creatureTrades.json") as f:
            data = json.load(f)
        
        self.trades = data
    
    def addTrade(self, id, tradeData):

        if self.trades == None:
            self.getTrades()

        self.trades[str(id)] = tradeData 
    
    def saveTrades(self):
        with open("data/zoo/creatureTrades.json", "w") as f:
            data = json.dump(self.trades, f)

    def validateCreatureExists(self, creatureName):

        foundCreature = False
        
        for section in self.creatures:
            if creatureName in section:
                foundCreature = True
        
        if foundCreature == False:
            return Validator(foundCreature, "The creature specified does not exist")
        return Validator(True)
    
class Shop():

    def __init__(self):
        self.conversionRate = self.getConversionRate()

    def getConversionRate(self):
        date = datetime.today()

        day = date.day 
        hour = date.hour 

        if hour > day:
            randomCalc = day / hour 
        else:
            randomCalc = hour / day

        lowest = 1
        highest = 4
        final = lowest

        for i in range(10, 110, 10):
            if randomCalc * i > lowest and randomCalc * i < highest:
                final = randomCalc * i
                
        return final


class User():

    class EconomyUser():

        def __init__(self, user : discord.User, guild : discord.Guild = None):
            
            self.guild = guild
            self.userClass = user
        
        def setGuild(self, guild):
            self.guild = guild
        
        def loadBal(self, guild=None):
            if guild != None:
                self.setGuild(guild)

            r = requests.get(var.UBbase + f"/guilds/{self.guild.id}/users/{self.userClass.user.id}", headers=var.UBheaders)
            data = r.json()

            self.rank = data["rank"]

            self.cash = data["cash"]
            self.bank = data["bank"]

            self.total = data["total"]

            return self
        
        def addBal(self, cash = 0, bank = 0, guild=None):
            if guild != None:
                self.setGuild(guild)
            
            r = requests.patch(var.UBbase + f"/guilds/{self.guild.id}/users/{self.userClass.user.id}", data=json.dumps({"cash":cash, "bank":bank}), headers=var.UBheaders)
            data = r.json()

            self.cash = data["cash"]
            self.bank = data["bank"]
            self.total = data["total"]

            return self

    class ZooUser():

        def __init__(self, user):

            self.userClass = user
            self.zoo : Zoo = None

            self.creatures = None
            self.shardProducers = None
        
        def getZoo(self):
            self.zoo = Zoo()

        def getCreatures(self):

            with open("data/zoo/ownedCreatures.json") as f:
                data = json.load(f)

                self.creatures = data[str(self.userClass.user.id)] if str(self.userClass.user.id) in data else []

                return self.creatures
        
        def getShardProducers(self):

            with open("data/zoo/ownedShardProducers.json") as f:
                data = json.load(f)

            self.shardProducers = data[str(self.userClass.user.id)] if str(self.userClass.user.id) in data else {}

            return self.shardProducers
        
        def validateCreature(self, creatureName):

            if self.zoo == None:
                self.getZoo()
        
            creatureExists = self.zoo.validateCreatureExists(creatureName)

            if creatureExists.valid == False:
                return Validator(False, creatureExists.message)
            
            if self.creatures == None:
                self.getCreatures()
            
            if creatureName not in self.creatures:
                return Validator(False, "You do not own this creature")
            
            return Validator(True)
            
        def removeCreature(self, creatureName, amount=1):

            if self.creatures == None:
                self.getCreatures()
            
            if self.zoo == None:
                self.getZoo()
            
            creatureData = self.zoo.creatures[creatureName]
            
            self.creatures.remove(creatureName)

            for i in range(amount-1):
                self.creatures.remove(creatureName)

            return creatureData
        
        def addCreature(self, creatureName):

            if self.creatures == None:
                self.getCreatures()
            
            self.creatures.append(creatureName)
        
        def saveCreatures(self):
            with open("data/zoo/ownedCreatures.json") as f:
                owned = json.load(f)
            
            owned[str(self.userClass.user.id)] = self.creatures

            with open("data/zoo/ownedCreatures.json", "w") as f:
                json.dump(owned, f, indent=4) 
        
        def saveShardProducers(self):
            with open("data/zoo/ownedShardProducers.json") as f:
                owned = json.load(f)
            
            owned[str(self.userClass.user.id)] = self.shardProducers

            with open("data/zoo/ownedShardProducers.json", "w") as f:
                json.dump(owned, f, indent=4) 
        
        def refreshProducers(self):

            user = self.userClass

            if not self.shardProducers:
                self.getShardProducers()
            
            if not self.zoo:
                self.getZoo()
            
            for shardProducer in self.shardProducers:
                producer = self.zoo.ShardProducer(
                    shardProducer, 
                    self.shardProducers[shardProducer]["birthdate"], 
                    self.shardProducers[shardProducer]["level"],
                    self.shardProducers[shardProducer]["last_refreshed"]
                )

                sinceRefresh = (datetime.now() - producer.lastRefreshed).total_seconds() / 60 / 60

                while sinceRefresh >= producer.hoursForShard:
                    sinceRefresh -= producer.hoursForShard
                    self.userClass.addShards(producer.shards)

                sinceRefresh = datetime.now() - timedelta(hours=sinceRefresh)

                self.shardProducers[shardProducer]["last_refreshed"] = sinceRefresh.strftime("%d-%b-%Y (%H:%M:%S.%f)")

            self.saveShardProducers()
            

    
    def __init__(self, user : discord.User):
        
        self.user = user

        self.zoo = self.ZooUser(self)
        self.economy = self.EconomyUser(self)

        self.xp = self.getXP()
        self.shards = self.getShards()
    
    def getXP(self):
        return self.getValue("xp")
    def addXP(self, amount):
        return self.setValue("xp", amount)
    
    def getShards(self):
        return self.getValue("shards")
    def addShards(self, amount):
        return self.setValue("shards", amount)

    def getValue(self, type):
        with open(f"data/values.json") as f:
            data = json.load(f)
        setattr(self, type, 0)
        if str(self.user.id) in data:
            setattr(self, type, data[str(self.user.id)][type]) 
        return getattr(self, type)

    def setValue(self, type, amount):
        with open(f"data/values.json") as f:
            data = json.load(f)

        if str(self.user.id) not in data:
            data[str(self.user.id)] = {"xp":0, "shards":0}

        data[str(self.user.id)][type] += amount
        setattr(self, type, data[str(self.user.id)][type])

        with open(f"data/values.json", "w") as f:
            json.dump(data, f, indent=4)
        
        return getattr(self, type)

class Reward():

    def __init__(self, stars = 0, xp = 0):
        self.stars = stars 
        self.xp = xp

class QuestProgress():

    def __init__(self, quest : QuestFr, user : discord.User):
        with open(f"data/quests/{quest.name}.json") as f:
            data = json.load(f)

        started = False
        finished = False
        redeemed = False
        
        if str(user.id) in data:
            if "progress" in data[str(user.id)]:

                if "started" in data[str(user.id)]["progress"]:
                    started = data[str(user.id)]["progress"]["started"]
                
                if "finished" in data[str(user.id)]["progress"]:
                    finished = data[str(user.id)]["progress"]["finished"]

                if "redeemed" in data[str(user.id)]["progress"]:
                    redeemed = data[str(user.id)]["progress"]["redeemed"]
        
        self.started = started
        self.finished = finished 
        self.redeemed = redeemed

        self.tier = 1
        if str(user.id) in data:
            self.tier = data[str(user.id)]["tier"]
        
        self.value = 0
        if str(user.id) in data:
            self.value = data[str(user.id)]["value"]
        
        self.vcs = []
        if quest.name == "voice_channel" and str(user.id) in data and "vcs" in data[str(user.id)]:
            self.vcs = data[str(user.id)]["vcs"]
        
        self.newMembers = []
        if quest.name == "greetings" and str(user.id) in data and "newMembers" in data[str(user.id)]:
            self.newMembers = data[str(user.id)]["newMembers"]

class Quest:

    def __init__(self, name : str, description : str, tiers : int, resetOnTier : bool, required : typing.List[int], reward : typing.List[Reward], check : Coro, validate : Coro = None, start = None, tierUp = None):

        self.name = name 
        self.description = description 
        self.tiers = tiers 
        self.resetOnTier = resetOnTier
        self.required = required
        self.reward = reward

        self.check = check 

        if validate:
            self.validate = validate 

        if start:
            self.start = start 
        
        if tierUp:
            self.tierUp = tierUp
    
    def getProgress(self, user : discord.Member):

        return QuestProgress(self, user)

    def setCustom(self, user : discord.Member, name, value):

        with open(f"data/quests/{self.name}.json") as f:
            data = json.load(f)
        data[str(user.id)][name] = value
        with open(f"data/quests/{self.name}.json", "w") as f:
            json.dump(data, f, indent=4)
        return data[str(user.id)][name]

    def setValue(self, user : discord.Member, amount):

        with open(f"data/quests/{self.name}.json") as f:
            data = json.load(f)
        data[str(user.id)]["value"] = amount
        with open(f"data/quests/{self.name}.json", "w") as f:
            json.dump(data, f, indent=4)
        return data[str(user.id)]["value"]

    def addValue(self, user : discord.Member, amount):

        with open(f"data/quests/{self.name}.json") as f:
            data = json.load(f)
        data[str(user.id)]["value"] += amount
        with open(f"data/quests/{self.name}.json", "w") as f:
            json.dump(data, f, indent=4)
        return data[str(user.id)]["value"]

    def setProgress(self, user : discord.Member, values):

        with open(f"data/quests/{self.name}.json") as f:
            data = json.load(f)

        data[str(user.id)]["progress"] = {"started":values[0], "finished":values[1], "redeemed":values[2]}

        with open(f"data/quests/{self.name}.json", "w") as f:
            json.dump(data, f, indent=4)

        return data[str(user.id)]["progress"]
    

    async def check(client : ClientFr, message : discord.Message):
        pass

    async def validate(self, client : ClientFr, message : discord.Message):
        user = message.author

        if self.getProgress(user).started:
            if not self.getProgress(user).finished:
                await self.check(client, message)

    def start(self, user : discord.Member):
        with open(f"data/quests/{self.name}.json") as f:
            data = json.load(f)

        if str(user.id) not in data:
            data[str(user.id)] = {}

        data[str(user.id)]["value"] = 0
        data[str(user.id)]["progress"] = {"started": True, "finished": False, "redeemed": False}
        data[str(user.id)]["tier"] = data[str(user.id)].get("tier") or 1

        with open(f"data/quests/{self.name}.json", "w") as f:
            json.dump(data, f, indent=4)

    def tierUp(self, user : discord.Member):
        with open(f"data/quests/{self.name}.json") as f:
            data = json.load(f)

        data[str(user.id)]["value"] = 0
        data[str(user.id)]["progress"] = {"started": False, "finished": False, "redeemed": False}
        data[str(user.id)]["tier"] += 1

        with open(f"data/quests/{self.name}.json", "w") as f:
            json.dump(data, f, indent=4)

    



    async def announceFinished(self, client : ClientFr, guild : discord.Guild, user : discord.Member):

        view = discord.ui.View(timeout=None)

        class button(discord.ui.Button):

            def __init__(self, client : ClientFr, quest):
                self.quest = quest
                self.client = client

                super().__init__(style=discord.ButtonStyle.blurple, label="Redeem Quest Reward")

            async def callback(self, interaction: discord.Interaction):

                tree : app_commands.CommandTree = client.bot.tree

                if interaction.user.id != user.id:
                    return await interaction.response.send_message("You are not the initiator.", ephemeral=True)
                
                self.disabled = True

                await interaction.response.edit_message(content=f"Your redemption message can be found in <#{var.commandsChannel}>", view=self.view)

                class FakeCog():
                    def __init__(self, client : ClientFr):
                        self.client = client 
                        self.bot = client.bot
                
                class FakeCtx():
                    def __init__(self, channel : discord.TextChannel, user : discord.Member):
                        self.channel  = channel 
                        self.guild = channel.guild 
                        self.author = user 

                        self.send = channel.send


                await tree.get_command("redeem")._callback(FakeCog(self.client), FakeCtx(self.client.bot.get_channel(self.client.var.commandsChannel), user), self.quest.name)

        view.add_item(button(client=client, quest=self))

        await user.send(embed=discord.Embed(color=var.embed, title=f"You completed the **{self.name.replace('_', ' ').title()}** quest!", 
            description=f"Use **{var.prefix}redeem {self.name}** in {guild.name} to claim your reward"), view=view)
