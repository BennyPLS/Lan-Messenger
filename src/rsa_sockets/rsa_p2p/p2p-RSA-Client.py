import threading
from misc.reg_logger import reg_logger
from src import key_mgr
from src.rsa_sockets import server_mgr, client_mgr, socket_mgr
from src.rsa_sockets.rsa_p2p import input_mgr

# from misc.UserClass import User

########################################
#                Logging               #
########################################

logger = reg_logger(__name__)


def main():
    # Variables #

    server = None
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
                if not server:
                    server_ip = input_mgr.input_ip()
                    server_port = input_mgr.input_port()
                    server, server_private_key, server_thread = server_mgr.initialize_server(server_ip, server_port)
                    if server:
                        logger.info('Server initialized')
                if server:
                    logger.info('Server already on')

            case 'connect' | 'conn' | 'connect to server':
                conn_ip = input_mgr.input_ip()
                conn_port = input_mgr.input_port()
                conn, username, conn_private_key, public_key_server = client_mgr.inicialize_connection(conn_ip,
                                                                                                       conn_port)
                if conn:
                    logger.info('Successfully established connection')
                    public_key_server = key_mgr.unstringify_key(public_key_server)

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
