#!/usr/bin/env python
import time
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

    finished = False

    def __init__(self, sockutil, client_sock):
        # import pdb; pdb.set_trace()
        self.sockutil = sockutil
        self.client_sock = client_sock

        self.sockutil.register_handler(
            'enter_level', self.handle_enter_level, force=True);
        self.sockutil.register_handler(
            'level0_bot_killed', self.handle_level0_bot_killed, force=True);

        self._awake()

    def _awake(self):
        print 'ShootGame awake'

    def start(self, *args, **kwargs):
        print 'ShootGame start'
        self.level_id = kwargs.get('level_id', 0)
        # TODO:
        # self._start_level0()
        # TODO: error
        self._remote('start_level', actor_id=0, level_id=0)
    
    def handle_enter_level(self):
        self.max_bot_count = 3
        self.spawn_spot = [
            (20, -0.05, 15, 90),
            (18, -0.05, 16, 90),
            (19, -0.05, 18, 90),
        ]

        self.bot_count = 0
        self.spawn_interval = 5
        self.time_since_start = time.clock()
        self.next_spawn_time = self.time_since_start + self.spawn_interval

        # self._start_level0();
        spot = self.spawn_spot[self.bot_count]
        self._spawn_bot('spider', x=spot[0], y=spot[1],
                        z=spot[2], rot_y=spot[3])

    def handle_level0_bot_killed(self):
        if self.bot_count == self.max_bot_count:
            print '[+] finish level0 bot_count=%d, max_bot_count=%d'\
                % (self.bot_count, self.max_bot_count)
            self._remote('finish_level')
            self.finished = True
        else:
            print '[+] spawn bot level0 bot_count=%d, max_bot_count=%d'\
                % (self.bot_count, self.max_bot_count)
            spot = self.spawn_spot[self.bot_count]
            self._spawn_bot('spider', x=spot[0], y=spot[1],
                            z=spot[2], rot_y=spot[3])

    # TODO
    # def _start_level0(self):
        # self._spawn_bot('spider')

    def _spawn_bot(self, bot_type,
                   x=0, y=0, z=0, rot_y=0):
        self.bot_count += 1
        self._remote_callback(
            'spawn_bot', bot_id=self.bot_id, bot_type=bot_type,
            position=message.Vector3(x,y,z), rotation=rot_y)
        self.bot_id += 1

    def _remote(self, method, *args, **kwargs):
        self.sockutil.send_request(self.client_sock, method=method, *args, **kwargs)

    def _remote_callback(self, method, *args, **kwargs):
        callback = getattr(self, 'on_%s' % method)
        onerror = getattr(self, 'on_%s_error' % method)

        self.sockutil.send_request(
            self.client_sock, method=method, callback=callback, onerror=onerror,
            *args, **kwargs)

    def update(self):
        print 'ShootGame update'
        if self.finished:
            return
        
        # if (self.bot_count < self.max_bot_count
                # and time.clock() > self.next_spawn_time):
            # self.next_spawn_time += self.spawn_interval
            # self._spawn_bot('spider')

        # self._remote('finish_level')
        # self.finished = True

    def destroy(self):
        pass

    def on_spawn_bot(self, sock, **response_):
        print 'on_create_bot:', response_['errno'], response_['request_id']

    def on_spawn_bot_error(self, sock, error, request_id):
        print '[-] on_create_error, error:', error, 'request_id:', request_id

