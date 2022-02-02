########################################
#                Imports               #
########################################

import socket
from dataclasses import dataclass, field
from pathlib import Path
from Crypto.PublicKey import RSA

from sockets.socket_mgr import send
from misc.reg_logger import reg_logger
from misc.yaml_mgr import yaml_load, yaml_dump

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
    aes_key: bytes

    # password: str = field(init=False)
    # password_required: bool = field(init=False)

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
    User1: str  # Client username
    User2: str  # Client username
    SaveDir: Path  # Directory / filename
    History: list  # The Message History

    ########################################
    #               Methods                #
    ########################################

    def __init__(self):
        pass

    def new(self, save_path, chat_id, user1, user2):
        self.User1 = user1
        self.User2 = user2
        self.chat_id = chat_id
        self.SaveDir = save_path.joinpath(f'./{self.chat_id}/')
        self.History = []
        try:
            self.SaveDir.mkdir()
        except FileExistsError:
            logger.error(f'The {self.SaveDir} is already created')
            # ASK to substitute information

    def load(self, save_path):
        info = yaml_load(save_path)
        self.SaveDir = info['SaveDir']
        self.User1 = info['User1']
        self.User1 = info['User2']
        self.chat_id = info['chat_id']

        logger.info(f'Chat ID: {self.chat_id} loaded successfully')

    def save_chat_info(self):
        info = self.info()
        yaml_dump(self.SaveDir.joinpath(f'./Info.yaml'), info)

    def save_chat_history(self):
        yaml_dump(self.SaveDir.joinpath('History.yaml'), self.History)

    def load_chat_history(self):
        info = yaml_load(self.SaveDir.joinpath('History.yaml'))
        self.History = info['History']

    def info(self):
        return {key: value for key, value in self.__dict__.items()
                if not key.startswith('__') and not callable(key) and key != 'History'}

    def reinitialize_chat(self):
        pass