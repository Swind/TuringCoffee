import os
import sys
sys.path.insert(0, '../src')

os.chdir('../src')

import time
import api_server

from data import test_cookbook_manager_data
from data import test_circle_data
from data import test_fixed_point_data
from data import test_spiral_data
from data import test_refill_data
from data import test_heat_data
from data import test_wait_data
from data import test_move_data

import unittest
import json


class TestAPIServer(unittest.TestCase):

    def setUp(self):
        api_server.app.debug = True
        self.app = api_server.app.test_client()

    def test_cookbook_manager(self):
        test_data = test_cookbook_manager_data.data

        # Create a new cookbook
        self.app.put('/cookbooks/test_cookbook_manager')

        # List all cookbooks
        resp = self.app.get('/cookbooks')

        # Update the cookbook content
        self.app.put(
            '/cookbooks/test_cookbook_manager/content', data=test_data)

        # Rename the cookbook
        payload = {
            'name': 'new_test_cookbook_manager'
        }
        self.app.put(
            '/cookbooks/test_cookbook_manager', data=json.dumps(payload))

        # Delete the cookbook
        self.app.delete('/cookbooks/new_test_cookbook_manager')

    def test_brew_circle(self):
        self.__test_brew(test_circle_data.data)

    def test_brew_fixed_point(self):
        self.__test_brew(test_fixed_point_data.data)

    def test_brew_spiral(self):
        self.__test_brew(test_spiral_data.data)

    def test_brew_refill(self):
        self.__test_brew(test_refill_data.data)

    def test_brew_heat(self):
        self.__test_brew(test_heat_data.data)

    def test_brew_wait(self):
        self.__test_brew(test_wait_data.data)

    def test_brew_move(self):
        self.__test_brew(test_move_data.data)

    def __test_brew(self, test_data):
        # Create a new cookbook
        self.app.put('/cookbooks/test_cookbook_manager')

        # Update the cookbook content
        self.app.put(
            '/cookbooks/test_cookbook_manager/content', data=test_data)

        # Brew
        payload = {
            'Command': 'Start',
            'Name': 'test_cookbook_manager'
        }
        self.app.put('/barista', data=json.dumps(payload))

        # Wait the state change to start
        time.sleep(1)

        # Wait
        while True:
            resp = json.loads(self.app.get('/barista').data)
            state = resp['State']
            now_name = resp['Now cookbook name']

            if state == 'Idle':
                break

            time.sleep(0.1)

        # Delete the cookbook
        self.app.delete('/cookbooks/test_cookbook_manager')

    def test_read_points(self):
        # Create a new cookbook
        self.app.put('/cookbooks/test_cookbook_manager')

        # Update the cookbook content
        self.app.put(
            '/cookbooks/test_cookbook_manager/content', data=test_spiral_data.data)

        self.app.get('/cookbooks/test_cookbook_manager/points')

        time.sleep(1)


    def tearDown(self):
        pass

if __name__ == '__main__':
    suite = unittest.TestSuite()

   # suite.addTest(TestAPIServer('test_brew_circle'))
   # suite.addTest(TestAPIServer('test_brew_spiral'))
   # suite.addTest(TestAPIServer('test_brew_fixed_point'))
   # suite.addTest(TestAPIServer('test_brew_refill'))
   # suite.addTest(TestAPIServer('test_brew_heat'))
   # suite.addTest(TestAPIServer('test_brew_wait'))
   # suite.addTest(TestAPIServer('test_brew_move'))
    suite.addTest(TestAPIServer('test_read_points')) 

    unittest.TextTestRunner().run(suite)
