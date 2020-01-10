import socket
import time 

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_addr = ('localhost', 9090)
client_socket.connect(server_addr)

msg = (client_socket.recv(1024))
print (msg)
client_socket.send(bytes("Thorben1337", "utf8"))
time.sleep(3)

msg = (client_socket.recv(1024))
print (msg)
client_socket.send(bytes("shutdown", "utf8"))
time.sleep(3)

msg = (client_socket.recv(1024))
print (msg)
