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
    while True:
        entry = input(" =>")

        match entry.lower():
            case 'encrypt':
                print("Encrypt file or text input?")
                match input('=> '):

                    case 'file':
                        encrypt_decrypt_mgr.encrypt_file(input('Path =>'), public_key)

                    case 'text':
                        msg_encoded = encrypt_decrypt_mgr.encrypt_msg(input('Enter msg =>'), public_key)
                        print(msg_encoded)

                    case _:
                        print('Selection not valid.\n Returning to main menu...')

            case 'decrypt':
                print("Decrypt file or text input?")
                match input('=> '):

                    case 'file':
                        encrypt_decrypt_mgr.decrypt_file(input('Path =>'), private_key)

                    case 'text':
                        msg = encrypt_decrypt_mgr.decrypt_msg(input('Enter encrypted msg =>'), private_key)
                        print(msg)

                    case _:
                        print('Selection not valid.\n Returning to main menu...')

            case 'generate private key' | 'gprik':
                private_key = key_mgr.gen_private_key()

            case 'generate public key' | 'gpubk':
                if private_key is None:
                    print('Private key not found')
                    continue

                public_key = key_mgr.gen_public_key(private_key)

            case 'import':
                print('Import from a file or a string?')
                match input('=>'):

                    case 'string':
                        print('Import as a private_key or public_key?')
                        match input('=>'):

                            case 'private_key':
                                private_key = key_mgr.unstringify_key(input('=>'))

                            case 'public_key':
                                public_key = key_mgr.unstringify_key(input('=>'))

                            case _:
                                print('Selection not valid.\n Returning to main menu...')

                    case 'file':
                        print('Import as a private_key or public_key?')
                        match input('=>'):

                            case 'private_key':
                                private_key = key_mgr.import_key_from_file(input('Location =>'))

                            case 'public_key':
                                public_key = key_mgr.import_key_from_file(input('Location =>'))

                            case _:
                                print('Selection not valid.\n Returning to main menu...')

            case 'import key from file' | 'ikf':
                file_directory = input('Input the complete file directory =>')
                print('save import as private_key or public_key?')
                match input('=>'):

                    case 'private_key':
                        private_key = key_mgr.import_key_from_file(file_directory)

                    case 'public_key':
                        public_key = key_mgr.import_key_from_file(file_directory)

            case 'import key from str' | 'iks':
                str_key_import = input('only Keys in a string = >')
                print('save import as private_key or public_key?')
                match input('=>'):

                    case 'private_key':
                        private_key = key_mgr.unstringify_key(str_key_import)

                    case 'public_key':
                        public_key = key_mgr.unstringify_key(str_key_import)

                    case _:
                        print('Selection not valid.\n Returning to main menu...')

            case 'export':
                print('Export Public key or Private key')
                match input('=>'):

                    case 'private_key' | 'private':
                        key_mgr.export_key_to_file(private_key, input('Input the complete file directory =>'))

                    case 'public_key' | 'public':
                        key_mgr.export_key_to_file(public_key, input('Input the complete file directory =>'))

                    case _:
                        print('Selection not valid.\n Returning to main menu...')

            case 'print private_key':
                print(key_mgr.stringify_key(private_key))

            case 'print public_key':
                print(key_mgr.stringify_key(public_key))

            case _:
                print('Selection not valid.')


if __name__ == '__main__':
    main()
