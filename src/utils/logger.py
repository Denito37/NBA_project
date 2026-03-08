"""
    logger
"""
import logging

def get_logger(name):
    """
    Docstring for get_logger
    
    """
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
