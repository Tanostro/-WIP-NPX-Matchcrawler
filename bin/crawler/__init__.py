import bin.threads.crawler_thread as thread
import bin.threads as threads
import bin.apicalls as apicalls
import bin.crawler.main as m
import pymysql

def main(r,settings,debug):
    
    #load currrent matchid
    f = open("matchids/curmatchid_"+str(r["region"])+".txt","r")
    matchid = int(f.read())
    f.close()

    while threads.vars.shutdown == False:
        
        #start thread cycle
        thread.main(matchid,r["region"],r["threads"],settings,debug)

        #add matchid with  threadcount
        matchid = matchid + r["threads"]

        #save new currrent matchid
        f = open("matchids/curmatchid_"+str(r["region"])+".txt","w+")
        f.write(str(matchid))
        f.close()

def run(region,matchid,settings,debug,mysql):
    #crawl for given matchid
    data = apicalls.main("matchdata",region, matchid)

    #check for game version
    if data != 0:
        splitPatch = data["gameVersion"].split('.')
        patch = splitPatch[0] + "_" + splitPatch[1]

        try:
            mysql.execute("SELECT * FROM "+ patch +"_picks WHERE id=1")
            res = mysql.fetchone()
        except pymysql.err.ProgrammingError:
            #If Table dont exist create a new one

            # ----- Create Picks Table -----
            db = open("bin/crawler/createdb_picks.sql","r")
            createdb_picks = str(db.read())
            db.close()
            createdb_picks = createdb_picks.replace("%dbname%", patch + "_picks")
            mysql.execute(createdb_picks)
            # ----- Create Bans Table -----
            db = open("bin/crawler/createdb_bans.sql","r")
            createdb_bans = str(db.read())
            db.close()
            createdb_bans = createdb_bans.replace("%dbname%", patch + "_bans")
            mysql.execute(createdb_bans)
            db.close()

        # check if it is a ranked game
        if data["queueId"] == 420 or data["queueId"] == 440:

            # start Matchanalysis
            m.main(data,debug,mysql,region,patch)            
