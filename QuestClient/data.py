
from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from QuestClient.classes import Quest as QuestFr
    from QuestClient import Client as ClientFr
    import QuestClient as qcFr

class ShopItem():
    def __init__(self, name : str):
        self.name = name 
    
    def get(self, user : qcFr.classes.User):
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
    
    async def redeem(self, user : qcFr.classes.User):

        await user.economy.addBal(bank=self.amount)

questXPLevels = [None,
    StarReward(8000),
    Shop().reward.mushroom
]