########################################
#                Imports               #
########################################

import socket
from threading import Thread

from Crypto.PublicKey import RSA

from misc.reg_logger import reg_logger
from rsa import key_mgr
from sockets.socket_mgr import recv, send

########################################
#                Logging               #
########################################

logger = reg_logger(__name__)


########################################
#           Client functions           #
########################################

def initialize_connection(ip, port):
    """This function creates the private keys and public keys of the user,
    after start a connection to the selected server by the given ip and port,
    when connected to server, start the interchange of information to establish a encrypted connection,
    finally start the handle_recv_client with the conn, and private key of the user, and the server name"""
    address = (ip, port)

    private_key = key_mgr.gen_private_key()
    public_key = key_mgr.gen_public_key(private_key)

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect(address)
    except ConnectionRefusedError:
        logger.exception('Connection failed to establish')
        return None, None, None, None, None
    print(f'############################### \n'
          f'Connection established with \n '
          f'IP   : {ip}     \n'
          f'Port : {port}   \n'
          f'###############################')

    # Interchange of information #
    # public keys, usernames #

    send(key_mgr.stringify_key(public_key), conn)

    public_key_server = recv(conn)

    username = input('Input your username: ')
    send(username, conn)

    server_name = recv(conn)

    Thread(target=handle_recv_client, args=[conn, private_key, server_name]).start()

    return conn, username, server_name, private_key, public_key_server


def handle_recv_client(conn: socket, private_key: RSA.RsaKey, server_name: str):
    """This function Manages the reciving messages of a connection of a instance of a client."""
    while True:
        msg = recv(conn, private_key)

        print(f'{server_name} > {msg}')

