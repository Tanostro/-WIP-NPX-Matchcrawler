import bin.logging as logging
import bin.crawler as crawler
import bin.threads as threads
import bin.stats as stats

import threading

class Thread(threading.Thread):
    def __init__(self,iD, name,settings,debug):
        threading.Thread.__init__(self)
        self.iD = iD
        self.name = name
        self.settings = settings
        self.debug = debug
            
    def run(self):
        debug = self.debug
        settings = self.settings

        while threads.vars.shutdown == False:
            try:
                stats.main(settings,debug)
            except Exception as e:
                logging.log(str(e),"error")
                if debug:
                    print("Error: "+str(e))
        
def main(settings,debug):
    Thread(0,"StatsThread", settings,debug).start()
