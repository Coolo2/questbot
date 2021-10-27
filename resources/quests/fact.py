
import discord, json
from resources import questCommons as functions
from resources import var, questData

async def check(bot, message):
    user = message.author

    if message.content.lower().startswith("c!fact"):

        messages = functions.addValue("fact", user, 1)
        if messages >= questData.Fact.required[functions.getProgress("fact", user).tier]:
            functions.setProgress("fact", user, [True, True, False])
            await functions.announceFinished(bot, message.author.guild, message.author, "fact")

async def validate(bot, message):
    user = message.author

    if functions.getProgress("fact", user).started:
        if not functions.getProgress("fact", user).finished:
            await check(bot, message)

def start(user):
    
    with open(f"data/quests/fact.json") as f:
        data = json.load(f)

    data[str(user.id)] = {}

    data[str(user.id)]["value"] = 0
    data[str(user.id)]["progress"] = {"started": True, "finished": False, "redeemed": False}
    data[str(user.id)]["tier"] = 1

    with open(f"data/quests/fact.json", "w") as f:
        json.dump(data, f, indent=4)

def tierUp(user):
    with open(f"data/quests/fact.json") as f:
        data = json.load(f)

    data[str(user.id)]["value"] = 0
    data[str(user.id)]["progress"] = {"started": False, "finished": False, "redeemed": False}
    data[str(user.id)]["tier"] += 1

    with open(f"data/quests/fact.json", "w") as f:
        json.dump(data, f, indent=4)
                
        
