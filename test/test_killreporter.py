#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys; sys.path.append(os.getcwd())

import unittest

import game
import server
import message
import level1


class TestKillReporter(unittest.TestCase):

    def test_basic(self):
        kill_reporter = level1.KillReporter()
        self.assertEquals(kill_reporter.get_triple_kill(), 0)
        kill_reporter.add_kill()
        self.assertEquals(kill_reporter.get_triple_kill(), 0)
        kill_reporter.add_kill()
        self.assertEquals(kill_reporter.get_triple_kill(), 0)
        kill_reporter.add_kill()
        self.assertEquals(kill_reporter.get_triple_kill(), 1)

        import time
        time.sleep(2)
        kill_reporter.update(0)

        kill_reporter.add_kill()
        self.assertEquals(kill_reporter.get_triple_kill(), 1)
        kill_reporter.add_kill()
        self.assertEquals(kill_reporter.get_triple_kill(), 1)
        kill_reporter.add_kill()
        self.assertEquals(kill_reporter.get_triple_kill(), 2)
        # import pdb; pdb.set_trace()


if __name__ == '__main__':
    unittest.main()
