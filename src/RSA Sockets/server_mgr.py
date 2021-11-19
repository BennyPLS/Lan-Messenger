import key_mgr
import msg_mgr
import socket
from misc.reg_logger import reg_logger
from threading import Thread
from socket_mgr import recv, send


########################################
#                Logging               #
########################################

logger = reg_logger(__name__)
logger.info('puta')


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

    return server, server_private_key


def listen(server: socket):
    server.listen()
    while True:
        try:
            client_conn, client_addr = server.accept()
            client = Thread(target=handle_connection, args=(client_conn, client_addr)).start()
        except OSError:
            print('Server Closed [FORCED]')
            break


def handle_connection(conn: socket, addr):
    logger.info(f'[NEW CONNECTION] {addr} connected')

    public_key = recv(conn)
    public_key = key_mgr.unstringify_key(public_key)

    send(key_mgr.stringify_key(server_public_key), conn)

    username = recv(conn)
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
    try:
        username_info = userDict[username]
        if username_info:
            public_key = username_info[2]
            return public_key
        else:
            print('No information available found liked to that username')
    except KeyError:
        print('There are not a user in the database with that username')


def search_conn_by_username(username):
    username_info = userDict[username]
    if username_info:
        conn = username_info[1]
        return conn
    else:
        print('No information available found liked to that username')
