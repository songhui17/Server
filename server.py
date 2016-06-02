#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import select
import argparse
from socket import *

import message
from sockutil import *


E_OK = 0                    # success
E_NO_USERNAME = 1           # no account with name username
E_INVALID_PASSWORD = 2      # invalid password
E_USER_NOT_LOGINED = 3      # user has not logined, login required
E_ACTOR_EXIST = 4           # actor already bound to account
E_ACTOR_NOT_CREATED = 5     # actor_id == -1, no actor bound to account


class NotLoginedError(Exception):
    def __init__(self):
        pass

def validate_username(username_):
    """
    valid username_: [a-zA-Z](1,10)

    >>> validate_username('a')
    >>> validate_username('abc')
    >>> validate_username('aaaaaaaaaa')

    >>> validate_username(None)
    Traceback (most recent call last):
        ...
    Exception: username_ is None
    >>> validate_username('')
    Traceback (most recent call last):
        ...
    Exception: username_(len=0) is too short or long
    >>> validate_username('aaaaaaaaaaa')
    Traceback (most recent call last):
        ...
    Exception: username_(len=11) is too short or long

    """
    return True

    if username_ is None:
        raise Exception('username_ is None')

    if not (0 < len(username_) < 11):
        raise Exception('username_(len=%d) is too'
                        ' short or long' % len(username_))

    for i_ in username_:
        if i_ not in 'abc':
            raise Exception('Invalid username_:' + username_)


def validate_password(password_):
    """
    valid password_: [a-zA-Z](1,10)

    >>> validate_password('a')
    >>> validate_password('abc')
    >>> validate_password('aaaaaaaaaa')

    >>> validate_password(None)
    Traceback (most recent call last):
        ...
    Exception: password_ is None
    >>> validate_password('')
    Traceback (most recent call last):
        ...
    Exception: password_(len=0) is too short or long
    >>> validate_password('aaaaaaaaaaa')
    Traceback (most recent call last):
        ...
    Exception: password_(len=11) is too short or long

    """
    if password_ is None:
        raise Exception('password_ is None')
    if not (0 < len(password_) < 11):
        raise Exception('password_(len=%d) is'
                        ' too short or long' % len(password_))
    for i_ in password_:
        if i_ not in 'abc':
            raise Exception('Invalid password_: ' + password_)


def create_account(userdb_, username_, password_):
    """create_account(...) -> True|False, raise Exception on invalid username or
    password. Once created, insert into userdb
    {name, password, level, gold, experience}

    >>> userdb = {}
    >>> create_account(userdb, 'abc', 'abc')
    >>> account = userdb['abc']
    >>> print account
    {'name': 'abc', 'password': 'abc', 'actor_id': -1}
    """
    validate_username(username_)
    validate_password(password_)
    print '[+] username_:', username_
    print '[+] password_:', password_
    userdb_.get(username_)
    if userdb_.get(username_):
        print '[-] username_: %s exits' % username_
        return False
    else:
        print '[+] add username_: %s' % username_
        userdb_[username_] = password_
        new_user = {
            'name': username_,
            'password': password_,
            'actor_id': -1
        }
        userdb_[username_] = new_user
        return True


def db_login(userdb_, username_, password_):
    """db_login(...) -> T|F, E_NO

    Errno:

    E_OK
    E_NO_USERNAME
    E_INVALID_PASSWORD

    """
    validate_username(username_)
    validate_password(password_)
    print '[+] username_:', username_
    print '[+] password_:', password_

    user = userdb_.get(username_, None)
    if not user:
        print '[-] no username_: %s' % username_
        return False, E_NO_USERNAME
    if user.get('password', None) != password_:
        print '[-] invalid password_: %s' % password_
        return False, E_INVALID_PASSWORD
    return True, E_OK


