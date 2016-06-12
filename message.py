import sockutil


class StartLevelRequestResponse:

    def __init__(self, **kwargs):
        """
        Params:

        errno: int

        """
        self.errno = kwargs.get('errno')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.errno = kwargs['errno']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['errno'] = sockutil.dump(self.errno)
        return ret


class UseItemRequest:

    def __init__(self, **kwargs):
        """
        Params:

        item_type: str

        """
        self.item_type = kwargs.get('item_type')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.item_type = kwargs['item_type']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['item_type'] = sockutil.dump(self.item_type)
        return ret


class BotExploseRequestResponse:

    def __init__(self):
        pass

    def load(self):
        pass

    def dump(self):
        return {}


class GetLevelInfoRequestResponse:

    def __init__(self, **kwargs):
        """
        Params:

        level_info: LevelInfo[]
        errno: int

        """
        self.level_info = kwargs.get('level_info')
        self.errno = kwargs.get('errno')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.level_info = kwargs['level_info']
        self.errno = kwargs['errno']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['level_info'] = sockutil.dump(self.level_info)
        ret['errno'] = sockutil.dump(self.errno)
        return ret


class CreateActorRequestResponse:

    def __init__(self, **kwargs):
        """
        Params:

        result: bool
        errno: int

        """
        self.result = kwargs.get('result')
        self.errno = kwargs.get('errno')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.result = kwargs['result']
        self.errno = kwargs['errno']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['result'] = sockutil.dump(self.result)
        ret['errno'] = sockutil.dump(self.errno)
        return ret


class GetActorLevelInfoRequest:

    def __init__(self, **kwargs):
        """
        Params:

        username: str

        """
        self.username = kwargs.get('username')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.username = kwargs['username']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['username'] = sockutil.dump(self.username)
        return ret


class UseItemRequestResponse:

    def __init__(self):
        pass

    def load(self):
        pass

    def dump(self):
        return {}


class GetAccountInfoRequestResponse:

    def __init__(self, **kwargs):
        """
        Params:

        account_info: Account
        errno: int

        """
        self.account_info = kwargs.get('account_info')
        self.errno = kwargs.get('errno')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.account_info = kwargs['account_info']
        self.errno = kwargs['errno']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['account_info'] = sockutil.dump(self.account_info)
        ret['errno'] = sockutil.dump(self.errno)
        return ret


class GetActorLevelInfoRequestResponse:

    def __init__(self, **kwargs):
        """
        Params:

        actor_level_info: ActorLevelInfo[]
        errno: int

        """
        self.actor_level_info = kwargs.get('actor_level_info')
        self.errno = kwargs.get('errno')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.actor_level_info = kwargs['actor_level_info']
        self.errno = kwargs['errno']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['actor_level_info'] = sockutil.dump(self.actor_level_info)
        ret['errno'] = sockutil.dump(self.errno)
        return ret


class BotPlayAnimationRequest:

    def __init__(self, **kwargs):
        """
        Params:

        bot_id: int
        animation_clip: str

        """
        self.bot_id = kwargs.get('bot_id')
        self.animation_clip = kwargs.get('animation_clip')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.bot_id = kwargs['bot_id']
        self.animation_clip = kwargs['animation_clip']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['bot_id'] = sockutil.dump(self.bot_id)
        ret['animation_clip'] = sockutil.dump(self.animation_clip)
        return ret


class ActorLevelInfo:

    def __init__(self, **kwargs):
        """
        Params:

        actor_id: int
        level_id: int
        passed: bool
        star1: bool
        star2: bool
        star3: bool

        """
        self.actor_id = kwargs.get('actor_id')
        self.level_id = kwargs.get('level_id')
        self.passed = kwargs.get('passed')
        self.star1 = kwargs.get('star1')
        self.star2 = kwargs.get('star2')
        self.star3 = kwargs.get('star3')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.actor_id = kwargs['actor_id']
        self.level_id = kwargs['level_id']
        self.passed = kwargs['passed']
        self.star1 = kwargs['star1']
        self.star2 = kwargs['star2']
        self.star3 = kwargs['star3']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['actor_id'] = sockutil.dump(self.actor_id)
        ret['level_id'] = sockutil.dump(self.level_id)
        ret['passed'] = sockutil.dump(self.passed)
        ret['star1'] = sockutil.dump(self.star1)
        ret['star2'] = sockutil.dump(self.star2)
        ret['star3'] = sockutil.dump(self.star3)
        return ret


