#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__=['validate_username', 'validate_password']

from servererrno import *

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
    return True

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


def login(userdb_, username_, password_):
    """login(...) -> T|F, E_NO

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


def actor_update(actordb, actor):
    """update
    """
    print '[+] update actrodb'
    actordb[actor.actor_id] = actor.dump()


def actor_level_info_update(actorleveldb, info):
    """update -> actorleveldb
    """
    print '[+] update actorlveldb'
    actorleveldb[(info.actor_id, info.level_id)] = info.dump()

if __name__ == '__main__':
    import doctest
    doctest.testmod()

