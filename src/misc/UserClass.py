########################################
#                Imports               #
########################################

import socket
from dataclasses import dataclass

from Crypto.PublicKey import RSA


@dataclass(frozen=True)
class User:
    username: str
    addr: list
    conn: socket
    public_key: RSA.RsaKey
