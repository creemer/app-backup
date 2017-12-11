# coding=utf-8

import json
import logging
from otcommon.logging_utils import LoggingUtils
from otcommon.path_utils import PathUtils
import splunk.entity as entity

APP_NAME = 'ot_common_library'

class ProtectedStoreError(Exception):
    pass

class ProtectedStore(object):
    STORAGE_PATH = 'storage/passwords'
    STORAGE_OWNER = 'nobody'

    ENTITY_FIELD_REALM = 'realm'
    ENTITY_FIELD_KEY = 'username'
    ENTITY_FIELD_VALUE_ENCRYPTED = 'encr_password'

    # если пароль не удается расшифровать, то этого поля в Entity не будет!!!
    # поэтому перед использованием проверить надичие и выкинуть соотв ошибку
    ENTITY_FIELD_VALUE = 'clear_password'

    def __init__(self, session_key, app_name):
        path_logfile = PathUtils.get_app_log_path(APP_NAME, 'protected_store.log')
        self.logger = logging.getLogger('protected_store_logger')
        if len(self.logger.handlers) == 0:
            self.logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
            from logging.handlers import RotatingFileHandler

            fh = RotatingFileHandler(filename=path_logfile, encoding='utf-8', mode='a',
                                     maxBytes=5 * 1024 * 1024, backupCount=9)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

        if session_key is None or session_key == '':
            raise Exception('session_key required!')
        self.session_key = session_key
        if app_name is None or app_name == '':
            raise Exception('app_name required!')
        self.app_name = app_name

        self.logger = logging.getLogger(APP_NAME)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(LoggingUtils.create_default_fh(
            PathUtils.get_app_log_path(APP_NAME, 'passwords_conf.log'),
            formatter=LoggingUtils.default_log_formatter()
        ))

    def save_protected_dict(self, realm, key, value_dict):
        value_dict_stringified = json.dumps(value_dict, indent=0, sort_keys=1)
        self.save_protected_str(realm, key, value_dict_stringified)

    @staticmethod
    def _entity_encrypt_new_password_value(e, newvalue):
        e.properties['password'] = newvalue

    def save_protected_str(self, realm, key, value_str):
        self.logger.debug('save_protected_str(obj, "%s", "%s", "%s")'
                         % (realm, key, None if value_str is None else 'secret len=%s' % len(value_str)))
        reload(entity)
        e = self._try_find_entity(realm, key)
        if e is not None:
            e[self.ENTITY_FIELD_VALUE] = None
            e[self.ENTITY_FIELD_VALUE_ENCRYPTED] = None
            e[self.ENTITY_FIELD_KEY] = None

            # BUG
            # если не почистить realm, то будет ошибка 'Argument "realm" is not supported by this handler.'
            e[self.ENTITY_FIELD_REALM] = None
            self._entity_encrypt_new_password_value(e, value_str)

            # BUG
            # если тут добавить сессионный ключ, то спланк иногда не может сохранить записи
            try:
                entity.setEntity(e)
            except:
                entity.setEntity(e, sessionKey=self.session_key)
        else:
            e = entity.Entity(self.STORAGE_PATH, key)
            e.namespace = self.app_name
            e[self.ENTITY_FIELD_REALM] = realm
            self._entity_encrypt_new_password_value(e, value_str)
            entity.setEntity(e, sessionKey=self.session_key)

    def load_protected_items_dict(self, realms=None):
        items = self.load_protected_items_str(realms)
        for item in items:
            item['value'] = json.loads(item['value'])
        return items

    def load_protected_items_str(self, realms=None):
        reload(entity)
        storage = self.STORAGE_PATH
        app = self.app_name
        owner = self.STORAGE_OWNER

        # BUG !
        # если не задать search=, то вернутся записи от всех приложений, но расшифроваться не смогут и упадут
        ee = entity.getEntities(storage, search=None, namespace=app, owner=owner, sessionKey=self.session_key)
        result = []
        for full_key, e in ee.items():
            if realms is not None and e[self.ENTITY_FIELD_REALM] not in realms:
                continue
            if self.ENTITY_FIELD_REALM not in e.properties:
                raise ProtectedStoreError('Password cant be decrypted (usually after splunk upgrade)')
            item = {
                'realm': e[self.ENTITY_FIELD_REALM],
                'key': e[self.ENTITY_FIELD_KEY],
                'value': e[self.ENTITY_FIELD_VALUE]
            }
            result.append(item)
        return result


    def _try_find_entity(self, realm, key):
        try:
            e = entity.getEntity(
                self.STORAGE_PATH,
                '%s:%s' % (realm, key),
                namespace=self.app_name, owner=self.STORAGE_OWNER,
                sessionKey=self.session_key
            )
            return e
        except:
            return None

    def load_protected_dict(self, realm, key):
        item = self.load_protected_str(realm, key)
        if item is not None:
            item['value'] = json.loads(item['value'])
        return item

    def load_protected_str(self, realm, key):
        self.logger.debug('load_protected_str(obj, "%s", "%s")' % (realm, key))
        e = self._try_find_entity(realm, key)
        if e is not None:
            if e[self.ENTITY_FIELD_REALM] != realm:
                self.logger.debug('e in other realm = %s' % e[self.ENTITY_FIELD_REALM])
                return None
            # self.logger.info(json.dumps(e.properties, indent=1, ensure_ascii=False, encoding='utf8', sort_keys=True))
            if self.ENTITY_FIELD_REALM not in e.properties:
                raise ProtectedStoreError('Password cant be decrypted (usually after splunk upgrade)')
            item = {
                'realm': e[self.ENTITY_FIELD_REALM],
                'key': e[self.ENTITY_FIELD_KEY],
                'value': e[self.ENTITY_FIELD_VALUE]
            }
            return item
        else:
            self.logger.info('e is None')
        return None

    def force_encrypt_all(self, realms=None):
        for item in self.load_protected_items_str(realms):
            self.save_protected_str(item['realm'], item['key'], item['value'])
