#!/home/ucm/opt/CJ-Python2/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import ConfigParser


class ConfigManager():
    def __init__(self, config_path):
        self.conf_file = config_path
        self.cf = ConfigParser.ConfigParser()
        self.mtime = os.path.getmtime(self.conf_file)
        self.cf.read(self.conf_file)

    def reload(self):
        mtime_new = os.path.getmtime(self.conf_file)
        if self.mtime != mtime_new:
            self.cf.read(self.conf_file)
            self.mtime = mtime_new

    def get(self, section, option):
        self.reload()
        return self.cf.get(section, option)

    def sections(self):
        self.reload()
        return self.cf.sections()

    def options(self, section):
        self.reload()
        return self.cf.options(section)


def test():
    cm = ConfigManager('groot_conf.ini')
    print cm.get('hbase', 'version')


if __name__ == '__main__':
    test()


