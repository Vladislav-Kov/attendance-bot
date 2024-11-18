import logging
from logging.handlers import RotatingFileHandler

from config import LOGS_PATH


def configure_logging(level=logging.WARNING):
    max_size = 5 * 1025 * 1024 # 5 MB

    handler = RotatingFileHandler(LOGS_PATH, maxBytes=max_size, backupCount=3)
    logging.basicConfig(level=level,
                        format='[%(asctime)s.%(msecs)03d] %(levelname)-7s %(module)-20s: %(lineno)-3d - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        )


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    configure_logging(level=logging.DEBUG)
    number = 5
    logger.warning('warrning message number: %s',number)
    logger.info('info message')
    logger.debug('debug message')