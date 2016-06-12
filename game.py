#!/usr/bin/env python
import time
import message

import server

from level0 import ShootGameLevel0
from level1 import ShootGameLevel1

def _remote(obj, method, *args, **kwargs):
    obj.sockutil.send_request(obj.client_sock, method=method, *args, **kwargs)

def _remote_callback(obj, method, *args, **kwargs):
    callback = getattr(obj, 'on_%s' % method)
    onerror = getattr(obj, 'on_%s_error' % method)

    obj.sockutil.send_request(
        obj.client_sock, method=method, callback=callback, onerror=onerror,
        *args, **kwargs)


class ShootGame:

    def __init__(self, connection, level):
        """
        Exception:

        NotImplementedError
        """
        self.connection = connection
        self.level_info = level

        connection.sockutil.register_handler(
            'enter_level', self.handle_enter_level, force=True);

        if self.level_info.level_id == 0:
            self.level = ShootGameLevel0(self.connection, self.level_info)
        elif self.level_info.level_id == 1:
            self.level = ShootGameLevel1(self.connection, self.level_info)
        else:
            raise NotImplementedError(
                "Levels other than 0 && 1 is not implemented")

    def handle_enter_level(self):
        self.level.handle_enter_level()

    def start(self):
        print '[+] start level_info.level_id', self.level_info.level_id
        self.level.start(level_id=self.level_info.level_id)

    def update(self):
        self.level.update()

    def destroy(self):
        if self.level is not None:
            self.level.destroy()
