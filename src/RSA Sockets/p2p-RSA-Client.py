import key_mgr
import socket_mgr
from switch import Switch
from threading import Thread
import socket


# Variables #
server_ip = socket.gethostbyname(socket.gethostname())
server = None
server_port = None
conn_port = None

print('''
########################################
#          RSA Socket Client           #
########################################
''')
while True:
    entry = input(" =>")

    with Switch(entry.lower()) as case:
        if case('inicialize server', 'init server'):
            server_port = input('Input port number: ')
            try:
                server_port = int(server_port)
                if server_port < 0 or server_port is False:
                    raise ValueError
            except ValueError:
                print('The port has to be a positive integer')
            if server_port <= 49151:
                print('WARNING: You may be using a port in use or reserved')
            server, server_private_key = socket_mgr.inicialize_server(server_ip, server_port)
            if server:
                Thread(target=socket_mgr.listen, args=[server]).start()
        if case('connect', 'conn', 'connect to server'):
            conn_ip = input('Input IP address: ')
            conn_port = input('Input port number: ')
            try:
                conn_port = int(conn_port)
                if conn_port < 0 or conn_port is False:
                    raise ValueError
            except ValueError:
                print('The port has to be a positive integer')

            conn, username, conn_private_key, public_key_server = socket_mgr.inicialize_connection(conn_ip, conn_port)
            public_key_server = key_mgr.unstringify_key(public_key_server)
        if case('send msg', 'send msg to server'):
            if conn:
                msg = input('Input Message: ')

                socket_mgr.send(msg, conn, public_key_server)
            else:
                print('No active connections')
        if case('stop server', 'close server'):
            if server:
                try:
                    server.close()
                except OSError:
                    print('Server Closed [FORCED]')
        if case.default:
            print('No valid option found')
