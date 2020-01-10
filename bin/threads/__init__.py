import threading
import bin.threads.region_thread as region_thread
import bin.threads.input_thread as input_thread
import bin.threads.server_thread as server_thread
import bin.threads.stats_main_thread as stats
import json
import time

f = open("settings.json","r")
settings = json.loads(f.read())
f.close()
f = open("regions.json","r")
regions = json.loads(f.read())
f.close()
    
class vars():
    #Threadsave vars
    lock = threading.Lock()
    shutdown = False
    ratelimittimestmp1 = ratelimitcount1 = ratelimittimestmp2 = ratelimitcount2 = {"euw1":0,
        "na1":0,"kr":0,"eun1":0,"br1":0,"jp1":0,"la1":0,"la2":0,"oc1":0,"tr1":0,"ru":0}
    status = {"euw1":"running","na1":"running","kr":"running","eun1":"running","br1":"running",
               "jp1":"running","la1":"running","la2":"running","oc1":"running","tr1":"running","ru":"running"}
    stats = {"status": "running", "progress": 0, "last_duration":0}
def main(debug):
    vars()
    # Starting crawler
    for r in regions:
        region_thread.main(r,settings,debug)

    # Starting Statisticsbuilder
    stats.main(settings,debug)
    
    #Enable external input
    time.sleep(.5)
    server_thread.main(regions,settings,debug)
    
    #Enable console
    time.sleep(.5)
    input_thread.main(regions,settings,debug)

    #Shutdown routine
    while True:
        if vars.shutdown:
            break
