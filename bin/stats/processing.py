import pymysql
import json
import time
import bin.stats.func as f

def main(tier,role,champ,mysql,patch):
    mysql.execute("SELECT matchdata FROM " + patch + "_picks WHERE tag='"+ tier +
                  "_"+ role +"_"+ champ +"'")
    data = mysql.fetchall()

    # Set vars
    kills = deaths = assists = income = cs = wins = magicDamage = physicalDamage = trueDamage = 0
    totalDamage = redTrinket = yellowTrinket = blueTrinket = 0
    sumSpellsPickrate = sumSpellsWinrate = skillorderPickrate = skillorderWinrate = runesPickrate = {}
    runesWinrate = itemsPickrate = itemsWinrate = champsPicked = champsWins = {}

    # Handle empty sql result
    if data == ():
        return None
    
    for entry in data[0]:
        d = json.loads(entry)
        # ----- DefaultStats -----
        kills = kills + d["kills"]
        deaths = deaths + d["deaths"]
        assists = assists + d["assists"]
        income = income + d["income"]
        cs = cs + d["cs"]
        wins = wins + d["win"]

        # ----- DamageComposition -----
        magicDamage = magicDamage + d["damageComp"]["magicDamageDealtToChampions"]
        physicalDamage = physicalDamage + d["damageComp"]["physicalDamageDealtToChampions"]
        trueDamage = trueDamage + d["damageComp"]["trueDamageDealtToChampions"]
        totalDamage = totalDamage + d["damageComp"]["totalDamageDealtToChampions"]

        # ----- TrinketStats -----
        if d["ward"] == 3364:
            redTrinket = redTrinket + 1
        elif d["ward"]  == 3340:
            yellowTrinket = yellowTrinket + 1
        elif d["ward"] == 3363:
            blueTrinket = blueTrinket + 1

        # ----- sumSpells -----
        if d["sumSpell0"] > d["sumSpell1"]:
            sumSpellsPickrate = f.joinData(sumSpellsPickrate,str(d["sumSpell0"]) + "-" +str(d["sumSpell1"]))
        else:
            sumSpellsPickrate = f.joinData(sumSpellsPickrate,str(d["sumSpell1"]) + "-" +str(d["sumSpell0"]))
        if d["win"]:
            if d["sumSpell0"] > d["sumSpell1"]:
                sumSpellsWinrate = f.joinData(sumSpellsWinrate,str(d["sumSpell0"]) + "-" +str(d["sumSpell1"]))
            else:
                sumSpellsWinrate = f.joinData(sumSpellsWinrate,str(d["sumSpell1"]) + "-" +str(d["sumSpell0"]))

        # ----- Skillorder -----
        if d["skillorder"] != []:
            skillorderPickrate = f.joinData(skillorderPickrate,entry[14]) 
            if d["win"]:
               skillorderWinrate = f.joinData(skillorderWinrate,entry[14])   

        # ----- Runes -----
        runesPickrate = f.joinData(runesPickrate,d["runes"])   
        if d["win"]:
           runesWinrate = f.joinData(runesWinrate,d["runes"])   

        # ----- Items -----
        if d["itemlist"] != {}:
            itemsPickrate = f.joinData(itemsPickrate,d["itemlist"])   
            if d["win"]:
               itemsWinrate = f.joinData(itemsWinrate,d["itemlist"])     

        # ----- Champs -----
        for champion in d["ChampsPlayedAgainst"]:
            champsPicked = f.joinData(champsPicked,str(champion))
            if d["win"]:
                champsWins = f.joinData(champsWins,str(champion))   

    roleEntrys = len(data)
    picks = str(roleEntrys)
    winrate = str(round((wins * 100) / roleEntrys, 5))
    defaultStats = json.dumps({"kills": round(kills/roleEntrys), "deaths": round(deaths/roleEntrys),"assists": round(assists/roleEntrys),
                               "income": round(income/roleEntrys), "cs": round(cs/roleEntrys)})
    damageComp = json.dumps({"magicDamage": magicDamage, "physicalDamage": physicalDamage, "trueDamage":  trueDamage,
                             "totalDamage":  totalDamage})
    trinketStats = json.dumps({"redTrinket": redTrinket, "yellowTrinket": yellowTrinket, "blueTrinket": blueTrinket})

    print(json.dumps(sumSpellsPickrate))
    sumSpellcalc =  f.calcWinrate(sumSpellsPickrate,sumSpellsWinrate,50)
    skillordercalc = f.calcWinrate(skillorderPickrate,skillorderWinrate,50)
    runescalc = f.calcWinrate(runesPickrate,runesWinrate,25)
    itemscalc = f.calcWinrate(itemsPickrate,itemsWinrate,25)
    
    sumSpellsHighestPickrate = f.highestByPickrate(sumSpellcalc, sumSpellsPickrate )
    skillorderHighestPickrate = f.highestByPickrate( skillordercalc ,skillorderPickrate )
    runesHighestPickrate = f.highestByPickrate( runescalc ,runesPickrate )
    itemsHighestPickrate = f.highestByPickrate( itemscalc ,itemsPickrate )
    
    sumSpellsHighestWinrate = f.highestByWinrate( sumSpellcalc, sumSpellsPickrate )
    skillorderHighestWinrate = highestByWinrate( skillordercalc ,skillorderPickrate )
    runesHighestWinrate = highestByWinrate( runescalc ,runesPickrate )
    itemsHighestWinrate = highestByWinrate( itemscalc ,itemsPickrate )
    
    champsWinrate = f.calcWinrate(champsPicked,champsWins,50)
    champsWinrateSorted = sorted(champsWinrate, key=champsWinrate.get, reverse=True)
    champsPlayedAgainst = {}
    for r in champsWinrateSorted:
        champsPlayedAgainst.update({r: {}})
        champsPlayedAgainst[r].update({"winrate": champsWinrate[r], "timesPicked": roleEntrys})
    champsPlayedAgainst = json.dumps(champsPlayedAgainst)
     
    mysql.execute("SELECT ban FROM " + LiveVersion + "_bans WHERE championId='"+ champ +"' AND tier='"+ tier +"'")
    try:
        bans = str(mysql.fetchone()[0])
    except TypeError:
        bans = 0
    mysql.execute("SELECT SUM(ban) FROM " + LiveVersion + "_bans WHERE tier='"+  tier +"'")
    totalBans = str(mysql.fetchone()[0])
    banrate = (int(bans) * 100) / int(totalBans)
    banrate = str(round(banrate,5))

    idKey = str(tier+"_"+champ+"_"+role)

    # ----- INSERT DATA TO TABLE ------
    mysql.execute("SELECT * FROM " + LiveVersion + "_stats WHERE idKey='"+ idKey +"'")
    res = mysql.fetchone()
    lastchanged = str(time.time())
    if res == None:
        q="INSERT INTO "+ LiveVersion +"_stats (idKey,lastchanged,championId,lane,tier,winrate,picks,banrate,defaultStats,percentageStats,damageComposition,"\
                    "trinketStats,sumSpellsPickrate,sumSpellsWinrate,skillorderPickrate,skillorderWinrate,runesPickrate,runesWinrate,itemsPickrate,itemsWinrate,"\
                    "champsPlayedAgainst) VALUES ('"+ idKey +"',"+lastchanged+",'"+ champ +"','"+ role +"','"+ tier+"','"+ winrate +"','"+ picks +"','"+ banrate +"','"+ defaultStats +"','0',' "\
                    ""+ damageComp +"','"+ trinketStats +"','"+ sumSpellsHighestPickrate +"','"+ sumSpellsHighestWinrate +"','"+ skillorderHighestPickrate +"','"\
                    ""+ skillorderHighestWinrate +"','"+ runesHighestPickrate +"','"+ runesHighestWinrate +"','"+ itemsHighestPickrate +"','"+ itemsHighestWinrate +"','"\
                    ""+ champsPlayedAgainst +"')"
    else:
        q="UPDATE "+ LiveVersion +"_stats  SET championId='"+ champ +"', lastchanged='"+ lastchanged +"', lane='"+ role +"', tier='"+ tier +"', winrate='"+ winrate +"', picks='"+ picks +"'"\
                ", banrate='"+ banrate +"', defaultStats='"+ defaultStats +"', damageComposition='"+ damageComp +"', trinketStats='"+ trinketStats +"'"\
                ", sumSpellsPickrate='"+ sumSpellsHighestPickrate +"', sumSpellsWinrate='"+ sumSpellsHighestWinrate +"'"\
                ", skillorderPickrate='"+ skillorderHighestPickrate +"', skillorderWinrate='"+ skillorderHighestWinrate +"'"\
                ", runesPickrate='"+  runesHighestPickrate +"', runesWinrate='"+ runesHighestWinrate +"', itemsPickrate='"+ itemsHighestPickrate +"'"\
                ", itemsWinrate='"+ itemsHighestWinrate +"', champsPlayedAgainst='"+ champsPlayedAgainst +"' WHERE idKey='"+ idKey +"'"
    mysql.execute(q)
