#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys; sys.path.append(os.getcwd())

import unittest

import game
import server
import message


class TestGame(unittest.TestCase):

    def test_level0(self):
        
        class MockSockUtil:

            spawn_request_count = 0
            finish_request_count = 0

            def register_handler(self, *args, **kwargs):
                pass
            
            def send_request(self, *args, **kwargs):
                request = kwargs['method']
                if request == 'spawn_bot':
                    self.spawn_request_count+=1
                elif request == 'finish_level':
                    self.finish_request_count += 1

        class MockConnection:
            level = None

            def __init__(self, sockutil):
                self.sockutil = sockutil
                self.client_sock = None
                self.actor = server.Actor()
                self.actordb = {}
                self.actorleveldb = {}

        leveldb = {
            'level_id': 0,
            'title': u'磨刀霍霍',
            'task1': u'击败1个蜘蛛',
            'task2': u'击败2个蜘蛛',
            'task3': u'击败3个蜘蛛',
            'bonuses': [u'1000金币', u'1000经验', u'随机金币', u'随机经验']
        }
        level = message.LevelInfo(
            level_id=leveldb['level_id'],
            title=leveldb['title'],
            task1=leveldb['task1'],
            task2=leveldb['task2'],
            task3=leveldb['task3'],
            bonuses=leveldb['bonuses']
        )

        connection = MockConnection(MockSockUtil())
        shoot_game = game.ShootGame(connection, level)
        shoot_game.start()
        # start
        shoot_game.level.handle_enter_level()
        self.assertEqual(shoot_game.level.bot_count, 1)
        self.assertEqual(shoot_game.level.finished, False)

        # kill && spawn
        shoot_game.level.handle_level0_bot_killed()
        self.assertEqual(shoot_game.level.bot_count, 2)
        self.assertEqual(shoot_game.level.finished, False)

        # kill && spawn
        shoot_game.level.handle_level0_bot_killed()
        self.assertEqual(shoot_game.level.bot_count, 3)
        self.assertEqual(shoot_game.level.finished, False)

        # kill && finish
        shoot_game.level.handle_level0_bot_killed()
        self.assertEqual(shoot_game.level.bot_count, 3)
        self.assertEqual(shoot_game.level.finished, True)
    
        self.assertEqual(connection.sockutil.spawn_request_count, 3)
        self.assertEqual(connection.sockutil.finish_request_count, 1)

        print connection.actordb
        print connection.actorleveldb


if __name__ == '__main__':
    unittest.main()
