import logging
import os
import sys

def get_logger(save_dir = 'log', filename = "log.txt"):
    logger = logging.getLogger("system")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(stream = sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if(os.path.exists(save_dir)==False):
        os.makedirs(save_dir)
    fh = logging.FileHandler(os.path.join(save_dir, filename))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


# logger = get_logger()
# logger.info('hello world')
# logger.info('good world')
