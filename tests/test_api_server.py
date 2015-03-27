import os
import sys
sys.path.insert(0, "../src")

import api_server

import unittest

class TestAPIServer(unittest.TestCase):
    def setUp(self):
        api_server.app.debug = True
        self.app = api_server.app.test_client()

    def test_cookbook_manager(self):
        # Create a cookbook
        self.app.put("/cookbooks/test_cookbook_manager")
        # List all cookbooks
        resp = self.app.get("/cookbooks")
        print resp

    def tearDown(self):
        pass

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestAPIServer("test_cookbook_manager"))

    unittest.TextTestRunner().run(suite)
