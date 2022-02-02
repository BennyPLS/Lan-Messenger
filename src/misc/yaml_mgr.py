########################################
#                Imports               #
########################################

from misc.reg_logger import reg_logger
from yaml import load, dump, Loader
from chromalog.mark.helpers import simple as sh
from misc.input_mgr import path_validation

########################################
#                Logging               #
########################################

logger = reg_logger(__name__)


########################################
#           YAML Manipulation          #
########################################

def yaml_load(filename):

    if not path_validation(filename):
        return

    with open(filename, 'r') as f:
        data = load(f, Loader)

    logger.info(f'Loaded YAML file, %s', sh.success('correctly'))
    return data


def yaml_dump(filename, data):

    if not path_validation(filename, True):
        return

    with open(filename, 'w') as f:
        dump(data, f)

    logger.info(f'Dumped YAML file, %s', sh.success('correctly'))

