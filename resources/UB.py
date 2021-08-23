import aiohttp, discord, requests, os, json

version = "v1"
headers = {"Authorization": os.getenv("UBtoken")}
base = f"https://unbelievaboat.com/api/{version}"

class EconomyUser():

    def __init__(self, guild, user):
        
        self.guild = guild 
        self.user = user
        
    
    def loadBal(self):
        r = requests.get(base + f"/guilds/{self.guild.id}/users/{self.user.id}", headers=headers)
        data = r.json()

        self.rank = data["rank"]

        self.cash = data["cash"]
        self.bank = data["bank"]

        self.total = data["total"]

        return self
    
    def addBal(self, cash = 0, bank = 0):
        
        r = requests.patch(base + f"/guilds/{self.guild.id}/users/{self.user.id}", data=json.dumps({"cash":cash, "bank":bank}), headers=headers)
        data = r.json()

        self.cash = data["cash"]
        self.bank = data["bank"]
        self.total = data["total"]

        return self




