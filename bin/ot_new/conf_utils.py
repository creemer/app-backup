# coding=utf-8

from ot_new.stacktrace import Stacktrace
from splunk.clilib import cli_common


# noinspection PyBroadException
class ConfUtils:
    def __init__(self):
        pass

    @staticmethod
    def get_value(conf_name, stanza_name, param_name, default_value, logger=None):
        try:
            stanza = cli_common.getConfStanza(conf_name, stanza_name)
            try:
                v = stanza[param_name]
            except:
                if logger is not None:
                    logger.warn('%s.conf->[%s]->%s not found, using default value (%s=%s)'
                                % (conf_name, stanza_name, param_name, param_name, default_value))
                v = default_value
        except:
            if logger is not None:
                logger.warn(Stacktrace.getn())
            v = default_value
        return v
