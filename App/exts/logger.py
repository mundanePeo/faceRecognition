import os
import sys
import logging

from App.settings import MESSAGE_DATA_FORMAT


def get_logger(output_dir, level=logging.DEBUG):
    logger = logging.getLogger(output_dir)

    logger.setLevel(level)

    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s", datefmt=MESSAGE_DATA_FORMAT)
    if level == logging.DEBUG:
        ch = logging.StreamHandler(stream=sys.stdout)
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    fh = logging.FileHandler(os.path.join(output_dir, 'log.txt'), mode='w')
    fh.setLevel(level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
