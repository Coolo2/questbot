
import discord, json
from resources import questCommons as functions
from resources import var, questData

async def check(bot, message):
    user = message.author

    if message.content.isdigit():
        counts = functions.addValue("count", user, 1)
        if counts >= questData.Count.required[functions.getProgress("count", user).tier]:
            functions.setProgress("count", user, [True, True, False])
            await functions.announceFinished(bot, message.author.guild, message.author, "count")

async def validate(bot, message):
    user = message.author

    if message.channel.name == 'counting':
        if functions.getProgress("count", user).started:
            if not functions.getProgress("count", user).finished:
                await check(bot, message)

def start(user):
    
    with open(f"data/quests/count.json") as f:
        data = json.load(f)

    data[str(user.id)] = {}

    data[str(user.id)]["value"] = 0
    data[str(user.id)]["progress"] = {"started": True, "finished": False, "redeemed": False}
    data[str(user.id)]["tier"] = 1

    with open(f"data/quests/count.json", "w") as f:
        json.dump(data, f, indent=4)

def tierUp(user):
    with open(f"data/quests/count.json") as f:
        data = json.load(f)

    data[str(user.id)]["value"] = 0
    data[str(user.id)]["progress"] = {"started": False, "finished": False, "redeemed": False}
    data[str(user.id)]["tier"] += 1

    with open(f"data/quests/count.json", "w") as f:
        json.dump(data, f, indent=4)
                
        
