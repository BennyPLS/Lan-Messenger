import socket
from threading import Thread
import msg_mgr
import key_mgr

########################################
#    Standard Var  global functions    #
########################################

encode_format = 'utf8'
header = 64
disconnection_message = '!DISCONNECT'
userDict = {}  # { usuername:[addr, conn, public_key] }
connDict = {}
pubkeyDict = {}
server_private_key = None
server_public_key = None


########################################
#        Basic socket functions        #
########################################

def recv(conn: socket):
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


def send(msg: str, conn: socket, rsa_key=None):
    if rsa_key:
        msg = msg_mgr.encrypt_msg(msg, rsa_key)

    msg = msg.encode(encode_format)
    msg_length = len(msg)
    send_length = str(msg_length).encode(encode_format)
    send_length += b' ' * (header - len(send_length))
    conn.send(send_length)
    conn.send(msg)


########################################
#           Server functions           #
########################################

def inicialize_server(ip, port):
    global server_private_key, server_public_key
    address = (ip, port)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(address)
    except OSError:
        print('ERROR: Port in use or not aviable')
        return None, None

    server_private_key = key_mgr.gen_private_key()
    server_public_key = key_mgr.gen_public_key(server_private_key)

    print(f'############################### \n'
          f'Started Server at \n'
          f'IP   : {ip}     \n'
          f'Port : {port}   \n'
          f'###############################')

    return server, server_private_key


def listen(server: socket):
    server.listen()
    while True:
        client_conn, client_addr = server.accept()
        Thread(target=handle_connection, args=(client_conn, client_addr)).start()


def handle_connection(conn: socket, addr):
    print(f'[NEW CONNECTION] {addr} connected')

    public_key = recv(conn)
    public_key = key_mgr.unstringify_key(public_key)

    send(key_mgr.stringify_key(server_public_key), conn)

    username = recv(conn)
    userDict[username] = [addr, conn, public_key]

    connected = True

    # Recv Handler #

    while connected:
        msg = recv(conn)
        if msg is ConnectionResetError:
            connected = False
            print(f'{username} has disconnected')

        if msg is False:
            continue
        msg = msg_mgr.decrypt_msg(msg, server_private_key)

        if msg == disconnection_message:
            connected = False
            print(f'{username} has disconnected')

        print(f'{username} > {msg}')

    conn.close()


########################################
#           Client functions           #
########################################

def inicialize_connection(ip, port):
    address = (ip, port)

    private_key = key_mgr.gen_private_key()
    public_key = key_mgr.gen_public_key(private_key)

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect(address)
    except ConnectionRefusedError:
        print('Connection failed')
        exit()
    print(f'############################### \n'
          f'Connection established with \n '
          f'IP   : {ip}     \n'
          f'Port : {port}   \n'
          f'###############################')

    # Interchange of information #
    # public keys, usernames #

    send(key_mgr.stringify_key(public_key), conn)

    public_key_server = recv(conn)

    username = input('Input your username: ')

    send(username, conn)

    Thread(target=handle_recv_client, args=[conn, private_key]).start()

    return conn, username, private_key, public_key_server


def handle_recv_client(conn, private_key):
    while True:
        msg = recv(conn)

        msg = msg_mgr.decrypt_msg(msg, private_key)

        print(f'Server send > {msg}')


########################################
#       miscellaneous  functions       #
########################################

def search_public_key_by_username(username):
    usuername_info = userDict[username]
    if usuername_info:
        if usuername_info:
            public_key = usuername_info[2]
            return public_key
    else:
        print('No information available found liked to that username')


def search_conn_by_username(username):
    usuername_info = userDict[username]
    if usuername_info:
        conn = usuername_info[1]
        return conn
    else:
        print('No information available found liked to that username')
