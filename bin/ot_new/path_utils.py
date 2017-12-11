# coding=utf-8

import os


class PathUtils:
    def __init__(self):
        pass

    @staticmethod
    def get_splunk_home():
        return os.getenv('SPLUNK_HOME')

    @staticmethod
    def get_splunk_app_root(app_name):
        return os.path.join(PathUtils.get_splunk_home(), 'etc', 'apps', app_name)

    @staticmethod
    def get_splunk_app_bin(app_name):
        return os.path.join(PathUtils.get_splunk_app_root(app_name), 'bin')

    @staticmethod
    def get_splunk_log_root():
        return os.path.join(PathUtils.get_splunk_home(), 'var', 'log')

    @staticmethod
    def get_splunk_run_root():
        return os.path.join(PathUtils.get_splunk_home(), 'var', 'run')

    @staticmethod
    def get_app_log_path(app_name, log_name):
        path = os.path.join(PathUtils.get_splunk_log_root(), app_name)
        if not os.path.exists(path):
            os.makedirs(path)
        return os.path.join(path, log_name)

    @staticmethod
    def get_app_run_path(app_name, run_name):
        path = os.path.join(PathUtils.get_splunk_run_root(), app_name)
        if not os.path.exists(path):
            os.makedirs(path)
        return os.path.join(path, run_name)
