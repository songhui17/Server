#!/usr/bin/env python

# TODO: error code
E_OK = 0
E_NO_USERNAME = 1
E_INVALID_PASSWORD = 2

def validate_username(username_):
    '''
    valid username_: [a-zA-Z](1,10)
    '''
    if username_ is None:
        raise Exception('username_ is None')

    if not (0 < len(username_) < 10):
        raise Exception('username_ is too long', len(username_))

    for i_ in username_:
        if i_ not in 'abc':
            raise Exception('Invalid username_:' + username_)


def validate_password(password_):
    '''
    valid password_: [a-zA-Z](1,10)
    '''
    if password_ is None:
        raise Exception('password_ is None')
    if not (0 < len(password_) < 10):
        raise Exception('password_ is too long', len(password_))
    for i_ in password_:
        if i_ not in 'abc':
            raise Exception('Invalid password_: ' + password_)


def create_user(userdb_, username_, password_):
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


def main():
    userdb = {}
    create_user(userdb, 'abc', 'abc')
    login(userdb, 'abc', 'abc')

if __name__ == '__main__':
    main()
