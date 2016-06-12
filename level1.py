#!/usr/bin/env python
import math
import time
import json
import heapq
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


def v3_direction(start, end):
    return v3_minus(end, start)


def v3_distance(start, end):
    return v3_magnitude(v3_minus(start, end))


def v3_rotate(v3, angle):
    """v3_rotate
    -> (cosT + (- angle), 0, sinT + (- angle))
    -> (cosT * cosAngle - sinT * sinAngle, sinT * cosAngle + cosT * sinAngle)
    >>> v = message.Vector3(x=0, y=0, z=1)
    >>> v2 = v3_rotate(v, 90)
    >>> int(v2.x), int(v2.z)
    (1, 0)
    >>> v3 = v3_rotate(v2, -90)
    >>> int(v3.x), int(v3.z)
    (0, 1)
    """
    angle = -math.radians(angle)
    x = v3.x
    z = v3.z
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    new_x = x * cos_angle - z * sin_angle
    new_z = z * cos_angle + x * sin_angle
    return message.Vector3(x=new_x, y=0, z=new_z)


def v3_euler_y(rot_y):
    """v3_euler_y -> vector3 (forward)
    rot_y: angle
    """
    return v3_rotate(message.Vector3(x=0, y=0, z=1), rot_y)


def v3_to_euler_y(v3):
    """v3_to_euler_y -> forward to euler angle (around y-axis)
    >>> v = message.Vector3(x=1, y=0, z=1)
    >>> int(v3_to_euler_y(v))
    45
    """
    v = message.Vector3(x=v3.x, y=0, z=v3.z)
    return v3_angle_cw(message.Vector3(x=0, y=0, z=1), v)

def v3_angle_cw(start, end):
    """v3_angle_cw -> clockwise angle
    >>> v1 = message.Vector3(x=0, y=0, z=1)
    >>> v2 = message.Vector3(x=1, y=0, z=0)
    >>> int(v3_angle_cw(v1, v2))
    90
    """
    dot = v3_dot(start, end)
    mag = v3_magnitude(start) * v3_magnitude(end)
    if mag == 0:
        return 0
    cost_t = dot / mag
    if cost_t < -1:
        cost_t = -1
    if cost_t > 1:
        cost_t = 1

    theta = math.degrees(math.acos(cost_t))
    is_left = v3_xz_isleft(start, end)
    return theta if is_left else -theta


def v3_xz_isleft(left, right):
    """
    >>> v1 = message.Vector3(x=0, y=0, z=1)
    >>> v2 = message.Vector3(x=1, y=0, z=0)
    >>> v3_xz_isleft(v1, v2)
    True
    """
    return v3_xz_signed_area(left, right) < 0


def v3_xz_signed_area(left, right):
    """
    >>> v1 = message.Vector3(x=0, y=0, z=1)
    >>> v2 = message.Vector3(x=1, y=0, z=0)
    >>> v3_xz_signed_area(v1, v2)
    -1
    """
    return left.x * right.z - left.z * right.x


def v3_minus(left, right):
    return message.Vector3(
        x=left.x - right.x,
        y=left.y - right.y,
        z=left.z - right.z)


def v3_add(left, right):
    return message.Vector3(
        x=left.x + right.x,
        y=left.y + right.y,
        z=left.z + right.z)

def v3_magnitude(v3):
    return math.sqrt(v3.x * v3.x + v3.y * v3.y + v3.z * v3.z) 


def v3_sqr_magnitude(v3):
    return v3.x * v3.x + v3.y * v3.y + v3.z * v3.z 


def v3_dot(left, right):
    return left.x * right.x + left.y * right.y + left.z * right.z


def v3_multiple(v3, f):
    v3.x *= f
    v3.y *= f
    v3.z *= f
    return v3


def v3_normalize(v3):
    mag = v3_magnitude(v3)
    if mag == 0:
        return v3
    else:
        return v3_multiple(v3, 1.0 / mag)


STATE_IDLE = 0
STATE_ATTACK = 0
STATE_GOTO = 1
STATE_EXPLOSE = 2

