########################################
#                Imports               #
########################################

import socket

from Crypto.PublicKey import RSA

from rsa import encrypt_decrypt_mgr

########################################
#    Standard Var  global functions    #
########################################

encode_format = 'utf8'
header = 64


########################################
#           Socket functions           #
########################################

def recv(conn: socket, rsa_key: RSA.RsaKey = None):
    """This function handles the received data, with the headers of the messages and
    decrypt the message if an RSA key is provided
    if the decryption gave an error the return is a None"""
    while True:
        try:
            msg_length = conn.recv(header).decode(encode_format)
        except ConnectionResetError:
            print('[FORCED CLOSED CONNECTION]')
            return
        except ConnectionAbortedError:
            print('[CLOSED CONNECTION]')
            return
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(encode_format)
            if rsa_key is not None:
                msg = encrypt_decrypt_mgr.decrypt_msg(msg, rsa_key)

            return msg


def send(msg: str, conn: socket, rsa_key: RSA.RsaKey = None):
    """This function handles all the preparation for the message to be sent
    and encrypts the message if an RSA key is provided"""

    if rsa_key:
        msg = encrypt_decrypt_mgr.encrypt_msg(msg, rsa_key)

    msg = msg.encode(encode_format)
    msg_length = len(msg)
    send_length = str(msg_length).encode(encode_format)
    send_length += b' ' * (header - len(send_length))
    try:
        conn.send(send_length)
        conn.send(msg)
    except ConnectionResetError:
        print('[CLOSED CONNECTION]')
