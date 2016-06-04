import server


class CreateActorRequestResponse:

    def __init__(self, *args):
        self.result = args[0]
        self.errno = args[1]

    def dump(self):
        ret = {}
        ret['result'] = server.dump(self.result)
        ret['errno'] = server.dump(self.errno)
        return ret


class EnterLevelRequestResponse:

    def __init__(self, *args):
        self.errno = args[0]

    def dump(self):
        ret = {}
        ret['errno'] = server.dump(self.errno)
        return ret


class Level0BotKilledRequest:

    def __init__(self, *args):
        pass

    def dump(self):
        ret = {}
        return ret


class StartLevelRequestResponse:

    def __init__(self, *args):
        self.errno = args[0]

    def dump(self):
        ret = {}
        ret['errno'] = server.dump(self.errno)
        return ret


class FinishLevelRequestResponse:

    def __init__(self, *args):
        self.errno = args[0]

    def dump(self):
        ret = {}
        ret['errno'] = server.dump(self.errno)
        return ret


class GetLevelInfoRequestResponse:

    def __init__(self, *args):
        self.level_info = args[0]
        self.errno = args[1]

    def dump(self):
        ret = {}
        ret['level_info'] = server.dump(self.level_info)
        ret['errno'] = server.dump(self.errno)
        return ret


class LeaveLevelRequestResponse:

    def __init__(self, *args):
        self.errno = args[0]

    def dump(self):
        ret = {}
        ret['errno'] = server.dump(self.errno)
        return ret


class SpawnBotRequest:

    def __init__(self, *args):
        self.bot_id = args[0]
        self.bot_type = args[1]
        self.position = args[2]
        self.rotation = args[3]

    def dump(self):
        ret = {}
        ret['bot_id'] = server.dump(self.bot_id)
        ret['bot_type'] = server.dump(self.bot_type)
        ret['position'] = server.dump(self.position)
        ret['rotation'] = server.dump(self.rotation)
        return ret


class Vector3:

    def __init__(self, *args):
        self.x = args[0]
        self.y = args[1]
        self.z = args[2]

    def dump(self):
        ret = {}
        ret['x'] = server.dump(self.x)
        ret['y'] = server.dump(self.y)
        ret['z'] = server.dump(self.z)
        return ret


class Actor:

    def __init__(self, *args):
        self.actor_id = args[0]
        self.name = args[1]
        self.level = args[2]
        self.gold = args[3]
        self.experience = args[4]

    def dump(self):
        ret = {}
        ret['actor_id'] = server.dump(self.actor_id)
        ret['name'] = server.dump(self.name)
        ret['level'] = server.dump(self.level)
        ret['gold'] = server.dump(self.gold)
        ret['experience'] = server.dump(self.experience)
        return ret


class GetActorInfoRequestResponse:

    def __init__(self, *args):
        self.actor_info = args[0]
        self.errno = args[1]

    def dump(self):
        ret = {}
        ret['actor_info'] = server.dump(self.actor_info)
        ret['errno'] = server.dump(self.errno)
        return ret


class GetActorLevelInfoRequest:

    def __init__(self, *args):
        self.username = args[0]

    def dump(self):
        ret = {}
        ret['username'] = server.dump(self.username)
        return ret


class LoginRequest:

    def __init__(self, *args):
        self.username = args[0]
        self.password = args[1]

    def dump(self):
        ret = {}
        ret['username'] = server.dump(self.username)
        ret['password'] = server.dump(self.password)
        return ret


class LevelInfo:

    def __init__(self, *args):
        self.level_id = args[0]
        self.title = args[1]
        self.task1 = args[2]
        self.task2 = args[3]
        self.task3 = args[4]
        self.bonuses = args[5]

    def dump(self):
        ret = {}
        ret['level_id'] = server.dump(self.level_id)
        ret['title'] = server.dump(self.title)
        ret['task1'] = server.dump(self.task1)
        ret['task2'] = server.dump(self.task2)
        ret['task3'] = server.dump(self.task3)
        ret['bonuses'] = server.dump(self.bonuses)
        return ret


