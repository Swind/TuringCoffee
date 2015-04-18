import os
import sys
sys.path.insert(0, '../src')

import unittest

from cookbook import Cookbook


class TestCookbook(unittest.TestCase):

    def test_cookbook(self):
        with open('test.md', 'r') as f:
            cookbook = Cookbook('test', f.read())

        steps = cookbook.steps
        print 'Description {}'.format(cookbook.description)

        for step in steps:
            for process in step.processes:
                for block in process.blocks:
                    block.points()

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestCookbook('test_cookbook'))
    unittest.TextTestRunner().run(suite)
