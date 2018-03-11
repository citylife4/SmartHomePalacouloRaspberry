from concurrent.futures import thread

import _thread
from time import sleep

from socket_connection import socket_connection
import threading
from homedash.socket_connection.socket_connection import send_socket
from homedash.config import q

def send_open():
    global q
    to_do = "open"

    if q is not None:
        print(q.isAlive())
        while q.isAlive() :
            sleep(5)

    download_thread = threading.Thread(target=send_socket, args=(to_do,) )
    download_thread.start()
    q = download_thread


    #thread_used = download_thread

    #_thread.start_new_thread(send_socket("open"), ())
    #t1 = threading.Thread(target=send_socket("open"))  #for now
    #t1.start()
    #t1.join()