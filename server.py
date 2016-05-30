#!/usr/bin/env python
import time
import select
import argparse
from socket import *
from sockutil import *


E_OK = 0                    # success
E_NO_USERNAME = 1           # no account with name username
E_INVALID_PASSWORD = 2      # invalid password
E_USER_NOT_LOGINED = 3      # user has not logined, login required
E_ACTOR_EXIST = 4           # actor already bound to account
E_ACTOR_NOT_CREATED = 5     # actor_id == -1, no actor bound to account


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
    {'name': 'abc', 'password': 'abc', 'level': 0, 'gold': 0, 'experience': 0}
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
            'level': 0,
            'gold': 0,
            'experience': 0
        }
        userdb_[username_] = new_user
        return True


def db_login(userdb_, username_, password_):
    """db_login(...) -> T|F, E_NO

    Error number:

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

    def load(self, dict_):
        """load(dict_) init from dict_
        """
        name = dict_.get('name', None)
        if not name:
            raise ValueError('There is no entry name in dict_')

        password = dict_.get('password', None)
        if not password:
            raise ValueError('There is no entry password in dict_')

        self.name = name
        self.password = password

    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['name'] = self.name
        ret['password'] = self.password
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
            tmp = ActorLevelInfo()
            tmp.actor_id = data.get('actor_id')
            tmp.level_id = data.get('level_id')
            tmp.passed = data.get('passed')
            tmp.star1 = data.get('star1')
            tmp.star2 = data.get('star2')
            tmp.star3 = data.get('star3')

            self.copy(tmp)
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
        self.actor_id = tmp.actor_id
        self.name = tmp.name
        self.level = tmp.level
        self.gold = tmp.gold
        self.experience = tmp.experience

    def load(self, dict_):
        try:
            tmp.actor_id = dict_.get('actor_id')
            tmp.name = dict_.get('name')
            tmp.level = dict_.get('level')
            tmp.gold = dict_.get('gold')
            tmp.experience = dict_.get('experience')

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

        ErrorNo:

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

        user = accountdb_.get(username, None)
        if not user:
            print '[-] no username: %s' % username
            return False, E_NO_USERNAME

        account = accountmap_.get(username, None)
        if not account:
            print '[+] Create Account for ', username
            account = Account()
            account.load(user)
            account.userdb = accountdb_

            accountmap_[username] = account

        if not account.login(password):
            print '[-] invalid password'
            return False, E_INVALID_PASSWORD

        print 'account logined:'
        print str(account)

        if account.actor_id != -1:
            actor_data = actordb_.get(account.actor_id, None)
            if not actor:
                info = 'Fatal error: actor_id: {0} doesnt exist in'\
                    ' database'.format(account.actor_id)
                raise Exception(info)
            actor = Actor()
            actor.load(actor_data)
            actormap_[actor.actor_id] = actor
        return True, E_OK

    def handle_logout(self, username):
        pass

    def handle_get_actor_info(self, username):
        """handle_get_actor_info -> E_NO | dict { name, level, gold, experience }
        or None on error

        Error number:

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
                return None, E_USER_NOT_LOGINED

            actor_id = account.actor_id
            if actor_id == -1:
                print '[-] no actor for this account', account.name
                return None, E_ACTOR_NOT_CREATED

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
            return actor.dump(), E_OK

        except Exception, ex:
            print '[-]', ex
            raise ex


    def handle_get_account_info(self, username):
        """handle_get_account_info -> E_NO | dict {name, actor_id}
        or None on error

        Error Number:

        E_OK
        E_USER_NOT_LOGINED

        Exception:

        InvalidUsername

        """
        accountmap = self.accountmap

        print '[+] handle_get_account_info'
        validate_username(username)
        account = accountmap.get(username, None)
        if not account:
            print '[-] user: {0} is not logined'.format(username)
            return None, E_USER_NOT_LOGINED

        return {'name': account.name, 'actor_id': account.actor_id}, E_OK


    def handle_create_actor(self, username, actorname):
        """handle_create_actor -> T|F, E_NO
        :insert into actordb, create instance into actormap

        Error number:

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
            return False, E_USER_NOT_LOGINED

        if account.actor_id != -1:
            return False, E_ACTOR_EXIST

        actor = Actor()
        actor.actor_id = 0
        actor.name = actorname
        actor.level = 1
        actor.gold = 100
        actor.experience = 0

        if actor.actor_id in actordb:
            info = 'actor_id: {0} conflict for {1}'.format(
                actor.actor_id, actorname)
            print '[-]', info
            raise Exception(info)

        actordb[actor.actor_id] = actor.dump()
        actormap[actor.actor_id] = actor
        account.actor_id = actor.actor_id
        print actor
        return True, E_OK


    def handle_get_actor_level_info(self, username):
        """handle_get_actor_info -> dict{} or None on error, errno

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
            return None, E_USER_NOT_LOGINED

        actor_id = account.actor_id
        if actor_id == -1:
            print '[-] no actor for this account', account.name
            return None, E_ACTOR_NOT_CREATED

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

        level_data = [v for k, v in actorleveldb if k[0] == actor_id]
        # TODO: handle empty
        return level_data


    def load_leveldb(self, leveldb):
        """load_leveldb: init level database
        """
        leveldb[0] = {
            'level_id': 0,
            'title': 'level_0',
            'task1': 'task desc 1',
            'task2': 'task desc 2',
            'task3': 'task desc 3',
            'bonuses': ['a', 'b']
        }

        leveldb[1] = {
            'level_id': 1,
            'title': 'level_1',
            'task1': 'task desc 1',
            'task2': 'task desc 2',
            'task3': 'task desc 3',
            'bonuses': ['a', 'b']
        }

        leveldb[2] = {
            'level_id': 2,
            'title': 'level_2',
            'task1': 'task desc 1',
            'task2': 'task desc 2',
            'task3': 'task desc 3',
            'bonuses': ['a', 'b']
        }

        leveldb[3] = {
            'level_id': 3,
            'title': 'level_3',
            'task1': 'task desc 1',
            'task2': 'task desc 2',
            'task3': 'task desc 3',
            'bonuses': ['a', 'b']
        }


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
        self.accountmap = {}

        print '[+] init actor database'
        self.actordb = {}
        self.actormap = {}

        print '[+] init level database'
        self.leveldb = {}
        self.load_leveldb(self.leveldb)

        self.actorleveldb = {}

        print '[+] init listening socket'
        listen_sock = socket(AF_INET, SOCK_STREAM)
        print listen_sock
        listen_sock.bind(('127.0.0.1', 10240))
        listen_sock.listen(10)
        print '[+] sockname:', listen_sock.getsockname()

        client_sock = None
        buf = ''
        index = 0
        sockutil = SockUtil()
        sockutil.register_handler('login', self.handle_login)
        sockutil.register_handler('logout', self.handle_logout)

        print '[+] init done'
        print ''

        try:
            while True:
                # TODO
                command = None
                if args.command:
                    print '>',
                    command = raw_input()
                else:
                    read_socks = [listen_sock]
                    if client_sock:
                        read_socks.append(client_sock)

                    read_socks, _, _= select.select(read_socks, [], [], 1)
                    if client_sock in read_socks:
                        recved = ''
                        try:
                            recved = client_sock.recv(1024)
                        except Exception, ex:
                            print ex

                        print '[+] recv', buf
                        if len(recved) == 0:
                            print '[+] close socket', recved
                            client_sock.close()
                            client_sock = None
                        
                        buf += recved
                        buf = buf[index:]
                        index = 0
                        if len(buf) >= 2:
                            prev_index = index

                            msg_length = str2short(buf[index:index+3])
                            index+=2
                            if msg_length > 1024:
                                # TODO: handle and close socket
                                raise Exception('fatal error')
                            if msg_length < len(buf) - index:
                                # not ready
                                index = prev_index
                            else:
                                payload = buf[index:index+msg_length]
                                index += msg_length
                                sockutil.recv_message(client_sock, payload)

                    if listen_sock in read_socks:
                        if client_sock:
                            # TODO: multi clients
                            print '[-] multi client is not implemented',\
                                'close the prev client'
                            client_sock.close()

                        client_sock, client_addr = listen_sock.accept()
                        print '[+] recv client:', client_addr
                    print '.',
                    time.sleep(1)

                if command:
                    tokens = command.split(' ')
                    if tokens[0] == 'login':
                        if len(tokens) == 3:
                            try:
                                username, password = tokens[1], tokens[2]
                                self.handle_login(username, password)
                            except Exception, ex:
                                print ex
                        else:
                            print '[-] syntax error: login username password'
                    elif tokens[0] == 'get_account_info':
                        if len(tokens) == 2:
                            try:
                                username = tokens[1]
                                account_info, errno = self.handle_get_account_info(username)
                                if account_info:
                                    print account_info
                                else:
                                    # print '[-] user is not logined'.\
                                    #     format(username)
                                    pass
                            except Exception, ex:
                                print ex
                        else:
                            print '[-] syntax error: get_account_info username'
                    elif tokens[0] == 'get_actor_info':
                        if len(tokens) == 2:
                            try:
                                username = tokens[1]
                                actor_info, errno = self.handle_get_actor_info(username)
                                if actor_info:
                                    print 'actor_info:', actor_info
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
                                actorname = tokens[2]
                                ret, errno = self.handle_create_actor(username, actorname)
                                if not ret:
                                    print '[-] failed to create actor',\
                                        'errno:', errno
                            except Exception, ex:
                                print ex
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
                    elif tokens[0] == 'break':
                        import pdb; pdb.set_trace()
                    elif tokens[0] == 'exit':
                        print '[+] exit, 88'
                        break
        except (Exception, KeyboardInterrupt) as ex:
            print ex

        if client_sock:
            print '[-] close client socket'
            client_sock.close()

        if listen_sock:
            print '[-] close listening socket'
            listen_sock.close()


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
