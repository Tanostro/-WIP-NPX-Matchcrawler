import bin.logging as logging
import bin.crawler.processing as processing
import bin.threads as threads
import time

def main(data,debug,mysql,region,patch):

    # ----- Count Participants and detect averageElo----
    pid = 0
    averageElo = 0
    for participantId in data["participants"]:
        try:
            elo = data["participants"][pid]["highestAchievedSeasonTier"]
        except Exception:
            elo = "UNRANKED"
            data["participants"][pid]["highestAchievedSeasonTier"] = "UNRANKED"
        if elo == "BRONZE" or elo == "UNRAKED":
            averageElo = averageElo + 0
        elif elo == "SILVER":
            averageElo = averageElo + 400
        elif elo == "GOLD":
            averageElo = averageElo + 800
        elif elo == "PLATINUM":
            averageElo = averageElo + 1200
        else:
            averageElo = averageElo + 1600

        #process every  participation
        p = processing.main(data,debug,mysql,pid)

        try:
            if p != "No Lane" and  p != "No Rank":
                mysql.execute("INSERT INTO "+ patch +"_picks" + p)
        except Exception as e:
            logging.log("Failed database insertion ("+str(e)+")","error")
            if debug:
                print("INSERT INTO "+ patch +"_picks" + p)
        pid = pid +1
        
    averageElo = averageElo / 10
    if averageElo < 400:
        Elo = "BRONZE"
    elif averageElo >= 400 and averageElo < 800 :
        Elo = "SILVER"
    elif averageElo >= 800 and averageElo < 1200 :
        Elo = "GOLD"
    elif averageElo >= 1200 and averageElo < 1600 :
        Elo = "PLATINUM"
    elif averageElo >= 1600 :
        Elo = "PLATINUM+"
    else:
        Elo = "UNRANKED"

    # ----- Count Bans -----
    for ban in data["teams"][0]["bans"]:
        bankey = str(Elo) + "_" + str(ban["championId"])
        mysql.execute("INSERT INTO "+ patch +"_bans (idKey,championId,tier,ban) VALUES ('" + bankey + "','" + str(ban["championId"])+ "','" + Elo + "',1)" +
                        "ON DUPLICATE KEY UPDATE ban=(ban+1)" )
    for ban in data["teams"][1]["bans"]:
        bankey = str(Elo) + "_" + str(ban["championId"])
        mysql.execute("INSERT INTO "+ patch +"_bans (idKey,championId,tier,ban) VALUES ('" + bankey + "','" + str(ban["championId"])+ "','" + Elo + "',1)" +
                        "ON DUPLICATE KEY UPDATE ban=(ban+1)" )

    millis = int(round(time.time() *1000 ))
    onehour = data["gameCreation"] + 14400000
    if onehour > millis:
        if debug:
            print("reached current live games")
        threads.vars.status[region] = "waiting"
        time.sleep(14400)
        threads.vars.status[region] = "running"
