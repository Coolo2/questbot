from resources import var
import discord
import json, requests, random
from datetime import datetime, timedelta

from discord_components import *

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
        
        def getCreature(self):
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

            self.hoursForShard = [None, 24, 8, 15, 12, 8][int(self.level)]

            if self.rarity == "shiny":
                self.shards = 5
            else:
                self.shards = 1
            
    class Crates():

        def __init__(self, zoo):

            self.zoo = zoo

            self.creature = zoo.Crate(
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
                self.creature = creature 
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

            self.fromUser = bot.get_user(int(self.fromData.userID))
            self.toUser = bot.get_user(int(self.toData.userID))

            self.fromUserClass = User(self.fromUser)
            self.toUserClass = User(self.toUser)

            self.channel = bot.get_channel(int(self.data.channelID))
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
        
        self.trades = None 
    
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
    
    

class User():

    class EconomyUser():

        def __init__(self, user, guild = None):
            
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
            self.zoo = None

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
            

    
    def __init__(self, user):
        
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

    def __init__(self, quest, user):
        with open(f"data/quests/{quest}.json") as f:
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
        if quest == "voice_channel" and str(user.id) in data and "vcs" in data[str(user.id)]:
            self.vcs = data[str(user.id)]["vcs"]
        
        self.newMembers = []
        if quest == "greetings" and str(user.id) in data and "newMembers" in data[str(user.id)]:
            self.newMembers = data[str(user.id)]["newMembers"]