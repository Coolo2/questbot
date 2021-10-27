
import discord, json
from resources import questCommons as functions
from resources import var, questData

import datetime

questName = "greetings"

async def check(bot, message):
    user = message.author

    has_phrase = False

    for required_phrase in ["hi", "hello", "yo", "ayo", "welcome"]:
        if required_phrase in message.content.lower():
            has_phrase = True
    
    prog = functions.getProgress(questName, user)



    if has_phrase:
        for member in message.mentions:
            if (datetime.datetime.now() - member.joined_at).total_seconds() < (24 * 60 * 60) and member.id not in prog.newMembers:
                prog.newMembers.append(member.id)
                messages = functions.addValue(questName, user, 1)
                functions.setCustom(questName, user, "newMembers", prog.newMembers)

                if messages >= questData.Greetings.required[functions.getProgress(questName, user).tier]:
                    functions.setProgress(questName, user, [True, True, False])
                    await functions.announceFinished(bot, message.author.guild, message.author, questName)

async def validate(bot, message):
    user = message.author

    if functions.getProgress(questName, user).started:
        if not functions.getProgress(questName, user).finished:
            await check(bot, message)

def start(user):
    
    with open(f"data/quests/{questName}.json") as f:
        data = json.load(f)

    data[str(user.id)] = {}

    data[str(user.id)]["value"] = 0
    data[str(user.id)]["progress"] = {"started": True, "finished": False, "redeemed": False}
    data[str(user.id)]["tier"] = 1
    data[str(user.id)]["newMembers"] = []

    with open(f"data/quests/{questName}.json", "w") as f:
        json.dump(data, f, indent=4)

def tierUp(user):
    with open(f"data/quests/{questName}.json") as f:
        data = json.load(f)

    data[str(user.id)]["value"] = 0
    data[str(user.id)]["progress"] = {"started": False, "finished": False, "redeemed": False}
    data[str(user.id)]["tier"] += 1
    data[str(user.id)]["newMembers"] = []

    with open(f"data/quests/{questName}.json", "w") as f:
        json.dump(data, f, indent=4)
                
        
