########################################
#                Imports               #
########################################

import socket
from threading import Thread

from Crypto.PublicKey import RSA

from misc.UserClass import User
from misc.reg_logger import reg_logger
from rsa import key_mgr
from sockets.socket_mgr import recv, send

########################################
#                Logging               #
########################################

logger = reg_logger(__name__)

########################################
#              Server Var              #
########################################

disconnection_message = '!DISCONNECT'
userDict = {}  # { username:UserClass }
server_private_key = None
server_public_key = None


########################################
#           Server functions           #
########################################

def initialize_server(ip: str, port: int, server_name: str):
    """This function initializes the server,
    Binds de Ip and the port for preparation of the start of {listen} function,
    Creates the server private key,
    Initializes the Thread of {listen} function."""
    global server_private_key, server_public_key
    address = (ip, port)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind(address)
    except OSError:
        logger.error('Port in use or not available')
        return None, None, None

    server_private_key = key_mgr.gen_private_key()
    server_public_key = key_mgr.gen_public_key(server_private_key)

    print(f'############################### \n'
          f'Started Server at \n'
          f'IP   : {ip}     \n'
          f'Port : {port}   \n'
          f'###############################')

    server_thread = Thread(target=listen, args=[server, server_name]).start()
    return server, server_private_key, server_thread


def listen(server: socket, server_name: str):
    """This function wait for income connection and redirects them to the {handle_connection} function"""
    server.listen()
    logger.info('Server listening...')
    while True:
        try:
            client_conn, client_addr = server.accept()
            # noinspection PyUnusedLocal
            client = Thread(target=handle_connection, args=(client_conn, client_addr, server_name)).start()
        except OSError:
            print('Server Closed [FORCED]')
            break


# noinspection PyTypeChecker
def handle_connection(conn: socket, addr, server_name: str = 'Server'):
    """This function is the handler of an incoming connection to the server,
    this make the neccesary interchange of info to stablish a encrypted connection"""
    logger.info(f'[NEW CONNECTION] {addr} connected')

    public_key = recv(conn)
    public_key = key_mgr.unstringify_key(public_key)

    send(key_mgr.stringify_key(server_public_key), conn)

    username = recv(conn)
    userDict[username] = User(username, addr, conn, public_key)

    send(server_name, conn)

    p2p_recive_handler(conn, server_private_key, username)

    # connected = True
    # while connected:
    #     msg = recv(conn)
    #     if msg is ConnectionResetError:
    #         connected = False
    #         print(f'{username} has disconnected')
    #
    #     if msg is False:
    #         continue
    #     msg = msg_mgr.decrypt_msg(msg, server_private_key)
    #
    #     if msg == disconnection_message:
    #         connected = False
    #         print(f'{username} has disconnected')
    #
    #     print(f'{username} > {msg}')
    #
    # conn.close()


def p2p_recive_handler(conn: socket, rsa_key: RSA.RsaKey, client_username: str):
    connected = True
    while connected:
        msg = recv(conn, rsa_key)

        if msg == disconnection_message:
            connected = False
            print(f'{client_username} has disconnected')

        print(f'{client_username} > {msg}')

    conn.close()


########################################
#       miscellaneous  functions       #
########################################

def search_public_key_by_username(username):
    """This function search the public key of a user, by username"""
    try:
        username_info = userDict[username]
        if username_info:
            public_key = username_info.public_key
            return public_key
        else:
            print('No information available found liked to that username')

    except KeyError:
        print('There are not a user in the database with that username')


def search_conn_by_username(username):
    """This function search the conn; socket of a user, by username"""
    try:
        username_info = userDict[username]
        if username_info:
            conn = username_info.conn
            return conn
        else:
            print('No information available found liked to that username')

    except KeyError:
        print('There are not a user in the database with that username')