class Account:
    """Account

    Fields:
        logined     :bool

        userdb      :dict

    Serialized:
        name        :string(primary)
        password    :string(not used)

        actor_created   :actor_id == -1
        actor_id        :int
    """
    logined = False
    name = ''

    actor_id = -1

    def __init__(self):
        pass

    def __eq__(self):
        pass

    def __str__(self):
        """dump -> string
        """
        info = ''
        info += 'logined: {0}\n'.format(self.logined)
        info += 'name: {0}\n'.format(self.name)
        return info

    def load(self, data):
        """load(data) init from data
        Exception:

        KeyError
        """
        name = data['name']
        password = data['password']
        actor_id = data['actor_id']

        self.name = name
        self.password = password
        self.actor_id = actor_id

    def dump(self, ignore_password=True):
        """dump -> dict
        """
        ret = {}
        ret['name'] = self.name
        if not ignore_password:
            ret['password'] = self.password
        ret['actor_id'] = self.actor_id
        return ret

    def login(self, password_):
        """login() -> T|F
        """
        if self.logined:
            print '[+] account has logined'
            return True

        ret, error = db_login(self.userdb, self.name, password_)
        self.logined = ret
        if ret:
            print '[+] account:%s logined' % self.name
        else:
            print '[-] account:%s failed to login' % self.name
        return ret

    def _validate_login(self):
        """_validate_login -> raise Exception if self.logined == False
        """
        if not self.logined:
            raise Exception('User is not logined')


class LevelInfo:
    """LevelInfo
    Fields:

    level_id    :int
    title       :string
    task1       :string
    task2       :string
    task3       :string

    bonuses     :list<string>
    """

    def __init__(self):
        pass


class ActorLevelInfo:
    """ActorLevelInfo: Per Actor level stat
    Fields:

    actor_id    :int

    level_id    :int
    passed      :bool
    star1      :bool
    star2      :bool
    star3      :bool
    """

    def __init__(self):
        pass

    def __init__(self, data):
        self.load(data)

    def _copy(self, copy):
        self.actor_id = copy.actor_id
        self.level_id = copy.level_id
        self.passed = copy.passed
        self.star1 = copy.star1
        self.star2 = copy.star2
        self.star3 = copy.star3

    def load(self, data):
        """load :from data

        Exception:

        KeyError
        """
        try:
            import pdb; pdb.set_trace()
            tmp = ActorLevelInfo()
            tmp.actor_id = data.get('actor_id')
            tmp.level_id = data.get('level_id')
            tmp.passed = data.get('passed')
            tmp.star1 = data.get('star1')
            tmp.star2 = data.get('star2')
            tmp.star3 = data.get('star3')

            self._copy(tmp)
        except KeyError, ex:
            print '[-]', ex
            raise ex

    def dump(self):
        """dump -> dict{actor_id, level_id, passed, star1, star2, star3}
        """
        ret = {}
        ret['actor_id'] = self.actor_id
        ret['level_id'] = self.level_id
        ret['passed'] = self.passed
        ret['star1'] = self.star1
        ret['star2'] = self.star2
        ret['star3'] = self.star3
        return ret


class Actor:
    """Actor:
    Fields

    account     :Account (back ref)

    actor_id    :int
    name        :int
    level       :int
    gold        :int
    experience  :int

    """

    def __init__(self):
        pass

    def __str__(self):
        info = ''
        info += 'actor_id: {0}\n'.format(self.actor_id)
        info += 'name: {0}\n'.format(self.name)
        info += 'level: {0}\n'.format(self.level)
        info += 'gold: {0}\n'.format(self.gold)
        info += 'experience: {0}\n'.format(self.experience)
        return info

    def _copy(self, copy):
        self.actor_id = copy.actor_id
        self.name = copy.name
        self.level = copy.level
        self.gold = copy.gold
        self.experience = copy.experience

    def load(self, data):
        try:
            tmp = Actor()
            tmp.actor_id = data.get('actor_id')
            tmp.name = data.get('name')
            tmp.level = data.get('level')
            tmp.gold = data.get('gold')
            tmp.experience = data.get('experience')

            self._copy(tmp)
        except KeyError, ex:
            print '[-] Failed to load: ', ex
            raise ex

    def dump(self):
        ret = {}
        ret['actor_id'] = self.actor_id
        ret['name'] = self.name
        ret['level'] = self.level
        ret['gold'] = self.gold
        ret['experience'] = self.experience
        return ret


