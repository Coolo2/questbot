
from resources import questbot, var
from resources.quests import count, place, message, voiceChannel, fact, cookie, alex


class Count:

    quest = count
    name = "count"
    description = "Count in the counting channel to get rewards!"
    tiers = 6
    resetOnTier = True
    required = ["", 250, 500, 1000, 2500, 5000, 10000]
    reward = [
        "", 
        questbot.Reward(2500, 350), 
        questbot.Reward(5000, 500), 
        questbot.Reward(10_000, 700), 
        questbot.Reward(25_000, 2500), 
        questbot.Reward(50_000, 5500), 
        questbot.Reward(100_000, 10_000)
    ]

class Place:

    quest = place
    name = "place"
    description = "Place RoboTop pixels!"
    tiers = 6
    resetOnTier = True
    required = ["", 5, 15, 50, 80, 120, 200]
    reward = [
        "", 
        questbot.Reward(1000, 400), 
        questbot.Reward(2500, 750), 
        questbot.Reward(5000, 2500), 
        questbot.Reward(7500, 3000), 
        questbot.Reward(11_500, 7500), 
        questbot.Reward(20_000, 12_000)
    ]

class Message:

    quest = message
    name = "message"
    description = "Send messages"
    tiers = 6
    resetOnTier = True
    required = ["", 100, 250, 750, 1250, 2000, 3000]
    reward = [
        "", 
        questbot.Reward(500, 250), 
        questbot.Reward(1000, 750), 
        questbot.Reward(3000, 2250), 
        questbot.Reward(6250, 3750), 
        questbot.Reward(10_000, 7500), 
        questbot.Reward(15_000, 11_250)
    ]

class VoiceChannel:

    quest = voiceChannel
    name = "voice_channel"
    description = "Join every voice channel in the server"
    tiers = 1
    resetOnTier = True
    required = ["", var.voiceChannels]
    reward = [
        "", 
        questbot.Reward(2000, 500)
    ]

class Fact:

    quest = fact
    name = "fact"
    description = "Use c!fact 100 times!"
    tiers = 1
    resetOnTier = True
    required = ["", 100]
    reward = [
        "", 
        questbot.Reward(3000, 1000)
    ]

class Cookie:

    quest = cookie
    name = "cookie"
    description = "Use c!cookie 100 times!"
    tiers = 1
    resetOnTier = True
    required = ["", 100]
    reward = [
        "", 
        questbot.Reward(3000, 1000)
    ]

class Alex:

    quest = alex
    name = "alex"
    description = "Use c!alex 100 times!"
    tiers = 1
    resetOnTier = True
    required = ["", 100]
    reward = [
        "", 
        questbot.Reward(3000, 1000)
    ]