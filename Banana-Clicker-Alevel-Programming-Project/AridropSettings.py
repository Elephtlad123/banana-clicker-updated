import random

AirdropData = {
    "Drops": {
        #code to be run, time in ms (if -1 then it is an immediate bonus such as instant bananas)
        1: ["AwardBananas((UserData['BananasPerSecond']+1)*random.randint(1800,3600))", -1],
        2: ["BoostBananasPerSecond = int(BananasPerSecond * 77)", 77000],
        3: ["BoostBananasPerSecond = int(BananasPerSecond * 777)", 7000],
        4: ["BoostBananasPerClick = int(BananasPerClick * 7)", 77000],
        5: ["BoostBananasPerClick = int(BananasPerClick * 77)", 7000],
    }
}

def GetRandomBonus():
    #return (AirdropData["Drops"][random.randint(1,len(AirdropData["Drops"]))])
    return (AirdropData["Drops"][1])