class UpdateActorHpRequestResponse:

    def __init__(self, **kwargs):
        """
        Params:

        errno: int

        """
        self.errno = kwargs.get('errno')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.errno = kwargs['errno']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['errno'] = sockutil.dump(self.errno)
        return ret


class Account:

    def __init__(self, **kwargs):
        """
        Params:

        name: str
        actor_id: int

        """
        self.name = kwargs.get('name')
        self.actor_id = kwargs.get('actor_id')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.name = kwargs['name']
        self.actor_id = kwargs['actor_id']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['name'] = sockutil.dump(self.name)
        ret['actor_id'] = sockutil.dump(self.actor_id)
        return ret


class GetAccountInfoRequest:

    def __init__(self, **kwargs):
        """
        Params:

        username: str

        """
        self.username = kwargs.get('username')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.username = kwargs['username']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['username'] = sockutil.dump(self.username)
        return ret


class BotPlayAnimationRequestResponse:

    def __init__(self):
        pass

    def load(self):
        pass

    def dump(self):
        return {}


class GetLevelInfoRequest:

    def __init__(self, **kwargs):
        """
        Params:

        username: str

        """
        self.username = kwargs.get('username')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.username = kwargs['username']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['username'] = sockutil.dump(self.username)
        return ret


class CreateActorRequest:

    def __init__(self, **kwargs):
        """
        Params:

        username: str
        actor_type: str

        """
        self.username = kwargs.get('username')
        self.actor_type = kwargs.get('actor_type')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.username = kwargs['username']
        self.actor_type = kwargs['actor_type']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['username'] = sockutil.dump(self.username)
        ret['actor_type'] = sockutil.dump(self.actor_type)
        return ret


class BotTransformSyncRequestResponse:

    def __init__(self):
        pass

    def load(self):
        pass

    def dump(self):
        return {}


class StartLevelRequest:

    def __init__(self, **kwargs):
        """
        Params:

        actor_id: int
        level_id: int

        """
        self.actor_id = kwargs.get('actor_id')
        self.level_id = kwargs.get('level_id')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.actor_id = kwargs['actor_id']
        self.level_id = kwargs['level_id']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['actor_id'] = sockutil.dump(self.actor_id)
        ret['level_id'] = sockutil.dump(self.level_id)
        return ret


class LeaveLevelRequest:

    def __init__(self):
        pass

    def load(self):
        pass

    def dump(self):
        return {}


class TowerHpSyncRequestResponse:

    def __init__(self):
        pass

    def load(self):
        pass

    def dump(self):
        return {}


class EnterLevelRequestResponse:

    def __init__(self, **kwargs):
        """
        Params:

        errno: int

        """
        self.errno = kwargs.get('errno')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.errno = kwargs['errno']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['errno'] = sockutil.dump(self.errno)
        return ret


class SpawnItemRequest:

    def __init__(self, **kwargs):
        """
        Params:

        item_type: str
        position: Vector3

        """
        self.item_type = kwargs.get('item_type')
        self.position = kwargs.get('position')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.item_type = kwargs['item_type']
        self.position = kwargs['position']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['item_type'] = sockutil.dump(self.item_type)
        ret['position'] = sockutil.dump(self.position)
        return ret


class Level0BotKilledRequest:

    def __init__(self, **kwargs):
        """
        Params:

        bot_id: int

        """
        self.bot_id = kwargs.get('bot_id')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.bot_id = kwargs['bot_id']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['bot_id'] = sockutil.dump(self.bot_id)
        return ret


class FinishLevelRequestResponse:

    def __init__(self, **kwargs):
        """
        Params:

        errno: int

        """
        self.errno = kwargs.get('errno')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.errno = kwargs['errno']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['errno'] = sockutil.dump(self.errno)
        return ret


class UpdateActorHpRequest:

    def __init__(self, **kwargs):
        """
        Params:

        actor_id: int
        hp: int
        max_ammo: int
        ammo: int

        """
        self.actor_id = kwargs.get('actor_id')
        self.hp = kwargs.get('hp')
        self.max_ammo = kwargs.get('max_ammo')
        self.ammo = kwargs.get('ammo')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.actor_id = kwargs['actor_id']
        self.hp = kwargs['hp']
        self.max_ammo = kwargs['max_ammo']
        self.ammo = kwargs['ammo']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['actor_id'] = sockutil.dump(self.actor_id)
        ret['hp'] = sockutil.dump(self.hp)
        ret['max_ammo'] = sockutil.dump(self.max_ammo)
        ret['ammo'] = sockutil.dump(self.ammo)
        return ret


