import json, discord, asyncio

from resources import questData, var, questbot

miniQuests = [questData.VoiceChannel, questData.Fact, questData.Cookie, questData.Alex]
allQuests = [questData.Count, questData.Place, questData.Message, questData.VoiceChannel, questData.Fact, questData.Cookie, questData.Alex]

from discord_components import *

from bot_commands import redeem

def getProgress(quest, user):

    return questbot.QuestProgress(quest, user)

def setCustom(quest, user, name, value):

    with open(f"data/quests/{quest}.json") as f:
        data = json.load(f)
    data[str(user.id)][name] = value
    with open(f"data/quests/{quest}.json", "w") as f:
        json.dump(data, f, indent=4)
    return data[str(user.id)][name]

def setValue(quest, user, amount):

    with open(f"data/quests/{quest}.json") as f:
        data = json.load(f)
    data[str(user.id)]["value"] = amount
    with open(f"data/quests/{quest}.json", "w") as f:
        json.dump(data, f, indent=4)
    return data[str(user.id)]["value"]

def addValue(quest, user, amount):

    with open(f"data/quests/{quest}.json") as f:
        data = json.load(f)
    data[str(user.id)]["value"] += amount
    with open(f"data/quests/{quest}.json", "w") as f:
        json.dump(data, f, indent=4)
    return data[str(user.id)]["value"]

def setProgress(quest, user, values):

    with open(f"data/quests/{quest}.json") as f:
        data = json.load(f)

    data[str(user.id)]["progress"] = {"started":values[0], "finished":values[1], "redeemed":values[2]}

    with open(f"data/quests/{quest}.json", "w") as f:
        json.dump(data, f, indent=4)

    return data[str(user.id)]["progress"]

async def useMultiplier(user):
    multiplier = 1

    with open("data/multipliers.json") as f:
        m = json.load(f)

    if str(user.id) in m:
        await user.send(f"Your {m[str(user.id)]}X quest reward power up was used!")
        multiplier = m[str(user.id)]
        del m[str(user.id)]
    
    with open('data/multipliers.json', 'w') as f:
        json.dump(m, f, indent=4)  
    
    return multiplier

class FakeContext():

    def __init__(self, channel, author):
        self.channel = channel
        self.author = author
        self.guild = channel.guild

        self.send = self.channel.send

async def announceFinished(bot, guild, user, quest):

    channel = bot.get_channel(var.commandsChannel)

    button = Button(style=ButtonStyle.blue, label="Redeem Quest Reward", disabled=False, id="redeemButton")

    msg = await user.send(embed=discord.Embed(color=var.embed, title=f"You completed the **{quest.replace('_', ' ').title()}** quest!", 
        description=f"Use **{var.prefix}redeem {quest}** in {guild.name} to claim your reward"), components=[button])

    button.set_disabled(True)
    button.set_style(3)

    try:
        async def wait_loop():
            res = await bot.wait_for("button_click", timeout= 30, check = lambda i: i.custom_id == "redeemButton")

            if res.user == user:
                
                msg.embeds[0].description = f"Your redemption message can be found in <#{var.commandsChannel}>"
                await res.respond(type=7, embed=msg.embeds[0], components=[button])

                

                await redeem.redeem(bot, FakeContext(channel, user), quest, user.mention)

                
            else:
                await res.send("Nice try... You aren't the right person!")
                await wait_loop()
        await wait_loop()

    except asyncio.TimeoutError:
        await msg.edit(components=[button])
    
    

    
