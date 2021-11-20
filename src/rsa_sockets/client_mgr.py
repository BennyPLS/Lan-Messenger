import socket
from threading import Thread
import key_mgr
import msg_mgr
from src.rsa_sockets.socket_mgr import recv, send


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

