
from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from QuestClient import Client as ClFr

import discord
import QuestClient as qc
from QuestClient import classes
import datetime


async def check(client : ClFr, message : discord.Message):
    user = message.author

    has_phrase = False

    for required_phrase in ["hi", "hello", "yo", "ayo", "welcome"]:
        if required_phrase in message.content.lower():
            has_phrase = True
    
    prog = quest.getProgress(user)

    if has_phrase:
        for member in message.mentions:
            if (datetime.datetime.now() - member.joined_at).total_seconds() < (24 * 60 * 60) and member.id not in prog.newMembers:
                prog.newMembers.append(member.id)
                messages = quest.addValue(user, 1)
                quest.setCustom(user, "newMembers", prog.newMembers)

                if messages >= quest.required[quest.getProgress(user).tier]:
                    quest.setProgress(user, [True, True, False])
                    await quest.announceFinished(client, message.author.guild, message.author)

                
quest = classes.Quest(
    name="greetings", 
    description="Mention and say hi to 5 new members", 
    tiers=1, 
    resetOnTier=True, 
    required=[None, 5], 
    reward=[None, 
        classes.Reward(5000, 3000) 
    ],
    check=check,
    amountType="members"
)
