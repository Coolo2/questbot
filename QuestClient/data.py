
from __future__ import annotations
import typing
from QuestClient.classes import Art, Badge
import QuestClient as qc

from discord.ext import commands
import discord
from bot_commands import buy

if typing.TYPE_CHECKING:
    from QuestClient.classes import Quest as QuestFr
    from QuestClient import Client as ClientFr
    import QuestClient as qcFr

class FakeContext():
    def __init__(self, user : discord.User, channel : discord.TextChannel):
        self.channel = channel 
        self.user = user 
        self.author = user 
        self.send = channel.send
        self.guild = channel.guild

class FakeCog():
    def __init__(self, client : ClientFr):
        self.client = client 
        self.bot = client.bot

class LevelReward():
    def __init__(self, 
                level : int, 
                stars : int = None, 
                item : str = None, 
                crate : str = None, 
                command : str = None,
                shards : int = None,
                amount : int = 1,
                badge : str = None
    ):
        self.stars = stars 
        self.shards = shards
        self.level = level
        self.item = item
        self.crate = crate
        self.command = command
        self.amount = amount
        self.badge = badge
    
    async def redeem(self, client: ClientFr, user : qcFr.classes.User, channel : discord.TextChannel):
        if self.stars:
            await user.economy.addBal(bank=self.stars, guild=qc.var.allowed_guilds[0])
            await channel.send(embed=discord.Embed(color=qc.var.embedSuccess, title="Gained Stars!", description=f"You levelled up to level {self.level} and gained {self.stars}{qc.var.currency}"))
            return True
        if self.shards:
            user.addShards(self.shards)
            await channel.send(embed=discord.Embed(color=qc.var.embedSuccess, title="Gained Shards!", description=f"You levelled up to level {self.level} and gained {self.shards}{qc.var.shards_currency}"))
            return True
        
        if self.crate:
            if self.crate == "creature":
                cost = qc.classes.Zoo().crates.creature.cost
            if self.crate == "shiny":
                cost = qc.classes.Zoo().crates.shiny.cost
            if self.crate == "collectors":
                cost = qc.classes.Zoo().crates.collectors.cost

            await user.economy.addBal(cost * self.amount)

            for i in range(self.amount):
                await buy.crate(client, FakeContext(user.user, channel), self.crate, FakeCog(client))
            return True
        
        if self.command:
            await channel.send(embed=discord.Embed(color=qc.var.embedSuccess, title="Unlocked new command!", description=f"Unlocked **{self.command}** command. Try it now!"))
        if self.badge:
            await channel.send(embed=discord.Embed(color=qc.var.embedSuccess, title="Unlocked new badge!", description=f"Unlocked **{self.badge}** badge. See your profile with **/profile**!"))

        return False
    
    @property 
    def name(self) -> str:
        if self.stars:
            return f"{self.stars} stars"
        if self.shards:
            return f"{self.shards} shards"
        if self.crate:
            return f"{self.amount} {self.crate} crate"
        if self.command:
            return f"{self.command} command"
        if self.badge:
            return f"{self.badge} badge"

class ShopItem():
    def __init__(self, name : str):
        self.name = name 
    
    def get(self, user : qcFr.User):
        pass

class Shop():

    mushroom = ShopItem("mushroom")

    def __init__(self):
        pass 
    
    @property
    def reward(self):
        return self

class StarReward():
    def __init__(self, amount : int):
        self.amount = amount 
    
    def __str__(self):
        return f"{self.amount} stars"
    
    async def redeem(self, user : qcFr.User):

        await user.economy.addBal(bank=self.amount)

questXPLevels = [None,
    StarReward(8000),
    Shop().reward.mushroom
]

profile_art : typing.Dict[str, Art] = {
    "background_2":Art("Geometry Dash Background", "Not unlockable", "background_2.png"),
    "background_3":Art("Dash background", "Not unlockable", "background_3.png"),
    "background_4":Art("Stripe background", "Not unlockable", "background_4.png"),
    "background_5":Art("Floor background", "Not unlockable", "background_5.png"),
    "background_6":Art("Cloud background", "Not unlockable", "background_6.png"),
    "banner_2":Art("Geometry Dash Banner", "Not unlockable", "banner_2.png"),
    "banner_3":Art("Dash banner", "Not unlockable", "banner_3.png"),
    "banner_4":Art("Stripe banner", "Not unlockable", "banner_4.png"),
    "banner_5":Art("Floor banner", "Not unlockable", "banner_5.png"),
    "banner_6":Art("Sky banner", "Not unlockable", "banner_6.png")
}
pa = profile_art

badges = {
    "messenger":Badge("Messenger", "Complete tier 6 of message quest", quest="message"),
    "pixel":Badge("Pixel", "Complete tier 6 of pixel quest", quest="pixel"),
    "item":Badge("Item", "Complete tier 6 of item quest", quest="item"),
    "count":Badge("Count", "Complete tier 6 of count quest", quest="count"),
    "star":Badge("Star", "Complete tier 6 of money maker quest", quest="money_maker"),
    "creature":Badge("Creature", "Complete tier 6 of creature quest", quest="creature"),
    "shard":Badge("Shard", "Complete tier 6 of shard quest", quest="shard"),
    "voice":Badge("Voice", "Complete tier 6 of voice quest", quest="voice"),
    "hoarder":Badge("Hoarder", "Complete tier 6 of hoarder quest", quest="hoarder"),
    "quest":Badge("Quest", "Complete tier 6 of quest quest", quest="quest"),
    "miniature":Badge("Miniature", "Complete all mini quests"),
    "polaris_i":Badge("Polaris I", "Reach level 3", polaris_level=3),
    "polaris_ii":Badge("Polaris II", "Reach level 5", polaris_level=5),
    "polaris_iii":Badge("Polaris III", "Reach level 10", polaris_level=10),
    "polaris_iv":Badge("Polaris IV", "Reach level 20", polaris_level=20),
    "polaris_v":Badge("Polaris V", "Reach level 30", polaris_level=30),
    "quest_i":Badge("Quest I", "Reach Quest XP level 10", quest_xp_level=10),
    "quest_ii":Badge("Quest II", "Reach Quest XP level 20", quest_xp_level=20),
    "quest_iii":Badge("Quest III", "Reach Quest XP level 30", quest_xp_level=30),
    "quest_iv":Badge("Quest IV", "Reach Quest XP level 40", quest_xp_level=40),
    "quest_v":Badge("Quest V", "Reach Quest XP level 50 (max)", quest_xp_level=50)
}

levels : typing.List[LevelReward] = [
    LevelReward(1, stars=1000),
    None,
    LevelReward(3, crate="creature"),
    LevelReward(4, stars=1500),
    LevelReward(5, command="compliment"),
    LevelReward(6, shards=3),
    LevelReward(7, stars=2000),
    LevelReward(8, crate="creature", amount=2),
    LevelReward(9, stars=3000),
    LevelReward(10, badge="Quest I"),
    LevelReward(11, shards=5),
    LevelReward(12, crate="shiny"),
    None,
    LevelReward(14, stars=5000),
]