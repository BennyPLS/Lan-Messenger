########################################
#                Imports               #
########################################

from misc.input_mgr import input_ip, input_port
from misc.reg_logger import reg_logger
from rsa import key_mgr
from sockets import socket_mgr
from sockets.ServerClass import Server
from sockets.ClientClass import Client

########################################
#                Logging               #
########################################

logger = reg_logger(__name__)


########################################
#                 Main                 #
########################################

def main():
    """Main Thread"""

    client = None
    server = None

    print('''
    ########################################
    #          RSA Socket Client           #
    ########################################
    ''')
    print('\nType help or -h for help.')
    while True:
        entry = input("=> ")

        match entry.lower():

            case 'help' | '-h':

                print('######################################################################################\n'
                      'initialize server            -initserv   | '
                      'Initializes the server with the given parameters\n'
                      'connect                      -conn       | '
                      'Try to connect to the specified server\n'
                      'send msg to server           -sms        | '
                      'Sends a msg to the connected server\n'
                      'send msg to a client         -smc        | '
                      'Sends a msg to a specified user connected to your server\n'
                      'stop server                  -clserver   | '
                      'Stop forcefully the socket server\n'
                      'exit                         -e          | '
                      'Exit the program\n'
                      '######################################################################################\n'
                      )

            case 'initialize server' | '-initserv':
                if server:
                    logger.info('Server already on')
                else:
                    server_name = input('Server name: ')
                    server = Server(server_name)
                    server_ip = input_ip()
                    server_port = input_port()
                    server.initialize(server_ip, server_port)
                    if server:
                        logger.info('Server initialized')

            case 'connect' | '-conn':
                conn_ip = input_ip()
                conn_port = input_port()
                username = input('Enter username: ')

                client = Client(username, conn_ip, conn_port)
                client.initialize_connection()

                if client:
                    logger.info('Successfully established connection')

            case 'send msg to server' | '-sms':
                if client.conn:
                    msg = input('Input Message: ')

                    client.send_server(msg)
                else:
                    print('No active connections')

            case 'send msg to a client' | '-smc':
                if server:
                    username = input('Input the username: ')
                    msg = input('Input Message: ')
                    server.send_to_user(username, msg)

            case 'Stop Server' | '-clserver':
                server.stop()

            case 'exit' | '-e':
                exit()

            case _:
                print('No valid option found.\n'
                      'Type help or -h for help.')


if __name__ == '__main__':
    main()
