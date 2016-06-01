import server


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


class GetActorInfoRequestResponse:

    def __init__(self, *args):
        self.actor_info = args[0]
        self.errno = args[1]

    def dump(self):
        ret = {}
        ret['actor_info'] = server.dump(self.actor_info)
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


class GetAccountInfoRequest:

    def __init__(self, *args):
        self.username = args[0]

    def dump(self):
        ret = {}
        ret['username'] = server.dump(self.username)
        return ret


class CreateActorRequestResponse:

    def __init__(self, *args):
        self.result = args[0]
        self.errno = args[1]

    def dump(self):
        ret = {}
        ret['result'] = server.dump(self.result)
        ret['errno'] = server.dump(self.errno)
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


class CreateActorRequest:

    def __init__(self, *args):
        self.username = args[0]
        self.actor_type = args[1]

    def dump(self):
        ret = {}
        ret['username'] = server.dump(self.username)
        ret['actor_type'] = server.dump(self.actor_type)
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


class GetActorInfoRequest:

    def __init__(self, *args):
        self.username = args[0]

    def dump(self):
        ret = {}
        ret['username'] = server.dump(self.username)
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

