########################################
#                Imports               #
########################################

from misc.reg_logger import reg_logger
from yaml import load, dump, Loader

########################################
#                Logging               #
########################################

logger = reg_logger(__name__)


########################################
#           YAML Manipulation          #
########################################

def yaml_load(filename):
    with open(filename, 'r') as f:
        data = load(f, Loader)
    return data


def yaml_dump(filename, data):
    with open(filename, 'w') as f:
        dump(data, f)
