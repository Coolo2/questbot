
from __future__ import annotations
import asyncio
import typing

if typing.TYPE_CHECKING:
    from QuestClient import Client as ClFr

import discord, json

import QuestClient as qc
from QuestClient import classes

import random

async def check(client : ClFr, message : discord.Message, embed_reader : classes.EmbedReader):

    user = embed_reader.user
    unb_user = classes.User(client, user)

    await unb_user.economy.loadBal(message.guild)

    if str(user.id) in client.eco_totals:
        difference = unb_user.economy.total - client.eco_totals[str(user.id)]

        # BlackJack specifics
        #if "Result:" in embed_reader.embed.description :
        #    if str(embed_reader.embed.color) == "#66bb6a":
        #        difference //= 2
        #    if str(embed_reader.embed.color) == "#ff8d01":
        #        difference = 0
        unb_user.item.refresh_items()

        if difference < 0 and (
                "You were caught" in embed_reader.embed.description
                ) or (
                str(embed_reader.embed.color) == "#ef5350" and "Reply" in str(embed_reader.embed.footer.text)
            ):
            if unb_user.item.has_item(name="mask") or unb_user.item.has_item("thunder_cloud"):
                await unb_user.economy.addBal(cash=0-difference)

            if unb_user.item.has_item(name="thunder_cloud"):
                member_id : int = int(random.choice([k for k in client.eco_totals.keys() if k != str(user.id)]))
                member = message.guild.get_member(member_id)

                unb_member = classes.User(client, member)
                unb_member.economy.guild = member.guild

                await unb_member.economy.addBal(cash=difference)

                await message.reply(f"This fine was directed to {member.mention}", allowed_mentions=discord.AllowedMentions().none())


        if difference > 0:

            # Items
            boost_div = None
            if unb_user.item.has_item(name="mushroom"):
                boost_div = 2
            if unb_user.item.has_item(name="mega_mushroom"):
                boost_div = 1
            
            if "You robbed" in embed_reader.embed.description:
                if unb_user.item.has_item(name="fire_flower"):
                    boost_div = 1
                    unb_user.item.remove_item("fire_flower")
                
                members = embed_reader.description_members(message.guild)
                unb_member = classes.User(client, members[0])
                if unb_member.item.has_item(name="bubble"):
                    await unb_member.economy.addBal(cash=difference, guild=message.guild)
                    await unb_user.economy.addBal(cash=0-difference)
                    return await message.reply("Rob failed. User has a bubble!")

            if boost_div:
                await unb_user.economy.addBal(difference // boost_div)
                difference += difference // boost_div
            

            counts = quest.addValue(user, difference)
            if counts >= quest.required[quest.getProgress(user).tier]:
                quest.setProgress(user, [True, True, False])
                await quest.announceFinished(client, message.guild, user)
            await message.reply(difference)

    client.eco_totals[str(user.id)] = unb_user.economy.total 

async def validate(client : qc.Client, message : discord.Message):
    
    user = message.author

    message.reference

    if message.author.id == client.var.unb_id and len(message.embeds) > 0:
        embed_reader = classes.EmbedReader(client, message.embeds[0])
        user = embed_reader.user

        if "receive" in str(embed_reader.embed.description):
            if embed_reader.desc_mention:
                client.eco_totals[str(embed_reader.desc_mention.id)] = (await classes.User(client, embed_reader.desc_mention).economy.loadBal(message.guild)).total
    
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