class GetAccountInfoRequestResponse:

    def __init__(self, *args):
        self.account_info = args[0]
        self.errno = args[1]

    def dump(self):
        ret = {}
        ret['account_info'] = server.dump(self.account_info)
        ret['errno'] = server.dump(self.errno)
        return ret


class GetActorLevelInfoRequestResponse:

    def __init__(self, *args):
        self.actor_level_info = args[0]
        self.errno = args[1]

    def dump(self):
        ret = {}
        ret['actor_level_info'] = server.dump(self.actor_level_info)
        ret['errno'] = server.dump(self.errno)
        return ret


class ActorLevelInfo:

    def __init__(self, *args):
        self.actor_id = args[0]
        self.level_id = args[1]
        self.passed = args[2]
        self.star1 = args[3]
        self.star2 = args[4]
        self.star3 = args[5]

    def dump(self):
        ret = {}
        ret['actor_id'] = server.dump(self.actor_id)
        ret['level_id'] = server.dump(self.level_id)
        ret['passed'] = server.dump(self.passed)
        ret['star1'] = server.dump(self.star1)
        ret['star2'] = server.dump(self.star2)
        ret['star3'] = server.dump(self.star3)
        return ret


class Level0BotKilledRequestResponse:

    def __init__(self, *args):
        self.errno = args[0]

    def dump(self):
        ret = {}
        ret['errno'] = server.dump(self.errno)
        return ret


class Account:

    def __init__(self, *args):
        self.name = args[0]
        self.actor_id = args[1]

    def dump(self):
        ret = {}
        ret['name'] = server.dump(self.name)
        ret['actor_id'] = server.dump(self.actor_id)
        return ret


class EnterLevelRequest:

    def __init__(self, *args):
        pass

    def dump(self):
        ret = {}
        return ret


class FinishLevelRequest:

    def __init__(self, *args):
        self.win = args[0]
        self.bonuses = args[1]

    def dump(self):
        ret = {}
        ret['win'] = server.dump(self.win)
        ret['bonuses'] = server.dump(self.bonuses)
        return ret


class GetAccountInfoRequest:

    def __init__(self, *args):
        self.username = args[0]

    def dump(self):
        ret = {}
        ret['username'] = server.dump(self.username)
        return ret


class GetLevelInfoRequest:

    def __init__(self, *args):
        self.username = args[0]

    def dump(self):
        ret = {}
        ret['username'] = server.dump(self.username)
        return ret


class CreateActorRequest:

    def __init__(self, *args):
        self.username = args[0]
        self.actor_type = args[1]

    def dump(self):
        ret = {}
        ret['username'] = server.dump(self.username)
        ret['actor_type'] = server.dump(self.actor_type)
        return ret


class SpawnBotRequestResponse:

    def __init__(self, *args):
        self.errno = args[0]

    def dump(self):
        ret = {}
        ret['errno'] = server.dump(self.errno)
        return ret


class LeaveLevelRequest:

    def __init__(self, *args):
        pass

    def dump(self):
        ret = {}
        return ret


class GetActorInfoRequest:

    def __init__(self, *args):
        self.username = args[0]

    def dump(self):
        ret = {}
        ret['username'] = server.dump(self.username)
        return ret


class StartLevelRequest:

    def __init__(self, *args):
        self.actor_id = args[0]
        self.level_id = args[1]

    def dump(self):
        ret = {}
        ret['actor_id'] = server.dump(self.actor_id)
        ret['level_id'] = server.dump(self.level_id)
        return ret


class LoginRequestResponse:

    def __init__(self, *args):
        self.result = args[0]
        self.errno = args[1]

    def dump(self):
        ret = {}
        ret['result'] = server.dump(self.result)
        ret['errno'] = server.dump(self.errno)
        return ret

