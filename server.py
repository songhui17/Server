#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import select
import argparse
from errno import *
from socket import *

import dbutil
import msgutil
import message
from dbutil import *
from sockutil import *
from servererrno import *

class NotLoginedError(Exception):
    def __init__(self):
        pass


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


# class ActorLevelInfo:
#     """ActorLevelInfo: Per Actor level stat
#     Fields:
# 
#     actor_id    :int
# 
#     level_id    :int
#     passed      :bool
#     star1      :bool
#     star2      :bool
#     star3      :bool
#     """
# 
#     actorleveldb = None
# 
#     def __init__(self):
#         pass
# 
#     def _copy(self, copy):
#         self.actor_id = copy.actor_id
#         self.level_id = copy.level_id
#         self.passed = copy.passed
#         self.star1 = copy.star1
#         self.star2 = copy.star2
#         self.star3 = copy.star3
# 
#     def load(self, data):
#         """load :from data
# 
#         Exception:
# 
#         KeyError
#         """
#         try:
#             # import pdb; pdb.set_trace()
#             tmp = ActorLevelInfo()
#             tmp.actor_id = data.get('actor_id')
#             tmp.level_id = data.get('level_id')
#             tmp.passed = data.get('passed')
#             tmp.star1 = data.get('star1')
#             tmp.star2 = data.get('star2')
#             tmp.star3 = data.get('star3')
# 
#             self._copy(tmp)
#         except KeyError, ex:
#             print '[-]', ex
#             raise ex
# 
#     def dump(self):
#         """dump -> dict{actor_id, level_id, passed, star1, star2, star3}
#         """
#         ret = {}
#         ret['actor_id'] = self.actor_id
#         ret['level_id'] = self.level_id
#         ret['passed'] = self.passed
#         ret['star1'] = self.star1
#         ret['star2'] = self.star2
#         ret['star3'] = self.star3
#         return ret
# 
#     def update(self):
#         """update -> actorleveldb
#         """
#         assert self.actorleveldb is not None
#         print '[+] update actorlveldb'
#         record = self.actorleveldb.get((self.actor_id, self.level_id))
#         self.actorleveldb[(self.actor_id, self.level_id)] = self.dump()


# class Actor:
#     """Actor:
#     Fields
# 
#     account     :Account (back ref)
# 
#     actor_id    :int
#     name        :int
#     level       :int
#     gold        :int
#     experience  :int
# 
#     """
# 
#     actordb = None
# 
#     def __init__(self):
#         """
#         Params:
# 
#         actor_id: int
#         name: str
#         level: int
#         gold: int
#         experience: int
#         max_hp: int
#         hp: int
#         max_ammo: int
#         ammo: int
# 
#         """
#         self.actor_id = kwargs.get('actor_id')
#         self.name = kwargs.get('name')
#         self.level = kwargs.get('level')
#         self.gold = kwargs.get('gold')
#         self.experience = kwargs.get('experience')
#         self.max_hp = kwargs.get('max_hp')
#         self.hp = kwargs.get('hp')
#         self.max_ammo = kwargs.get('max_ammo')
#         self.ammo = kwargs.get('ammo')
# 
#     def __str__(self):
#         info = ''
#         info += 'actor_id: {0}\n'.format(self.actor_id)
#         info += 'name: {0}\n'.format(self.name)
#         info += 'level: {0}\n'.format(self.level)
#         info += 'gold: {0}\n'.format(self.gold)
#         info += 'experience: {0}\n'.format(self.experience)
#         return info
# 
#     def load(self, data):
#         """load from dict
#         Exception:
# 
#         KeyError
# 
#         """
#         self.actor_id = kwargs['actor_id']
#         self.name = kwargs['name']
#         self.level = kwargs['level']
#         self.gold = kwargs['gold']
#         self.experience = kwargs['experience']
#         self.max_hp = kwargs['max_hp']
#         self.hp = kwargs['hp']
#         self.max_ammo = kwargs['max_ammo']
#         self.ammo = kwargs['ammo']
# 
#     def dump(self):
#         """dump -> dict
#         """
#         ret = {}
#         ret['actor_id'] = sockutil.dump(self.actor_id)
#         ret['name'] = sockutil.dump(self.name)
#         ret['level'] = sockutil.dump(self.level)
#         ret['gold'] = sockutil.dump(self.gold)
#         ret['experience'] = sockutil.dump(self.experience)
#         ret['max_hp'] = sockutil.dump(self.max_hp)
#         ret['hp'] = sockutil.dump(self.hp)
#         ret['max_ammo'] = sockutil.dump(self.max_ammo)
#         ret['ammo'] = sockutil.dump(self.ammo)
#         return ret
# 
#     def update(self):
#         """update -> actordb
#         """
#         print '[+] update actrodb'
#         assert self.actordb is not None
#         self.actordb[self.actor_id] = self.dump()


