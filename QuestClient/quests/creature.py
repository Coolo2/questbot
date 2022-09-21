
from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from QuestClient import Client as ClFr

import discord, json

import QuestClient as qc
from QuestClient import classes


async def check(client : ClFr, user : discord.Member):

    clUser = classes.User(user)
    

    counts = quest.setValue(user, len(clUser.zoo.creatures))
    if counts >= quest.required[quest.getProgress(user).tier]:
        quest.setProgress(user, [True, True, False])
        await quest.announceFinished(client, user.guild, user)

                
quest = classes.Quest(
    name="creature", 
    description="Collect zoo creatures!", 
    tiers=6, 
    resetOnTier=True, 
    required=[None, 5, 20, 50, 100, 150, 200], 
    reward=[None, 
        classes.Reward(2500, 350), 
        classes.Reward(5000, 500), 
        classes.Reward(10_000, 700), 
        classes.Reward(25_000, 2500), 
        classes.Reward(50_000, 5500), 
        classes.Reward(100_000, 10_000)
    ],
    check=check
)
