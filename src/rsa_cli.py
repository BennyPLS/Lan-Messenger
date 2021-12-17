########################################
#                Imports               #
########################################

from rsa import key_mgr, encrypt_decrypt_mgr


def main():
    # Variables #
    private_key = None
    public_key = None

    print("""
    ########################################
    #            RSA Cli Client            #
    ########################################
    """)
    print('\nType help or -h for help.')
    while True:
        entry = input(" => ")

        match entry.lower():
            case 'help' | '-h':
                print('##############################################################################################\n'
                      'encrypt                          | '
                      'encrypts a given file or string with the public key stored\n'
                      'decrypt                          | '
                      'decrypt a given file or string with the private key stored\n'
                      'generate private key     -gprik  | '
                      'generate a private key\n'
                      'generate public key      -gpubk  | '
                      'generate a public key based on the stored private key\n'
                      'import                           | '
                      'import from a file or string a key\n'
                      'import key from file     -ikf    | '
                      'import a key from a file\n'
                      'import key from str      -iks    | '
                      'import a key from a string\n'
                      'export                           | '
                      'export the selected key to string or file\n'
                      'print private_key                | '
                      'print the actual private key stored\n'
                      'print public_key                 | '
                      'print the actual public key stored\n'
                      'exit                         -e  | '
                      'Exit the program\n'
                      '##############################################################################################\n'
                      )

            case 'encrypt':
                if not public_key:
                    print('There are not public keys available.')
                    continue

                print("Encrypt text or other?")
                match input('=> '):
                    case 'other':
                        encrypt_decrypt_mgr.encrypt_file(input('Path =>'), public_key)

                    case 'text':
                        print('file or input string?')
                        match input('=> '):

                            case 'file':
                                encrypt_decrypt_mgr.encrypt_text_file(input('Path =>'), public_key)

                            case 'file' | 'input' | 'input string' | 'str':
                                msg_encoded = encrypt_decrypt_mgr.encrypt_msg(input('Enter msg =>'), public_key)
                                print(msg_encoded)

                    case _:
                        print('Selection not valid.\n Returning to main menu...')

            case 'decrypt':
                if not private_key:
                    print('There are not private keys available.')
                    continue

                print("Decrypt text or other?")
                match input('=> '):
                    case 'other':
                        encrypt_decrypt_mgr.decrypt_binary(input('Path =>'), public_key)

                    case 'text':
                        print('file or input string?')
                        match input('=> '):

                            case 'file':
                                encrypt_decrypt_mgr.decrypt_text_file(input('Path =>'), public_key)

                            case 'file' | 'input' | 'input string' | 'str':
                                msg_encoded = encrypt_decrypt_mgr.decrypt_msg(input('Enter msg =>'), public_key)
                                print(msg_encoded)

                    case _:
                        print('Selection not valid.\n Returning to main menu...')

            case 'generate private key' | '-gprik':
                private_key = key_mgr.gen_private_key()

            case 'generate public key' | '-gpubk':
                if private_key is None:
                    print('Private key not found')
                    continue

                public_key = key_mgr.gen_public_key(private_key)

            case 'import':
                print('Import from a file or a string?')
                match input('=> '):

                    case 'string':
                        print('Import as a private key or public key?')
                        match input('=>'):

                            case 'private key':
                                private_key = key_mgr.unstringify_key(input('=>'))

                            case 'public key':
                                public_key = key_mgr.unstringify_key(input('=>'))

                            case _:
                                print('Selection not valid.\n Returning to main menu...')

                    case 'file':
                        print('Import as a private_key or public_key?')
                        match input('=>').lower():

                            case 'private_key':
                                private_key = key_mgr.import_key_from_file(input('Location =>'))

                            case 'public_key':
                                public_key = key_mgr.import_key_from_file(input('Location =>'))

                            case _:
                                print('Selection not valid.\n Returning to main menu...')

            case 'import key from file' | '-ikf':
                file_directory = input('Input the complete file directory =>')
                print('save import as private_key or public_key?')
                match input('=>').lower():

                    case 'private key':
                        private_key = key_mgr.import_key_from_file(file_directory)

                    case 'public key':
                        public_key = key_mgr.import_key_from_file(file_directory)

            case 'import key from str' | '-iks':
                str_key_import = input('only Keys in a string = >')
                print('save import as private_key or public_key?')
                match input('=> '):

                    case 'private_key':
                        private_key = key_mgr.unstringify_key(str_key_import)

                    case 'public_key':
                        public_key = key_mgr.unstringify_key(str_key_import)

                    case _:
                        print('Selection not valid.\n Returning to main menu...')

            case 'export':
                print('Export Public key or Private key')
                match input('=> ').lower():

                    case 'private key':
                        key_mgr.export_key_to_file(private_key, input('Input the complete file directory =>'))

                    case 'public key':
                        key_mgr.export_key_to_file(public_key, input('Input the complete file directory =>'))

                    case _:
                        print('Selection not valid.\n Returning to main menu...')

            case 'print private_key':
                print(key_mgr.stringify_key(private_key))

            case 'print public_key':
                print(key_mgr.stringify_key(public_key))

            case 'exit' | '-e':
                exit()

            case _:
                print('Selection not valid.\n'
                      'Type help or -h for help.')


if __name__ == '__main__':
    main()
