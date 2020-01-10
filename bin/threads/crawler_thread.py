import time
import threading
import pymysql
import bin.crawler as crawler

def main(matchid,region,ThreadCount,settings,debug):
    s = settings
    conn = pymysql.connect(user=s["mysql_user"],passwd=s["mysql_password"],host=s["mysql_host"],db=s["mysql_db"],autocommit=True)
    mysql = conn.cursor()

    c = 0
    t = [None] * ThreadCount
    while c < ThreadCount:
        t[c] = Thread( c, "T"+ str(c), region, matchid,settings,debug,mysql)
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
    conn.close()

class Thread(threading.Thread):
    def __init__(self, iD, name, region, matchid,settings,debug,mysql):
        threading.Thread.__init__(self)
        self.iD = iD
        self.name = name
        self.region = region
        self.matchid = matchid
        self.settings = settings
        self.debug = debug
        self.mysql = mysql
        
    def run(self):
        mymatchid = self.matchid + self.iD
        crawler.run(self.region,mymatchid,self.settings,self.debug,self.mysql)
