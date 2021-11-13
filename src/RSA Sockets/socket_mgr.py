import socket
from threading import Thread
import threading
import msg_mgr
import key_mgr

########################################
#    Standard Var  global functions    #
########################################

encode_format = 'utf8'
header = 64
disconection_message = '!DISCONNECT'
timeoutmsg = ['!TIMEOUT', '!TIMEOUTRESPONSE']
userDict = {}
pubkeyDict = {}
prikeyDict = {}
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
            break
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(encode_format)

            return msg


def send(msg: str, conn: socket, rsa_key=None):
    if rsa_key:
        msg_mgr.encrypt_msg(msg, rsa_key)

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
        thread = Thread(target=handle_connection, args=(client_conn, client_addr))
        thread.start()


def handle_connection(conn: socket, addr):
    print(f'[NEW CONNECTION] {addr} connected')

    public_key = recv(conn)
    pubkeyDict[addr] = key_mgr.unstringify_key(public_key)

    send(key_mgr.stringify_key(server_public_key), conn)

    username = recv(conn)
    userDict[addr] = username

    connected = True

    while connected:
        msg_length = None
        try:
            msg_length = conn.recv(header).decode(encode_format)
        except ConnectionResetError:
            userDict.pop(addr)
            print(f'[FORCE CLOSED CONNECTION] {addr}')
            exit()
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(encode_format)

            if msg == disconection_message:
                connected = False
                print(f'{userDict[addr]} has disconnected')
            else:
                print(f'{userDict[addr]} > {msg}')

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

    send(key_mgr.stringify_key(public_key), conn)

    public_key_server = recv(conn)

    username = input('Input your username: ')

    send(username, conn)

    Thread(target=handle_recv_client, args=[conn, private_key]).start()

    return conn, username, private_key, public_key_server


def handle_recv_client(conn, private_key):
    while True:
        msg = recv(conn)

        msg_mgr.decrypt_msg(msg, private_key)

        print(msg)
