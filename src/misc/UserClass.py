########################################
#                Imports               #
########################################

import socket
from Crypto.PublicKey import RSA
from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    username: str
    addr: list
    conn: socket
    public_key: RSA.RsaKey
