import logging
import chromalog

format_logger = ('[%(asctime)s] - [File:%(filename)s -> FuncName:%(funcName)s -> ThreadName:%(threadName)s]\n'
                 'LOGGER:%(name)s - %(levelname)s: %(message)s')


def reg_logger(name, level=logging.INFO, format_msg=format_logger, filename=None, stream_handler=True):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if stream_handler:
        stream_handler = logging.StreamHandler()
        if format_msg:
            formatter = logging.Formatter(format_msg)
            stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    if filename:
        file_handler = logging.FileHandler(filename)
        if format_msg:
            formatter = logging.Formatter(format_msg)
            file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


if __name__ == '__main__':
    # logger = reg_logger(__name__)
    # chromalog.basicConfig(level=logging.DEBUG)
    # logger = logging.getLogger()
    # logger.debug("This is a debug message")
    # logger.info("This is an info message")
    # logger.warning("This is a warning message")
    # logger.error("This is an error message")
    # logger.critical("This is a critical message")
    input()
