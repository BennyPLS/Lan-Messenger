import key_mgr
import socket_mgr
from switch import Switch
from threading import Thread


def main():
    # Variables #
    server_ip = None
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
                server_ip = input('Input Server IP address: ')
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

                conn, username, conn_private_key, public_key_server = socket_mgr.inicialize_connection(conn_ip,
                                                                                                       conn_port)
                public_key_server = key_mgr.unstringify_key(public_key_server)
            if case('send msg to server', 'sms'):
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
            if case('send msg to a client', 'smc'):
                username = input('Input the username: ')
                pubkey_client = socket_mgr.search_public_key_by_username(username)
                conn = socket_mgr.search_conn_by_username(username)
                msg = input('Input Message: ')
                socket_mgr.send(msg, conn, pubkey_client)
            if case.default:
                print('No valid option found')


if __name__ == '__main__':
    main()