class DestroyTowerBehavior:
    
    def __init__(self, bot, target):
        self.bot = bot
        self.state = STATE_IDLE
        self._enter_idle()
        self.target_position = target

    def _enter_idle(self):
        pass

    def _update_idle(self):
        if self.target_position is not None:
            self._leave_idle()
            self._enter_goto()

    def _leave_idle(self):
        pass

    def _enter_goto(self):
        print '_enter_goto:', self.bot.bot_id
        self.state = STATE_GOTO
        _remote(self, 'bot_play_animation',
                bot_id=self.bot.bot_id,
                animation_clip='walk')

        self.path = self.tile_map.find_path(
            self.bot.position, self.target_position)
        self.next_position = self.path.get_next_waypoint(
            position=self.bot.position)
        # import pdb; pdb.set_trace()

        if self.next_position is None:
            print '_leave_goto:', self.bot.bot_id
            self._leave_goto()

    def on_bot_play_animation(self, sock, **response):
        pass

    def on_bot_play_animation_error(self, sock, error, request_id):
        pass

    def _update_goto(self):
        next_position = self.next_position
        next_position.y = 0
        position = self.bot.position
        position.y = 0
        # import pdb; pdb.set_trace()
        # TODO
        delta_time = 0.02
        speed = 1.0
        direction = v3_direction(position, next_position)
        v3_normalize(direction)
        movement = v3_multiple(direction, speed * delta_time)
        new_position = v3_add(position, movement)

        rotate_speed = 100
        rot_y = self.bot.rotation
        forward = v3_euler_y(rot_y)
        angle = v3_angle_cw(forward, direction)
        if -1 < angle < 1:
            pass
        else:
            angle_sign = 1 if angle > 0 else -1
            target_rot_y = rot_y + angle
            delta_angle = angle_sign * rotate_speed * delta_time
            new_rot_y = rot_y + delta_angle

            new_angle = target_rot_y - new_rot_y
            if new_angle * angle <= 0 or -1 < new_angle < 1:
                new_rot_y = target_rot_y

            self.bot.rotation = new_rot_y

        # go pass
        sqr_stoping_distance = 0.01
        to_next = v3_minus(next_position, position)
        new_to_next = v3_minus(next_position, new_position)

        self.bot.position = new_position
        if (v3_sqr_magnitude(new_to_next) < sqr_stoping_distance
                or v3_dot(to_next, new_to_next) <= 0):
            self.next_position = self.path.get_next_waypoint()
            if self.next_position is None:
                self._leave_goto()

                to_target = v3_minus(new_position, self.target_position)
                if v3_sqr_magnitude(to_target) < sqr_stoping_distance:
                    self._enter_explose()
                else:
                    # TODO:navigation failure
                    self._enter_explose()

        if self.state == STATE_GOTO:
            # resolve collision
            this_bot = self.bot
            for other in self.level1.bots:
                if other == this_bot:
                    continue
                distance = v3_distance(this_bot.position, other.position)
                if distance > 1:
                    continue

                # collision
                to_other = v3_minus(other.position, this_bot.position)
                if v3_dot(to_other, direction) < 0:
                    continue

                if other.get_is_moving():
                    # push
                    print '[+] push'
                    push_distance = distance - 1
                    v3_normalize(to_other)
                    new_position = v3_add(
                        position, v3_multiple(to_other, push_distance))
                    this_bot.position = new_position


    def _leave_goto(self):
        self.state = STATE_IDLE
    
    def _enter_explose(self):
        self.bot.explose()


    def _update_explose(self):
        pass

    def _leave_explose(self):
        pass

    def update(self):
        if self.state == STATE_IDLE:
            self._update_idle()
        elif self.state == STATE_GOTO:
            self._update_goto()
        elif self.state == STATE_EXPLOSE:
            pass


class Tower:

    def __init__(self, id, hp, position, on_dead=None):
        self.tower_id = 0
        self.hp = hp
        self.position = position
        self.on_dead = on_dead

    def apply_damage(self, damage):
        print '[+] apply_damage, self.hp:', self.hp, '->', self.hp - damage
        self.hp -= damage

        _remote(self, 'tower_hp_sync', tower_id=self.tower_id, hp=self.hp)
        if self.hp <= 0:
            self.hp = 0

            if self.on_dead:
                self.on_dead()

    def on_tower_hp_sync(self, sock, **response_):
        pass

    def on_tower_hp_sync_error(self, sock, error, request_id):
        pass


