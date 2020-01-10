import time
import urllib.request
import urllib.error
import json
import pymysql
import bin.threads as threads
import bin.threads.stats_thread as stats_thread
import bin.logging as logging
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)): 
    ssl._create_default_https_context = ssl._create_unverified_context

def geturl(url):
    while True:
        try:
            request = urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            err = e.read()
            status = e.getcode()
        else:
            status = request.getcode()

        if status == 200 and request != None:
            content = request.read()
            content = content.decode("utf-8")
            return json.loads(content)
            break
        
def main(settings,debug):
    s = settings
    conn = pymysql.connect(user=s["mysql_user"],passwd=s["mysql_password"],host=s["mysql_host"],db=s["mysql_db"],autocommit=True)
    mysql = conn.cursor()
    ThreadCount = s["stats_threadcount"]
    
    while threads.vars.shutdown == False:
        begintime= time.time()

        if debug:
            print("starting new Stats cycle")
        url = "https://www.nopex.net/source/loldata/championIds.json"
        ChampData = sorted(geturl(url))
    
        # GET current Live Version
        LiveVersion = geturl("https://ddragon.leagueoflegends.com/api/versions.json")[0].split('.')
        dbVersion = LiveVersion[0] + "_" + LiveVersion[1]

        try:
            mysql.execute("SELECT COUNT('id') FROM " + dbVersion + "_picks" )
            entrys = mysql.fetchone()[0]
        except pymysql.err.ProgrammingError:
            # ----- Create Picks Table -----
            db = open("bin/stats/createdb.sql","r")
            createdb_picks = str(db.read())
            db.close()
            createdb_picks = createdb_picks.replace("%dbname%",dbVersion + "_stats")
            try:
                mysql.execute(createdb_picks)
            except pymysql.err.InternalError:
                entrys = 0
            entrys = 0
        
        # If there where not enough entrys for a good statistic return to the previous patch
        if entrys <= settings["min_stats_entrys"]:
            dbVersion = LiveVersion[0] + "_" + str(int(LiveVersion[1]) - 1)

        uid = 0
        while threads.vars.shutdown == False:
            try:
                stats_thread.main(ThreadCount,mysql,dbVersion,uid,entrys,ChampData,settings,debug)
            except Exception as e:
                logging.log(str(e),"error")
                if debug:
                    print("Error: "+str(e))    
            uid = uid + ThreadCount
            progress = round(( uid * 100 ) / len(ChampData),1)
            if progress >= 100:
                threads.vars.stats["progress"] = 0
                break
            else:
                threads.vars.stats["progress"] = progress
        endtime = time.time()
        difference = str(round(endtime- begintime))
        threads.vars.stats["last_duration"] = difference
        if debug:
            print("Finished cycle ("+ difference +" seconds)")

        # wait 4 hours before updating next cycle
        threads.vars.stats["status"] = "waiting"
        time.sleep(7200)
        threads.vars.stats["status"] = "running"

    # mark  as stopped  
    threads.vars.stats["status"] = "stopped"
