import os
import sys
sys.path.insert(0, "../src")

os.chdir("../src")

import time
import api_server
#from test_cookbook_manager_data import data as test_data
from test_circle_data import data as test_data
#from test_fixed_point_data import data as test_data
#from test_spiral_data import data as test_data

import unittest
import json

class TestAPIServer(unittest.TestCase):
    def setUp(self):
        api_server.app.debug = True
        self.app = api_server.app.test_client()

    def test_cookbook_manager(self):
        # Create a new cookbook
        self.app.put("/cookbooks/test_cookbook_manager")

        # List all cookbooks
        resp = self.app.get("/cookbooks")

        # Update the cookbook content
        self.app.put("/cookbooks/test_cookbook_manager/content", data=test_data)

        # Rename the cookbook
        payload = {
            "name": "new_test_cookbook_manager"
        }
        self.app.put("/cookbooks/test_cookbook_manager", data=json.dumps(payload))

        # Delete the cookbook
        self.app.delete("/cookbooks/new_test_cookbook_manager")

    def test_brew(self):
        # Create a new cookbook
        self.app.put("/cookbooks/test_cookbook_manager")

        # Update the cookbook content
        self.app.put("/cookbooks/test_cookbook_manager/content", data=test_data)

        # Brew
        payload = {
            "Command": "Start",
            "Name": "test_cookbook_manager"
        }
        self.app.put("/barista", data=json.dumps(payload))

        # Wait
        while True:
            resp = json.loads(self.app.get("/barista").data)
            state = resp["State"]
            now_name = resp["Now cookbook name"]

            if state == "Idle" and now_name == "test_cookbook_manager":
                break

            time.sleep(0.1)

        # Delete the cookbook
        self.app.delete("/cookbooks/test_cookbook_manager")

    def tearDown(self):
        pass

if __name__ == "__main__":
    suite = unittest.TestSuite()
    #suite.addTest(TestAPIServer("test_cookbook_manager"))
    suite.addTest(TestAPIServer("test_brew"))

    unittest.TextTestRunner().run(suite)
