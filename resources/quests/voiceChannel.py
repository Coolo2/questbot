
import discord, json
from resources import questCommons as functions
from resources import var, questData


async def check(bot, member, before, after):
    user = member

    progress = functions.getProgress("voice_channel", user)

    vcs = progress.vcs
                
    try:
        print(member.name + " Just joined channel " + after.channel.name)
        if after.channel.name not in vcs:
            vcs.append(after.channel.name)
        
        functions.setCustom("voice_channel", user, "vcs", vcs)
        functions.addValue("voice_channel", user, 1)

        if len(functions.getProgress("voice_channel", user).vcs) >= var.voiceChannels:
            functions.setProgress("voice_channel", user, [True, True, False])
            await functions.announceFinished(bot, member.guild, member, "voice_channel")
    except:
        print(member.name + " Just left channel " + before.channel.name)

async def validate(bot, member, before, after):
    user = member

    if functions.getProgress("voice_channel", user).started:
        if not functions.getProgress("voice_channel", user).finished:
            await check(bot, member, before, after)

def start(user):
    
    with open(f"data/quests/voice_channel.json") as f:
        data = json.load(f)

    data[str(user.id)] = {}

    data[str(user.id)]["vcs"] = []
    data[str(user.id)]["value"] = 0
    data[str(user.id)]["progress"] = {"started": True, "finished": False, "redeemed": False}
    data[str(user.id)]["tier"] = 1

    with open(f"data/quests/voice_channel.json", "w") as f:
        json.dump(data, f, indent=4)

def tierUp(user):
    with open(f"data/quests/voice_channel.json") as f:
        data = json.load(f)

    data[str(user.id)]["vcs"] = []
    data[str(user.id)]["value"] = 0
    data[str(user.id)]["progress"] = {"started": False, "finished": False, "redeemed": False}
    data[str(user.id)]["tier"] += 1

    with open(f"data/quests/voice_channel.json", "w") as f:
        json.dump(data, f, indent=4)
                
        
