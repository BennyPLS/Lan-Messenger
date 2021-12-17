########################################
#                Imports               #
########################################

from misc import input_mgr
from misc.reg_logger import reg_logger
from rsa import key_mgr
from sockets import server_mgr, client_mgr, socket_mgr

########################################
#                Logging               #
########################################

logger = reg_logger(__name__)


def main():
    """Main Thread"""

    server = None
    conn = None
    public_key_server = None

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
                      'exit -e          | '
                      'Exit the programa\n'
                      '######################################################################################\n'
                      )

            case 'initialize server' | '-initserv':
                if server:
                    logger.info('Server already on')
                else:
                    server_ip = input_mgr.input_ip()
                    server_port = input_mgr.input_port()
                    server_name = input('Server name: ')
                    server, server_private_key, server_thread = \
                        server_mgr.initialize_server(server_ip, server_port, server_name)
                    if server:
                        logger.info('Server initialized')

            case 'connect' | '-conn':
                conn_ip = input_mgr.input_ip()
                conn_port = input_mgr.input_port()
                conn, username, server_name, conn_private_key, public_key_server = \
                    client_mgr.initialize_connection(conn_ip, conn_port)

                if conn:
                    logger.info('Successfully established connection')
                    public_key_server = key_mgr.unstringify_key(public_key_server)

            case 'send msg to server' | '-sms':
                if conn:
                    msg = input('Input Message: ')

                    socket_mgr.send(msg, conn, public_key_server)
                else:
                    print('No active connections')

            case 'send msg to a client' | '-smc':
                username = input('Input the username: ')
                pubkey_client = server_mgr.search_public_key_by_username(username)
                conn_server = server_mgr.search_conn_by_username(username)
                if conn_server is not None and pubkey_client is not None:
                    msg = input('Input Message: ')
                    socket_mgr.send(msg, conn_server, pubkey_client)
                else:
                    logger.debug(f'')
                    print(f'{username}, not found in dict ')

            case 'Stop Server' | '-clserver':
                if server:
                    try:
                        server.close()
                    except OSError:
                        print('Server Closed [FORCED]')

            case 'exit' | '-e':
                exit()

            case _:
                print('No valid option found.\n'
                      'Type help or -h for help.')


if __name__ == '__main__':
    main()
