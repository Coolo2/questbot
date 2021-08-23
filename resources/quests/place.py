
import discord, json
from resources import questCommons as functions
from resources import var, questData

async def check(bot, message):
    user = message.author

    if message.content.lower().startswith('r!place') or message.content.lower().startswith('r!pl'):
        
        def checkMSG(author):
            def inner_check(message):
                return message.author.name == "RoboTop"
            return inner_check

        msg = await bot.wait_for('message', check=checkMSG(message.author), timeout=5)
        fn = msg.attachments[0].filename if msg.attachments != [] else ""

        if fn  == "place.png" and True not in [item in message.content for item in ["raw", "small", "colors", "time"]]:
            counts = functions.addValue("place", user, 1)
            if counts >= questData.Place.required[functions.getProgress("place", user).tier]:
                functions.setProgress("place", user, [True, True, False])
                await functions.announceFinished(bot, message.author.guild, message.author, "place")
            else:
                pass

async def validate(bot, message):
    user = message.author

    if functions.getProgress("place", user).started:
        if not functions.getProgress("place", user).finished:
            await check(bot, message)

def start(user):
    
    with open(f"data/quests/place.json") as f:
        data = json.load(f)

    data[str(user.id)] = {}

    data[str(user.id)]["value"] = 0
    data[str(user.id)]["progress"] = {"started": True, "finished": False, "redeemed": False}
    data[str(user.id)]["tier"] = 1

    with open(f"data/quests/place.json", "w") as f:
        json.dump(data, f, indent=4)

def tierUp(user):
    with open(f"data/quests/place.json") as f:
        data = json.load(f)

    data[str(user.id)]["value"] = 0
    data[str(user.id)]["progress"] = {"started": False, "finished": False, "redeemed": False}
    data[str(user.id)]["tier"] += 1

    with open(f"data/quests/place.json", "w") as f:
        json.dump(data, f, indent=4)
                
        