class LeaveLevelRequestResponse:

    def __init__(self, **kwargs):
        """
        Params:

        errno: int

        """
        self.errno = kwargs.get('errno')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.errno = kwargs['errno']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['errno'] = sockutil.dump(self.errno)
        return ret


class BotTransformSyncRequest:

    def __init__(self, **kwargs):
        """
        Params:

        bot_id: int
        position: Vector3
        rotation: float
        waypoint_position: Vector3

        """
        self.bot_id = kwargs.get('bot_id')
        self.position = kwargs.get('position')
        self.rotation = kwargs.get('rotation')
        self.waypoint_position = kwargs.get('waypoint_position')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.bot_id = kwargs['bot_id']
        self.position = kwargs['position']
        self.rotation = kwargs['rotation']
        self.waypoint_position = kwargs['waypoint_position']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['bot_id'] = sockutil.dump(self.bot_id)
        ret['position'] = sockutil.dump(self.position)
        ret['rotation'] = sockutil.dump(self.rotation)
        ret['waypoint_position'] = sockutil.dump(self.waypoint_position)
        return ret


class Vector3:

    def __init__(self, **kwargs):
        """
        Params:

        x: float
        y: float
        z: float

        """
        self.x = kwargs.get('x')
        self.y = kwargs.get('y')
        self.z = kwargs.get('z')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.x = kwargs['x']
        self.y = kwargs['y']
        self.z = kwargs['z']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['x'] = sockutil.dump(self.x)
        ret['y'] = sockutil.dump(self.y)
        ret['z'] = sockutil.dump(self.z)
        return ret


class Actor:

    def __init__(self, **kwargs):
        """
        Params:

        actor_id: int
        name: str
        level: int
        gold: int
        experience: int
        max_hp: int
        hp: int
        max_ammo: int
        ammo: int

        """
        self.actor_id = kwargs.get('actor_id')
        self.name = kwargs.get('name')
        self.level = kwargs.get('level')
        self.gold = kwargs.get('gold')
        self.experience = kwargs.get('experience')
        self.max_hp = kwargs.get('max_hp')
        self.hp = kwargs.get('hp')
        self.max_ammo = kwargs.get('max_ammo')
        self.ammo = kwargs.get('ammo')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.actor_id = kwargs['actor_id']
        self.name = kwargs['name']
        self.level = kwargs['level']
        self.gold = kwargs['gold']
        self.experience = kwargs['experience']
        self.max_hp = kwargs['max_hp']
        self.hp = kwargs['hp']
        self.max_ammo = kwargs['max_ammo']
        self.ammo = kwargs['ammo']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['actor_id'] = sockutil.dump(self.actor_id)
        ret['name'] = sockutil.dump(self.name)
        ret['level'] = sockutil.dump(self.level)
        ret['gold'] = sockutil.dump(self.gold)
        ret['experience'] = sockutil.dump(self.experience)
        ret['max_hp'] = sockutil.dump(self.max_hp)
        ret['hp'] = sockutil.dump(self.hp)
        ret['max_ammo'] = sockutil.dump(self.max_ammo)
        ret['ammo'] = sockutil.dump(self.ammo)
        return ret


class GetActorInfoRequestResponse:

    def __init__(self, **kwargs):
        """
        Params:

        actor_info: Actor
        errno: int

        """
        self.actor_info = kwargs.get('actor_info')
        self.errno = kwargs.get('errno')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.actor_info = kwargs['actor_info']
        self.errno = kwargs['errno']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['actor_info'] = sockutil.dump(self.actor_info)
        ret['errno'] = sockutil.dump(self.errno)
        return ret


class LoginRequest:

    def __init__(self, **kwargs):
        """
        Params:

        username: str
        password: str

        """
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.username = kwargs['username']
        self.password = kwargs['password']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['username'] = sockutil.dump(self.username)
        ret['password'] = sockutil.dump(self.password)
        return ret


