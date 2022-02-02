########################################
#                Imports               #
########################################

import unittest
import string
import os
from pathlib import Path

from encryption import SimpleRSA


########################################
#                 Main                 #
########################################

class RsaTests(unittest.TestCase):
    test_files: Path = Path('./files/')
    encode_format: str = 'utf8'

    ########################################
    #                 Tests                #
    ########################################

    def test_encryption(self):
        private_key = SimpleRSA.gen_private_key()
        public_key = SimpleRSA.gen_public_key(private_key)
        ascii_lowercase = string.ascii_lowercase
        ascii_uppercase = string.ascii_uppercase
        text = test_text()

        self.assertEqual(ascii_lowercase,

                         SimpleRSA.decrypt(

                             SimpleRSA.encrypt(
                                 ascii_lowercase,
                                 public_key),

                             private_key))

        self.assertEqual(ascii_uppercase,

                         SimpleRSA.decrypt(

                             SimpleRSA.encrypt(
                                 ascii_uppercase,
                                 public_key),

                             private_key))

        self.assertEqual(text,

                         SimpleRSA.decrypt(

                             SimpleRSA.encrypt(
                                 text,
                                 public_key),

                             private_key))

    def test_file_encryption(self):
        private_key = SimpleRSA.gen_private_key()
        public_key = SimpleRSA.gen_public_key(private_key)
        testfile = self.test_files.joinpath("./test.txt")

        with open(testfile, "w") as f:
            f.write(test_text())

        SimpleRSA.encrypt_file(testfile, public_key)
        SimpleRSA.decrypt_file(testfile, private_key)

        with open(testfile, "r") as f:
            self.assertEqual(test_text(), f.read())

        os.remove(testfile)

    def test_keys_import_export(self):
        private_key = SimpleRSA.gen_private_key()
        public_key = SimpleRSA.gen_public_key(private_key)
        keyfile = self.test_files.joinpath('key.rsa')

        self.assertEqual(private_key,
                         SimpleRSA.un_stringify_key(
                             SimpleRSA.stringify_key(private_key)
                         ))

        self.assertEqual(public_key,
                         SimpleRSA.un_stringify_key(
                             SimpleRSA.stringify_key(public_key)
                         ))

        SimpleRSA.export_key_to_file(private_key, keyfile)

        self.assertEqual(private_key,
                         SimpleRSA.import_key_from_file(keyfile))

        SimpleRSA.export_key_to_file(public_key, keyfile)

        self.assertEqual(public_key,
                         SimpleRSA.import_key_from_file(keyfile))

        os.remove(keyfile)


########################################
#                Helpers               #
########################################

def test_text():
    return "Ut èét àùgúé magna. Suspeñdisse nec enim diam. Suspendisse augçue nulla, tempCs vel tuçpis id, " \
           "rhòóncus pharetra nuìía. · € ! | @ # $ ~ % & / ( ) = / ' ? ` ^ [ ] + * { } - _ . : , ; < > ¨ ¿ ¡"


if __name__ == '__main__':
    unittest.main()
