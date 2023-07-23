import logging
import os

import src.config

# Directory creation
if not os.path.exists(config.LOGGER_PATH):
    os.makedirs(config.LOGGER_PATH)

if not os.path.exists(config.DATA_PATH):
    os.makedirs(config.DATA_PATH)

# Logging
logger = logging.getLogger(config.LOGGER_NAME)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

file_handler = logging.FileHandler(config.LOGGER_PATH + config.LOGGER_FILE)  # Specify the file path here
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)


logger.addHandler(console_handler)
logger.addHandler(file_handler)
