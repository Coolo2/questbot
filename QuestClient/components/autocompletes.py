import discord 

import QuestClient as qc 
from discord import app_commands

async def creature_autocomplete(interaction : discord.Interaction, current : str):
    zoo = qc.classes.Zoo()

    

    return [
        app_commands.Choice(name=c.replace("_", " ").title(), value=c)
        for c in zoo.creatureList if current.lower().replace("_", " ") in c.lower().replace("_", " ")
    ][:25]

async def owned_creature_autocomplete(interaction : discord.Interaction, current : str):
    

    values = interaction.namespace.__dict__
    current_name = list(values.keys())[len(list(values))-1]

    if current_name == "their_creature":
        userO : discord.User = interaction.client.get_user(values["user"].id)
    else:
        userO = interaction.user

    user = qc.classes.User(userO)
    user.zoo.creatures

    return [
        app_commands.Choice(name=c.replace("_", " ").title(), value=c)
        for c in list(dict.fromkeys(user.zoo.creatures)) if current.lower().replace("_", " ") in c.lower().replace("_", " ")
    ][:25]

async def mergeable_autocomplete(interaction : discord.Interaction, current : str):

    user = qc.classes.User(interaction.user)
    user.zoo.creatures

    return [
        app_commands.Choice(name=c.replace("_", " ").title(), value=c)
        for c in list(dict.fromkeys(user.zoo.creatures)) if user.zoo.creatures.count(c) >= 5 and current.lower().replace("_", " ") in c.lower().replace("_", " ")
    ][:25]

async def owned_shard_producers(interaction : discord.Interaction, current : str):

    user = qc.classes.User(interaction.user)
    user.zoo.getShardProducers()

    

    return [
        app_commands.Choice(name=c.replace("_", " ").title(), value=c)
        for c in list(dict.fromkeys(user.zoo.shardProducers)) if current.lower().replace("_", " ") in c.lower().replace("_", " ")
    ][:25]