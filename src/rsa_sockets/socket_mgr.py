import socket
from Crypto.PublicKey import RSA
import msg_mgr

########################################
#    Standard Var  global functions    #
########################################

encode_format = 'utf8'
header = 64


########################################
#        Basic socket functions        #
########################################

def recv(conn: socket):
    """This function handles the recieved data, with the headers of the messages."""
    while True:
        try:
            msg_length = conn.recv(header).decode(encode_format)
        except ConnectionResetError:
            print('[CLOSED CONNECTION BY SERVER]')
            return ConnectionResetError
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(encode_format)

            return msg


def send(msg: str, conn: socket, rsa_key: RSA.RsaKey = None):
    """This function handles all the preparation for the message to be sent"""
    if rsa_key:
        msg = msg_mgr.encrypt_msg(msg, rsa_key)

    msg = msg.encode(encode_format)
    msg_length = len(msg)
    send_length = str(msg_length).encode(encode_format)
    send_length += b' ' * (header - len(send_length))
    conn.send(send_length)
    conn.send(msg)