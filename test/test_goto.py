#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys; sys.path.append(os.getcwd())

import unittest

import game
import server
import message
import level1


class TestGoto(unittest.TestCase):

    def test_basic(self):
        bot = level1.Bot(0, None)
        tile_map = level1.TileMap(map_text=r'''
        {
            "Stride":1,
            "Height":1.0,
            "ColumnCount":4,
            "RowCount":4,
            "Tiles":[
                0,0,0,0,
                0,0,0,0,
                0,0,0,0,
                0,0,0,0
            ]
        }
        ''')
        goto = level1.GotoBehavior(bot, tile_map)
        goto.set_destination(message.Vector3(x=3, y=0, z=3))

        self.assertTrue(goto.validate())
        goto.activate()

        self.assertTrue(goto._has_waypoint())
        self.assertFalse(goto._has_reached())

        self.assertFalse(goto.is_satisfied())
        self.assertFalse(goto.is_failed())

        for i in range(0, 400):
            goto.update()

        self.assertFalse(goto._has_waypoint())
        self.assertTrue(goto._has_reached())
        self.assertTrue(goto.is_satisfied())


if __name__ == '__main__':
    unittest.main()
