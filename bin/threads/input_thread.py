import bin.threads as threads
import bin.console as console
import threading

class Thread(threading.Thread):
    def __init__(self,iD, name,regions,settings,debug):
        threading.Thread.__init__(self)
        self.iD = iD
        self.name = name
        self.settings = settings
        self.debug = debug
        self.regions = regions
            
    def run(self):
        debug = self.debug
        settings = self.settings
        r = self.regions

        while threads.vars.shutdown == False:
            inputstr = input("Console > ")
            result = console.main(inputstr)
            print(result)
            
def main(r,settings,debug):
    Thread(0,"InputThread", r,settings,debug).start()
