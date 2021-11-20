import socket
from threading import Thread
import socket_mgr

header = 64
port = 5000
serverip = socket.gethostbyname(socket.gethostname())

server = socket_mgr.inicialize_server(serverip, port)

listenThread = Thread(target=socket_mgr.listen(server))
listenThread.start()
ClientBase = []
