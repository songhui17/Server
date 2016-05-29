#!/usr/bin/env python


# TODO: error code
E_OK = 0
E_NO_USERNAME = 1
E_INVALID_PASSWORD = 2

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
        raise Exception('username_(len=%d) is too short or long' % len(username_))

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
        raise Exception('password_(len=%d) is too short or long' % len(password_))
    for i_ in password_:
        if i_ not in 'abc':
            raise Exception('Invalid password_: ' + password_)


def create_account(userdb_, username_, password_):
    """create_account(...) -> True|False, raise Exception on invalid username or
    password. Once created, insert into userdb {name, password, level, gold, experience}

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
    exit =  userdb_.get(username_)
    if userdb_.get(username_):
        print '[-] username_: %s exits' % username_
        return False
    else:
        print '[+] add username_: %s' % username_
        userdb_[username_] = password_
        new_user = {
            'name':username_,
            'password':password_,
            'level':0,
            'gold':0,
            'experience':0
        };
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

    def load(self, dict_):
        """load(dict_) init from dict_
        """
        name = dict_.get('name', None)
        if not name:
            raise ValueError('There is no entry name in dict_')

        password = dict_.get('password', None)
        if not password:
            raise ValueError('There is no entry password in dict_')
        
        self.name = name;
        self.password = password;


    def dump(self):
        """dump -> dict
        """
        ret = {}
        ret['name'] = self.name
        ret['password'] = self.password
        return ret

    def __eq__(self):
        pass

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

    def __str__(self):
        """dump -> string
        """
        info = ''
        info += 'logined: {0}\n'.format(self.logined)
        info += 'name: {0}\n'.format(self.name)
        return info


class LevelInfo:
    """LevelInfo
    Fields:

    title       :string
    task1       :string
    task2       :string
    task3       :string

    banuses     :list<string>
    """

    def __init__(self):
        pass


class PlayerLevelInfo:
    """PlayerLevelInfo: Per Player level stat
    Fields:

    actor_id    :int

    passed      :bool
    stars       :int[0,3]
    """

    def __init__(self):
        pass


class Actor:
    """Actor:
    Fields

        level       :int
        gold        :int
        experience  :int
    """

    def __init__(self):
        pass

    def load(self, dict_):
        level = dict_.get('level', -1)
        if level < 0:
            raise ValueError('There is no entry level in dict_')

        gold = dict_.get('gold', -1)
        if gold < 0:
            raise ValueError('There is no entry gold in dict_')

        experience = dict_.get('experience', -1)
        if experience < 0:
            raise ValueError('There is no entry experience in dict_')

        self.level = level
        self.gold = gold
        self.experience = experience

    def dump(self):
        ret = {}
        ret['level'] = self.level
        ret['gold'] = self.gold
        ret['experience'] = self.experience
        return ret

def get_actor_info(accountdb_, username_):
    validate_username(username_)
    account = accountdb_.get(username_, None)
    if not account:
        return

    pass

def login(accountdb_, accountdb_, username_, password_):
    """login -> account or None when no username_
    Exception:

        Invalid username
        Invalid password

    """
    validate_username(username_)
    validate_password(password_)
    
    user = accountdb_.get(username_, None)
    if not user:
        print '[-] no username_: %s' % username_
        return None

    account = accountdb_.get(username_, None)
    if not account:
        account = Account()
        account.load(user)
        account.userdb = accountdb_

        accountdb_[username_] = account

    if not account.login(password_):
        print '[-] invalid password'
        return None

    print 'account:'
    print str(account)
    return account


def main():
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
    userdb = {}
    create_account(userdb, 'abc', 'abc')
    actordb = {}

    accountmap = {}
    try:
        while True:
            # TODO
            print('>')
            command = raw_input()

            if command:
                tokens = command.split(' ')
                if tokens[0] == 'login':
                    print '[+] login'
                    if len(tokens) == 3:
                        try:
                            account = login(userdb, accountmap, tokens[1], tokens[2])
                        except Exception, ex:
                            print ex
                    else:
                        print '[-] syntax error: login username password'
                elif tokens[0] == 'get_actor_info':
                    pass
    except Exception, ex:
        print ex
    # actor_id = create_actor(userdb, actordb, 'abc', 0)
    # actor = Actor()
    # actor.load(actordb[actor_id])


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()