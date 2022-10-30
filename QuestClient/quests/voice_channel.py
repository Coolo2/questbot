
from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from QuestClient import Client as ClFr

import discord
from QuestClient import classes
import QuestClient as qc

async def check(client : ClFr, member : discord.Member, before : discord.VoiceState, after : discord.VoiceState):
    user = member

    progress = quest.getProgress(user)
    vcs = progress.vcs
                
    try:
        if after.channel.name not in vcs:
            vcs.append(after.channel.name)
        
            quest.setCustom(user, "vcs", vcs)
            quest.addValue(user, 1)

        if len(quest.getProgress(user).vcs) >= client.var.voiceChannels:
            quest.setProgress(user, [True, True, False])
            await quest.announceFinished(client, member.guild, member)
    except:
        pass

async def validate(client : ClFr, member, before, after):
    user = member

    if quest.getProgress(user).started:
        if not quest.getProgress(user).finished:
            await check(client, member, before, after)

quest = classes.Quest(
    name="voice_channel", 
    description="Join all the voice channels in the server", 
    tiers=1, 
    resetOnTier=True, 
    required=[None, qc.var.voiceChannels], 
    reward=[None, 
        classes.Reward(2000, 500) 
    ],
    check=check,
    validate=validate,
    amountType="VCs"
)