class Connection:

    def __init__(self, server, instance_id, client_sock, client_addr):
        self.server = server
        self.instance_id = instance_id

        self.client_sock = client_sock
        self.client_addr = client_addr

        self.sockutil = SockUtil()

        self.accountdb = server.accountdb
        self.accountmap = server.accountmap

        self.actordb = server.actordb
        self.actormap = server.actormap

        self.actor = None

        self.leveldb = server.leveldb
        self.actorleveldb = server.actorleveldb

        self.buf = ''
        self.index = 0

        self.shoot_game = None

    def close_connection(self):
        print '[-] close connection'
        if self.client_sock is not None:
            self.client_sock.close()

        if self.shoot_game:
            self.shoot_game.destroy()
            self.shoot_game = None

    def on_remote_close(self):
        print '[+] close socket'
        self.server.connections.pop(self.instance_id)
        self.server.read_socks.pop(self.client_sock)

        self.client_sock.close()
        self.client_sock = None

        if self.shoot_game:
            self.shoot_game.destroy()
            self.shoot_game = None

    def recv_data(self, data):
        # print '[+] connection:%d, recv_data:%s' % (self.instance_id, data)
        if len(data) == 0:
            # import pdb; pdb.set_trace()
            self.on_remote_close()

        self.buf += data
        while True:
            self.buf = self.buf[self.index:]
            self.index = 0
            if len(self.buf) >= 2:
                prev_index = self.index

                msg_length = strtob128(self.buf[self.index:self.index+2])
                self.index += 2
                if msg_length > 10240:
                    raise Exception('fatal error')
                if msg_length > len(self.buf) - self.index:
                    # not ready
                    # import pdb; pdb.set_trace()
                    print '[-] not ready msg_length:', msg_length
                    self.index = prev_index
                    break
                else:
                    payload = self.buf[self.index:self.index+msg_length]
                    self.index += msg_length
                    self.sockutil.recv_message(
                        self.client_sock, payload, obj=self)
            else:
                break

    def handle_login_request(self, username, password):
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
            return message.LoginRequestResponse(result=False, errno=E_NO_USERNAME)

        account = accountmap_.get(username, None)
        if not account:
            print '[+] Create account for ', username
            # import pdb; pdb.set_trace()
            account = Account()
            account.load(account_data)
            account.userdb = accountdb_

            accountmap_[username] = account

        if not msgutil.account_login(account, password):
            print '[-] invalid password'
            return message.LoginRequestResponse(result=False, errno=E_INVALID_PASSWORD)

        print 'account logined:'
        print account.dump(ignore_password=True)

        if account.actor_id != -1:
            # TODO: create actor instance
            actor_data = actordb_.get(account.actor_id, None)
            if not actor_data:
                info = 'Fatal error: actor_id: {0} doesnt exist in'\
                    ' database'.format(account.actor_id)
                raise Exception(info)
            actor = message.Actor()
            actor.load(**actor_data)
            actormap_[actor.actor_id] = actor

            self.actor = actor

        return message.LoginRequestResponse(result=True, errno=E_OK)

    def handle_logout_request(self, username):
        pass

    def handle_get_actor_info_request(self, username):
        """handle_get_actor_info_request -> dict { name, level, gold, experience }
        | E_NO or None on error

        Errno:

        E_OK
        E_USER_NOT_LOGINED

        Exception:

        InvalidUsername
        ActorNotExistInDB

        """
        print '[+] handle_get_actor_info_request'
        # import pdb; pdb.set_trace()
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
                    actor_info=None, errno=E_USER_NOT_LOGINED)

            actor_id = account.actor_id
            if actor_id == -1:
                print '[-] no actor for this account', account.name
                return message.GetActorInfoRequestResponse(
                    actor_info=None, errno=E_ACTOR_NOT_CREATED)

            actor = actormap.get(actor_id, None)
            if not actor:
                print '[+] Create Actor instance'
                actor_data = actordb.get(actor_id, None)
                if not actor_data:
                    # TODO: should assert actor_data not None?
                    info = 'Fatal error: actor_id: {0} doesnt exist in'\
                        ' database'.format(account.actor_id)
                    raise Exception(info)
                actor = message.Actor()
                actor.load(**actor_data)
                actormap[actor_id, actor]
            # import pdb; pdb.set_trace()
            return message.GetActorInfoRequestResponse(
                actor_info=actor, errno=E_OK)
        except Exception, ex:
            print '[-]', ex
            raise ex

    def handle_get_actor_info2_request(self, actor_id):
        """handle_get_actor_info2_request -> actor.dump()

        Exception:

        KeyError    :Not actor instance created
        """
        try:
            actor = self.actormap[actor_id]
            assert actor.account is not None, 'account must be assgined'
            if not actor.account.logined:
                raise NotLoginedError()
            # import pdb; pdb.set_trace()
            return message.GetActorInfoRequestResponse(
                actor_info=actor.dump(), errno=E_OK)
        except KeyError, ex:
            # (1) actor created?
            # (2) actordb in db?
            raise NotImplementedError('handle actor instance not created')

    def handle_get_account_info_request(self, username):
        """handle_get_account_info_request -> account.dump(), E_NO

        Errno:
        
        E_OK
        E_USER_NOT_LOGINED

        Exception:

        # TODO: NotLoginedError
        InvalidUsername

        """
        accountmap = self.accountmap

        print '[+] handle_get_account_info_request'
        validate_username(username)
        account = accountmap.get(username, None)
        if not account:
            print '[-] user: {0} is not logined'.format(username)
            # raise NotLoginedError()
            return message.GetAccountInfoRequestResponse(
                account_info=None, errno=E_USER_NOT_LOGINED)

        return message.GetAccountInfoRequestResponse(
            account_info=account.dump(), errnor=E_OK)

    def handle_create_actor_request(self, username, actor_type):
        """handle_create_actor_request -> T|F, E_NO
        :insert into actordb, create instance into actormap

        Errno:

        E_OK
        E_USER_NOT_LOGINED
        E_ACTOR_EXIST

        Exception:

        InvalidUsername
        ActorIDConflict

        """
        print '[+] handle_create_actor_request'
        accountmap = self.accountmap
        actordb = self.actordb
        actormap = self.actormap

        validate_username(username)
        account = accountmap.get(username, None)
        if not account:
            print '[-] user: {0} is not logined'.format(username)
            return message.CreateActorRequestResponse(result=False, errno=E_USER_NOT_LOGINED)

        if account.actor_id != -1:
            return message.CreateActorRequestResponse(result=False, errno=E_ACTOR_EXIST)

        actor = message.Actor()
        actor.actor_id = self.server.actor_id;
        self.server.actor_id += 1
        actor.name = actor_type
        actor.level = 1
        actor.gold = 1000
        actor.experience = 100
        actor.max_hp = 1000
        actor.hp = actor.max_hp
        actor.max_ammo = 1800
        actor.ammo = 0

        if actor.actor_id in actordb:
            info = 'actor_id: {0} conflict for {1}'.format(
                actor.actor_id, actor_type)
            print '[-]', info
            raise Exception(info)

        actordb[actor.actor_id] = actor.dump()
        actormap[actor.actor_id] = actor
        account.actor_id = actor.actor_id
        actor.account = account
        print '[+] actor created:', actor
        self.actor = actor
        return message.CreateActorRequestResponse(result=True, errno=E_OK)

    def handle_get_actor_level_info_request(self, username):
        """handle_get_actor_level_info_request -> dict{} or None on error, errno

        Error Number:

        E_OK
        E_USER_NOT_LOGINED

        Exception:

        InvalidUsername

        """
        print '[+] handle_get_actor_level_info_request'
        print '[X] TODO: copy from get_actor_info'
        accountmap = self.accountmap
        actormap = self.actormap
        actorleveldb = self.actorleveldb

        validate_username(username)
        account = accountmap.get(username, None)
        if not account:
            print '[-] user: {0} is not logined'.format(username)
            return message.GetActorLevelInfoRequestResponse(
                actorl_level_info=None, errno=E_USER_NOT_LOGINED)

        actor_id = account.actor_id
        if actor_id == -1:
            print '[-] no actor for this account', account.name
            return message.GetActorLevelInfoRequestResponse(
                actor_level_info=None, errno=E_ACTOR_NOT_CREATED)

        actor = actormap.get(actor_id, None)
        if not actor:
            print '[+] Create Actor instance'
            actor_data = actordb.get(actor_id, None)
            if not actor_data:
                # TODO: should assert actor_data not None?
                info = 'Fatal error: actor_id: {0} doesnt exist in'\
                    ' database'.format(account.actor_id)
                raise Exception(info)
            actor = message.Actor()
            actor.load(**actor_data)
            actormap[actor_id, actor]

        level_data = [v for k, v in actorleveldb.iteritems() if k[0] == actor_id]
        print level_data
        # TODO: handle empty
        return message.GetActorLevelInfoRequestResponse(
            actor_level_info=level_data, errno=E_OK)

    def handle_get_level_info_request(self, username):
        """handle_get_level_info_request -> level_info, errno

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
            return message.GetLevelInfoRequestResponse(
                level_info=None, errno=E_USER_NOT_LOGINED)

        level_info = [
            message.LevelInfo(
                level_id=v['level_id'],
                title=v['title'],
                task1=v['task1'],
                task2=v['task2'],
                task3=v['task3'],
                bonuses=v['bonuses']) for v in self.leveldb.itervalues()]
        return message.GetLevelInfoRequestResponse(
            level_info=level_info, errno=E_OK)

    def handle_start_level_request(self, actor_id, level_id):
        """handle_start_level_request -> E_NO

        ErrorNo:

        E_OK
        E_USER_NOT_LOGINED

        """
        # TODO
        actor = self.actormap.get(actor_id, None)
        if actor is None:
            return E_USER_NOT_LOGINED

        if self.shoot_game is not None:
            raise NotImplementedError('ShootGame is running')

        import game
        # level_id = 1
        level = self.leveldb[level_id]
        if level is None:
            return message.StartLevelRequestResponse(errno=E_NO_SUCH_LEVEL)
        # TODO

        levelinfo = message.LevelInfo(
                level_id=level['level_id'],
                title=level['title'],
                task1=level['task1'],
                task2=level['task2'],
                task3=level['task3'],
                bonuses=level['bonuses'],
        )
        try:
            self.shoot_game = game.ShootGame(self, levelinfo)
        except NotImplementedError, ex:
            print '[-]', ex
            return message.StartLevelRequestResponse(errno=E_NO_SUCH_LEVEL);

        self.shoot_game.start()
    
    def handle_leave_level_request(self):
        if self.shoot_game:
            self.shoot_game.destroy()
            self.shoot_game = None
        return message.LeaveLevelRequestResponse(errno=E_OK)

    def _process_command(self, command):
        tokens = command.split(' ')
        if tokens[0] == 'login':
            if len(tokens) == 3:
                try:
                    username, password = tokens[1], tokens[2]
                    self.handle_login_request(username, password)
                except Exception, ex:
                    print '[-] failed to login:', ex
            else:
                print '[-] syntax error: login username password'
        elif tokens[0] == 'get_account_info':
            if len(tokens) == 2:
                try:
                    username = tokens[1]
                    result = self.handle_get_account_info_request(username)
                    print result.account_info
                except Exception, ex:
                    print ex
            else:
                print '[-] syntax error: get_account_info username'
        elif tokens[0] == 'get_actor_info':
            if len(tokens) == 2:
                try:
                    username = tokens[1]
                    result = self.handle_get_actor_info_request(username)
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
                    result = self.handle_create_actor_request(
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
                    ret = self.handle_get_actor_level_info_request(username)
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
                    ret = self.handle_get_level_info_request(username)
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
                    self.handle_start_level_request(actor_id, level_id)
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

    def update(self, delta_time):
        if self.shoot_game:
            self.shoot_game.update(delta_time)


class Server:

    def __init__(self):
        pass

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
            'task1': '完成1次三杀',
            'task2': '击败育母蜘蛛',
            'task3': '基地血量不少于50%',
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
        pass
        # actorleveldb[(0, 0)] = {
        #     "actor_id": 0,
        #     "level_id": 0,
        #     "passed": False,
        #     "star1": True,
        #     "star2": True,
        #     "star3": False
        # }

        # actorleveldb[(0, 1)] = {
        #     "actor_id": 0,
        #     "level_id": 1,
        #     "passed": False,
        #     "star1": False,
        #     "star2": True,
        #     "star3": False,
        # }

        # actorleveldb[(0, 2)] = {
        #     "actor_id": 0,
        #     "level_id": 2,
        #     "passed": False,
        #     "star1": False,
        #     "star2": False,
        #     "star3": False,
        # }

        # actorleveldb[(1, 0)] = {
        #     "actor_id": 1,
        #     "level_id": 0,
        #     "passed": False,
        #     "star1": False,
        #     "star2": False,
        #     "star3": False,
        # }

    def _del_connection(self, connection):
        del self.read_socks[connection.client_sock]
        connection.close_connection()

    def _process_network(self):
        read_socks = [self.listen_sock]
        read_socks.extend(self.read_socks.keys())

        read_socks, _, _= select.select(read_socks, [], [], 0)
        for read_sock in read_socks:
            if read_sock == self.listen_sock:
                client_sock, client_addr = self.listen_sock.accept()
                print '[+] recv client:', client_addr
                connection = Connection(self, self.connection_instance_id,
                                        client_sock, client_addr)
                # import pdb; pdb.set_trace()
                self.connection_instance_id += 1
                self.connections[connection.instance_id] = connection
                self.read_socks[client_sock] = connection
            else:
                try:
                    data = read_sock.recv(1024)
                    self.read_socks[read_sock].recv_data(data)
                except error, ex:
                    print '[-] recv error, connection:', self.read_socks[read_sock]
                    if ex.args[0] in (EAGAIN, EWOULDBLOCK,):
                        pass
                    else:
                        print '[-] delect conneciton'
                        self._del_connection(self.read_socks[read_sock])
                except Exception, ex:
                    # self.read_socks[read_sock].recv_error(ex)
                    print '[-] ex:%s, delect conneciton' % ex
                    self._del_connection(self.read_socks[read_sock])

        # time.sleep(0.02)

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
        dbutil.create_account(self.accountdb, 'netease1', '123456')
        dbutil.create_account(self.accountdb, 'netease2', '123456')
        dbutil.create_account(self.accountdb, 'netease3', '123456')
        dbutil.create_account(self.accountdb, u'主宰', '123456')
        self.accountmap = {}

        print '[+] init actor database'
        self.actordb = {}
        self.actormap = {}
        self.actor_id = 0

        print '[+] init level database'
        self.leveldb = {}
        self.load_leveldb(self.leveldb)

        self.actorleveldb = {}
        self.load_actorleveldb(self.actorleveldb)

        print '[+] init listening socket'
        self.listen_sock = socket(AF_INET, SOCK_STREAM)
        self.listen_sock.bind((args.ip, args.port))
        self.listen_sock.listen(10)
        print '[+] sockname:', self.listen_sock.getsockname()

        self.sockutil = SockUtil()
        self.connection_instance_id = 0
        self.connections = {}
        self.read_socks = {}

        print '[+] init done'
        print ''

        if args.command:
            pre_command = [
                'login abc abc',
                'create_actor abc sniper',
                'start_level 0 0'
            ]

            for c in pre_command:
                self._process_command(c)

        try:
            delta_time = 0.02
            start_time = time.clock()
            target_delta_time = 1.0 / 60

            while True:
                # print delta_time
                command = None
                if args.command:
                    print '>',
                    command = raw_input()
                    if self._process_command(command) == 'exit':
                        break
                else:
                    self._process_network()

                error_connections = []
                for k, v in self.connections.iteritems():
                    try:
                        v.update(delta_time)
                    except:
                        print '[-] error:', (k, v)
                        import traceback
                        traceback.print_exc()
                        error_connections.append(k)

                for k in error_connections:
                    connection = self.connections.pop(k)
                    self._del_connection(connection)

                cur_time = time.clock()
                delta_time = cur_time - start_time
                diff = target_delta_time - delta_time
                if diff > 0:
                    time.sleep(diff)
                cur_time = time.clock()
                delta_time = cur_time - start_time
                start_time = cur_time
        except (Exception, KeyboardInterrupt) as ex:
            import traceback
            traceback.print_exc()

        if self.listen_sock:
            print '[-] close listening socket'
            self.listen_sock.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--command', action='store_true')
    parser.add_argument('--ip', dest='ip', default='127.0.0.1')
    parser.add_argument('--port', dest='port', type=int, default=10240)
    args = parser.parse_args()

    server = Server()
    server.main(args)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
