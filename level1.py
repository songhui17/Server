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


def v3_sqr_distance(start, end):
    return v3_sqr_magnitude(v3_minus(start, end))


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
STATE_ATTACK = 1
STATE_GOTO = 2
STATE_EXPLOSE = 3


class GotoBehavior:

    def __init__(self, bot, tile_map):
        """
        Params:
        bot         :
        tile_map    :    
        """
        self.bot = bot
        self.tile_map = tile_map
        self.sqr_wp_stoping_distance = 0.01
        self.sqr_stoping_distance = 1
        self.level1 = None

        self.next_position = bot.position
        self.speed = 1.0  # 4.0

    def _has_waypoint(self):
        return self.next_position is not None

    def _has_reached(self):
        to_target = v3_minus(self.bot.position, self.target_position)
        return v3_sqr_magnitude(to_target) <= self.sqr_stoping_distance

    def set_destination(self, target_position):
        self.target_position = target_position

    def validate(self):
        return self.target_position is not None

    def activate(self):
        self.path = self.tile_map.find_path(
            self.bot.position, self.target_position)
        self.next_position = self.path.get_next_waypoint(
            position=self.bot.position)

    def move_toward(
            self, delta_time,
            next_position, sqr_stoping_distance=0.01,
            stoping_angle=1):
        """move_toward -> (in_range:T|F, in_angle:T|F), move to next_position
        """
        # next_position = self.next_position
        next_position.y = 0
        position = self.bot.position
        position.y = 0

        # import pdb; pdb.set_trace()
        # TODO

        # delta_time = 0.02
        # speed = 1.0
        speed = self.speed

        direction = v3_direction(position, next_position)
        v3_normalize(direction)
        movement = v3_multiple(direction, speed * delta_time)
        new_position = v3_add(position, movement)

        rotate_speed = 100
        rot_y = self.bot.rotation
        forward = v3_euler_y(rot_y)
        angle = v3_angle_cw(forward, direction)
        in_angle = False
        if -stoping_angle < angle < stoping_angle:
            new_rot_y = rot_y + angle
            self.bot.rotation = new_rot_y
            in_angle = True
        else:
            angle_sign = 1 if angle > 0 else -1
            target_rot_y = rot_y + angle
            delta_angle = angle_sign * rotate_speed * delta_time
            new_rot_y = rot_y + delta_angle

            new_angle = target_rot_y - new_rot_y
            if (new_angle * angle <= 0
                    or -stoping_angle < new_angle < stoping_angle):
                new_rot_y = target_rot_y
                in_angle = True

            self.bot.rotation = new_rot_y

        # go pass
        to_next = v3_minus(next_position, position)
        new_to_next = v3_minus(next_position, new_position)

        self.bot.position = new_position

        # resolve collision
        if self.level1 is not None:
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
                    # print '[+] push'
                    push_distance = distance - 1
                    v3_normalize(to_other)
                    new_position = v3_add(
                        position, v3_multiple(to_other, push_distance))
                    this_bot.position = new_position

        if (v3_sqr_magnitude(new_to_next) < sqr_stoping_distance
                or v3_dot(to_next, new_to_next) <= 0):
            return True, in_angle
        else:
            return False, in_angle

    def update(self, delta_time):
        if not self._has_waypoint():
            return

        in_range, in_angle = self.move_toward(
            delta_time, self.next_position, self.sqr_wp_stoping_distance)

        if in_range:
            self.next_position = self.path.get_next_waypoint()
            # if self.next_position is None:
                # self._leave_goto()

                # to_target = v3_minus(new_position, self.target_position)
                # if v3_sqr_magnitude(to_target) < self.sqr_wp_stoping_distance:
                #     self._enter_explose()
                # else:
                #     # TODO:navigation failure
                #     self._enter_explose()


    def is_failed(self):
        if not self._has_waypoint():
            return False
        return self._has_reached()

    def is_satisfied(self):
        # if not self._has_waypoint():
        #     return False
        return self._has_reached()


