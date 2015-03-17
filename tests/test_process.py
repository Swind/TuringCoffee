import os
import sys
sys.path.insert(0, "../src")

import unittest

from process.circle import Circle

class TestProcess(unittest.TestCase):
    def test_circle(self):
        test_data = {
            "Radius": "1 cm",
            "High": "80 mm to 90 mm",
            "Total Water": "40 ml",
            "Point interval": "0.01 mm",
            "Extrudate": "1 ml/mm",
            "Feedrate": "1 mm/min",
        }

        circle = Circle(test_data) 

        self.assertEqual(circle.radius, 10, "The radius should be {} mm ({} cm) but {}".format(1 * 10, 1, circle.radius))
        self.assertEqual(circle.high, (80, 90), "The high should be {} mm to {} mm but {} mm to {} mm".format(80, 90, circle.high[0], circle.high[1]))
        self.assertEqual(circle.total_water, 40, "The total water should be {} ml but {} ml".format(40, circle.total_water))
        self.assertEqual(circle.feedrate, 1, "The feedrate should be 1 mm/min but {} mm/min".format(1, circle.feedrate))
        self.assertEqual(circle.point_interval, 0.01, "The point interval should be {} mm but {}".format(0.01, circle.point_interval))
        self.assertEqual(circle.extrudate, 1, "The extrudate should be {} ml/mm but {}".format(1, circle.extrudate))

        points = circle.points()

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestProcess("test_circle"))

    unittest.TextTestRunner().run(suite)
