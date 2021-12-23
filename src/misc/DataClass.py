########################################
#                Imports               #
########################################

import socket
from dataclasses import dataclass, field
from pathlib import Path

from misc.reg_logger import reg_logger
from Crypto.PublicKey import RSA

from sockets.socket_mgr import send

########################################
#                Logging               #
########################################

logger = reg_logger(__name__)


########################################
#              UserClass               #
########################################


@dataclass
class User:
    """This class stores and manages the user data."""

    ########################################
    #              Attributes              #
    ########################################

    username: str
    addr: tuple
    conn: socket or None
    public_key: RSA.RsaKey

    ########################################
    #               Methods                #
    ########################################

    def conn_close(self):
        send('The Server has closed the connection', self.conn, self.public_key)
        self.conn.close()

    def dict(self):
        return {key: value for key, value in self.__dict__.items() if not key.startswith('__') and not callable(key)}

    # def change_password(self, new_password):
    #     if self.password != new_password:
    #         self.password = new_password
    #     else:
    #         logger.warning(f'The new password matches the old password. No changes will be made')


########################################
#              ChatClass               #
########################################


@dataclass(init=False)
class Chat:
    """This class stores and manages the chat data and methods."""

    ########################################
    #              Attributes              #
    ########################################

    chat_id: int
    User1: str  # Server username
    User2: str  # Client username
    SaveDir: Path  # Directory / filename
    History: list  # The Message History

    ########################################
    #               Methods                #
    ########################################

    def __init__(self):
        pass

    def new(self, save_path, chat_id, user1, user2):
        self.SaveDir = save_path.joinpath(f'/{self.chat_id}.yaml')
        self.User1 = user1
        self.User2 = user2
        self.chat_id = chat_id
        self.History = []

    def load(self, save_path):
        # Load Info from YAML file
        pass

    def save_chat_history(self):
        pass

    def reinitialize_chat(self):
        pass
