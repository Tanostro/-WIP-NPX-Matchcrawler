import bin.threads as threads
import bin.console as console
import threading
import socket
import bin.logging as logging
import time

class Thread(threading.Thread):
    server_socket = None
    
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
        
        Thread.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            Thread.server_socket.bind(('localhost', settings["serverport"]))
        except Exception as e:
            logging.log(str(e),"error")
            if debug:
                print("Error: "+str(e))
        Thread.server_socket.listen(1)
        print("Rcon available on port " + str(settings["serverport"])) 
        while threads.vars.shutdown == False:
            try:
                (client_socket, addr) = Thread.server_socket.accept()
                clientthread(client_socket, addr,debug,settings)
            except Exception as e:
                error = e
                    
def main(r,settings,debug):
    Thread.consoleThread = Thread(0,"ServerThread", r,settings,debug)
    Thread.consoleThread.start()
    
def clientthread(client_socket, addr,debug,settings):
    timeout = time.time() + 10
    client_socket.send(bytes("Waiting for Password", "utf8"))
    msg = ""
    authentication = False

    #Waiting for correct password
    client_socket.send(bytes("Waiting for Password", "utf8"))
    while timeout >= time.time():
        msg = client_socket.recv(1024)
        if msg != "":
            break

    #Checking Input 
    if  msg != "":
        if  msg == bytes(settings["console_password"], "utf-8"):
            client_socket.send(bytes("Authenticated waiting for commmands", "utf8"))
            authentication = True
        else:
            client_socket.send(bytes("Wrong Password - Disconnected", "utf8"))
            client_socket.close()
            if debug:
                print("Wrong Password  " + str(addr))
    else:
        client_socket.send(bytes("Timeout - Disconnected", "utf8"))
        if debug:
            print("Failed connection with " + str(addr))
        client_socket.close()

    # Input to Console
    if authentication:
        while True:
            try:
                msg = client_socket.recv(1024)
                if msg != b'':

                    #Disable shutdown with rcon
                    msg = msg.decode("utf-8")
                    if msg.find("shutdown") == -1 and msg != "shutdown":
                        #Handle Input with console function
                        result = console.main( msg )
                        client_socket.send(bytes(result, "utf8"))
                    else:
                        #Display hint for rcon users
                        client_socket.send(bytes("Shutdown command is not available with rcon", "utf8"))
            except  Exception:
                break
                    
                    
                
