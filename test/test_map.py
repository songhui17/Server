#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys; sys.path.append(os.getcwd())

import level1
import message
import unittest


class TestMap(unittest.TestCase):

    def test_basic(self):
        m = level1.TileMap()
        raw = m.raw
        self.assertEquals(raw['Stride'], 1)
        self.assertEquals(raw['Height'], 2)
        self.assertEquals(raw['ColumnCount'], 50)
        self.assertEquals(raw['RowCount'], 30)
        # import pdb; pdb.set_trace()

    def test_see_through(self):
        print 'test_see_through'
        m = level1.TileMap()

        start = message.Vector3(x=42, y=0, z=9)
        end = message.Vector3(x=14, y=0, z=4)
        self.assertFalse(
            m.see_through(m.position_to_index(start),
                          m.position_to_index(end)))

        self.assertTrue(m.see_through((5, 16), (6, 17)))
        self.assertTrue(m.see_through((12, 36), (14, 34)))
        self.assertTrue(m.see_through((14, 34), (12, 36)))
        self.assertTrue(m.see_through((13, 33), (9, 40)))


    def test_find_path(self):
        m = level1.TileMap()
        # path = m._find_path(message.Vector3(x=42, y=0, z=9),
        #                    message.Vector3(x=14, y=0, z=4),
        #                    smooth=True)
        # path = m._find_path(message.Vector3(x=42, y=0, z=9),
        #                    message.Vector3(x=22, y=0, z=26),
        #                    smooth=True)
        # path = m._find_path(message.Vector3(x=42, y=0, z=9),
        #                    message.Vector3(x=7.79, y=0, z=1.60),
        #                    smooth=True)
        # path = m._find_path(message.Vector3(x=37.54, y=0, z=7.49),
        #                    message.Vector3(x=7.79, y=0, z=1.60),
        #                    smooth=True)
        path = m._find_path(message.Vector3(x=19, y=0, z=8),
                           message.Vector3(x=34, y=0, z=16.4),
                           smooth=True)
        print path
        result = {}
        result['Waypoints'] = []
        for p in path:
            result['Waypoints'].append(
            {
                'Index': p[0]
            })

        with open(r'..\Shooter\find_path_result', 'w') as f:
            import json
            json.dump(result, f)


if __name__ == '__main__':
    unittest.main()