class DestroyTowerBehavior:
    
    def __init__(self, bot, target, goto_behavior):
        self.bot = bot
        self.state = STATE_IDLE
        self._enter_idle()
        self.target_position = target

        self.goto = goto_behavior
        self.goto.set_destination(self.target_position)

    def _enter_idle(self):
        self.state = STATE_IDLE

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

        self.goto.activate()

        # self.path = self.tile_map.find_path(
        #     self.bot.position, self.target_position)
        # self.next_position = self.path.get_next_waypoint(
        #     position=self.bot.position)
        # # import pdb; pdb.set_trace()

        # if self.next_position is None:
        #     print '_leave_goto:', self.bot.bot_id
        #     self._leave_goto()

    def on_bot_play_animation(self, sock, **response):
        pass

    def on_bot_play_animation_error(self, sock, error, request_id):
        pass

    def get_next_position(self):
        return self.goto.next_position

    def _update_goto(self, delta_time):
        self.goto.update(delta_time)

        if self.goto.is_satisfied():
            self._leave_goto()
            self._enter_explose()

        if self.goto.is_failed():
            # TODO: navigation failure
            self._leave_goto()
            self._enter_explose()

    def _leave_goto(self):
        self.state = STATE_IDLE
    
    def _enter_explose(self):
        self.bot.explose()


    def _update_explose(self):
        pass

    def _leave_explose(self):
        pass

    def update(self, delta_time):
        if self.state == STATE_IDLE:
            self._update_idle()
        elif self.state == STATE_GOTO:
            self._update_goto(delta_time)
        elif self.state == STATE_EXPLOSE:
            pass


class PlayerSensor:
    def __init__(self, player):
        self.target = player


class DefenseBehavior:

    def __init__(self, bot, sensor, radius, goto_behavior):
        self.bot = bot

        self.init_position = bot.position

        self.sensor = sensor
        self.radius = radius
        self.state = STATE_IDLE
        self.goto = goto_behavior

        self.sqr_attack_range = 4
        self.stoping_angle = 0.1

        self.animation_state = 'idle'

    def _is_target_in_radius(self):
        if self.sensor.target is None:
            return False
        target_position = self.sensor.target.position
        return v3_distance(target_position, self.init_position) <= self.radius

    def _enter_idle(self):
        self.state = STATE_IDLE
        self._play_animation('idle')
    
    def _play_animation(self, clip):
        self.animation_state = clip
        _remote(self, 'bot_play_animation',
                bot_id=self.bot.bot_id,
                animation_clip=clip)

    def _update_idle(self, delta_time):
        # no target
        no_target = self.sensor.target is None
        if no_target or (not self._is_target_in_radius()):
            # TODO: movement
            if v3_sqr_distance(self.bot.position, self.init_position) < 0.01:
                if self.animation_state != 'idle':
                    self._play_animation('idle')
            else:
                if self.animation_state != 'run':
                    self._play_animation('run')
                self.goto.move_toward(delta_time, self.init_position, 0.01)
        else:
            self._leave_idle()
            self._enter_goto()

    def _leave_idle(self):
        pass

    def _enter_goto(self):
        print '_enter_goto:', self.bot.bot_id

        self.state = STATE_GOTO
        self._play_animation('run')

        self.goto.speed = 2

    def _update_goto(self, delta_time):
        in_range, in_angle = self.goto.move_toward(
            delta_time, self.sensor.target.position,
            self.sqr_attack_range, self.stoping_angle)
        if in_range and in_angle:
            self._leave_goto()
            if self._can_attack():
                self._enter_attack()
            else:
                self._enter_idle()

    def _leave_goto(self):
        pass

    def _enter_attack(self):
        self.state = STATE_ATTACK
        self.attack_start = time.clock()
        self.attack_interval = 2

        self._play_animation('attack')

    def _can_attack(self):
        if self.sensor.target is None:
            return False

        position = self.bot.position
        target_position = self.sensor.target.position

        in_range = v3_sqr_distance(position, target_position) <=\
            self.sqr_attack_range
        if not in_range:
            return False

        rot_y = self.bot.rotation
        forward = v3_euler_y(rot_y)
        direction = v3_direction(position, target_position)
        angle = v3_angle_cw(forward, direction)
        in_angle = -self.stoping_angle < angle < self.stoping_angle
        if not in_angle:
            return False

        can_see = self.tile_map.see_through(position, target_position)
        return can_see

    def _update_attack(self):
        """
        """
        if time.clock() - self.attack_start <= self.attack_interval:
            return

        target = self.sensor.target
        if target is None:
            self._leave_attack()
            self._enter_idle()
            return

        target_position = target.position
        if not self._is_target_in_radius():
            self._leave_attack()
            self._enter_idle()
            return

        if not self._can_attack():
            self._leave_attack()
            self._enter_goto()
            return

        self._enter_attack()

    def _leave_attack(self):
        pass

    def get_next_position(self):
        return self.goto.next_position

    def update(self, delta_time):
        if self.state == STATE_IDLE:
            self._update_idle(delta_time)
        elif self.state == STATE_GOTO:
            self._update_goto(delta_time)
        elif self.state == STATE_ATTACK:
            self._update_attack()
        elif self.state == STATE_EXPLOSE:
            pass


