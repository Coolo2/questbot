import discord 

import QuestClient as qc 
from discord import app_commands

async def creature_autocomplete(interaction : discord.Interaction, current : str):
    zoo = qc.classes.Zoo()

    return [
        app_commands.Choice(name=c.name_formatted, value=c.name)
        for c in zoo.creatures if current.lower().replace("_", " ") in c.name_formatted.lower()
    ][:25]

async def owned_creature_autocomplete(interaction : discord.Interaction, current : str):
    
    values = interaction.namespace.__dict__
    current_name = list(values.keys())[len(list(values))-1]

    if current_name == "their_creature":
        userO : discord.User = interaction.client.get_user(values["user"].id)
    else:
        userO = interaction.user

    user = qc.classes.User(interaction.client.client, userO)

    return [
        app_commands.Choice(name=c.name_formatted, value=c.name)
        for c in list(dict.fromkeys(user.zoo.creatures)) if current.lower().replace("_", " ") in c.name_formatted.lower()
    ][:25]

async def mergeable_autocomplete(interaction : discord.Interaction, current : str):

    user = qc.classes.User(interaction.client.client, interaction.user)

    return [
        app_commands.Choice(name=c.name_formatted, value=c.name)
        for c in list(dict.fromkeys(user.zoo.creatures)) if user.zoo.creatures.count(c) >= 5 and current.lower().replace("_", " ") in c.name_formatted.lower()
    ][:25]

async def owned_shard_producers(interaction : discord.Interaction, current : str):

    user = qc.classes.User(interaction.client.client, interaction.user)

    return [
        app_commands.Choice(name=s.name_formatted, value=s.name)
        for s in list(dict.fromkeys(user.zoo.shard_producers)) if current.lower().replace("_", " ") in s.name_formatted.lower()
    ][:25]

async def unlockables(interaction : discord.Interaction, current : str):
    user = qc.classes.User(interaction.client.client, interaction.user)
    
    return [app_commands.Choice(name=i.role.title(), value=i.role) for i in user.unlockable_roles][:25]