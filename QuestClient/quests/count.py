
from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from QuestClient import Client as ClFr

import discord, json
#from resources import questCommons as functions
#from resources import var, questData

import QuestClient as qc
from QuestClient import classes



async def check(client : ClFr, message : discord.Message):
    user = message.author

    if message.content.isdigit():
        counts = quest.addValue(user, 1)
        if counts >= quest.required[quest.getProgress(user).tier]:
            quest.setProgress(user, [True, True, False])
            await quest.announceFinished(client, message.guild, message.author)

async def validate(client : qc.Client, message : discord.Message):
    user = message.author

    if message.channel.name == 'counting':
        if quest.getProgress(user).started:
            if not quest.getProgress(user).finished:
                await check(client, message)

                
quest = classes.Quest(
    name="count", 
    description="Count in the counting channel to get rewards!", 
    tiers=6, 
    resetOnTier=True, 
    required=[None, 250, 500, 1000, 2500, 5000, 10000], 
    reward=[None, 
        classes.Reward(2500, 350), 
        classes.Reward(5000, 500), 
        classes.Reward(10_000, 700), 
        classes.Reward(25_000, 2500), 
        classes.Reward(50_000, 5500), 
        classes.Reward(100_000, 10_000)
    ],
    check=check,
    validate=validate
)
