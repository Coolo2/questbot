
from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from QuestClient import Client as ClFr

import discord
from QuestClient import classes

async def check(client : ClFr, message : discord.Message):
    user = message.author
    msg = message.content.lower()

    if "519850624939196417" in message.content:

        messages = quest.addValue(user, 1)
        if messages >= quest.required[quest.getProgress(user).tier]:
            quest.setProgress(user, [True, True, False])
            await quest.announceFinished(client, message.guild, message.author)
                
quest = classes.Quest(
    name="ping_dino", 
    description="Ping dino 5 times", 
    tiers=1, 
    resetOnTier=True, 
    required=[None, 5], 
    reward=[None, 
        classes.Reward(3000, 1000) 
    ],
    check=check
)