class Bot:

    def __init__(self, bot_id, tile_map, target, level1):
        self.bot_id = 0
        # self.tile_map = tile_map
        self.position = message.Vector3(x=0, y=0, z=0)
        self.rotation = 0
        self.explose_target = target  # 
        self.behavior = DestroyTowerBehavior(
            self, self.explose_target.position)
        # self.behavior.tile_map = self.tile_map
        self.behavior.tile_map = tile_map

        # TODO
        self.behavior.level1 = level1

        self.behavior.sockutil = level1.sockutil
        self.behavior.client_sock = level1.client_sock


        self.dead = False

    def get_is_moving(self):
        return (not self.dead) and self.behavior.state == STATE_GOTO

    def update(self, delta_time=0.02):
        # self.position.x += 1 * delta_time
        if self.dead:
            return

        self.behavior.update()

        _remote(self, 'bot_transform_sync',
                bot_id=self.bot_id, position=self.position,
                rotation=self.rotation,
                waypoint_position=self.behavior.next_position)

    def on_bot_transform_sync(self, sock, **response_):
        pass

    def on_bot_transform_sync_error(self, sock, error, request_id):
        pass

    def explose(self):
        self.dead = True
        print '[+] explose, bot_id:', self.bot_id
        # TODO:
        self.explose_target.apply_damage(10)
        _remote(self, 'bot_explose',
                bot_id=self.bot_id)

    def on_bot_explose(self, sock, **response_):
        pass

    def on_bot_explose_error(self, sock, error, request_id):
        pass

class Waypoint:

    def __init__(self, position):
        """
        position: tuple (x, y)
        """
        self.position = position
    
    def get_vector3(self):
        """get_vector3 -> message.Vector3
        """
        return message.Vector3(
            x=self.position[0],
            y = 0,
            z=self.position[1]
        )


class Path:

    tile_map = None

    def __init__(self):
        self.index = 0
        self.waypoints = []


    def _get_vector3(self, index):
        x, y, z = self.tile_map.get_center(index)
        return message.Vector3(x=x, y=y, z=z)

    def get_next_waypoint(self, position=None):
        """get_next_waypoint -> message.Vector3, None is no more waypoint.
        Give position if to smooth the path based on position
        """
        if self.index >= len(self.waypoints):
            return None

        if not isinstance(position, message.Vector3):
            next_position = self._get_vector3(self.waypoints[self.index].position)
            self.index += 1
            return next_position

        for i in range(self.index, len(self.waypoints)):
            next_position = self._get_vector3(self.waypoints[i].position)
            if self.tile_map.see_through(position, next_position):
                self.index = i
            else:
                break

        next_position = self._get_vector3(self.waypoints[self.index].position)
        self.index += 1
        return next_position


class Tile:

    def __init__(self, index=(0, 0), cost=0xFFFFFFFF, height=0):
        self.index = index
        self.cost = cost
        self.closed = False
        self.visited = False
        self.prev = self.index
        self.height = height

    def reset_find(self):
        self.cost = 0xFFFFFFFF
        self.closed = False
        self.visited = False
        self.prev = self.index
        # self.height = height

    def __lt__(self, other):
        return self.cost < other.cost

    def __str__(self):
        info = ''
        info += 'index: %s\n' % str(self.index)
        info += 'cost: %s\n' % self.cost
        info += 'closed: %s\n' % self.closed
        info += 'visited: %s\n' % self.visited
        info += 'prev: %s\n' % str(self.prev)
        info += 'height: %s\n' % self.height
        return info


