#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys; sys.path.append(os.getcwd())

import game
import unittest


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

        shoot_game = game.ShootGame(MockSockUtil(), None)
        # start
        shoot_game.handle_enter_level()
        self.assertEqual(shoot_game.bot_count, 1)
        self.assertEqual(shoot_game.finished, False)

        # kill && spawn
        shoot_game.handle_level0_bot_killed()
        self.assertEqual(shoot_game.bot_count, 2)
        self.assertEqual(shoot_game.finished, False)

        # kill && spawn
        shoot_game.handle_level0_bot_killed()
        self.assertEqual(shoot_game.bot_count, 3)
        self.assertEqual(shoot_game.finished, False)

        # kill && finish
        shoot_game.handle_level0_bot_killed()
        self.assertEqual(shoot_game.bot_count, 3)
        self.assertEqual(shoot_game.finished, True)
    
        self.assertEqual(shoot_game.sockutil.spawn_request_count, 3)
        self.assertEqual(shoot_game.sockutil.finish_request_count, 1)


if __name__ == '__main__':
    unittest.main()
