#!/usr/bin/env python
import time
import message

import server
import dbutil
from servererrno import *

# TODO
def _remote(obj, method, *args, **kwargs):
    obj.sockutil.send_request(obj.client_sock, method=method, *args, **kwargs)

def _remote_callback(obj, method, *args, **kwargs):
    callback = getattr(obj, 'on_%s' % method)
    onerror = getattr(obj, 'on_%s_error' % method)

    obj.sockutil.send_request(
        obj.client_sock, method=method, callback=callback, onerror=onerror,
        *args, **kwargs)


class ShootGameLevel0:

    level_id = 0
    sockutil = None
    client_sock = None

    bot_id = 0
    bots = []

    # TODO
    connection = None
    finished = False

    def __init__(self, connection, level):
        # import pdb; pdb.set_trace()
        print '[+] ShootGameLevel0'
        self.connection = connection

        self.actor = connection.actor
        self.sockutil = connection.sockutil
        self.client_sock = connection.client_sock
        self.level = level

        self.entered = False

        # TODO
        self.sockutil.register_handler(
            'level0_bot_killed', self.handle_level0_bot_killed, force=True);
        self.sockutil.register_handler(
            'update_actor_hp', self.handle_update_actor_hp, force=True);

    def handle_level0_bot_killed(self, bot_id):
        print '[+] kill'
        if bot_id == -2:  # player
            _remote(self, 'finish_level', win=False)
            self.finished = True
            return

        self.killed += 1
        if self.killed == self.max_bot_count:
            print '[+] finish level0 bot_count=%d, max_bot_count=%d'\
                % (self.bot_count, self.max_bot_count)

            self.update_actor_info()

            _remote(self, 'finish_level', win=True)
            self.finished = True
        else:
            spot = self.spawn_spot[self.bot_count]
            self._spawn_bot('spider', x=spot[0], y=spot[1],
                            z=spot[2], rot_y=spot[3])

    def _clamp(self, value, min, max):
        assert min <= max
        if value < min:
            value = min
        if value > max:
            value = max
        return value

    def handle_update_actor_hp(self, actor_id, hp, max_ammo, ammo):
        # if self.actor.actor_id != actor_id:
        #     return message.UpdateActorHpRequestResponse(errno=E_INVALID
        if hp <= 0:  # never dead
            hp = 10
        if max_ammo <= 0:
            max_ammo = 18

        self.actor.hp = self._clamp(hp, 0, self.actor.max_hp)
        self.actor.max_ammo = self._clamp(max_ammo, 0, 4096)
        self.actor.ammo = self._clamp(ammo, 0, 18)  #TODO: magic number
        dbutil.actor_update(self.connection.actordb, self.actor)
        return message.UpdateActorHpRequestResponse(errno=E_OK)

    def start(self, *args, **kwargs):
        print 'ShootGame start'
        self.level_id = kwargs.get('level_id', 0)
        _remote(self, 'start_level', actor_id=0, level_id=self.level_id)
    
    def handle_enter_level(self):
        self.entered = True
        self.max_bot_count = 3
        self.killed = 0
        self.spawn_spot = [
            (20, -0.05, 15, 90),
            (18, -0.05, 16, 90),
            (19, -0.05, 18, 90),
        ]

        self.bot_count = 0
        self.spawn_interval = 5
        self.time_since_start = time.clock()
        # self.next_spawn_time = self.time_since_start + self.spawn_interval

        spot = self.spawn_spot[self.bot_count]
        self._spawn_bot('spider', x=spot[0], y=spot[1],
                        z=spot[2], rot_y=spot[3])

    def update_actor_info(self):
        self.actor.experience += 1000
        self.actor.gold += 100
        self.actor.level += 1
        # self.actor.actordb = self.connection.actordb
        # self.actor.update()
        dbutil.actor_update(self.connection.actordb, self.actor)

        actor_level_info = message.ActorLevelInfo()
        actor_level_info.actor_id = self.actor.actor_id
        actor_level_info.level_id = self.level.level_id
        actor_level_info.passed = True
        actor_level_info.star1 = True
        actor_level_info.star2= True
        actor_level_info.star3= True
        # actor_level_info.actorleveldb = self.connection.actorleveldb
        # actor_level_info.update()
        dbutil.actor_level_info_update(
            self.connection.actorleveldb,
            actor_level_info)

    def _spawn_bot(self, bot_type,
                   x=0, y=0, z=0, rot_y=0):
        self.bot_count += 1
        _remote_callback(
            self, 'spawn_bot', bot_id=self.bot_id, bot_type=bot_type,
            position=message.Vector3(x=x, y=y, z=z), rotation=rot_y)
        self.bot_id += 1

    def on_spawn_bot(self, sock, **response_):
        print 'on_create_bot:', response_['errno'], response_['request_id']

    def on_spawn_bot_error(self, sock, error, request_id):
        print '[-] on_create_error, error:', error, 'request_id:', request_id

    def update(self):
        pass

    def destroy(self):
        pass
