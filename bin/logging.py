import time

def init():
    f = open("logs/errorlogs.txt","a+")
    f.write("[ RESTART - "+str(time.strftime("%H:%M:%S")) + " "+ str(time.strftime("%d/%m/%Y"))+"] ################ \n")
    f.close()

def log(msg,logtype):
    if logtype == "error":
        f = open("logs/errorlogs.txt","a+")
        f.write("["+str(time.strftime("%H:%M:%S")) + " "+ str(time.strftime("%d/%m/%Y"))+"] Error:" + str(msg) + "\n")
        f.close()
    
