#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import sys
import logging

class Logger():
    def __init__(self):
        self.info = logging.info
        self.debug = logging.debug
        self.warning = logging.warning
        self.error = logging.error
        self.critical = logging.critical
        self.__log_path = 'logs/groot.log'
        self.log_init()

    def log_init(self):
        formatter = logging.Formatter('%(asctime)s %(levelname)s [%(filename)s:%(lineno)d %(funcName)s]: %(message)s')
        self.formatter = formatter
        self.set_file_handler()
        self.set_console_handler()

    def set_file_handler(self):
        fh = logging.FileHandler(self.__log_path)
        fh.setFormatter(self.formatter)
        logging.getLogger('').addHandler(fh)

    def set_console_handler(self):
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(self.formatter)
        logging.getLogger('').addHandler(console)
        logging.getLogger('').setLevel(logging.INFO)

def test():
    logger = Logger()
    logger.info('hi logger!')

if __name__ == '__main__':
    test()