class Server:
    def __init__(self):
        pass

    def handle_login(self, username, password):
        """login -> T|F, errno, create actor instance in
        actormap_ if there is actor bound to this account

        Errno:

        E_OK
        E_NO_USERNAME
        E_INVALID_PASSWORD

        Exception:

            Invalid username
            Invalid password

        """
        accountdb_ = self.accountdb
        accountmap_ = self.accountmap
        actordb_ = self.actordb
        actormap_ = self.actormap

        validate_username(username)
        validate_password(password)

        account_data = accountdb_.get(username, None)
        if not account_data:
            print '[-] no username: %s' % username
            return message.LoginRequestResponse(False, E_NO_USERNAME)

        account = accountmap_.get(username, None)
        if not account:
            print '[+] Create account for ', username
            # import pdb; pdb.set_trace()
            account = Account()
            account.load(account_data)
            account.userdb = accountdb_

            accountmap_[username] = account

        if not account.login(password):
            print '[-] invalid password'
            return message.LoginRequestResponse(False, E_INVALID_PASSWORD)

        print 'account logined:'
        print account.dump(ignore_password=True)

        if account.actor_id != -1:
            # TODO: create actor instance
            actor_data = actordb_.get(account.actor_id, None)
            if not actor_data:
                info = 'Fatal error: actor_id: {0} doesnt exist in'\
                    ' database'.format(account.actor_id)
                raise Exception(info)
            actor = Actor()
            actor.load(actor_data)
            actormap_[actor.actor_id] = actor
        return message.LoginRequestResponse(True, E_OK)

    def handle_logout(self, username):
        pass

    def handle_get_actor_info(self, username):
        """handle_get_actor_info -> dict { name, level, gold, experience }
        | E_NO or None on error

        Errno:

        E_OK
        E_USER_NOT_LOGINED

        Exception:

        InvalidUsername
        ActorNotExistInDB

        """
        print '[+] handle_get_actor_info'
        accountdb = self.accountdb
        accountmap = self.accountmap
        actordb = self.actordb
        actormap = self.actormap

        try:
            validate_username(username)
            account = accountmap.get(username, None)
            if not account:
                print '[-] user: {0} is not logined'.format(username)
                return message.GetActorInfoRequestResponse(
                    None, E_USER_NOT_LOGINED)

            actor_id = account.actor_id
            if actor_id == -1:
                print '[-] no actor for this account', account.name
                return message.GetActorInfoRequestResponse(
                    None, E_ACTOR_NOT_CREATED)

            actor = actormap.get(actor_id, None)
            if not actor:
                print '[+] Create Actor instance'
                actor_data = actordb.get(actor_id, None)
                if not actor_data:
                    # TODO: should assert actor_data not None?
                    info = 'Fatal error: actor_id: {0} doesnt exist in'\
                        ' database'.format(account.actor_id)
                    raise Exception(info)
                actor = Actor()
                actor.load(actor_data)
                actormap[actor_id, actor]
            return message.GetActorInfoRequestResponse(actor, E_OK)
        except Exception, ex:
            print '[-]', ex
            raise ex

    def handle_get_actor_info2(self, actor_id):
        """handle_get_actor_info2 -> actor.dump()

        Exception:

        KeyError    :Not actor instance created
        """
        try:
            actor = self.actormap[actor_id]
            assert actor.account is not None, 'account must be assgined'
            if not actor.account.logined:
                raise NotLoginedError()
            return message.GetActorInfoRequestResponse(actor.dump(), E_OK)
        except KeyError, ex:
            # (1) actor created?
            # (2) actordb in db?
            raise NotImplemented('handle actor instance not created')

    def handle_get_account_info(self, username):
        """handle_get_account_info -> account.dump(), E_NO

        Errno:
        
        E_OK
        E_USER_NOT_LOGINED

        Exception:

        # TODO: NotLoginedError
        InvalidUsername

        """
        accountmap = self.accountmap

        print '[+] handle_get_account_info'
        validate_username(username)
        account = accountmap.get(username, None)
        if not account:
            print '[-] user: {0} is not logined'.format(username)
            # raise NotLoginedError()
            return message.GetAccountInfoRequestResponse(None, E_USER_NOT_LOGINED)

        return message.GetAccountInfoRequestResponse(account.dump(), E_OK)

    def handle_create_actor(self, username, actor_type):
        """handle_create_actor -> T|F, E_NO
        :insert into actordb, create instance into actormap

        Errno:

        E_OK
        E_USER_NOT_LOGINED
        E_ACTOR_EXIST

        Exception:

        InvalidUsername
        ActorIDConflict

        """
        print '[+] handle_create_actor'
        accountmap = self.accountmap
        actordb = self.actordb
        actormap = self.actormap

        validate_username(username)
        account = accountmap.get(username, None)
        if not account:
            print '[-] user: {0} is not logined'.format(username)
            return message.CreateActorRequestResponse(False, E_USER_NOT_LOGINED)

        if account.actor_id != -1:
            return message.CreateActorRequestResponse(False, E_ACTOR_EXIST)

        actor = Actor()
        actor.actor_id = 0
        actor.name = actor_type
        actor.level = 1
        actor.gold = 100
        actor.experience = 0

        if actor.actor_id in actordb:
            info = 'actor_id: {0} conflict for {1}'.format(
                actor.actor_id, actor_type)
            print '[-]', info
            raise Exception(info)

        actordb[actor.actor_id] = actor.dump()
        actormap[actor.actor_id] = actor
        account.actor_id = actor.actor_id
        actor.account = account
        print actor
        return message.CreateActorRequestResponse(True, E_OK)

    def handle_get_actor_level_info(self, username):
        """handle_get_actor_level_info -> dict{} or None on error, errno

        Error Number:

        E_OK
        E_USER_NOT_LOGINED

        Exception:

        InvalidUsername

        """
        print '[+] handle_get_actor_level_info'
        print '[X] TODO: copy from get_actor_info'
        accountmap = self.accountmap
        actormap = self.actormap
        actorleveldb = self.actorleveldb

        validate_username(username)
        account = accountmap.get(username, None)
        if not account:
            print '[-] user: {0} is not logined'.format(username)
            return message.GetActorLevelInfoRequestResponse(None, E_USER_NOT_LOGINED)

        actor_id = account.actor_id
        if actor_id == -1:
            print '[-] no actor for this account', account.name
            return message.GetActorLevelInfoRequestResponse(None, E_ACTOR_NOT_CREATED)

        actor = actormap.get(actor_id, None)
        if not actor:
            print '[+] Create Actor instance'
            actor_data = actordb.get(actor_id, None)
            if not actor_data:
                # TODO: should assert actor_data not None?
                info = 'Fatal error: actor_id: {0} doesnt exist in'\
                    ' database'.format(account.actor_id)
                raise Exception(info)
            actor = Actor()
            actor.load(actor_data)
            actormap[actor_id, actor]

        level_data = [v for k, v in actorleveldb.iteritems() if k[0] == actor_id]
        print level_data
        # TODO: handle empty
        return message.GetActorLevelInfoRequestResponse(level_data, E_OK)
                # {i: j for i, j in enumerate(level_data)}, E_OK)

    def handle_get_level_info(self, username):
        """handle_get_level_info -> level_info, errno

        Errno:

        E_OK
        E_USER_NOT_LOGINED

        Exception:

        InvalidUsername
        """
        validate_username(username)
        account = self.accountmap.get(username, None)
        if not account:
            print '[-] user: {0} is not logined'.format(username)
            return message.GetLevelInfoRequestResponse(None, E_USER_NOT_LOGINED)

        level_info = [
            message.LevelInfo(
                v['level_id'],
                v['title'],
                v['task1'],
                v['task2'],
                v['task3'],
                v['bonuses']) for v in self.leveldb.itervalues()]
        return message.GetLevelInfoRequestResponse(level_info, E_OK)

    def handle_start_level(self, actor_id, level_id):
        """handle_start_level -> E_NO

        ErrorNo:

        E_OK
        E_USER_NOT_LOGINED

        """
        actor = self.actormap.get(actor_id, None)
        if actor is None:
            return E_USER_NOT_LOGINED

        if self.shoot_game is not None:
            raise NotImplemented('ShootGame is running')

        import game
        self.shoot_game = game.ShootGame(self.sockutil, self.client_sock)
        self.shoot_game.start(level_id=level_id)
    
    def handle_leave_level(self):
        if self.shoot_game:
            self.shoot_game.destroy()
            self.shoot_game = None
        return message.LeaveLevelRequestResponse(E_OK)

    # TODO:
    # def handle_finish_level(self):
    #     pass

    def load_leveldb(self, leveldb):
        """load_leveldb: init level database
        """
        leveldb[0] = {
            'level_id': 0,
            'title': u'磨刀霍霍',
            'task1': u'击败1个蜘蛛',
            'task2': u'击败2个蜘蛛',
            'task3': u'击败3个蜘蛛',
            'bonuses': [u'1000金币', u'1000经验', u'随机金币', u'随机经验']
        }

        leveldb[1] = {
            'level_id': 1,
            'title': '小试牛刀',
            'task1': '完成1次双杀',
            'task2': '击败隐藏僵尸',
            'task3': '血量不少于50%',
            'bonuses': [u'1000金币', u'1000经验', u'随机金币', u'随机经验']
        }

        leveldb[2] = {
            'level_id': 2,
            'title': '千钧一发',
            'task1': '任务一',
            'task2': '任务二',
            'task3': '任务三',
            'bonuses': [u'1000金币', u'1000经验', u'随机金币', u'随机经验']
        }

        leveldb[3] = {
            'level_id': 3,
            'title': '骑虎难下',
            'task1': '任务一',
            'task2': '任务二',
            'task3': '任务三',
            'bonuses': [u'1000金币', u'1000经验', u'随机金币', u'随机经验']
        }

        leveldb[4] = {
            'level_id': 4,
            'title': '决战千里',
            'task1': '任务一',
            'task2': '任务二',
            'task3': '任务三',
            'bonuses': [u'1000金币', u'1000经验', u'随机金币', u'随机经验']
        }

    def load_actorleveldb(self, actorleveldb):
        actorleveldb[(0, 0)] = {
            "actor_id": 0,
            "level_id": 0,
            "passed": True,
            "star1": True,
            "star2": True,
            "star3": True
        }

        actorleveldb[(0, 1)] = {
            "actor_id": 0,
            "level_id": 1,
            "passed": True,
            "star1": False,
            "star2": True,
            "star3": False,
        }

        actorleveldb[(0, 2)] = {
            "actor_id": 0,
            "level_id": 2,
            "passed": False,
            "star1": False,
            "star2": False,
            "star3": False,
        }

        actorleveldb[(1, 0)] = {
            "actor_id": 1,
            "level_id": 0,
            "passed": False,
            "star1": False,
            "star2": False,
            "star3": False,
        }

    def _process_command(self, command):
        tokens = command.split(' ')
        if tokens[0] == 'login':
            if len(tokens) == 3:
                try:
                    username, password = tokens[1], tokens[2]
                    self.handle_login(username, password)
                except Exception, ex:
                    print '[-] failed to login:', ex
            else:
                print '[-] syntax error: login username password'
        elif tokens[0] == 'get_account_info':
            if len(tokens) == 2:
                try:
                    username = tokens[1]
                    result = self.handle_get_account_info(username)
                    print result.account_info
                except Exception, ex:
                    print ex
            else:
                print '[-] syntax error: get_account_info username'
        elif tokens[0] == 'get_actor_info':
            if len(tokens) == 2:
                try:
                    username = tokens[1]
                    result = self.handle_get_actor_info(username)
                    if result.actor_info:
                        print 'actor_info:', result.actor_info
                    else:
                        # user not logined
                        pass
                except Exception, ex:
                    print ex
            else:
                print '[-] syntax error: get_actor_info username'
        elif tokens[0] == 'create_actor':
            if len(tokens) == 3:
                try:
                    username = tokens[1]
                    actor_type = tokens[2]
                    result = self.handle_create_actor(
                        username, actor_type)
                    if not result.result:
                        print '[-] failed to create actor',\
                            'errno:', result.errno
                except Exception, ex:
                    print 'failed to create_actor:', ex
            else:
                print '[-] syntax error:',\
                    'create_actor username actor_name := [sniper]'
        elif tokens[0] == 'get_actor_level_info':
            if len(tokens) == 2:
                try:
                    username = tokens[1]
                    ret = self.handle_get_actor_level_info(username)
                    print ret
                except Exception, ex:
                    print '[-] failed to get_actor_info:', ex
            else:
                print '[-] syntax error:'\
                    'get_actor_level_info username'
        elif tokens[0] == 'get_level_info':
            if len(tokens) == 2:
                try:
                    username = tokens[1]
                    ret = self.handle_get_level_info(username)
                    print ret.dump()
                except Exception, ex:
                    print '[-] failed to get_level_info:', ex
            else:
                print '[-] syntax error:',\
                    'get_level_info username'
        elif tokens[0] == 'start_level':
            if len(tokens) == 3:
                try:
                    actor_id = int(tokens[1])
                    level_id = int(tokens[2])
                    self.handle_start_level(actor_id, level_id)
                except Exception, ex:
                    print '[-] failed to start_level:', ex
            else:
                print '[-] syntax error:',\
                   'start_level actor_id level_id'  
        elif tokens[0] == 'break':
            import pdb; pdb.set_trace()
            subcommand = command[len('break'):].strip()
            if subcommand:
                self._process_command(subcommand)
        elif tokens[0] == 'exit':
            print '[+] exit, 88'
            # break
        return tokens[0]

    def _process_network(self):
        sockutil = self.sockutil

        read_socks = [self.listen_sock]
        if self.client_sock:
            read_socks.append(self.client_sock)

        read_socks, _, _= select.select(read_socks, [], [], 1)
        if self.client_sock in read_socks:
            recved = ''
            try:
                recved = self.client_sock.recv(1024)
            except Exception, ex:
                print ex

            print '[+] recved', recved
            if len(recved) == 0:
                print '[+] close socket'
                self.client_sock.close()
                self.client_sock = None
            
            self.buf += recved
            while True:
                self.buf = self.buf[self.index:]
                self.index = 0
                if len(self.buf) >= 2:
                    prev_index = self.index

                    msg_length = strtob128(self.buf[self.index:self.index+2])
                    self.index+=2
                    if msg_length > 10240:
                        # TODO: handle and close socket
                        raise Exception('fatal error')
                    if msg_length > len(self.buf) - self.index:
                        # not ready
                        import pdb; pdb.set_trace()
                        print '[-] not ready msg_length:', msg_length
                        self.index = prev_index
                        break
                    else:
                        payload = self.buf[self.index:self.index+msg_length]
                        self.index += msg_length
                        sockutil.recv_message(self.client_sock, payload)
                else:
                    break

        if self.listen_sock in read_socks:
            if self.client_sock:
                # TODO: multi clients
                print '[-] multi client is not implemented',\
                    'close the prev client'
                import pdb; pdb.set_trace()
                self.client_sock.close()
                self.index = 0
                self.buf = ''

            self.client_sock, client_addr = self.listen_sock.accept()
            print '[+] recv client:', client_addr
        # print '.',
        time.sleep(0.05)

    def main(self, args):
        """main flow ([+] are requests)

        (1) init account database
        (2) init actor database
        (3) server loop
            1) [+] receiver account login request/command
            2) handle login request
            3) [+] get actor info bound to this account:
                a) yes, return
                b) no, create actor
                    i. [+] create actor
                    ii. on success, goto 3)
                    iii.on failure, failure info
            4) [+] get level info && [+] per actor level info
            5) [+] start a level
            [TODO] ...
        """
        print '======== mini Shoot Server ========'
        print '[+] init account database'
        self.accountdb = {}
        create_account(self.accountdb, 'abc', 'abc')
        create_account(self.accountdb, u'主宰', 'abc')
        self.accountmap = {}

        print '[+] init actor database'
        self.actordb = {}
        self.actormap = {}

        print '[+] init level database'
        self.leveldb = {}
        self.load_leveldb(self.leveldb)

        self.actorleveldb = {}
        self.load_actorleveldb(self.actorleveldb)

        print '[+] init listening socket'
        self.listen_sock = socket(AF_INET, SOCK_STREAM)
        self.listen_sock.bind(('127.0.0.1', 10240))
        self.listen_sock.listen(10)
        print '[+] sockname:', self.listen_sock.getsockname()

        self.client_sock = None
        self.buf = ''
        self.index = 0

        self.sockutil = SockUtil()
        self.sockutil.register_handler(
            'login', self.handle_login)
        self.sockutil.register_handler(
            'logout', self.handle_logout)
        self.sockutil.register_handler(
            'get_account_info', self.handle_get_account_info)
        self.sockutil.register_handler(
            'create_actor', self.handle_create_actor)
        self.sockutil.register_handler(
            'get_actor_info', self.handle_get_actor_info)
        self.sockutil.register_handler(
            'get_actor_level_info', self.handle_get_actor_level_info)
        self.sockutil.register_handler(
            'get_level_info', self.handle_get_level_info)
        self.sockutil.register_handler(
            'start_level', self.handle_start_level)
        self.sockutil.register_handler(
            'leave_level', self.handle_leave_level)

        print '[+] init done'
        print ''

        self.shoot_game = None

        if args.command:
            pre_command = [
                'login abc abc',
                'create_actor abc sniper',
                'start_level 0 0'
            ]

            for c in pre_command:
                self._process_command(c)

        try:
            while True:
                # TODO
                command = None
                if args.command:
                    print '>',
                    command = raw_input()
                    if self._process_command(command) == 'exit':
                        break
                else:
                    self._process_network()

                if self.shoot_game:
                    self.shoot_game.update()

        except (Exception, KeyboardInterrupt) as ex:
            print ex

        if self.client_sock:
            print '[-] close client socket'
            self.client_sock.close()

        if self.listen_sock:
            print '[-] close listening socket'
            self.listen_sock.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--command', action='store_true')
    args = parser.parse_args()

    server = Server()
    server.main(args)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
