import urllib.request
import urllib.error
import json
import time
import bin.threads as threads
import bin.logging as logging

# --------- Settings ---------------------
f = open("settings.json","r")
settings = json.loads(f.read())
f.close()

apikey = settings["apikey"]

ratelimitscore1 = settings["ratelimit_1"]
ratelimitsec1 = 10

ratelimitscore2 = settings["ratelimit_2"]
ratelimitsec2 = 600
# ------------------------------------------

def main(typ, RegionId, var1):
    if typ == "matchdata":
        url = "https://" + RegionId + ".api.riotgames.com/lol/match/v4/matches/" + str(var1) + "?api_key=" + apikey
        
        urlavailbe = True
    elif typ == "mastery":
        url = "https://" + RegionId + ".api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/" + str(var1) + "?api_key=" + apikey
        
        urlavailbe = True
    elif typ == "matchtimeline":
        url = "https://" + RegionId + ".api.riotgames.com/lol/match/v4/timelines/by-match/" + str(var1) + "?api_key=" + apikey
        
        urlavailbe = True
    elif typ == "league":
        url = "https://" + RegionId + ".api.riotgames.com/lol/league/v4/entries/by-summoner/" + str(var1) + "?api_key=" + apikey
        return 0
        urlavailbe = True        
    else:
        urlavailbe = False

    request = None

    if urlavailbe:
        while True:
            threads.vars.lock.acquire()
            
            #ratelimit 2
            if threads.vars.ratelimittimestmp2[RegionId] < time.time():
                threads.vars.ratelimittimestmp2[RegionId] = time.time() + ratelimitsec2 + 0.5
                threads.vars.ratelimitcount2[RegionId] = 0 

            if threads.vars.ratelimitcount2[RegionId] >= ratelimitscore2 - 1 :
                print("RateLimit | wait " + str(threads.vars.ratelimittimestmp2[RegionId] - time.time()) + "s")
                try:
                    time.sleep(threads.vars.ratelimittimestmp2[RegionId] - time.time())
                except Exception as e:
                    print(str(e) + " : " +  str(threads.vars.ratelimittimestmp2[RegionId] - time.time()))
            else:
                threads.vars.ratelimitcount2[RegionId] = threads.vars.ratelimitcount2[RegionId] + 1
                #print("count2: "+str(threads.vars.ratelimitcount2[RegionId]))

            # ratelimit 1
            if threads.vars.ratelimittimestmp1[RegionId] < time.time():
                threads.vars.ratelimittimestmp1[RegionId] = time.time() + ratelimitsec1 + 0.5
                threads.vars.ratelimitcount1[RegionId] = 0
                
            if threads.vars.ratelimitcount1[RegionId] >= ratelimitscore1 - 1 :
                print("I need 2 wait " + str(threads.vars.ratelimittimestmp1[RegionId] - time.time()) + "s")
                try:
                    time.sleep(threads.vars.ratelimittimestmp1[RegionId] - time.time())
                except Exception as e:
                    print(str(e) + " : " +  str(threads.vars.ratelimittimestmp1[RegionId] - time.time()))
            else:
                threads.vars.ratelimitcount1[RegionId] = threads.vars.ratelimitcount1[RegionId] + 1
                #print("count1: "+str(threads.vars.ratelimitcount1[RegionId]))
            threads.vars.lock.release()
            try:
                request = urllib.request.urlopen(url)
            except urllib.error.HTTPError as e:
                err = e.read()
                status = e.getcode()
                headers = e.getheaders()
            else:
                status = request.getcode()
                headers = None

            if status == 200 and request != None:
                content = request.read()
                content = content.decode("utf-8")
                data  = json.loads(content)
                break
            elif status == 404:
                data = 0
                break
            elif status == 429:
                for h in headers:
                    if h[0] == "Retry-After":
                        retryAfter = int(h[1])
                        #threads.vars.retrytimestamp[RegionId] =  time.time() + retryAfter + 1
                        print("["+typ+"] Rate Limit  retry after "+ str(retryAfter) +"s")
                        break
                    else:
                        retryAfter = 60
                
                time.sleep(retryAfter + 1)
            elif status == 403:
                log("API - 403 Forbidden\n","error")
                time.sleep(6000)
            else:
                print("["+typ+"]"+str(status))
        return data
    print("API ERROR")
