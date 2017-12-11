# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import os
from fasteners.process_lock import InterProcessLock


class UidSequence:
    def __init__(self, uid_value_filepath, uid_pidlock_filepath):
        self.uid_value_filepath = uid_value_filepath
        self.uid_pidlock_filepath = uid_pidlock_filepath
        if not os.path.exists(self.uid_value_filepath):
            self.save_value(0)

    def save_value(self, v):
        fv = open(self.uid_value_filepath, 'w')
        try:
            fv.write(str(v))
        finally:
            fv.close()

    def load_value(self):
        fv = open(self.uid_value_filepath, 'r')
        try:
            v = int(fv.read())
            return v
        finally:
            fv.close()

    def get_next(self):
        a_lock = None
        locked = False
        try:
            a_lock = InterProcessLock(self.uid_pidlock_filepath)
            locked = a_lock.acquire(blocking=True)
            if locked:
                v = self.load_value()
                v_next = v + 1
                self.save_value(v_next)
                return v_next
        finally:
            if locked and a_lock is not None:
                a_lock.release()
