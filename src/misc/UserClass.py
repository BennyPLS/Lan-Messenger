import socket
from Crypto.PublicKey import RSA
from dataclasses import dataclass
import reg_logger




format_logger = ('[%(asctime)s] - [File:%(filename)s -> FuncName:%(funcName)s -> ThreadName:%(threadName)s]\n'
                 'LOGGER:%(name)s - %(levelname)s: %(message)s')

log = reg_logger(__name__, logging.DEBUG, format_logger)


def error():
    log.debug('DEBUG')
    log.info('Informacion')
    log.warning('Esto es una advertencia')
    log.error('Se ha encontraod un error.')
    log.critical('Se ha encontraod un error CRITICO.')


error()


@dataclass(frozen=True)
class User:
    username: str
    addr: list
    conn: socket
    public_key: RSA.RsaKey
