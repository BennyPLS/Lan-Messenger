########################################
#                Imports               #
########################################
import re  # regular expressions
from src.misc.reg_logger import reg_logger

########################################
#                Logging               #
########################################

logger = reg_logger(__name__)


########################################
#           Filters & Inputs           #
########################################

def input_ip():
    """This function takes the input of the user and checks
    if is correct and return the processed input
    if not try again"""
    print('Input a ip with this format {x.x.x.x} \n'
          '(Note : Without the keys) \n'
          '=> ')
    while True:
        ip = input('=> ')

        ip = ip.replace(".", ":")

        if re.search(r".?.?.?:.?.?.?:.?.?.?:.?.?.?$", ip):
            list_ip_sections = ip.split(":")
        else:
            logger.warning(f"The introduced ip, {ip}, it was not in the required format")
            continue

        for ip_part in list_ip_sections:
            if int(ip_part) not in range(0, 256):
                logger.warning(f"The introduced ip, {ip}, Exceeds 8-bit rendering capability")
                continue

        return ip


def input_port():
    """This function takes the input from the usser and processed it
    to confirm that the input of the user is a valid port
    if the port is non ephemeral, register a debug log"""
    while True:
        server_port = input('Input port number: ')
        try:
            server_port = int(server_port)
            if server_port < 0 or server_port is False:
                raise ValueError
            elif server_port <= 49151:
                logger.debug(f'You may be using a port in use or reserved. Port = {server_port}')
            elif server_port >= 65535:
                raise IndexError

            return server_port

        except ValueError:
            logger.error('The port has to be a positive integer')
        except IndexError:
            logger.error('You exceeded the maximum possible port numbers')
