########################################
#                Imports               #
########################################

from chromalog.mark.helpers import simple as sh
from misc.reg_logger import reg_logger
from pathlib import Path

########################################
#                Logging               #
########################################

logger = reg_logger(__name__)

logger.info(f'Module loaded [%s]', sh.success(f'{Path(__file__).parent.name}'))