class Tower:

    def __init__(self, id, hp, position, on_dead=None):
        self.tower_id = 0
        self.max_hp = hp
        self.hp = hp
        self.position = position
        self.on_dead = on_dead
        self.on_damage = None

    def apply_damage(self, damage):
        print '[+] apply_damage, self.hp:', self.hp, '->', self.hp - damage
        self.hp -= damage

        if self.on_damage:
            self.on_damage()

        _remote(self, 'tower_hp_sync',
                tower_id=self.tower_id, hp=self.hp,
                max_hp=self.max_hp)
        if self.hp <= 0:
            self.hp = 0

            if self.on_dead:
                self.on_dead()

    def get_normalized_hp(self):
        return self.hp / float(self.max_hp)

    def on_tower_hp_sync(self, sock, **response_):
        pass

    def on_tower_hp_sync_error(self, sock, error, request_id):
        pass


class Bot:

    def __init__(self, bot_id, target):
        self.bot_id = bot_id
        self.position = message.Vector3(x=0, y=0, z=0)
        self.rotation = 0
        self.explose_target = target  # TODO

        self.behavior = None

        self.dead = False

    def get_is_moving(self):
        return (not self.dead) and self.behavior.state == STATE_GOTO

    def get_is_idle(self):
        return (not self.dead) and self.behavior.state == STATE_IDLE

    def update(self, delta_time):
        if self.dead:
            return

        if self.behavior is not None:
            self.behavior.update(delta_time)

            _remote(self, 'bot_transform_sync',
                    bot_id=self.bot_id, position=self.position,
                    rotation=self.rotation,
                    waypoint_position=self.behavior.get_next_position())

    def on_bot_transform_sync(self, sock, **response_):
        pass

    def on_bot_transform_sync_error(self, sock, error, request_id):
        pass

    def explose(self):
        self.dead = True
        print '[+] explose, bot_id:', self.bot_id
        # TODO:
        assert self.explose_target is not None
        self.explose_target.apply_damage(10)
        _remote(self, 'bot_explose',
                bot_id=self.bot_id)

    def on_bot_explose(self, sock, **response_):
        pass

    def on_bot_explose_error(self, sock, error, request_id):
        pass

class Waypoint:

    def __init__(self, index, position):
        """
        index: tuple (row, column)
        """
        self.index = index
        self.position = position
    

class Path:

    tile_map = None

    def __init__(self):
        self.index = 0
        self.waypoints = []

    # def _get_vector3(self, index):
    #     x, y, z = self.tile_map.get_center(index)
    #     return message.Vector3(x=x, y=y, z=z)

    def get_next_waypoint(self, position=None):
        """get_next_waypoint -> message.Vector3, None is no more waypoint.
        Give position if to smooth the path based on position
        """
        if self.index >= len(self.waypoints):
            return None

        if not isinstance(position, message.Vector3):
            # next_position = self._get_vector3(self.waypoints[self.index].position)
            next_position = self.waypoints[self.index].position
            self.index += 1
            return next_position

        for i in range(self.index, len(self.waypoints)):
            # next_position = self._get_vector3(self.waypoints[i].position)
            next_position = self.waypoints[i].position
            print next_position
            if self.tile_map.see_through(position, next_position):
                self.index = i
            else:
                break

        # next_position = self._get_vector3(self.waypoints[self.index].position)
        next_position = self.waypoints[self.index].position
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

    def __init__(self, map_text=None):
        from os import path
        if path.isfile('..\map'):
            with open('..\map') as f:
                self.raw = json.load(f)

        if path.isfile('map'):
            with open('map') as f:
                self.raw = json.load(f)

        if map_text:
            self.raw = json.loads(map_text)

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
            return p
        else:
            p = Path()
            p.tile_map = self
            for point_index in range(len(path) - 1, -1, -1):
                index = path[point_index][0]
                x, y, z = self.get_center(index)
                p.waypoints.append(Waypoint(
                    index, message.Vector3(x=x, y=y, z=z)))
                # TODO: test
            p.waypoints.append(Waypoint((-1, -1), target_pos))
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
            pass
            # print '[+] not found'
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


