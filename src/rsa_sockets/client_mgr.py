import socket
from threading import Thread
import key_mgr
import msg_mgr
from src.rsa_sockets.socket_mgr import recv, send
from misc.reg_logger import reg_logger

########################################
#                Logging               #
########################################

logger = reg_logger(__name__)


########################################
#           Client functions           #
########################################

def inicialize_connection(ip, port):
    """This function creates the private keys and public keys of the user,
    after start a connection to the selected server by the given ip and port,
    when connected to server, start the interchange of information to establish a encrypted connection,
    finally start the handle_recv_client with the conn, and private key of the user"""
    address = (ip, port)

    private_key = key_mgr.gen_private_key()
    public_key = key_mgr.gen_public_key(private_key)

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect(address)
    except ConnectionRefusedError:
        logger.error('Connection failed to establish')
        return ConnectionRefusedError
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

    Thread(target=handle_recv_client, args=[conn, private_key]).start()

    return conn, username, private_key, public_key_server


def handle_recv_client(conn, private_key):
    """This function Manages the reciving messages of a connection of a instance of a client."""
    while True:
        msg = recv(conn)

        msg = msg_mgr.decrypt_msg(msg, private_key)

        print(f'Server send > {msg}')

