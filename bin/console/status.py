import bin.threads as threads

def main():
    status = threads.vars.status
    string = "###### Status for each region ##### \n"
    for key, value in status.items():
        string = string + "["+ str(key) + "]  " + str(value) + "\n"
    string = string + "############################"
    return string
