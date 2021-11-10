# This python script, creates the keys for the save transmission of data.
import binascii

import Crypto
from Crypto.PublicKey import RSA


########################################
#         Generating functions         #
########################################

def gen_private_key():
    # random number generator with cryptographic method #
    rand_gen = Crypto.Random.new().read

    # Generating Private Key, based of random number generator, length = 1024 #
    private_key = RSA.generate(4192, rand_gen)

    return private_key


def gen_public_key(private_key):
    public_key = private_key.public_key()

    return public_key


########################################
#           Export functions           #
########################################


def export_key_to_file(key, filename):
    file_key = open(filename, 'wb')
    file_key.write(key.export_key('PEM'))


########################################
#           Import functions           #
########################################

def unstringify_key(key):
    # Importacion de 'RSA keys' ( String Key --> RSA object(key) )
    key = RSA.importKey(binascii.unhexlify(key))

    return key


def import_key_from_file(file):
    keyfile = open(file, 'rb')
    key = keyfile.read()
    key = RSA.importKey(key)
    return key


########################################
#            Misc functions            #
########################################

def stringify_key(key):
    key = key.exportKey(format='DER')

    key = binascii.hexlify(key).decode('utf8')

    return key
