import os
import sys
sys.path.insert(0, "../src")

import api_server
from test_cookbook_manager_data import data as test_data

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
        #payload = {
        #    "name": "new_test_cookbook_manager"
        #}
        #self.app.put("/cookbooks/test_cookbook_manager", data=json.dumps(payload))

        # Cook
        payload = {
            "Command": "Start",
            "Cookbook Name": "test_cookbook_manager"
        }
        self.app.put("/printer", data=json.dumps(payload))

        # Delete the cookbook
        self.app.delete("/cookbooks/new_test_cookbook_manager")

    def tearDown(self):
        pass

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestAPIServer("test_cookbook_manager"))

    unittest.TextTestRunner().run(suite)
