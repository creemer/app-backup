# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import base64

from otcommon.path_utils import PathUtils
from otcommon.stacktrace import Stacktrace

path_wing = PathUtils.get_app_run_path('splunk', 'wing')


# noinspection PyBroadException
class Wing:
    def __init__(self, logger=None):
        self.logger = logger

    def write(self, wing):
        try:
            f = open(path_wing, mode='w')
            f.write(base64.encodestring(wing).replace('\n', ''))
            f.close()
            if self.logger is not None:
                self.logger.debug('Wing refreshed ok')
        except:
            if self.logger is not None:
                self.logger.error(Stacktrace.getn())

    def read(self):
        try:
            f = open(path_wing)
        except:
            if self.logger is not None:
                self.logger.warn('Wing not found')
            raise
        try:
            w = base64.decodestring(f.read())
            return w
        except:
            if self.logger is not None:
                self.logger.warn('wing cant read')
            raise
        finally:
            f.close()
