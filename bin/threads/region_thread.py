import bin.logging as logging
import bin.crawler as crawler
import bin.threads as threads
import threading

class Thread(threading.Thread):
    def __init__(self,iD, name,region,settings,debug):
        threading.Thread.__init__(self)
        self.iD = iD
        self.name = name
        self.settings = settings
        self.debug = debug
        self.region = region
            
    def run(self):
        debug = self.debug
        settings = self.settings
        r = self.region

        while threads.vars.shutdown == False:
            try:
                crawler.main(r,settings,debug)
            except Exception as e:
                logging.log(str(e),"error")
                if debug:
                    print("Error: "+str(e))

        #Set status to stopped
        threads.vars.status[r["region"]] = False
        
def main(r,settings,debug):
    Thread(0,"RegionThread["+ r["region"] +"]", r,settings,debug).start()
