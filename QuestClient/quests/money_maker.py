
from __future__ import annotations
import asyncio
import typing

if typing.TYPE_CHECKING:
    from QuestClient import Client as ClFr

import discord, json

import QuestClient as qc
from QuestClient import classes

async def check(client : ClFr, message : discord.Message, embed_reader : classes.EmbedReader):

    user = embed_reader.user

    unb_user = classes.User(user)

    await unb_user.economy.loadBal(message.guild)

    if str(user.id) in client.eco_totals:
        difference = unb_user.economy.total - client.eco_totals[str(user.id)]

        # BlackJack specifics
        #if "Result:" in embed_reader.embed.description :
        #    if str(embed_reader.embed.color) == "#66bb6a":
        #        difference //= 2
        #    if str(embed_reader.embed.color) == "#ff8d01":
        #        difference = 0

        if difference > 0:
            counts = quest.addValue(user, difference)
            if counts >= quest.required[quest.getProgress(user).tier]:
                quest.setProgress(user, [True, True, False])
                await quest.announceFinished(client, message.guild, user)
            await message.reply(difference)

    client.eco_totals[str(user.id)] = unb_user.economy.total 

async def validate(client : qc.Client, message : discord.Message):
    
    user = message.author

    message.reference

    if message.author.id == client.var.unb_id:
        embed_reader = classes.EmbedReader(client, message.embeds[0])
        user = embed_reader.user

        if "receive" in str(embed_reader.embed.description):
            if embed_reader.desc_mention:
                client.eco_totals[str(embed_reader.desc_mention.id)] = (await classes.User(embed_reader.desc_mention).economy.loadBal(message.guild)).total
    
        if "command" in message.channel.name and user:
            if quest.getProgress(user).started:
                if not quest.getProgress(user).finished:
                    await check(client, message, embed_reader)

                
quest = classes.Quest(
    name="money_maker", 
    description="Make money using UnbelievaBoat!", 
    tiers=6, 
    resetOnTier=True, 
    required=[None, 5000, 10000, 20000, 50000, 100000, 250000], 
    reward=[None, 
        classes.Reward(2500, 300), 
        classes.Reward(5000, 500), 
        classes.Reward(10_000, 750), 
        classes.Reward(25_000, 2500), 
        classes.Reward(50_000, 5500), 
        classes.Reward(100_000, 10_000)
    ],
    check=check,
    validate=validate
)
