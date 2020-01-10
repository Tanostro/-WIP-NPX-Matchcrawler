def joinData(array,arrayInput):
    arrayInput = str(arrayInput)
    if arrayInput in array:
        array[arrayInput]= array[arrayInput] + 1
    else:
        array.update({arrayInput: 1})
    return array

def highestByWinrate(data, Pickrate):
    highestValue = 0
    highestKey = 0
    for key in data:
        if  data[key] > highestValue:
            highestKey = key
            highestValue = data[key]
    if highestKey != 0:
        returndata = {}
        try:
            returndata.update({"data": json.loads(highestKey) })
        except Exception:
            returndata.update({"data": highestKey})
        returndata.update({"timesPicked" : Pickrate[highestKey]})
        try:
            returndata.update({"winrate":  highestValue})
        except:
            returndata.update({"winrate":  0.0 })
        returndata = json.dumps(returndata)
    else:
        returndata = "[]"
    return returndata

def highestByPickrate(Winrate, data):
    highestValue = 0
    highestKey = 0
    for key in data:
        if  data[key] > highestValue:
            highestKey = key
            highestValue = data[key]
    if highestKey != 0 and highestValue > 25:
        returndata = {}
        try:
            returndata.update({"data": json.loads(highestKey) })
        except Exception:
            returndata.update({"data": highestKey})
        returndata.update({"timesPicked" : highestValue})
        try:
            returndata.update({"winrate": Winrate[highestKey] })
        except:
            returndata.update({"winrate": 0.0 })
        returndata = json.dumps(returndata)
    else:
        returndata = "[]"
    return returndata

def calcWinrate(Pickrate,Winrate,count):
    for key, value in Pickrate.items():
        try:
            Winrate[key] = round((Winrate[key] * 100) / Pickrate[key], 5)
        except KeyError:
            Winrate.update({key: 0})
        except ZeroDivisionError:
            Winrate[key] = 0
        if Pickrate[key] < count:
            del Winrate[key] 
    return Winrate
