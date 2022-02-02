########################################
#                Imports               #
########################################

import socket
from Crypto.PublicKey import RSA
import errno
from chromalog.mark.helpers import simple as sh

from misc.reg_logger import reg_logger
from encryption import SimpleRSA, SimpleAES

########################################
#               Logging                #
########################################

logger = reg_logger(__name__)

########################################
#    Standard Var global functions     #
########################################

encode_format = 'utf8'
header = 64


########################################
#        Init Socket functions         #
########################################

def bind(address):
    """
    This is a function that will bind a socket to a given address.

    :param address:
      This is a list or tuple that needs to contain
      in the first element the IP of the server
      and the second element the port number.
    :type address: tuple or list

    :return:
      This functions return the bound socket object.
    :rtype socket. socket:

    :raises OSError:
      This exception is raised if port is being used already.

    """

    bind_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bind_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        bind_sock.bind(address)

    except OSError as e:

        if e == errno.EADDRINUSE:
            logger.error(f'The {address[1]} is already in use.')

        else:
            logger.error(f'The socket cannot be bound to {address}')

        raise e

    logger.info('Bind socket, %s', sh.success('successfully'))
    return bind_sock


def connect(address):
    """
    This is a function to connect to a certain address.

    :param address:
      This is a list or tuple that needs to contain
      in the first element the IP of the server
      and the second element the port number.
    :type address: tuple or list

    :return:
      This functions return the connected socket object.
    :rtype socket. socket:

    :raises ConnectionRefusedError:
      This exception is raised if the connection is actively refused by any factor.
    """

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        conn.connect(address)

    except ConnectionRefusedError as e:
        logger.error('Connection failed to establish')
        raise e

    logger.info('Connection established, %s', sh.success('successfully'))
    return conn


########################################
#   Communications Socket functions    #
########################################

def raw_recv(conn):
    """

    :param conn:
      This is the connection that will be receiving the message
    :type conn: socket. socket

    :raises ConnectionAbortedError:
      This exception is raised if the connection is aborted

    :raises ConnectionResetError:
      This exception is raised if the connection is reset or just disconnected

    :return:
      This functions returns the bytes received from the connection.
    :rtype bytes:
    """

    try:
        msg_length = conn.recv(header).decode(encode_format)

    except ConnectionResetError as e:
        logger.error('[FORCED CLOSED CONNECTION]')
        raise e

    except ConnectionAbortedError as e:
        logger.error('[CLOSED CONNECTION]')
        raise e

    if msg_length:
        msg_length = int(msg_length)
        binaries = conn.recv(msg_length)

        logger.info('Message received, %s', sh.success('successfully'))
        return binaries


def recv(conn, mode='plaintext', **kwargs):
    """
    This is a high level function that manages the receiving of a specified
    socket and returns the processed received information defined by the mode /
    behaviour.

    :param conn:
      This is the connection that will be receiving the message
    :type conn: socket. socket

    :param mode:
      This is the variables that will determine what method
      of all available will be used to receive the message through
      the socket object the default method is plaintext.
      Available behaviours ['plaintext', 'RSA', 'AES']
    :type mode: str

    :param kwargs:
      There are a couple of keyword arguments depending on the mode of
      selected, for the default behaviour not need a keyword argument.

      :key rsa_key: RSA.RsaKey - Required for the RSA mode
      :key aes_key: bytes      - Required for the AES mode

    :raises ValueError:
      If the mode introduced is not supported or not valid, the keyword arguments are not valid,
      the key introduced for the RSA mode or AES mode is incorrect

    :raises ConnectionAbortedError:
      This exception is raised if the connection is aborted

    :raises ConnectionResetError:
      This exception is raised if the connection is reset or just disconnected

    :return:
      This functions returns the string value received and processed.
    :rtype str:
    """

    modes = ('plaintext', 'RSA', 'AES')
    kwargs_valid = ('rsa_key', 'aes_key', 'decode')

    for kwarg in kwargs:
        if kwarg not in kwargs_valid and kwargs != {}:
            raise ValueError(f'The introduced kwargs are not valid: {kwargs_valid}, and ')

    if mode not in modes:
        raise ValueError(f'The introduced mode - {mode} - is not valid or supported')

    decode = kwargs.get('decode', True)

    if not isinstance(decode, bool):
        raise ValueError(f'The introduced decode kwarg is not valid [True or False] ')

    if mode == modes[0]:

        try:
            raw = raw_recv(conn)
            if decode:
                return raw.decode(encode_format)
            else:
                return raw

        except ConnectionAbortedError or ConnectionResetError as e:
            raise e

    elif mode == modes[1]:

        try:
            rsa_key = kwargs.get('rsa_key')

            ciphertext = raw_recv(conn)
            msg = SimpleRSA.decrypt(ciphertext, rsa_key, decode=decode)

            return msg

        except ValueError as e:
            raise e

        except ConnectionAbortedError or ConnectionResetError as e:
            raise e

        except IndexError:
            raise TypeError(f'The specified mode - {mode} - is required an RSA key ')

    elif mode == modes[2]:

        try:
            aes_key = kwargs.get('aes_key')

            ciphertext = raw_recv(conn)
            tag = raw_recv(conn)
            nonce = raw_recv(conn)

            msg = SimpleAES.decrypt(ciphertext, tag, nonce, aes_key, decode=decode)
            return msg

        except ValueError as e:
            raise e

        except ConnectionAbortedError or ConnectionResetError as e:
            raise e

        except IndexError:
            raise TypeError(f'The specified mode - {mode} - is required a aes_key')


