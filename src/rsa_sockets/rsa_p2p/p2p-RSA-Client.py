import key_mgr
import socket_mgr
import client_mgr
import server_mgr
from threading import Thread
import threading

from misc.reg_logger import reg_logger
# from misc.UserClass import User

########################################
#                Logging               #
########################################

logger = reg_logger(__name__, color=True)


def main():
    # Variables #

    server = None
    server_thread = None
    conn = None
    public_key_server = None

    print('''
    ########################################
    #          RSA Socket Client           #
    ########################################
    ''')
    while True:
        entry = input(" =>")

        match entry.lower():
            case 'initialize server' | 'init server':
                server_ip = input('Input Server IP address: ')
                server_port = input('Input port number: ')
                try:
                    server_port = int(server_port)
                    if server_port < 0 or server_port is False:
                        raise ValueError
                    if server_port <= 49151:
                        logger.debug('You may be using a prot in use or reserved')
                    server, server_private_key = server_mgr.initialize_server(server_ip, server_port)
                    if server:
                        server_thread = Thread(target=server_mgr.listen, args=[server])
                        server_thread.start()
                        logger.info('Server initialized')
                except ValueError:
                    print('The port has to be a positive integer')

            case 'connect' | 'conn' | 'connect to server':
                conn_ip = input('Input IP address: ')
                conn_port = input('Input port number: ')
                try:
                    conn_port = int(conn_port)
                    if conn_port < 0 or conn_port is False:
                        raise ValueError
                    conn, username, conn_private_key, public_key_server = client_mgr.inicialize_connection(conn_ip,
                                                                                                           conn_port)
                    logger.info('Successfully established connection')
                    public_key_server = key_mgr.unstringify_key(public_key_server)
                except ValueError:
                    print('The port has to be a positive integer')

            case 'send msg to server' | 'sms':
                if conn:
                    msg = input('Input Message: ')

                    socket_mgr.send(msg, conn, public_key_server)
                else:
                    print('No active connections')

            case 'stop server' | 'close server':
                if server:
                    try:
                        server.close()
                    except OSError:
                        print('Server Closed [FORCED]')

            case 'send msg to a client' | 'smc':
                username = input('Input the username: ')
                pubkey_client = server_mgr.search_public_key_by_username(username)
                conn = server_mgr.search_conn_by_username(username)
                msg = input('Input Message: ')
                socket_mgr.send(msg, conn, pubkey_client)

            case 'threads':
                print(threading.active_count())

            case 'exit':
                exit()

            case _:
                print('No valid option found')


if __name__ == '__main__':
    main()