class TileMap:

    def __init__(self):
        from os import path
        if path.isfile('..\map'):
            with open('..\map') as f:
                self.raw = json.load(f)

        if path.isfile('map'):
            with open('map') as f:
                self.raw = json.load(f)

        self.row_count = self.raw['RowCount']
        self.column_count = self.raw['ColumnCount']
        self.stride = self.raw['Stride']
        self.tiles = []
        row, column = (0, 0)
        for tile in self.raw['Tiles']:
            self.tiles.append(Tile(index=(row, column), height=tile))

            if column == self.column_count - 1:
                row += 1
                column = 0
            else:
                column += 1

    def get_center(self, tile):
        """get_center -> (x, y, z)
        """
        index = tile.index if isinstance(tile, Tile) else tile
        x = (index[1] + 0.5) * self.stride
        y = 0
        z = (index[0] + 0.5) * self.stride
        return x, y, z

    def _one_dim_index(self, index):
        """_one_dim_index -> int
        index: (row, colum)
        """
        return index[0] * self.column_count + index[1]

    def _get_tile(self, index):
        """_get_tile -> Tile
        index: (row, colum)
        """
        return self.tiles[self._one_dim_index(index)]

    def position_to_index(self, pos):
        """position_to_index -> (row, column)
        pos: message.Vector3
        """
        return int(math.floor(pos.z)), int(math.floor(pos.x))

    def see_through(self, start, end):
        """see_through -> T|F
        Params
        start   :message.Vector3 or tuple(row, column)
        end     :message.Vector3 or tuple(row, column)
        """
        print start, '-?->', end
        start_index = start
        if isinstance(start, message.Vector3):
            start_index = self.position_to_index(start)

        end_index = end
        if isinstance(end, message.Vector3):
            end_index = self.position_to_index(end)

        start_row = min(start_index[0], end_index[0])
        end_row = max(start_index[0], end_index[0])
        start_column = min(start_index[1], end_index[1])
        end_column = max(start_index[1], end_index[1])

        s_x, _, s_z = self.get_center(start_index)
        for row in range(start_row, end_row + 1):
            for column in range(start_column, end_column + 1):
                tile = self._get_tile((row, column))
                # intersect
                o_x, _, o_z = self.get_center(tile)
                d = 0
                # u dot v = ||u|| * ||v|| * cosT
                # os dot n = ||os|| * cosT * 1
                # d = (os dot n)
                v = (end_index[1] - start_index[1],
                     end_index[0] - start_index[0])
                n = (-v[1], v[0])
                mag = math.sqrt(n[0] * n[0] + n[1] * n[1])
                os = (s_x - o_x, s_z - o_z)
                d = os[0] * n[0] + os[1] * n[1]
                # d /= mag
                d = d / mag if mag > 0 else 0
                if d < 0:
                    d = -d
                # print d, tile.height, self.stride / 2.0
                if d < self.stride / 2.0 and tile.height != 0:
                    # import pdb; pdb.set_trace()
                    return False

        return True

    def find_path(self, start_pos, target_pos):
        path = self._find_path(start_pos, target_pos, smooth=True)
        if path is None:
            p = Path()
            p.tile_map = self
            return Path()
        else:
            p = Path()
            p.tile_map = self
            for point_index in range(len(path) - 1, -1, -1):
                p.waypoints.append(Waypoint(path[point_index][0]))
            return p

    def _find_path(self, start_pos, target_pos, smooth=False):
        for tile in self.tiles:
            tile.reset_find()

        open_list = []
        # closed_list = []
        start_index = int(math.floor(start_pos.z)),\
            int(math.floor(start_pos.x))

        target_index = int(math.floor(target_pos.z)),\
            int(math.floor(target_pos.x))

        start_tile = self._get_tile(start_index)
        start_tile.cost = 0
        if start_tile.height != 0:
            print '[+] invalid start pos'
            return

        target_tile = self._get_tile(target_index)
        if target_tile.height != 0:
            print '[+] invalid target pos'
            return

        heapq.heappush(open_list, start_tile)
        found_tile = None
        while True:
            if not open_list:
                break

            top = heapq.heappop(open_list)
            top.closed = True
            if top.index == target_index:
                print '[+] found:', top
                found_tile = top
                break

            #   2((-1, 1), 1.4)   3((0, 1), 1.0)   4((1, 1), 1.4)     
            #                                 
            #   1((-1, 0), 1)                      5((1, 0), 1)       
            #                                 
            #   0((-1, -1), 1.4)  7((0, -1), 1.0)  6((1, -1), 1.4)   
            neigh_index = [
                ((-1, +1), 1.4), ((0, 1), 1.0), ((+1, +1), 1.4),
                ((-1, +0), 1.0),                ((+1, +0), 1.0),
                ((-1, -1), 1.4), ((0, -1), 1.0), ((+1, -1), 1.4),
            ]

            for neigh in neigh_index:
                top_index = top.index
                index = neigh[0]
                index = (top_index[0] + index[0], top_index[1] + index[1])
                if not (0 < index[0] < self.row_count
                        and 0 < index[1] < self.column_count):
                    continue

                neigh_tile = self._get_tile(index)
                if neigh_tile.closed or neigh_tile.height != 0:
                    continue

                cost = top.cost + neigh[1]
                if cost < neigh_tile.cost:
                    neigh_tile.cost = cost
                    neigh_tile.prev = top_index

                    if neigh_tile.visited:
                        heapq.heapify(open_list)
                    else:
                        neigh_tile.visited = True
                        heapq.heappush(open_list, neigh_tile)

        if smooth and found_tile:
            self.smooth_path(found_tile, start_tile)

        if found_tile:
            print '[+] found'
            path = []
            while True:
                path.append((found_tile.index, found_tile.cost))
                prev_index = found_tile.prev
                if prev_index == found_tile.index:
                    break
                found_tile = self._get_tile(prev_index)
            return path
        else:
            print '[+] not found'
            # import pdb; pdb.set_trace()

    def smooth_path(self, target_tile, start_tile):
        print 'target_tile:\n', target_tile
        current_tile = target_tile
        prev_tile = self._get_tile(current_tile.prev)
        farest_tile = prev_tile
        while True:
            if farest_tile.index == start_tile.index:
                print '[+] done farest_tile:', farest_tile
                break

            while True:
                def min(x, y):
                    return x if x < y else y

                def max(x, y):
                    return x if x >= y else x

                # print 'check', current_tile, '->', prev_tile
                if self.see_through(current_tile.index, prev_tile.index):
                    farest_tile = prev_tile
                    prev_tile = self._get_tile(prev_tile.prev)
                else:
                    print '[-] miss farest_tile', farest_tile
                    break

                if farest_tile.index == farest_tile.prev:
                    break

            if current_tile == farest_tile:
                # corner
                current_tile = self._get_tile(current_tile.prev)
                farest_tile = current_tile
            else:
                current_tile.prev = farest_tile.index
                current_tile = farest_tile


