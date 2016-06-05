#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys; sys.path.append(os.getcwd())

import sockutil as su
import unittest

class TestSockUtil(unittest.TestCase):

    def test_send_request(self):

        class Handler:

            def __init__(self):
                self.instance_id = 0

            def handle_invalid_name(self, *args, **kwargs):
                pass

            def handle_ok_request(self, *args, **kwargs):
                pass

            def handle_exception_request(self, *args, **kwargs):
                raise Exception('exception')

        sockutil = su.SockUtil()

        def send_error(*args, **kwargs):
            print 'error', kwargs['error']

        sockutil.send_error = send_error

        handler = Handler()
        sockutil.register_object(Handler())
        sockutil.send_request(None, 'invalid_name')


if __name__ == '__main__':
    unittest.main()
