########################################
#                Imports               #
########################################

import re  # regular expressions

from misc.reg_logger import reg_logger
from pathlib import Path

########################################
#                Logging               #
########################################

logger = reg_logger(__name__)


########################################
#           Filters & Inputs           #
########################################

def input_ip(msg='Input a ip with this format {x.x.x.x} \n (Note : Without the keys)'):
    """This function takes the input of the user and checks
    if is correct and return the processed input
    if not try again"""
    print(msg, end="")
    while True:
        ip = input('=> ')

        if re.search(r"\d{1,4}[.]\d{1,4}[.]\d{1,4}[.]\d{1,4}", ip.strip()):
            list_ip_sections = ip.split(".")
        else:
            logger.warning(f"The introduced ip, {ip}, it was not in the required format")
            continue

        for ip_part in list_ip_sections:
            if int(ip_part) not in range(0, 256):
                logger.warning(f"The introduced ip, {ip}, Exceeds 8-bit rendering capability")
                continue

        return ip


def input_port(msg='Input port number: '):
    """This function takes the input from the user and processed it
    to confirm that the input of the user is a valid port
    if the port is non ephemeral, register a debug log"""
    while True:
        server_port = input(msg)
        try:
            server_port = int(server_port)
            if server_port < 0 or server_port is False:
                raise ValueError
            elif server_port <= 49151:
                logger.warning(f'You may be using a port in use or reserved. Port = {server_port}')
            elif server_port >= 65535:
                raise IndexError

            return server_port

        except ValueError:
            logger.error('The port has to be a positive integer')
        except IndexError:
            logger.error('You exceeded the maximum possible port numbers')


def path_validation(location: Path or str, parent: bool = False, strictly: bool = True):
    """This function validates the path passed and checks the conditions passed or the default"""
    if isinstance(location, str):
        location = Path(location)

    try:
        location.resolve(strict=strictly)

    except FileNotFoundError:
        logger.error(f"The Path:{location} could be not resolved strictly")
        return False

    if parent:
        if not location.parent.is_dir() or location.parent == location.anchor:
            logger.error(f"The Path: {location.parent} location is don't exist or is not directory")
            return False

    else:
        if not location.is_file():
            logger.error(f"The Path :{location} is not a file or not exist")
            return False

    return True
