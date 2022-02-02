########################################
#                Imports               #
########################################

from pathlib import Path
from secrets import token_bytes

from chromalog.mark.helpers import simple as sh
from Crypto.Cipher import AES

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

def gen_key(
        key_length: int = 32
) -> bytes:
    """

    This function generates a random key with the specified length.

    :param key_length:
      This is the length of the generated key the default length is 32 bytes.
    :type key_length: int

    :return:
      This function returns a random key with the specified length, in bytes.
    :rtype bytes:

    """
    return token_bytes(key_length)


def string_key(
        string: str,
        key_length: int = 32
) -> bytes:
    """
    W.I.P
    """
    keynotes = string.encode('utf8')
    if keynotes.__len__() == key_length:
        print('LENGTH CORRECT!')
        return keynotes

    else:
        print(f'INCORRECT {keynotes.__len__()}')


########################################
#           Export functions           #
########################################

def export_key(
        filename: str | Path,
        key: bytes
) -> None:
    """

    This is function to export in plaintext in a file

    :param filename:
      This is the path to the file that wll contain the key
    :type filename: str | Path

    :param key:
      The key to be exported.
    :type key: bytes

    :return:
      This functions does not return anything.
    :rtype None:

    :raises FileNotFoundError:
      This error is raises if the file is not found.

    """

    if not path_validation(filename, True):
        raise FileNotFoundError

    with open(filename, 'bw') as f:
        f.write(key)
        logger.info(f'The key has benn exported to {filename}, %s', sh.success('successfully'))


########################################
#           Import functions           #
########################################

def import_key(
        filename: Path | str
) -> bytes:
    """

    This gives the ket stored in plaintext in a file

    :param filename:
      This is the path to the file containing the key to be imported.
    :type filename: str | Path

    :return:
      This functions return the stored key in the file selected.
    :rtype bytes:

    :raises FileNotFoundError:
      This error is raises if the file is not found.

    """

    if not path_validation(filename):
        raise FileNotFoundError

    with open(filename, 'br') as f:
        key = f.read()

    logger.info(f'The key has been imported, %s', sh.success('successfully'))
    return key


########################################
#          Encrypt  functions          #
########################################

def encrypt(
        msg: str | bytes,
        key: bytes
) -> tuple[bytes, bytes, bytes]:
    """

    This function encrypts a message using the given key with the AES protocol.

    :param msg:
      This is the message to be encrypted can be a string or simply bytes.
    :type msg: str | bytes

    :param key:
      This is the key used to encrypt the message is an 32 bytes key
    :type key: bytes

    :return:
      This returns a tuple containing the encrypted message the tag related to the encrypted message and the
      initialization vector (ciphertext, tag, nonce)
    :rtype tuple:

    """
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce

    if not isinstance(msg, bytes):
        msg = msg.encode(encode_format)

    ciphertext, tag = cipher.encrypt_and_digest(msg)
    return ciphertext, tag, nonce


########################################
#          Decrypt  functions          #
########################################


def decrypt(
        ciphertext: bytes,
        tag: bytes,
        nonce: bytes,
        key: bytes,
        decode: bool = True
) -> bytes | str:
    """

    This function decrypt the ciphertext of an encrypted message with the AES protocol requires a
    key, tag, nonce with the encrypted message ciphertext.

    :param ciphertext:
      This is the encrypted text of the message.
    :type ciphertext: bytes

    :param tag:
      This is the tag generated from the ciphertext is required for verification of the cipher.
    :type tag: bytes

    :param nonce:
      Is the Initialization Factor of the encrypted message is a different value every time.
    :type nonce: bytes

    :param key:
      This is the actual key used to decrypt the message in combination of the all the previous parameters.
    :type key: bytes

    :param decode:
      This is a variable to determine if the message needs to be decoded into a string.
    :type decode: bool


    :return:
      This function returns the decrypted message.
    :rtype str | bytes:

    :raises ValueError:
      This exception is raised if the message cannot be verified with the given arguments. Still return the message

    """

    cipher = AES.new(key, mode=AES.MODE_EAX, nonce=nonce)
    binary = cipher.decrypt(ciphertext)
    try:
        cipher.verify(tag)
    except ValueError:
        logger.warning('The message cannot verify the integrity of the message or the confidentiality with the given '
                       'tag.')
        raise ValueError

    if decode:
        return binary.decode(encode_format)

    else:
        return binary
