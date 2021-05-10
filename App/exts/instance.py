from .recognizer import Recognizer
from App.settings import DIR_DATA_FORMATE, DIR_OUTPUT
from App.exts.logger import get_logger

import time
import os

# logger
dir_name = time.strftime(DIR_DATA_FORMATE, time.localtime(time.time()))
output_dir = os.path.join(DIR_OUTPUT, dir_name)
os.makedirs(output_dir, exist_ok=True)
logger = get_logger(output_dir=output_dir)


# Recognizer
fr = Recognizer(logger)
