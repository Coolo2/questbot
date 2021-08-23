
import discord, json
from resources import questCommons as functions
from resources import var, questData

async def check(bot, message):
    user = message.author
    msg = message.content.lower()

    if msg.startswith("c!cookie") or msg.startswith("c!ookie") or msg.startswith("c!c"):

        messages = functions.addValue("cookie", user, 1)
        if messages >= questData.Message.required[functions.getProgress("cookie", user).tier]:
            functions.setProgress("cookie", user, [True, True, False])
            await functions.announceFinished(bot, message.author.guild, message.author, "cookie")

async def validate(bot, message):
    user = message.author

    if functions.getProgress("cookie", user).started:
        if not functions.getProgress("cookie", user).finished:
            await check(bot, message)

def start(user):
    
    with open(f"data/quests/cookie.json") as f:
        data = json.load(f)

    data[str(user.id)] = {}

    data[str(user.id)]["value"] = 0
    data[str(user.id)]["progress"] = {"started": True, "finished": False, "redeemed": False}
    data[str(user.id)]["tier"] = 1

    with open(f"data/quests/cookie.json", "w") as f:
        json.dump(data, f, indent=4)

def tierUp(user):
    with open(f"data/quests/cookie.json") as f:
        data = json.load(f)

    data[str(user.id)]["value"] = 0
    data[str(user.id)]["progress"] = {"started": False, "finished": False, "redeemed": False}
    data[str(user.id)]["tier"] += 1

    with open(f"data/quests/cookie.json", "w") as f:
        json.dump(data, f, indent=4)
                
        
