
import discord, json
from resources import questCommons as functions
from resources import var, questData

questName = "ping_dino"

async def check(bot, message):
    user = message.author
    msg = message.content.lower()

    if "519850624939196417" in message.content:

        messages = functions.addValue(questName, user, 1)
        if messages >= questData.PingDino.required[functions.getProgress(questName, user).tier]:
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

    with open(f"data/quests/{questName}.json", "w") as f:
        json.dump(data, f, indent=4)

def tierUp(user):
    with open(f"data/quests/{questName}.json") as f:
        data = json.load(f)

    data[str(user.id)]["value"] = 0
    data[str(user.id)]["progress"] = {"started": False, "finished": False, "redeemed": False}
    data[str(user.id)]["tier"] += 1

    with open(f"data/quests/{questName}.json", "w") as f:
        json.dump(data, f, indent=4)
                
        
