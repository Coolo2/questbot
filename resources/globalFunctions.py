import json

def getXP(user):
    
    with open(f"data/xp.json") as f:
        data = json.load(f)

    balance = 0

    if str(user.id) in data:
        balance = data[str(user.id)]
    
    return balance

def addXP(user, amount):
    
    with open(f"data/xp.json") as f:
        data = json.load(f)

    if str(user.id) not in data:
        data[str(user.id)] = 0
        
    data[str(user.id)] += amount

    with open(f"data/xp.json", "w") as f:
        json.dump(data, f, indent=4)
    
    return data[str(user.id)]