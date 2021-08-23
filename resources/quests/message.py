
import discord, json
from resources import questCommons as functions
from resources import var, questData

prefixes = ["r!", "q!", "qt!", "/", ".", "^", "!"]

async def check(bot, message):
    user = message.author

    if True not in [message.content.lower().startswith(prefix) for prefix in prefixes]:

        messages = functions.addValue("message", user, 1)
        if messages >= questData.Message.required[functions.getProgress("message", user).tier]:
            functions.setProgress("message", user, [True, True, False])
            await functions.announceFinished(bot, message.author.guild, message.author, "message")

async def validate(bot, message):
    user = message.author

    if "commands" not in message.channel.name:
        if functions.getProgress("message", user).started:
            if not functions.getProgress("message", user).finished:
                await check(bot, message)

def start(user):
    
    with open(f"data/quests/message.json") as f:
        data = json.load(f)

    data[str(user.id)] = {}

    data[str(user.id)]["value"] = 0
    data[str(user.id)]["progress"] = {"started": True, "finished": False, "redeemed": False}
    data[str(user.id)]["tier"] = 1

    with open(f"data/quests/message.json", "w") as f:
        json.dump(data, f, indent=4)

def tierUp(user):
    with open(f"data/quests/message.json") as f:
        data = json.load(f)

    data[str(user.id)]["value"] = 0
    data[str(user.id)]["progress"] = {"started": False, "finished": False, "redeemed": False}
    data[str(user.id)]["tier"] += 1

    with open(f"data/quests/message.json", "w") as f:
        json.dump(data, f, indent=4)
                
        
