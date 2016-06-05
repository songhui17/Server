#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dbutil


# Account

def account_login(self, password_):
    """login() -> T|F
    """
    if self.logined:
        print '[+] account has logined'
        return True

    ret, error = dbutil.login(self.userdb, self.name, password_)
    self.logined = ret
    if ret:
        print '[+] account:%s logined' % self.name
    else:
        print '[-] account:%s failed to login' % self.name
    return ret