class LevelInfo:

    def __init__(self, **kwargs):
        """
        Params:

        level_id: int
        title: str
        task1: str
        task2: str
        task3: str
        bonuses: str[]

        """
        self.level_id = kwargs.get('level_id')
        self.title = kwargs.get('title')
        self.task1 = kwargs.get('task1')
        self.task2 = kwargs.get('task2')
        self.task3 = kwargs.get('task3')
        self.bonuses = kwargs.get('bonuses')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.level_id = kwargs['level_id']
        self.title = kwargs['title']
        self.task1 = kwargs['task1']
        self.task2 = kwargs['task2']
        self.task3 = kwargs['task3']
        self.bonuses = kwargs['bonuses']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['level_id'] = sockutil.dump(self.level_id)
        ret['title'] = sockutil.dump(self.title)
        ret['task1'] = sockutil.dump(self.task1)
        ret['task2'] = sockutil.dump(self.task2)
        ret['task3'] = sockutil.dump(self.task3)
        ret['bonuses'] = sockutil.dump(self.bonuses)
        return ret


class BotExploseRequest:

    def __init__(self, **kwargs):
        """
        Params:

        bot_id: int

        """
        self.bot_id = kwargs.get('bot_id')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.bot_id = kwargs['bot_id']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['bot_id'] = sockutil.dump(self.bot_id)
        return ret


class SpawnItemRequestResponse:

    def __init__(self):
        pass

    def load(self):
        pass

    def dump(self):
        return {}


class Level0BotKilledRequestResponse:

    def __init__(self, **kwargs):
        """
        Params:

        errno: int

        """
        self.errno = kwargs.get('errno')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.errno = kwargs['errno']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['errno'] = sockutil.dump(self.errno)
        return ret


class EnterLevelRequest:

    def __init__(self):
        pass

    def load(self):
        pass

    def dump(self):
        return {}


class TowerHpSyncRequest:

    def __init__(self, **kwargs):
        """
        Params:

        tower_id: int
        hp: int

        """
        self.tower_id = kwargs.get('tower_id')
        self.hp = kwargs.get('hp')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.tower_id = kwargs['tower_id']
        self.hp = kwargs['hp']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['tower_id'] = sockutil.dump(self.tower_id)
        ret['hp'] = sockutil.dump(self.hp)
        return ret


class FinishLevelRequest:

    def __init__(self, **kwargs):
        """
        Params:

        win: bool
        bonuses: str[]

        """
        self.win = kwargs.get('win')
        self.bonuses = kwargs.get('bonuses')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.win = kwargs['win']
        self.bonuses = kwargs['bonuses']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['win'] = sockutil.dump(self.win)
        ret['bonuses'] = sockutil.dump(self.bonuses)
        return ret


class SpawnBotRequest:

    def __init__(self, **kwargs):
        """
        Params:

        bot_id: int
        bot_type: str
        position: Vector3
        rotation: float

        """
        self.bot_id = kwargs.get('bot_id')
        self.bot_type = kwargs.get('bot_type')
        self.position = kwargs.get('position')
        self.rotation = kwargs.get('rotation')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.bot_id = kwargs['bot_id']
        self.bot_type = kwargs['bot_type']
        self.position = kwargs['position']
        self.rotation = kwargs['rotation']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['bot_id'] = sockutil.dump(self.bot_id)
        ret['bot_type'] = sockutil.dump(self.bot_type)
        ret['position'] = sockutil.dump(self.position)
        ret['rotation'] = sockutil.dump(self.rotation)
        return ret


class SpawnBotRequestResponse:

    def __init__(self, **kwargs):
        """
        Params:

        errno: int

        """
        self.errno = kwargs.get('errno')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.errno = kwargs['errno']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['errno'] = sockutil.dump(self.errno)
        return ret


class LoginRequestResponse:

    def __init__(self, **kwargs):
        """
        Params:

        result: bool
        errno: int

        """
        self.result = kwargs.get('result')
        self.errno = kwargs.get('errno')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.result = kwargs['result']
        self.errno = kwargs['errno']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['result'] = sockutil.dump(self.result)
        ret['errno'] = sockutil.dump(self.errno)
        return ret


class GetActorInfoRequest:

    def __init__(self, **kwargs):
        """
        Params:

        username: str

        """
        self.username = kwargs.get('username')

    def load(self, **kwargs):
        """load from dict
        Exception:

        KeyError

        """
        self.username = kwargs['username']

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['username'] = sockutil.dump(self.username)
        return ret

