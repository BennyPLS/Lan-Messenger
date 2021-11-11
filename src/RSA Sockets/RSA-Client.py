import socket
import threading
from threading import Thread

from requests.packages import target

import socket_mgr

header = 64
encode_format = 'utf8'
disconection_message = '!DISCONECT'

server_port = 5000
server_ip = input('Enter server IP =>')

Server_conn = socket_mgr.inicialize_connection(server_ip, server_port)
recv = Thread(target=socket_mgr.recv(Server_conn)).start()

