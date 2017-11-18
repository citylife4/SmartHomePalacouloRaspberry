import fcntl
import struct
import socket
import time
import protocol
from config import interface, FOR_RASP


# create the connection and check if something is getting through
def receive_socket(threadName):
    # Create a TCP/IP socket
    sock_for_ip = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address given on the command line
    server_address = ('', 4662)
    print('starting up on %s port %s' % server_address)
    sock_for_ip.bind(server_address)
    sock_for_ip.listen(1)
    connection_for_ip, raspberry_address = sock_for_ip.accept()
    data = connection_for_ip.recv(16)
    print('received "%s"' % data)
    connection_for_ip.close()

def send_socket(threadName):
