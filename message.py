import server


class LoginRequest:

    def __init__(self, *args):
        self.username = args[0]
        self.password = args[1]

    def dump(self):
        ret = {}
        ret['username'] = server.dump(self.username)
        ret['password'] = server.dump(self.password)
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


class GetActorInfoRequestResponse:

    def __init__(self, *args):
        self.actor_info = args[0]
        self.errno = args[1]

    def dump(self):
        ret = {}
        ret['actor_info'] = server.dump(self.actor_info)
        ret['errno'] = server.dump(self.errno)
        return ret

