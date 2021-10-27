
import discord, json
from resources import questCommons as functions
from resources import var, questData

async def check(bot, message):
    user = message.author
    msg = message.content.lower()

    if msg.startswith("c!alex") or msg.startswith("c!a"):

        messages = functions.addValue("alex", user, 1)
        if messages >= questData.Alex.required[functions.getProgress("alex", user).tier]:
            functions.setProgress("alex", user, [True, True, False])
            await functions.announceFinished(bot, message.author.guild, message.author, "alex")

async def validate(bot, message):
    user = message.author

    if functions.getProgress("alex", user).started:
        if not functions.getProgress("alex", user).finished:
            await check(bot, message)

def start(user):
    
    with open(f"data/quests/alex.json") as f:
        data = json.load(f)

    data[str(user.id)] = {}

    data[str(user.id)]["value"] = 0
    data[str(user.id)]["progress"] = {"started": True, "finished": False, "redeemed": False}
    data[str(user.id)]["tier"] = 1

    with open(f"data/quests/alex.json", "w") as f:
        json.dump(data, f, indent=4)

def tierUp(user):
    with open(f"data/quests/alex.json") as f:
        data = json.load(f)

    data[str(user.id)]["value"] = 0
    data[str(user.id)]["progress"] = {"started": False, "finished": False, "redeemed": False}
    data[str(user.id)]["tier"] += 1

    with open(f"data/quests/alex.json", "w") as f:
        json.dump(data, f, indent=4)
                
        
