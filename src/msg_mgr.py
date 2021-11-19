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
    file = open(filename, 'rt')
    text = file.read()
    text = text.encode(encode_format)
    cipher = PKCS1_OAEP.new(key)
    text = cipher.encrypt(text)
    file.close()
    file = open(filename, 'wb')
    file.write(text)


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
    file = open(filename, 'rb')
    text = file.read()
    cipher = PKCS1_OAEP.new(key)
    text = cipher.decrypt(text)
    text = str(text)
    file.close()
    file = open(filename, 'wt')
    text = str(text)
    text = text[2:-1]
    file.write(text)
