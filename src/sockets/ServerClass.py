########################################
#                Imports               #
########################################

import socket
from threading import Thread

from Crypto.PublicKey import RSA
from pathlib import Path

from misc.DataClass import User, Chat
from misc.reg_logger import reg_logger
from encryption import SimpleRSA, SimpleAES
from sockets.socket_mgr import recv, send, bind

########################################
#                Logging               #
########################################

logger = reg_logger(__name__)


########################################
#             Server Class             #
########################################

class Server:
    """This is class created to contain all the server info and methods to simplify the process"""

    ########################################
    #              Attributes              #
    ########################################

    server_name: str  # Server Name
    private_key: RSA.RsaKey  # Server Private Key
    public_key: RSA.RsaKey  # Server Public key
    server_socket: socket  # Server socket object
    save_path: Path  # To import the server and export the server
    address: tuple  # (ip, port)

    user_dict: dict  # { username:UserClass, ... }
    chat_list: list

    ########################################
    #               Methods                #
    ########################################

    def __init__(self, server_name: str):

        self.server_name = server_name
        self.user_dict = {}
        self.save_path = Path(__file__).parent.resolve().joinpath(f'./Saves/{self.server_name}')

        if self.save_path.is_dir():
            pass  # Ask if import all existent info or delete everything.

        else:
            self.save_path.mkdir()

    def initialize(self, ip: str, port: int):

        self.address = (ip, port)

        self.server_socket = bind(self.address)

        self.private_key = SimpleRSA.gen_private_key()
        self.public_key = SimpleRSA.gen_public_key(self.private_key)

        print(f'############################### \n'
              f'Started Server at \n'
              f'IP   : {ip}     \n'
              f'Port : {port}   \n'
              f'###############################')

        Thread(target=self.listen).start()

    def listen(self):
        """This function wait for income connection and redirects them to the {handle_connection} function"""

        self.server_socket.listen()
        logger.info('Server listening...')
        while True:
            try:
                client_conn, client_addr = self.server_socket.accept()
                Thread(target=self.handle_connection, args=(client_conn, client_addr)).start()
            except OSError:
                print('Server Closed [FORCED]')
                break

    def handle_connection(self, conn: socket, addr):
        """This function is the handler of an incoming connection to the server,
        this make the necessary interchange of info to establish an encrypted connection"""

        logger.info(f'[NEW CONNECTION] {addr} connected')

        public_key = recv(conn)
        public_key = SimpleRSA.un_stringify_key(public_key)

        send(SimpleRSA.stringify_key(self.public_key), conn)

        aes_key = SimpleAES.gen_key()
        send(aes_key, conn)

        username = recv(conn, mode='AES', aes_key=aes_key)

        self.user_dict[username] = User(username, addr, conn, public_key, aes_key)

        send(self.server_name, conn, mode='AES', aes_key=aes_key)

        self.recv_handler(conn, username, aes_key)

    def recv_handler(self, conn: socket, client_username: str, aes_key):

        connected = True
        while connected:
            try:
                msg = recv(conn, mode='AES', aes_key=aes_key)

            except ConnectionResetError as e:
                return e

            except ConnectionAbortedError as e:
                return e

            if msg == '!DISCONNECT':
                connected = False
                print(f'{client_username} has disconnected')

            print(f'{client_username} > {msg}')

        conn.close()

    def stop(self) -> None:

        for username_info in self.user_dict.values():
            if username_info.conn is None:
                continue

            username_info.conn.close()
            username_info.conn = None

    def search_by_username(self, username, *args) -> tuple or None:

        """This function search the solicited information of a given user by username"""
        valid_search_args = ["username", "addr", "conn", "public_key", "aes_key"]
        search, search_result = [], []

        for arg in args:
            if arg in valid_search_args:
                search.append(arg)
            else:
                logger.error('The arg given to search was not valid, Valid search arguments:'
                             f'{valid_search_args}')

        try:
            username_info = self.user_dict[username]
            if username_info:
                info = username_info.dict()
                for key in search:
                    search_result.append(info[key])
                return search_result
            else:
                print('No information available found liked to that username')

        except KeyError:
            print('There are not a user in the database with that username')
            return

    def send_to_user(self, username, msg):

        aes_key, conn_server = self.search_by_username(username, "aes_key", "conn")
        if conn_server is not None and aes_key is not None:
            send(msg, conn_server, mode='AES', aes_key=aes_key)