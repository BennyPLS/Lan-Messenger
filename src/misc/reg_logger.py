########################################
#                Imports               #
########################################

import logging

import chromalog

########################################
#           global variables           #
########################################

default_format_logger = ('\n[%(asctime)s] - [File:%(filename)s -> FuncName:%(funcName)s -> ThreadName:%(threadName)s]\n'
                         'LOGGER:%(name)s - %(levelname)s: %(message)s')


########################################
#               functions              #
########################################

def reg_logger(
        name: str,
        level: int = logging.ERROR,
        format_msg: str = default_format_logger,
        filename='./logs.log',
        stream_handler: bool = True
):
    """This creates a logger with the given parameters
    name, Name of the logger,
    level, the levels that we shows """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if stream_handler:
        chromalog.basicConfig(default_format_logger)
    if filename:
        file_handler = logging.FileHandler(filename)
        if format_msg:
            formatter = logging.Formatter(format_msg)
            file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
