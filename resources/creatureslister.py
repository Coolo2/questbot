
import discord
import typing
from discord.ext import commands
from QuestClient import classes

async def lister( bot : typing.Union[commands.Bot, discord.client.Client]):
    string = """
from QuestClient.classes import Creature, CreatureType, CreatureCategory
import typing

creatures : typing.List[Creature] = ["""

    category_ids = [879827631955148820, 1026208728409702470, 1036290494600314880]

    for category_id in category_ids:
        category = bot.get_channel(category_id)

        for channel in category.channels:
            async for msg in channel.history(limit=100):

                split_raw : typing.List[str] = msg.content.split("\n\n")

                for raw_creautre_data in split_raw:
                    
                    cc = None
                    ct = None
                    for creature_type in classes.CreatureType.ALL:
                        if creature_type in channel.category.name.lower():
                            ct = creature_type
                    for creature_category in classes.CreatureCategory.ALL:
                        if creature_category.replace("_", "-") in channel.name.lower():
                            cc = creature_category

                    split_asterisk = raw_creautre_data.split("**")
                    name = split_asterisk[1].lower().replace(" ", "_")
                    emoji = split_asterisk[2].split("[")[0].split(" ")[1]
                    
                    quips = raw_creautre_data.split('"')[1::2]
                    string += f"""
                Creature("{name}", "{emoji}", CreatureType.{ct.upper()}, CreatureCategory.{cc.upper()}, {quips}),"""

    string += "\n]"
    

    with open("creatures_test.py", "w", encoding="utf-8") as f:
        f.write(string)
        