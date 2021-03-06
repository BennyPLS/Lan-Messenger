########################################
#                Imports               #
########################################

import socket
from threading import Thread
from Crypto.PublicKey import RSA

from misc.reg_logger import reg_logger
from encryption import SimpleRSA
from sockets.socket_mgr import recv, send

########################################
#                Logging               #
########################################

logger = reg_logger(__name__)


########################################
#             Client Class             #
########################################

class Client:
    ########################################
    #              Attributes              #
    ########################################

    username: str  # The Name of the client.
    private_key: RSA.RsaKey  # Client private key.
    public_key: RSA.RsaKey  # Client public key.
    aes_key: bytes  # The symmetric key shared with the server.
    conn: socket  # Socket connection with the server.

    server_address: tuple  # The server address
    server_name: str  # The server name that is connected to.
    server_key: RSA.RsaKey  # Server public key

    ########################################
    #               Methods                #
    ########################################

    def __init__(self, username, ip, port):
        self.address = (ip, port)
        self.username = username

        self.private_key = SimpleRSA.gen_private_key()
        self.public_key = SimpleRSA.gen_public_key(self.private_key)

    def initialize_connection(self):
        """This function creates the private keys and public keys of the user,
        after start a connection to the selected server by the given ip and port,
        when connected to server, start the interchange of information to establish an encrypted connection,
        finally start the handle_recv_client with the conn object, and private key of the user, and the server name"""

        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.conn.connect(self.address)

        except ConnectionRefusedError as e:
            logger.error('Connection failed to establish')
            return e

        print(f'############################### \n'
              f'Connection established with \n '
              f'IP   : {self.address[0]}     \n'
              f'Port : {self.address[1]}   \n'
              f'###############################')

        ########################################
        #       Interchange information        #
        ########################################

        send(SimpleRSA.stringify_key(self.public_key), self.conn)

        str_server_key = recv(self.conn)
        self.server_key = SimpleRSA.un_stringify_key(str_server_key)

        self.aes_key = recv(self.conn, decode=False)

        self.send_server(self.username)

        self.server_name = recv(self.conn, mode='AES', aes_key=self.aes_key)

        Thread(target=self.handle_recv).start()

    def handle_recv(self):
        """This method manages the recv operation with the connected server."""
        while True:

            try:
                msg = recv(self.conn, mode='AES', aes_key=self.aes_key)

            except ConnectionResetError as e:
                return e

            except ConnectionAbortedError as e:
                return e

            print(f'{self.server_name} > {msg}')

    def send_server(self, msg):
        """This method send a msg to the connected server of this object."""
        send(msg, self.conn, mode='AES', aes_key=self.aes_key)
