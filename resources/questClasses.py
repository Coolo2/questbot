import json

class Reward():

    def __init__(self, stars = 0, xp = 0):
        self.stars = stars 
        self.xp = xp

class QuestProgress():

    def __init__(self, quest, user):
        with open(f"data/quests/{quest}.json") as f:
            data = json.load(f)

        started = False
        finished = False
        redeemed = False
        
        if str(user.id) in data:
            if "progress" in data[str(user.id)]:

                if "started" in data[str(user.id)]["progress"]:
                    started = data[str(user.id)]["progress"]["started"]
                
                if "finished" in data[str(user.id)]["progress"]:
                    finished = data[str(user.id)]["progress"]["finished"]

                if "redeemed" in data[str(user.id)]["progress"]:
                    redeemed = data[str(user.id)]["progress"]["redeemed"]
        
        self.started = started
        self.finished = finished 
        self.redeemed = redeemed

        self.tier = 1
        if str(user.id) in data:
            self.tier = data[str(user.id)]["tier"]
        
        self.value = 0
        if str(user.id) in data:
            self.value = data[str(user.id)]["value"]
        
        self.vcs = []
        if quest == "voice_channel" and str(user.id) in data and "vcs" in data[str(user.id)]:
            self.vcs = data[str(user.id)]["vcs"]