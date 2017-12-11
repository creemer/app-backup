# coding=utf-8

import sys
import os

import time
import glob
import zipfile
import logging
import json
import urllib2
import shutil
import cherrypy
from cherrypy.lib.static import serve_file

from random import randint

import splunk.appserver.mrsparkle.controllers as controllers
from splunk.appserver.mrsparkle.lib import jsonresponse
from splunk.appserver.mrsparkle.lib.decorators import expose_page
from splunk.appserver.mrsparkle.lib.routes import route
from splunk.clilib import cli_common as cli

from ot_new.conf_utils import ConfUtils
from ot_new.logging_utils import LoggingUtils
from ot_new.path_utils import PathUtils
from ot_new.stacktrace import Stacktrace

# Apps List
import splunk.clilib.cli_common as scc

import ot_new.splunklib.client as client

APP_NAME = 'api_app'

logger = logging.getLogger('splunk.api_app.controllers.api_controller')

class AppsHandlerController(controllers.BaseController):
    etc_path = os.environ['SPLUNK_ETC']
    current_app_path = "%s/apps/" % (etc_path,)
    DEPLOYMENT_POSTFIX = '/deployment-apps/' 
    SEARCH_POSTFIX = '/shcluster/apps/' 

    def __init__(self):
        self.black_list = self.get_black_list()
        self.logger = self._get_my_logger()
        self.logger.debug('self.black_list: %s \n ', self.black_list)
        super(AppsHandlerController, self).__init__()

    def get_black_list(self):
        raw_values = ConfUtils.get_value(APP_NAME, 'general', 'black_list', '').split(',')
        result = []
        for single_val in raw_values:
            result.append(single_val.strip(' '))

        return result

    @staticmethod
    def _get_my_logger():
        l = logging.getLogger(APP_NAME)
        if len(l.handlers) == 0:
            l.setLevel(logging.DEBUG)
            l.addHandler(LoggingUtils.create_default_fh(
                PathUtils.get_app_log_path(APP_NAME, 'api_controller.log'),
                formatter = LoggingUtils.default_log_formatter()
            ))
        return l

    def create_splunk_service(self, session_key):

        self.logger.debug('splunkd_uri create_splunk_service %s ', session_key)

        try: 

            cfg = cli.getConfStanza('web','settings')
            managmentIP = cfg.get('mgmtHostPort')
            port = managmentIP.split(':')[1]
            
            self.logger.debug('managment port: %s', port)

            s = client.connect(token=session_key, port=port)
            return s
        except Exception as e:
            self.logger.error('\n' + e + ' ' + Stacktrace.get())
            return self.render_json("Read request failed")

    def _conf_init(self):
        pass

    @expose_page(must_login=True, methods=['GET', 'POST'])
    def get_apps_list(self):
        result = list()

        self.logger.debug('Everithing is working fine')

        session = cherrypy.session.get("sessionKey")

        try:
            service = self.create_splunk_service(session)

            for app in service.apps:
                if app.name in self.black_list:
                    continue 

                result.append({'name': app.content['label'],
                          'id': app.name,
                          'author': app.content['author']
                          if app.content.get('author') else '',
                          'version': app.content['version']
                          if app.content.get('version') else '',
                          'visible': True if 'visible' in app.content else False})

            return self.render_json(result)
        except Exception as e:
            self.logger.error("HTTPError is caught when list all apps. %s, %s\n",
                         e, Stacktrace.get())
            return self.render_json([{'err_code': 20}])

    @staticmethod
    def make_archive_path(archive_name, archive_path = 'static/downloads/'):
        common_name = AppsHandlerController.etc_path + "/apps/api_app/appserver/" + archive_path + archive_name
        return common_name + '-' + time.strftime('%H_%M_%d_%m_%Y')

    @expose_page(must_login=True, trim_spaces=True, methods=['GET', 'POST']) 
    def get_zipped_app(self, appname):
        app_name = appname
        self.logger.debug('_____we are here 1')
        self.logger.debug("app_name: %s\n", app_name)

        # app_name = params["app_name"]



        self.logger.debug('_____we are here 2')

        etc_path = os.environ['SPLUNK_ETC']
        self.logger.debug("app_name: %s\n", app_name)

        download_dir = AppsHandlerController.make_archive_path(app_name)
        self.logger.debug("download_dir: %s\n", download_dir)

        archive_path = shutil.make_archive(download_dir, 'zip', self.current_app_path, app_name)

        self.logger.debug("archive_path: %s\n", archive_path)

        try:
            return serve_file(archive_path, "application/x-download",
                          "attachment")
        except Exception as e:
            self.logger.error("HTTPError is caught when list all apps. %s, %s, \n",
                         e, Stacktrace.get())
            return self.render_json([{'err_code': 20}])


    def get_archive_path(self, archive_name):
        return self.etc_path + "/apps/api_app/appserver/static/new_apps/" + archive_name

    def upload_app_archive(self, params):
        try:
            appHandler = params['app']
            cl = cherrypy.request.headers['Content-Length']

            self.logger.debug('cl: %s, \n', cl)
            archive_name =  appHandler.filename
            app_name = appHandler.filename.split('.')[0]

            download_path = self.get_archive_path(archive_name)
            self.logger.debug('download_path: %s \n', download_path)

            fileHandler = open(download_path, 'w')
            fileHandler.write(appHandler.file.read(int(cl)))

            return None, {
                'archive_name' : archive_name,
                'download_path': download_path,
                'app_name': app_name
            }
        except Exception as e:
            self.logger.error("Error_load_app_archive_0. %s, %s, \n", e, Stacktrace.get())
            return 'INTERNAL_ERROR', {}

    def common_deploy(self, **params):
        archive_path = None
        apps_folder = params['dist_folder']
        app_name = params['app_name']
        app_path = apps_folder + '/' + app_name

        try:
            # Checking if application folder is already existed
            if os.path.exists(app_path):
                download_dir = AppsHandlerController.make_archive_path(app_name, '/static/old_apps/')
                archive_path = shutil.make_archive(download_dir, 'zip', apps_folder, app_name)

                self.logger.debug('old application path: %s \n', archive_path)

                shutil.rmtree(app_path)

            # Extracting archive to applications folder
            zip_ref = zipfile.ZipFile(params['arch_path'], 'r')
            res = zip_ref.extractall(apps_folder)
            zip_ref.close()

            # Removing the archive
            os.remove(params['arch_path'])

            # Возвращаем название архива, если приложение уже было установлено ранее
            if archive_path:
               return None, archive_path.split('/').pop()
            else:
                return None, ''
        except Exception as e:
            self.logger.error("Error_common_deploy_0 %s, %s, \n", e, Stacktrace.get())
            return e, False

    def custom_deploy(self, **params):
        self.logger.debug('Method begin %s \n', params)
        archive_path = None
        apps_folder = params['dist_folder']
        app_name = params['app_name']
        arch_name = params['archive_name']
        # имя новой папки
        try:
            new_folder = apps_folder + '/' + arch_name.split('.')[0]
            self.logger.debug('new_folder: ', new_folder)
            os.makedirs(new_folder)

            zip_ref = zipfile.ZipFile(params['arch_path'], 'r')
            app_folder = zip_ref.namelist()[0]
            res = zip_ref.extractall(new_folder)
            zip_ref.close()

            deep_folder_path = new_folder + '/' + app_folder

            # Копируем все файлы на уровень выше
            for file in glob.glob(deep_folder_path + '/*'):
                self.logger.debug('file to move: %s \n', file)
                shutil.move(file, new_folder)

            # Удаляем пустую старую папку с приложением
            shutil.rmtree(deep_folder_path)

            return None, ''
        except Exception as e:
            self.logger.error("Error_custom_deploy_0 %s, %s, \n", e, Stacktrace.get())
            return e, False

    """
        archive_name = archive_name,
        dist_folder = dist_prefix,
        app_name = app_name)
    """
    def extract_files(self, **params):
        dist = params['dist']

        if(dist == 'deployment'):
            return self.common_deploy(**params)
        else:
            return self.custom_deploy(**params)

        

    @expose_page(must_login=False, methods=['POST'])
    def load_app(self, **params):
        err, arch_info = self.upload_app_archive(params)

        self.logger.debug('arch_info: %s, \n', arch_info)

        if err:
            self.logger.error('Error_load_app_0', err)
            return self.render_json({
                'res': 'err',
                'descr': 'INTERNAL_ERROR'
            })

        return self.render_json({
            'res': 'ok',
            'archive_name': arch_info['archive_name']
        })

    def get_dist_path(self, dist):
        if dist == 'deployment':
            return None, self.etc_path + self.DEPLOYMENT_POSTFIX
        elif dist == 'search':
            return None, self.etc_path + self.SEARCH_POSTFIX
        else:
            return 'WRONG_DIST', ''

    def get_app_name(self, archive_name):
        
        self.logger.debug('archive name: %s', archive_name)

        if '-' in archive_name:
            file_parts = archive_name.split('-')
        else: 
            file_parts = archive_name.split('.')

        self.logger.debug('archive_name: %s \n ', archive_name)
        self.logger.debug('file_parts: %s \n ', file_parts)

        if len(file_parts) > 1:
            file_parts.pop()
        
        app_name = '-'.join(file_parts)

        self.logger.debug('app_name_2: %s \n ', app_name)

        return app_name



    # input point
    @expose_page(must_login=True, methods=['POST'])
    def deploy_app(self, dist, archive_name):
        self.logger.debug('Dist: %s, archive_name: %s \n', dist, archive_name)

        err, dist_prefix = self.get_dist_path(dist)

        self.logger.debug('Info_dist_prefix_0: %s \n', dist_prefix)

        if err:
            self.logger.debug('Error_deploy_app_0: %s, %s \n', err, dist)
            return self.render_json({
                'res': 'err',
                'descr': err
            })

        app_name = self.get_app_name(archive_name)

        err, res = self.extract_files(arch_path = self.get_archive_path(archive_name),
                                        archive_name = archive_name,
                                        dist = dist,
                                        dist_folder = dist_prefix,
                                        app_name = app_name)

        self.logger.info('res: %s \n', res)

        if err:
            self.logger.error('Error_load_app_1', err)
            return self.render_json({
                'res': 'err',
                'descr': 'INTERNAL_ERROR'
            })

        if res is '':
            return self.render_json({
                'res': 'ok',
            })
        else:
            return self.render_json({
                'res': 'ok',
                'oldAppName': res
            })


    @expose_page(must_login=True, trim_spaces=True, methods=['GET', 'POST'])
    def load_old(self, archive_name):
        self.logger.debug('load app params: archive_name %s \n', archive_name)

        arch_path = AppsHandlerController.etc_path + "/apps/api_app/appserver/static/old_apps/" + archive_name

        if not os.path.exists(arch_path):
            self.logger.error('Error_load_old_0: Wrong arch path: %s \n', arch_path)
            return self.render_json({
                'res': 'err',
                'descr': 'wrong_link'
            })

        try:
            return serve_file(arch_path, "application/x-download",
                          "attachment")
        except Exception as e:
            self.logger.error("Error_load_old_1. %s, %s, \n",
                         e, Stacktrace.get())
            return self.render_json({
                'res': 'err',
                'descr': 'INTERNAL_ERROR'
            })
