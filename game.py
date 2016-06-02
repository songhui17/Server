#!/usr/bin/env python
import message

class Bot:
    bot_id = 0

    def __init__(self):
        pass
    
    def update(self):
        pass

class ShootGame:

    level_id = 0
    sockutil = None
    client_sock = None

    bot_id = 0
    bots = []

    def __init__(self, sockutil, client_sock):
        self.sockutil = sockutil
        self.client_sock = client_sock
        self._awake()

    def _awake(self):
        print 'ShootGame awake'

    def start(self, *args, **kwargs):
        print 'ShootGame start'
        self.level_id = kwargs.get('level_id', 0)
        self._start_level0()
    
    def _start_level0(self):
        self._spawn_bot('spider')

    def _spawn_bot(self, bot_type):
        self._remote_callback(
                self.client_sock, 'spawn_bot',
                bot_id=self.bot_id, bot_type=bot_type,
                position=message.Vector3(0,0,0),
                rotation=0)
        self.bot_id += 1

    def _remote(self, sock, method, *args, **kwargs):
        self.sockutil.send_request(sock, method=method, *args, **kwargs)

    def _remote_callback(self, sock, method, *args, **kwargs):
        callback = getattr(self, 'on_%s' % method)
        onerror = getattr(self, 'on_%s_error' % method)

        self.sockutil.send_request(
            sock, method=method, callback=callback, onerror=onerror,
            *args, **kwargs)

    def on_spawn_bot(self, sock, **response_):
        print 'on_create_bot:', response_['errno'], response_['request_id']

    def on_spawn_bot_error(self, sock, error, request_id):
        print '[-] on_create_error, error:', error, 'request_id:', request_id

    def update(self):
        print 'ShootGame update'
