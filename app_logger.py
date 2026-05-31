import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

def get_logger(logger_name: str) -> logging.Logger:
    if logger_name == "root":
        logger = logging.getLogger()
        if logger.handlers:
            return logger
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("{asctime} | {name} | {levelname} | {message}", style="{")
        warning_handler = TimedRotatingFileHandler(filename="warning.log", when="midnight", interval=1, backupCount=30)
        info_handler = TimedRotatingFileHandler(filename="info.log", when="midnight", interval=1, backupCount=7)
        debug_handler = TimedRotatingFileHandler(filename="debug.log", when="midnight", interval=1, backupCount=1)
        
        warning_handler.setFormatter(formatter)
        info_handler.setFormatter(formatter)
        debug_handler.setFormatter(formatter)
        
        warning_handler.setLevel(logging.WARNING)
        info_handler.setLevel(logging.INFO)
        debug_handler.setLevel(logging.DEBUG)
        


        logger.addHandler(warning_handler)
        logger.addHandler(info_handler)
        logger.addHandler(debug_handler)
        return logger
    
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    return logger

get_logger("root")