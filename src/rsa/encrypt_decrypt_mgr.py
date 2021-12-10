########################################
#                Imports               #
########################################

import binascii
from pathlib import Path

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

from misc.reg_logger import reg_logger

########################################
#                Logging               #
########################################

logger = reg_logger(__name__)

########################################
#           Global variables           #
########################################

encode_format = 'utf8'


########################################
#          Encrypt  functions          #
########################################

def encrypt_msg(msg: str, key: RSA.RsaKey):
    """decrypt an str with the given key"""
    msg = msg.encode(encode_format)
    cipher = PKCS1_OAEP.new(key)
    msg = cipher.encrypt(msg)
    msg = binascii.hexlify(msg)
    msg = str(msg)
    msg = msg[2:-1]
    return msg


def encrypt_file(filename: str or Path, key: RSA.RsaKey):
    """This function encrypts a file content with the given key"""
    if isinstance(filename, str):
        filename = Path(filename)
    try:
        filename.resolve(strict=True)

        if not filename.is_file() or not filename.parent.is_dir():
            raise FileNotFoundError

        with open(filename, 'rt') as f:
            text = f.read()
            text = text.encode(encode_format)
            cipher = PKCS1_OAEP.new(key)
            text = cipher.encrypt(text)

        with open(filename, 'wb') as f:
            f.write(text)
    
    except FileNotFoundError:
        logger.error(f"The {filename} doesn't exists")


########################################
#          Decrypt  functions          #
########################################


def decrypt_msg(msg: str, key: RSA.RsaKey):
    """This function decrypts a str with the given key"""
    if msg is not bytes:
        msg = bytes(msg, encode_format)

    msg = binascii.unhexlify(msg)
    msg = bytes(msg)
    cipher = PKCS1_OAEP.new(key)
    try:
        msg = cipher.decrypt(msg)
    except ValueError:
        logger.error('Decrypt failed, possible incorrect key')
        return None
    msg = str(msg)
    msg = msg[2:-1]
    return msg


def decrypt_file(filename: str or Path, key: RSA.RsaKey):
    """This function decrypt a file content with the given key"""
    if isinstance(filename, str):
        filename = Path(filename)
    try:
        filename.resolve(strict=True)
        if not filename.is_file():
            raise FileNotFoundError

        with open(filename, 'rb') as f:
            text = f.read()
            cipher = PKCS1_OAEP.new(key)
            text = cipher.decrypt(text)
            text = str(text)

        with open(filename, 'wt') as f:
            text = str(text)
            text = text[2:-1]
            f.write(text)

    except FileNotFoundError:
        logger.error(f"The {filename} doesn't exists")
