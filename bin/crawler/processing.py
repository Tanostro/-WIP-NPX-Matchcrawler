import json
import bin.apicalls as apicalls

def main(matchdata,debug,mysql,pid):
    participantId = pid + 1
    data = {"champId":"","region":"","tier":"","lane":"","sumSpell0":"","sumSpell1":"","kills":"","deaths":"",
            "assists":"","income":"","cs":"","itemlist":"","ward":"","skillorder":"","win":"","DamageComp":"",
            "runes":"","ChampsPlayedAgainst":"","gameDuration":""}   

    # Set data to matchdata
    matchId = matchdata["gameId"]
    summonerId = matchdata["participantIdentities"][pid]["player"]["summonerId"]
    data["lane"] = matchdata["participants"][pid]["timeline"]["lane"]
    data["champId"] = matchdata["participants"][pid]["championId"]
    data["region"] = region = matchdata["platformId"].lower()
    data["sumSpell0"] = matchdata["participants"][pid]["spell1Id"]
    data["sumSpell1"] = matchdata["participants"][pid]["spell2Id"]
    data["kills"] = matchdata["participants"][pid]["stats"]["kills"]
    data["deaths"] = matchdata["participants"][pid]["stats"]["deaths"]
    data["assists"] = matchdata["participants"][pid]["stats"]["assists"]
    data["income"] = matchdata["participants"][pid]["stats"]["goldEarned"]
    data["cs"] = matchdata["participants"][pid]["stats"]["totalMinionsKilled"]
    data["ward"] = matchdata["participants"][pid]["stats"]["item6"]
    data["win"] = matchdata["participants"][pid]["stats"]["win"]
    data["gameDuration"] = matchdata["gameDuration"]
    
    # Set Role
    if data["lane"]  == "BOT"  or  data["lane"]  == "BOTTOM":
        if matchdata["participants"][pid]["timeline"]["role"] == "DUO_CARRY":
            data["lane"] =  "ADC"
        elif matchdata["participants"][pid]["timeline"]["role"] == "DUO_SUPPORT":
            data["lane"] =  "SUPPORT"
        else:
             data["lane"] =  "NONE"

    # Set Ranked Tier
    try:
        data["tier"] = matchdata["participants"][pid]["highestAchievedSeasonTier"]
    except KeyError:
        data["tier"] = "NONE"

    # Set Itemlist
    data["itemlist"] = {"item0":"","item1":"","item2":"","item3":"","item4":"",
                    "item5":""}
    i = 0
    failBuild  = False 
    while i < 6:
        if matchdata["participants"][pid]["stats"]["item"+str(i)] == 0:
            failBuild = True
        data["itemlist"]["item"+str(i)] = matchdata["participants"][pid]["stats"]["item"+str(i)]
        i = i + 1
    if failBuild:
        data["itemlist"]= []

    # Set Skillorder
    data["skillorder"] = []
    if matchdata["participants"][pid]["stats"]["champLevel"] >= 18:
        matchtimeline = apicalls.main("matchtimeline",region, matchId)
        for frame in matchtimeline["frames"]:
            try:
                for event in frame["events"]:
                    if event["type"] == "SKILL_LEVEL_UP" and event["participantId"] == participantId:
                        data["skillorder"].append(event["skillSlot"])
                        break
            except Exception as e:
                LastError = e
                print(e)
    if len(data["skillorder"]) != 18 :
        data["skillorder"] = []

    # Set damageComp
    data["damageComp"] = {"magicDamageDealtToChampions":"","physicalDamageDealtToChampions":"",
                            "trueDamageDealtToChampions":"","totalDamageDealtToChampions":""}
    data["damageComp"]["magicDamageDealtToChampions"] = matchdata["participants"][pid]["stats"]["magicDamageDealtToChampions"]
    data["damageComp"]["physicalDamageDealtToChampions"] = matchdata["participants"][pid]["stats"]["physicalDamageDealtToChampions"]
    data["damageComp"]["trueDamageDealtToChampions"] = matchdata["participants"][pid]["stats"]["trueDamageDealtToChampions"]
    data["damageComp"]["totalDamageDealtToChampions"] = matchdata["participants"][pid]["stats"]["totalDamageDealtToChampions"]

    # Set runes
    data["runes"] = [matchdata["participants"][pid]["stats"]["perk0"], matchdata["participants"][pid]["stats"]["perk1"],
                         matchdata["participants"][pid]["stats"]["perk2"], matchdata["participants"][pid]["stats"]["perk3"],
                         matchdata["participants"][pid]["stats"]["perk4"], matchdata["participants"][pid]["stats"]["perk5"],
                         matchdata["participants"][pid]["stats"]["statPerk0"], matchdata["participants"][pid]["stats"]["statPerk1"],
                         matchdata["participants"][pid]["stats"]["statPerk2"]]

    # Set champsPlayedAgainst
    if matchdata["participants"][pid]["teamId"] == 100:
        data["ChampsPlayedAgainst"] = [ matchdata["participants"][5]["championId"],
                                            matchdata["participants"][6]["championId"], matchdata["participants"][7]["championId"],
                                            matchdata["participants"][8]["championId"], matchdata["participants"][9]["championId"] ]
    else:
        data["ChampsPlayedAgainst"] = [ matchdata["participants"][0]["championId"],
                                            matchdata["participants"][1]["championId"], matchdata["participants"][2]["championId"],
                                            matchdata["participants"][3]["championId"], matchdata["participants"][4]["championId"] ]

    # Format data for return string
    matchdata = json.dumps(data)
    returnstr = "(tag, region, matchId, summonerId, matchdata ) VALUES ("
    returnstr = returnstr + "'" + str(data["tier"])+ "_" + str(data["lane"])+ "_" + str(data["champId"]) + "',"
    returnstr = returnstr + "'" + str(region) + "',"
    returnstr = returnstr + "'" + str(matchId) + "',"
    returnstr = returnstr + "'" + str(summonerId) + "',"
    returnstr = returnstr + "'" + str(matchdata) +  "')"

    if data["lane"] == "NONE":
        return "No Lane"
    elif data["tier"] == "UNRANKED":
        return "No Rank"
    else:
        return returnstr 
