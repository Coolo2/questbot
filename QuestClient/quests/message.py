
from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from QuestClient import Client as ClFr

import discord, json
#from resources import questCommons as functions
#from resources import var, questData

import QuestClient as qc
from QuestClient import classes

prefixes = ["r!", "q!", "qt!", "/", ".", "^", "!", "c!"]

async def check(client : ClFr, message : discord.Message):
    user = message.author

    if True not in [message.content.lower().startswith(prefix) for prefix in prefixes]:

        messages = quest.addValue(user, 1)
        if messages >= quest.required[quest.getProgress(user).tier]:
            quest.setProgress(user, [True, True, False])
            await quest.announceFinished(client, message.author.guild, message.author)

async def validate(client : qc.Client, message : discord.Message):
    user = message.author

    if "commands" not in message.channel.name:
        if quest.getProgress(user).started:
            if not quest.getProgress(user).finished:
                await check(client, message)

                
quest = classes.Quest(
    name="message", 
    description="Send messages!", 
    tiers=6, 
    resetOnTier=True, 
    required=[None, 100, 250, 750, 1250, 2000, 3000], 
    reward=[None, 
        classes.Reward(500, 250), 
        classes.Reward(1000, 750), 
        classes.Reward(3000, 2250), 
        classes.Reward(6250, 3750), 
        classes.Reward(10_000, 7500), 
        classes.Reward(15_000, 11_250)
    ],
    check=check,
    validate=validate
)
