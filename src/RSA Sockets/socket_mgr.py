import socket
from threading import Thread
import threading

########################################
#        Standard Var functions        #
########################################

encode_format = 'utf8'
header = 64
disconection_message = '!DISCONNECT'


########################################
#         Connection functions         #
########################################

def inicialize_server(ip, port):
    address = (ip, port)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(address)

    print(f'############################### \n'
          f'Started Server at \n'
          f'IP   : {ip}     \n'
          f'Port : {port}   \n'
          f'###############################')

    return server


def inicialize_connection(ip, port):
    address = (ip, port)

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect(address)
    except:
        print('Connection failed')
        exit()
    print(f'############################### \n'
          f'Connection established with \n '
          f'IP   : {ip}     \n'
          f'Port : {port}   \n'
          f'###############################')

    return conn


def listen(server: socket):
    server.listen()
    while True:
        client_conn, client_addr = server.accept()
        thread = Thread(target=handle_connection, args=(client_conn, client_addr))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 1}')


def handle_connection(conn: socket, addr):
    print(f'[NEW CONNECTION] {addr} connected')

    send('BOM DIA', conn)

    connected = True
    while connected:
        try:
            msg_length = conn.recv(header).decode(encode_format)
        except ConnectionResetError:
            print(f'[FORCED RESET CONNECTION] {addr}')
            exit()
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(encode_format)

            if msg == disconection_message:
                connected = False
                print(f'{addr} has disconnected')
            else:
                print(f'{addr} {msg}')

    conn.close()


def recv(conn: socket):
    while True:
        msg_length = conn.recv(header).decode(encode_format)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(encode_format)

            print(msg)


def send(msg: str, conn: socket):
    msg = msg.encode(encode_format)
    msg_length = len(msg)
    send_length = str(msg_length).encode(encode_format)
    send_length += b' ' * (header - len(send_length))
    conn.send(send_length)
    conn.send(msg)
