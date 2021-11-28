import binascii
from pathlib import Path
from chromalog.mark.helpers import simple as sh
from src.misc.reg_logger import reg_logger
import Crypto
from Crypto.PublicKey import RSA

########################################
#                Logging               #
########################################

logger = reg_logger(__name__)


########################################
#         Generating functions         #
########################################

def gen_private_key(key_length: int = 2048):
    """This function generates a private key using a random cryptographic number
    with the length 2048 or specified in the args"""
    rand_gen = Crypto.Random.new().read
    private_key = RSA.generate(key_length, rand_gen)
    logger.info(f'Private key generated with length {key_length}, %s', sh.success('successfully'))

    return private_key


def gen_public_key(private_key: RSA.RsaKey):
    """This function generates a public key using a private key"""
    public_key = private_key.public_key()
    logger.info(f'Public key generated, %s', sh.success('successfully'))

    return public_key


########################################
#           Export functions           #
########################################

def stringify_key(key: RSA.RsaKey):
    """This function export a key to a string in hexadecimal"""
    key = key.exportKey(format='PEM')
    key = binascii.hexlify(key).decode('utf8')
    logger.info(f'Export key to hexadecimal, %s', sh.success('successfully'))
    return key


def export_key_to_file(key: RSA.RsaKey, filename: str or Path):
    """This function export a key to a file"""
    if isinstance(filename, str):
        filename = Path(filename)
    try:
        filename.resolve(strict=True)

        if not filename.is_file() or not filename.parent.is_dir():
            raise FileNotFoundError

        with open(filename, 'wb') as f:
            f.write(key.export_key('PEM'))

        logger.info(f'Imported key to file, %s', sh.success('successfully'))

    except FileNotFoundError:
        logger.exception(f"The {filename} doesn't exists")


########################################
#           Import functions           #
########################################

def unstringify_key(key: str):
    """This function imports a key in hexadecimal"""
    key = RSA.importKey(binascii.unhexlify(key))
    logger.info(f'Imported key from hexadecimal, %s', sh.success('successfully'))
    return key


def import_key_from_file(filename):
    """This function imports a key from a file"""
    if isinstance(filename, str):
        filename = Path(filename)
    try:
        filename.resolve(strict=True)

        if not filename.is_file() or not filename.parent.is_dir():
            raise FileNotFoundError

        with open(filename, 'rb') as f:
            key = f.read()
            key = RSA.importKey(key)
        logger.info(f'Imported key from file, %s', sh.success('successfully'))
        return key
    except FileNotFoundError:
        logger.exception(f"The {filename} doesn't exists")
