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
    password
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
        return True


def login(userdb_, username_, password_):
    """login(...) -> T|F, E_NO

    Error number:

    E_OK
    E_NO_USERNAME
    E_INVALID_PASSWORD

    """
    validate_username(username_)
    validate_password(password_)
    print '[+] username_:', username_
    print '[+] password_:', password_

    password = userdb_.get(username_, None)
    if not password:
        print '[-] no username_: %s' % username_
        return False, E_NO_USERNAME
    if password != password_:
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
    """
    logined = False
    name = ''

    def __init__(self):
        pass

    def login(self, password_):
        """login() -> T|F
        """
        if self.logined:
            print '[+] account has logined'
            return True

        ret, error = login(self.userdb, self.name, password_)
        self.logined = ret
        if ret:
            print '[+] account:%s logined' % self.name
        else:
            print '[-] account:%s failed to login' % self.name

    def dump(self):
        """dump -> string
        """
        info = ''
        info += 'logined: {0}\n'.format(self.logined)
        info += 'name: {0}\n'.format(self.name)
        return info

def main():
    userdb = {}
    create_account(userdb, 'abc', 'abc')
    # login(userdb, 'abc', 'abc')

    account = Account()
    account.name = 'abc'
    account.userdb = userdb
    account.login('abc')
    print account.dump()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
