import logging

class Logger :
    def __init__(self, logger_name='dev') : 
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
        

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)