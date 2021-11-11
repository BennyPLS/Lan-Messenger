import socket
from threading import Thread
import threading
import socket_mgr
import key_mgr
import msg_mgr

header = 64
port = 5000
serverip = socket.gethostbyname(socket.gethostname())

server = socket_mgr.inicialize_server(serverip, port)

listenThread = Thread(target=socket_mgr.listen(server)).start()

