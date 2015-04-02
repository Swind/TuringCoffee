import os
import sys
sys.path.insert(0, "../src")

os.chdir("../src")

import unittest

from test_cookbook_manager_data import data
from cookbook_manager import CookbookManager

class TestCookbookManager(unittest.TestCase):

    def test_cookbook_CRUD(self):
        name = "test_cookbook"
        manager = CookbookManager()
        manager.update(name, data)

        cookbook = manager.get(name)
        self.assertEqual(cookbook.content, data)

        manager.delete(name)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestCookbookManager("test_cookbook_CRUD"))
    unittest.TextTestRunner().run(suite)