class Item:

    def __init__(self):
        self.item_type = 'ammo'
        self.position = message.Vector3(x=0,y=0,z=0)


class ShootGameLevel1:

    level_id = 1
    sockutil = None
    client_sock = None

    bot_id = 0

    # TODO
    connection = None
    finished = False

    def __init__(self, connection, level):
        # import pdb; pdb.set_trace()
        print '[+] ShootGameLevel1'
        self.connection = connection

        self.actor = connection.actor
        self.sockutil = connection.sockutil
        self.client_sock = connection.client_sock
        self.level = level

        self.bots = []

        self.entered = False

        self.tile_map = TileMap()

        self.explose_target = Tower(
            0, 200, message.Vector3(x=34, y=0, z=16.4),
            self.on_tower_destroyed)
        self.explose_target.sockutil = self.sockutil
        self.explose_target.client_sock = self.client_sock

        # TODO
        self.sockutil.register_handler(
            'level0_bot_killed', self.handle_level0_bot_killed, force=True);
        self.sockutil.register_handler(
            'update_actor_hp', self.handle_update_actor_hp, force=True);
        self.sockutil.register_handler(
            'bot_transform_sync', self.handle_bot_transform_sync, force=True);

    def on_tower_destroyed(self):
        _remote(self, 'finish_level', win=False)
        self.finished = True

    # TODO: copy from level0.py
    def _clamp(self, value, min, max):
        assert min <= max
        if value < min:
            value = min
        if value > max:
            value = max
        return value

    def handle_bot_transform_sync(
            self, bot_id, position,
            rotation, waypoint_position):
        if bot_id != -2:
            return message.BotTransformSyncRequestResponse()

        if not self.ammo_item:
            return message.BotTransformSyncRequestResponse()

        item_position = self.ammo_item.position
        position = message.Vector3(**position)
        position.y = 0
        item_position = message.Vector3(
            x=item_position.x, y=0, z=item_position.z)
        if v3_distance(item_position, position) < 1:
            print '[+] use_item'
            self.actor.max_ammo += 18
            dbutil.actor_update(self.connection.actordb, self.actor)
            _remote(self, 'use_item', item_type=self.ammo_item.item_type)
            self.ammo_item = None
        return message.BotTransformSyncRequestResponse()

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

    def handle_level0_bot_killed(self, bot_id):
        print '[+] kill'
        if bot_id == -2:  # player
            _remote(self, 'finish_level', win=False)
            self.finished = True
            return

        self.killed += 1
        if bot_id == self.bot_king.bot_id:
            self.update_actor_info()

            _remote(self, 'finish_level', win=True)
            self.finished = True
        else:
            self.bots[bot_id - 1].dead = True

    def start(self, *args, **kwargs):
        print 'ShootGame start'
        self.level_id = kwargs.get('level_id', 0)
        _remote(self, 'start_level', actor_id=0, level_id=self.level_id)
    
    def handle_enter_level(self):
        self.entered = True
        self.max_bot_count = 100 * 3
        self.killed = 0
        self.spawn_spot = [
            (19, 0, 8, 0),
            (18, 0, 9, 0),
            (20, 0, 8, 0),
        ]

        self.bot_count = 0
        self.spawn_interval = 15
        self.time_since_start = time.clock()
        self.next_spawn_time = self.time_since_start + self.spawn_interval

        king_spot = (12, 0, 4, 90)
        self.bot_king = self._spawn_bot(
                'spider_king', x=king_spot[0], y=king_spot[1],
                z=king_spot[2], rot_y=king_spot[3])
        self.bots.pop()  # TODO

        # import pdb; pdb.set_trace()
        for spot in self.spawn_spot:
            self._spawn_bot('spider_remote', x=spot[0], y=spot[1],
                            z=spot[2], rot_y=spot[3])

        self.ammo_item = Item()
        self.ammo_item.position = message.Vector3(x=25.14, y=1.26, z=14.89)
        _remote(self, 'spawn_item', item_type=self.ammo_item.item_type,
                position=self.ammo_item.position)

    def on_spawn_item(self, sock, **response_):
        print 'on_spawn_item:', response_['request_id']

    def on_spawn_item_error(self, sock, error, request_id):
        print '[-] on_spawn_item_error, error:', error, 'request_id:', request_id

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
        bot = Bot(self.bot_id, self.tile_map, self.explose_target, self)
        bot.bot_id = self.bot_id
        bot.position = message.Vector3(x=x, y=y, z=z)
        bot.rotation = rot_y
        bot.sockutil = self.sockutil
        bot.client_sock = self.client_sock

        self.bots.append(bot)

        _remote_callback(
            self, 'spawn_bot', bot_id=self.bot_id, bot_type=bot_type,
            position=bot.position, rotation=bot.rotation)

        self.bot_id += 1
        return bot

    def on_spawn_bot(self, sock, **response_):
        print 'on_create_bot:', response_['errno'], response_['request_id']

    def on_spawn_bot_error(self, sock, error, request_id):
        print '[-] on_create_error, error:', error, 'request_id:', request_id

    def update(self):
        if self.finished or (not self.entered):
            return
        # import pdb; pdb.set_trace()
        
        if (self.bot_count < self.max_bot_count and time.clock() > self.next_spawn_time):
            print '[+] spawn'
            self.next_spawn_time += self.spawn_interval
            # self._spawn_bot('spider')

            for spot in self.spawn_spot:
                self._spawn_bot('spider_remote', x=spot[0], y=spot[1],
                                z=spot[2], rot_y=spot[3])

        for bot in self.bots:
            bot.update()

    def destroy(self):
        pass

    
if __name__ == '__main__':
    import doctest
    doctest.testmod()

