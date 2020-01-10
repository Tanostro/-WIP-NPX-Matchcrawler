import threading
import bin.threads as threads
import bin.stats.main as stats
import bin.logging as logging
import pymysql
import sys


class Thread(threading.Thread):
    def __init__(self,iD, name, mysql,LiveVersion, uid,entrys,ChampData,settings,debug):
        threading.Thread.__init__(self)
        self.iD = iD
        self.name = name
        self.settings = settings
        self.debug = debug
        self.LiveVersion = LiveVersion
        self.uid = uid
        self.entrys = entrys
        self.ChampData = ChampData
            
    def run(self):
        debug = self.debug
        settings = self.settings
        uid = self.uid + self.iD
        LiveVersion = self.LiveVersion
        entrys = self.entrys
        ChampData = self.ChampData

        s = settings
        conn = pymysql.connect(user=s["mysql_user"],passwd=s["mysql_password"],host=s["mysql_host"],db=s["mysql_db"],autocommit=True)
        mysql = conn.cursor()
    
        try:
            stats.main(mysql,LiveVersion,uid,entrys,ChampData,settings,debug)
        except Exception as e:
            logging.log(str(e),"error")
            if debug:
                print("Error: "+str(sys.exc_info()[0]))       

def main(ThreadCount,mysql,LiveVersion,uid,entrys,ChampData,settings,debug):    
    c = 0
    t = [None] * ThreadCount
    while c < ThreadCount:
        t[c] = Thread( c, "StatsThread"+ str(c), mysql,LiveVersion, uid,entrys,ChampData,settings,debug)
        t[c].start()
        c += 1
        if c == ThreadCount:
            break

    c = 0
    while c < ThreadCount:
        t[c].join()
        c += 1
        if c == ThreadCount:
            break
