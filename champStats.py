import bin.threads as threads
import bin.logging as logging

version = 1.3
debug = True

print("Version 1.3")

#start logging
logging.init()

#start main
threads.main(debug)
