from switch import Switch
import key_mgr
import msg_mgr

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

    with Switch(entry) as case:
        if case('encrypt'):
            print("Encrypt file or text input?")
            selection = input('=>')
            if selection == 'file':
                msg_mgr.encrypt_file(input('Path =>'), public_key)
            elif selection == 'text':
                msg_encoded = msg_mgr.encrypt_msg(input('Enter msg =>'), public_key)
                print(msg_encoded)

        if case('decrypt'):
            print("Decrypt file or text input?")
            selection = input('=>')
            if selection == 'file':
                msg_mgr.decrypt_file(input('Path =>'), private_key)
            elif selection == 'text':
                print('Warning : This function can give errors')
                msg = msg_mgr.decrypt_msg(input('Enter encrypted msg =>'), private_key)
                print(msg)

        if case('generate private key', 'gprik'):
            private_key = key_mgr.gen_private_key()

        if case('generate public key', 'gpubk'):
            if private_key is None:
                print('Private key not found')
            else:
                public_key = key_mgr.gen_public_key(private_key)
        if case('import'):
            print('Import from a file or a string?')
            selection = input('=>')
            if selection == 'string':
                print('Import as a private_key or public_key?')
                selection = input('=>')
                if selection == 'private_key':
                    private_key = key_mgr.unstringify_key(input('=>'))
                elif selection == 'public_key':
                    public_key = key_mgr.unstringify_key(input('=>'))
            elif selection == 'file':
                print('Import as a private_key or public_key?')
                selection = input('=>')
                if selection == 'private_key':
                    private_key = key_mgr.import_key_from_file(input('Location =>'))
                elif selection == 'public_key':
                    public_key = key_mgr.import_key_from_file(input('Location =>'))

        if case('import private key from file', 'import prik file'):
            file_directory = input('Input the complete file directory =>')
            private_key = key_mgr.import_key_from_file(file_directory)
        if case('import public key from file', 'import pubk file'):
            file_directory = input('Input the complete file directory =>')
            public_key = key_mgr.import_key_from_file(file_directory)
        if case('import key from str', 'import key str'):
            str_key_import = input('only Keys in a string = >')
            print('save import as private_key or public_key?')
            selection = input('=>')
            if selection == 'private_key':
                private_key = key_mgr.unstringify_key(str_key_import)
            elif selection == 'public_key':
                public_key = key_mgr.unstringify_key(str_key_import)
            else:
                print('selection not valid.\n Returing to main menu...')
        if case('export'):
            print('Export Public key or Private key')
            selection = input('=>')
            if selection == 'private_key' or selection == 'private':
                key_mgr.export_key_to_file(private_key, input('Input the complete file directory =>'))
            if selection == 'public_key' or selection == 'public':
                key_mgr.export_key_to_file(public_key, input('Input the complete file directory =>'))
        if case('print private_key'):
            print(key_mgr.stringify_key(private_key))
        if case('print public_key'):
            print(key_mgr.stringify_key(public_key))
        if case.default:
            print('option not found')
