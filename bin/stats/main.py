import urllib.request
import urllib.error
import json
import pymysql
import bin.stats.processing as process

def main(mysql,LiveVersion,uid,entrys,ChampData,settings,debug):
    roles =["TOP","JUNGLE","MIDDLE","ADC","SUPPORT"]
    elo=["BRONZE","SILVER","GOLD","PLATINUM","PLATINUM+"]

    try:
        champ = ChampData[uid]
    except IndexError:
        champ = None
    if champ != None:
        for tier in elo:
            for role in roles:
                process.main(tier,role,champ,mysql,LiveVersion)
