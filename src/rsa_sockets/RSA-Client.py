from threading import Thread
import socket_mgr

header = 64
encode_format = 'utf8'
disconection_message = '!DISCONECT'

server_port = 5000
server_ip = input('Enter server IP =>')

Server_conn, username = socket_mgr.inicialize_connection(server_ip, server_port)
Thread(target=socket_mgr.handle_recv_client, args=[Server_conn]).start()
Thread(target=socket_mgr.handle_send_client, args=[Server_conn]).start()
