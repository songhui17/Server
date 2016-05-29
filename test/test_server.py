#!/usr/bin/env python
import os, sys; sys.path.append(os.getcwd())
import unittest

import server


class ServerTest(unittest.TestCase):

    def test_create_account(self):
        userdb = {}

        # Sucess
        ret = server.create_account(userdb, 'abc', 'abc')
        self.assertTrue(ret)
        self.assertTrue(userdb.get('abc'))

        # Failure
        ret = server.create_account(userdb, 'abc', 'abc')
        self.assertFalse(ret)

    def test_login(self):
        userdb = {}
        server.create_account(userdb, 'abc', 'abc')

        # Success
        ret = server.login(userdb, 'abc', 'abc')
        self.assertEqual(ret, (True, server.E_OK))

        # Failure
        ret = server.login(userdb, 'abc', 'ab')
        self.assertTrue(ret, (True, server.E_INVALID_PASSWORD))

        ret = server.login(userdb, 'a', 'ab')
        self.assertTrue(ret, (True, server.E_NO_USERNAME))


if __name__ == '__main__':
    unittest.main()