def raw_send(msg, conn):
    """
    This function manages the headers necessary to send the message
    with the connection with the bytes to be sent.
    Is recommended to use  the -send()- function instead.

    :param msg:
      This is the message to be sent can be a string or bytes object.
    :type msg: str | bytes:

    :param conn:
      This is the connection that will be used to send the bytes or string
    :type conn: socket. socket:

    :return:
      This functions does not return a value.
    :rtype None:

    :raises ConnectionAbortedError:
      When the connection is closed by the peer.

    :raises ConnectionResetError:
      When the connection is unexpectedly closed
    """

    if not isinstance(msg, bytes):
        msg = msg.encode(encode_format)

    msg_length = len(msg)
    send_length = str(msg_length).encode(encode_format, 'ignore')
    send_length += b' ' * (header - len(send_length))

    try:
        conn.send(send_length)
        conn.send(msg)
        logger.info('Message send successfully')

        logger.info('The message was sent, %s', sh.success('successfully'))

    except ConnectionResetError as e:
        logger.error('[FORCED CLOSED CONNECTION]')
        raise e

    except ConnectionAbortedError as e:
        logger.error('[CLOSED CONNECTION]')
        raise e


def send(msg, conn, mode='plaintext', **kwargs):
    """
    This function manages all the modes and types of encryption
    to send a message through the connection. This is a high level function,
    see the raw_send to see the low level function.

    :param msg:
      This is the plaintext message to be sent.
    :type msg: str | bytes

    :param conn:
      This is the socket object that needs to be connected
      in order to send the message in the mode specified.
    :type conn: socket. socket

    :param mode:
      This is the variables that will determine what method
      of all available will be used to send the message through
      the socket object the default method is plaintext.
      Available behaviours ['plaintext', 'RSA', 'AES']
    :type mode: str

    :param kwargs:
      There are a couple of keyword arguments depending on the mode of
      selected, for the default behaviour not need a keyword argument.

      :key rsa_key: RSA.RsaKey - Required for the RSA mode
      :key aes_key: bytes      - Required for the AES mode

    :raises ValueError:
      If the mode introduced is not supported or not valid, the keyword arguments are not valid,
      the key introduced for the RSA mode is incorrect

    :raises ConnectionAbortedError:
      This exception is raised if the connection is aborted

    :raises ConnectionResetError:
      This exception is raised if the connection is reset or just disconnected

    :returns:
      This functions does not return a value.
    :rtype None:

    """
    modes = ('plaintext', 'RSA', 'AES')
    kwargs_valid = ('rsa_key', 'aes_key')

    for kwarg in kwargs:
        if kwarg not in kwargs_valid and kwargs != {}:
            raise ValueError(f'The introduced kwargs are not valid: {kwargs_valid}')

    if mode not in modes:
        raise ValueError(f'The introduced mode - {mode} - is not valid or supported')

    if mode is modes[0]:

        try:
            raw_send(msg, conn)

        except ConnectionAbortedError or ConnectionAbortedError as e:
            raise e

    elif mode is modes[1]:

        try:
            key = kwargs.get('rsa_key')
            if not isinstance(key, RSA.RsaKey):
                raise TypeError('This kwarg needs to be a RsaKey object')

            ciphertext = SimpleRSA.encrypt(msg, key)

            raw_send(ciphertext, conn)

        except IndexError:
            raise TypeError(f'The specified mode - {mode} - is required an RSA key ')

        except ValueError as e:
            raise e

        except ConnectionAbortedError or ConnectionAbortedError as e:
            raise e

    elif mode is modes[2]:

        try:
            key = kwargs.get('aes_key')

            if not isinstance(key, bytes):
                raise ValueError('This kwarg needs to be a bytes object')

            ciphertext, tag, nonce = SimpleAES.encrypt(msg, key)

            raw_send(ciphertext, conn)
            raw_send(tag, conn)
            raw_send(nonce, conn)

        except IndexError:
            raise TypeError(f'The specified mode - {mode} - is required a aes_key')

        except ConnectionAbortedError or ConnectionAbortedError as e:
            raise e