class Player:

    def __init__(self):
        self.position = message.Vector3(x=0, y=0, z=0)
        self.rotation = 0
        self.max_hp = 0
        self.hp = 0

    # def apply_damage(self, damage):
    #     _remote(self, 'bot_transform_sync


class KillReporter:

    def __init__(self):
        self.kill_counts = {}
        self.kill_count = 0
        self.timeout = 2
        self.kill_report = message.KillReport()

    def add_kill(self):
        self.last_kill = time.clock()

        self.kill_count += 1

        prev = self.kill_counts.get(self.kill_count, 0)
        prev +=  1
        self.kill_counts[self.kill_count] = prev
        
        self.kill_report.double_kill = self.kill_counts.get(2, 0)
        self.kill_report.triple_kill = self.kill_counts.get(3, 0)
        # print '+' * 10, self.kill_report.triple_kill, self.kill_count
        _remote(self, 'kill_report_sync', kill_report=self.kill_report)

    def get_triple_kill(self):
        return self.kill_counts.get(3, 0)

    def update(self, delta_time):
        if self.kill_count == 0:
            return

        if time.clock() - self.last_kill > self.timeout:
            self.kill_count = 0


class ShootGameLevel1:

    level_id = 1
    sockutil = None
    client_sock = None

    bot_id = 0

    # TODO
    connection = None
    finished = False

    def __init__(self, connection, level):
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
        self.explose_target.on_damage = self._on_tower_damage

        self.player = Player()

        self.kill_reporter = KillReporter()
        self.kill_reporter.sockutil = self.sockutil
        self.kill_reporter.client_sock = self.client_sock

        # TODO
        self.sockutil.register_handler(
            'level0_bot_killed', self.handle_level0_bot_killed, force=True);
        self.sockutil.register_handler(
            'update_actor_hp', self.handle_update_actor_hp, force=True);
        self.sockutil.register_handler(
            'bot_transform_sync', self.handle_bot_transform_sync, force=True);

    def _on_tower_damage(self):
        before_task3 = self.actor_level_info.star3
        after_task3 = self._is_third_task_ok()
        if before_task3 and (not after_task3):
            # import pdb; pdb.set_trace()
            self.actor_level_info.star3 = False
            _remote(self, 'actor_level_info_sync',
                    actor_level_info=self.actor_level_info)

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

        position = message.Vector3(**position)
        position.y = 0  # ???

        # use ammo
        if self.ammo_item:
            item_position = self.ammo_item.position
            item_position = message.Vector3(
                x=item_position.x, y=0, z=item_position.z)
            if v3_distance(item_position, position) < 1:
                print '[+] use_item'
                self.actor.max_ammo += 18
                dbutil.actor_update(self.connection.actordb, self.actor)
                _remote(self, 'use_item', item_type=self.ammo_item.item_type)
                self.ammo_item = None

        # TODO
        self.player.position = position
        self.player.rotation = rotation
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
        before_task1 = self._is_first_task_ok()
        self.kill_reporter.add_kill()
        after_task1 = self._is_first_task_ok()
        self.actor_level_info.star1 = after_task1

        if bot_id == -2:  # player
            _remote(self, 'finish_level', win=False)
            self.finished = True
            return

        self.killed += 1
        if bot_id == self.spider_king.bot_id:
            self.actor_level_info.star2 = True
            _remote(self, 'actor_level_info_sync',
                    actor_level_info=self.actor_level_info)

            self.update_actor_info()

            _remote(self, 'finish_level', win=True)
            self.finished = True
        else:
            if (not before_task1) and after_task1:
                _remote(self, 'actor_level_info_sync',
                        actor_level_info=self.actor_level_info)

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

        self.spawn_interval = 15
        self.time_since_start = time.clock()
        self.next_spawn_time = self.time_since_start + self.spawn_interval

        king_spot = (12, 0, 4, 90)
        self.spider_king = self._spawn_bot(
                'spider_king', x=king_spot[0], y=king_spot[1],
                z=king_spot[2], rot_y=king_spot[3])

        for spot in self.spawn_spot:
            self._spawn_bot('spider_remote', x=spot[0], y=spot[1],
                            z=spot[2], rot_y=spot[3])

        self.ammo_item = Item()
        self.ammo_item.position = message.Vector3(x=25.14, y=1.26, z=14.89)
        _remote(self, 'spawn_item', item_type=self.ammo_item.item_type,
                position=self.ammo_item.position)

        actor_level_info = message.ActorLevelInfo()
        actor_level_info.actor_id = self.actor.actor_id
        actor_level_info.level_id = self.level.level_id
        # actor_level_info.passed = True
        actor_level_info.star1 = False
        actor_level_info.star2 = False
        actor_level_info.star3 = self._is_third_task_ok()

        self.actor_level_info = actor_level_info
        _remote(self, 'actor_level_info_sync',
                actor_level_info=self.actor_level_info)

    def _is_first_task_ok(self):
        return self.kill_reporter.get_triple_kill() >= 1

    def _is_third_task_ok(self):
        return self.explose_target.get_normalized_hp() >= 0.5

    def on_spawn_item(self, sock, **response_):
        print 'on_spawn_item:', response_['request_id']

    def on_spawn_item_error(self, sock, error, request_id):
        print '[-] on_spawn_item_error, error:', error, 'request_id:', request_id

    def update_actor_info(self):
        self.actor.experience += 1000
        self.actor.gold += 100
        self.actor.level += 1
        dbutil.actor_update(self.connection.actordb, self.actor)

        # actor_level_info = message.ActorLevelInfo()
        # actor_level_info.actor_id = self.actor.actor_id
        # actor_level_info.level_id = self.level.level_id
        # actor_level_info.passed = True
        # actor_level_info.star1 = True
        # actor_level_info.star2= True
        # actor_level_info.star3= True
        self.actor_level_info.passed = self.actor_level_info.star2

        actor_level_info = dbutil.actor_level_info_get(
            self.connection.actorleveldb, self.actor_level_info)
        actor_level_info.star1 =\
            actor_level_info.star1 or self.actor_level_info.star1
        actor_level_info.star2 = \
            actor_level_info.star2 or self.actor_level_info.star2
        actor_level_info.star3 = \
            actor_level_info.star3 or self.actor_level_info.star3
        actor_level_info.passed = \
            actor_level_info.passed or self.actor_level_info.passed
            
        dbutil.actor_level_info_update(
            self.connection.actorleveldb, actor_level_info)

    def _spawn_bot(self, bot_type,
                   x=0, y=0, z=0, rot_y=0):
        # create bot
        bot = Bot(self.bot_id, self.explose_target)
        bot.position = message.Vector3(x=x, y=y, z=z)
        bot.rotation = rot_y
        bot.sockutil = self.sockutil
        bot.client_sock = self.client_sock

        goto = GotoBehavior(bot, self.tile_map)
        goto.level1 = self

        # behavior
        if bot_type == 'spider_remote':
            destroy_tower = DestroyTowerBehavior(
                bot, self.explose_target.position, goto)
            destroy_tower.tile_map = self.tile_map
            destroy_tower.level1 = self
            destroy_tower.sockutil = self.sockutil
            destroy_tower.client_sock = self.client_sock

            bot.behavior = destroy_tower

            self.bots.append(bot)
        elif bot_type == 'spider_king':
            sensor = PlayerSensor(self.player)
            defense = DefenseBehavior(bot, sensor, 8, goto)
            defense.sockutil = self.sockutil
            defense.client_sock = self.client_sock
            defense.tile_map = self.tile_map

            bot.behavior = defense
        else:
            raise NotImplementedError('No such bot_type: %s' % bot_type)

        _remote_callback(
            self, 'spawn_bot', bot_id=self.bot_id, bot_type=bot_type,
            position=bot.position, rotation=bot.rotation)

        self.bot_id += 1
        return bot

    def on_spawn_bot(self, sock, **response_):
        print 'on_create_bot:', response_['errno'], response_['request_id']

    def on_spawn_bot_error(self, sock, error, request_id):
        print '[-] on_create_error, error:', error, 'request_id:', request_id

    def update(self, delta_time):
        self.kill_reporter.update(delta_time)

        if self.finished or (not self.entered):
            return
        # import pdb; pdb.set_trace()
        
        if time.clock() > self.next_spawn_time:
            self.next_spawn_time += self.spawn_interval
            if self.spider_king.get_is_idle():
                print '[+] spawn'
                for spot in self.spawn_spot:
                    self._spawn_bot('spider_remote', x=spot[0], y=spot[1],
                                    z=spot[2], rot_y=spot[3])

        for bot in self.bots:
            bot.update(delta_time)

        self.spider_king.update(delta_time)

    def destroy(self):
        pass

    
if __name__ == '__main__':
    import doctest
    doctest.testmod()

