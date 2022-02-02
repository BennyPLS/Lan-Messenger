########################################
#                Imports               #
########################################

import binascii
from pathlib import Path

import Crypto
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from chromalog.mark.helpers import simple as sh

from misc.input_mgr import path_validation
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
#         Generating functions         #
########################################

def gen_private_key(
        key_length: int = 1024
) -> RSA.RsaKey:
    """
    This function generates a private key with a given key length, using the pycryptodome library.

    :param key_length:
      This value must be an integer and determine the length of the private key, by default is 2048 bytes long.
    :type key_length: int

    :return:
      This function returns an RSA.RsaKey object of the private key.
    :rtype RSA. RsaKey:
    """
    rand_gen = Crypto.Random.new().read
    private_key = RSA.generate(key_length, rand_gen)
    logger.info(f'Private key generated with length {key_length}, %s', sh.success('successfully'))

    return private_key


def gen_public_key(
        private_key: RSA.RsaKey
) -> RSA.RsaKey:
    """
    this function generates a public key with the given private key, using the pycryptodome library.

    :param private_key:
      This argument is required and need a private key object
    :type private_key: RSA.RsaKey

    :return:
      This function return an RSA.RsaKey object of the public key.
    :rtype RSA.RsaKey:
    """
    public_key = private_key.public_key()
    logger.info(f'Public key generated, %s', sh.success('successfully'))

    return public_key


########################################
#           Export functions           #
########################################

def stringify_key(
        key: RSA.RsaKey
) -> str:
    """This function export a key to a string in hexadecimal"""
    key = key.exportKey(format='PEM')
    key = binascii.hexlify(key).decode(encode_format)
    logger.info(f'Export key to hexadecimal, %s', sh.success('successfully'))
    return key


def export_key_to_file(
        key: RSA.RsaKey,
        filename: str | Path
) -> None:
    """This function export a key to a file in PEM format"""
    if not path_validation(filename, True):
        return

    with open(filename, 'wb') as f:
        f.write(key.export_key('PEM'))

    logger.info(f'Imported key to file, %s', sh.success('successfully'))


########################################
#           Import functions           #
########################################

def un_stringify_key(
        key: str
) -> RSA.RsaKey:
    """This function imports a key in hexadecimal"""
    key = RSA.importKey(binascii.unhexlify(key))
    logger.info(f'Imported key from hexadecimal, %s', sh.success('successfully'))
    return key


def import_key_from_file(
        filename: Path | str
) -> RSA.RsaKey:
    """This function imports a key from a file"""
    if not path_validation(filename):
        raise FileNotFoundError

    with open(filename, 'rb') as f:
        key = f.read()
        key = RSA.importKey(key)
    logger.info(f'Imported key from file, %s', sh.success('successfully'))
    return key


########################################
#          Encrypt  functions          #
########################################

def encrypt(
        msg: str,
        key: RSA.RsaKey
) -> bytes:
    """encrypt a str with the given key"""

    msg = msg.encode(encode_format)

    cipher = PKCS1_OAEP.new(key)
    try:
        ciphertext = cipher.encrypt(msg)

    except ValueError as e:
        logger.error('The message is too long')
        raise e

    logger.info('Text encrypted, %s', sh.success('successfully'))
    return ciphertext


def encrypt_file(
        filename: str | Path,
        key: RSA.RsaKey
) -> None:
    """Encrypts a file"""

    if not path_validation(filename):
        raise FileNotFoundError

    with open(filename, 'br') as f:
        binaries = f.read()
        cipher = PKCS1_OAEP.new(key)

        try:
            ciphertext = cipher.encrypt(binaries)

        except ValueError as e:
            logger.error('The message is too long')
            raise e

    with open(filename, 'bw') as f:
        f.write(ciphertext)

    logger.info('File encrypted, %s', sh.success('successfully'))


########################################
#          Decrypt  functions          #
########################################


def decrypt(
        ciphertext: bytes,
        key: RSA.RsaKey,
        decode: bool = True
) -> str | bytes:
    """This function decrypts a str with the given key"""

    cipher = PKCS1_OAEP.new(key)

    try:
        msg = cipher.decrypt(ciphertext)

    except ValueError as e:
        logger.error('Decrypt failed, possible incorrect key')
        raise e

    logger.info('Ciphertext decrypted, %s', sh.success('successfully'))
    if decode:
        return msg.decode(encode_format)

    else:
        return msg


def decrypt_file(
        filename: str | Path,
        key: RSA.RsaKey
) -> None:
    """This function decrypt a file content {binary} with the given key"""

    if not path_validation(filename):
        raise FileNotFoundError

    with open(filename, 'rb') as f:
        binaries = f.read()
        cipher = PKCS1_OAEP.new(key)
        ciphertext = cipher.decrypt(binaries)

    with open(filename, 'wb') as f:
        f.write(ciphertext)

    logger.info('File decrypted, %s', sh.success('successfully'))
