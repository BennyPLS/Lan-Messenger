import key_mgr
import msg_mgr
import socket
from misc.reg_logger import reg_logger
from misc.UserClass import User
from threading import Thread
from src.rsa_sockets.socket_mgr import recv, send


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

def initialize_server(ip, port):
    """This function initializes the server,
    Binds de Ip and the port for preparation of the start of {listen} function,
    Creates the server private key,
    Initializes the Thread of {listen} function."""
    global server_private_key, server_public_key
    address = (ip, port)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(address)
    except OSError:
        logger.exception('Port in use or not available')
        return None, None

    server_private_key = key_mgr.gen_private_key()
    server_public_key = key_mgr.gen_public_key(server_private_key)

    print(f'############################### \n'
          f'Started Server at \n'
          f'IP   : {ip}     \n'
          f'Port : {port}   \n'
          f'###############################')

    server_thread = Thread(target=listen, args=[server])
    return server, server_private_key, server_thread


def listen(server: socket):
    """This function wait for income connection and redirects them to the {handle_connection} function"""
    server.listen()
    while True:
        try:
            client_conn, client_addr = server.accept()
            # noinspection PyUnusedLocal
            client = Thread(target=handle_connection, args=(client_conn, client_addr)).start()
        except OSError:
            print('Server Closed [FORCED]')
            break


# noinspection PyTypeChecker
def handle_connection(conn: socket, addr):
    """This function is the handler of an incoming connection to the server,
    this make the neccesary interchange of info """
    logger.info(f'[NEW CONNECTION] {addr} connected')

    public_key = recv(conn)
    public_key = key_mgr.unstringify_key(public_key)

    send(key_mgr.stringify_key(server_public_key), conn)

    username = recv(conn)
    userDict[username] = User(username, addr, conn, public_key)
    userDict[username] = [addr, conn, public_key]

    connected = True

    # Receiving Handler #

    while connected:
        msg = recv(conn)
        if msg is ConnectionResetError:
            connected = False
            print(f'{username} has disconnected')

        if msg is False:
            continue
        msg = msg_mgr.decrypt_msg(msg, server_private_key)

        if msg == disconnection_message:
            connected = False
            print(f'{username} has disconnected')

        print(f'{username} > {msg}')

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
