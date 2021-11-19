from Crypto.Cipher import PKCS1_OAEP
import binascii

encode_format = 'utf8'

########################################
#          Encrypt  function           #
########################################


def encrypt_msg(msg, key):
    msg = msg.encode(encode_format)
    cipher = PKCS1_OAEP.new(key)
    msg = cipher.encrypt(msg)
    msg = binascii.hexlify(msg)
    msg = str(msg)
    msg = msg[2:-1]
    return msg


def encrypt_file(filename, key):
    with open(filename, 'rt') as f:
        text = f.read()
        text = text.encode(encode_format)
        cipher = PKCS1_OAEP.new(key)
        text = cipher.encrypt(text)

    with open(filename, 'wb') as f:
        f.write(text)


########################################
#          Decrypt  function           #
########################################


def decrypt_msg(msg, key):
    if msg is not bytes:
        msg = bytes(msg, encode_format)
    msg = binascii.unhexlify(msg)
    msg = bytes(msg)
    cipher = PKCS1_OAEP.new(key)
    msg = cipher.decrypt(msg)
    msg = str(msg)
    msg = msg[2:-1]
    return msg


def decrypt_file(filename, key):
    with open(filename, 'rb') as f:
        text = f.read()
        cipher = PKCS1_OAEP.new(key)
        text = cipher.decrypt(text)
        text = str(text)

    with open(filename, 'wt') as f:
        text = str(text)
        text = text[2:-1]
        f.write(text)
