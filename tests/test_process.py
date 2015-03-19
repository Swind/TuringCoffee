import os
import sys
sys.path.insert(0, "../src")

import unittest

from process.circle import Circle
from process.spiral import Spiral
from process.fixed_point import FixedPoint

import matplotlib.pyplot as plt
from matplotlib import animation


class TestProcess(unittest.TestCase):

    def test_circle(self):
        test_data = {
            "Radius": "1 cm",
            "High": "80 mm to 90 mm",
            "Total Water": "40 ml",
            "Point interval": "0.01 mm",
            "Extrudate": "0.1 ml/mm",
            "Feedrate": "1 mm/min",
        }

        circle = Circle(test_data)

        self.assertEqual(circle.radius, 10, "The radius should be {} mm ({} cm) but {}".format(1 * 10, 1, circle.radius))
        self.assertEqual(circle.high, (80, 90), "The high should be {} mm to {} mm but {} mm to {} mm".format(80, 90, circle.high[0], circle.high[1]))
        self.assertEqual(circle.total_water, 40, "The total water should be {} ml but {} ml".format(40, circle.total_water))
        self.assertEqual(circle.feedrate, 1, "The feedrate should be 1 mm/min but {} mm/min".format(1, circle.feedrate))
        self.assertEqual(circle.point_interval, 0.01, "The point interval should be {} mm but {}".format(0.01, circle.point_interval))
        self.assertEqual(circle.extrudate, 0.1, "The extrudate should be {} ml/mm but {}".format(0.1, circle.extrudate))

        points = circle.points()


    def test_spiral(self):
        test_data = {
            "Radius": "1 cm to 2 cm",
            "High": "80 mm to 90 mm",
            "Cylinder": "5",
            "Point interval": "0.01 mm",
            "Extrudate": "0.1 ml/mm",
            "Feedrate": "1 mm/min",
        }

        spiral = Spiral(test_data)

        self.assertEqual(spiral.radius, (10, 20), "The radius should be from {} mm to {} mm but {} mm to {} mm".format(1, 2, spiral.radius[0], spiral.radius[1]))
        self.assertEqual(spiral.high, (80, 90), "The high should be {} mm to {} mm but {} mm to {} mm".format(80, 90, spiral.high[0], spiral.high[1]))
        self.assertEqual(spiral.cylinder, 5, "The cylinder should be {} but {}".format(5, spiral.cylinder))
        self.assertEqual(spiral.feedrate, 1, "The feedrate should be 1 mm/min but {} mm/min".format(1, spiral.feedrate))
        self.assertEqual(spiral.point_interval, 0.01, "The point interval should be {} mm but {}".format(0.01, spiral.point_interval))
        self.assertEqual(spiral.extrudate, 0.1, "The extrudate should be {} ml/mm but {}".format(0.1, spiral.extrudate))

        points = spiral.points()

    def test_fixedpoint(self):
        test_data = {
            "Coordinates": "(0, 0)",
            "High": "80 mm to 90 mm",
            "Total Water": "40 ml",
            "Extrudate": "0.1 ml/step",
            "Feedrate": "80 mm/min",
        }

        fixedpoint = FixedPoint(test_data)
        self.assertEqual(fixedpoint.coordinates, (0, 0), "The coordinates should be {} but {}".format((0, 0), fixedpoint.coordinates))
        self.assertEqual(fixedpoint.high, (80, 90), "The high should be {} mm to {} mm but {} mm to {} mm".format(80, 90, fixedpoint.high[0], fixedpoint.high[1]))
        self.assertEqual(fixedpoint.total_water, 40, "The total water should be {} ml but {} ml".format(40, fixedpoint.total_water))
        self.assertEqual(fixedpoint.feedrate, 80, "The feedrate should be {} mm/min but {} mm/min".format(80, fixedpoint.feedrate))
        self.assertEqual(fixedpoint.extrudate, 0.1, "The extrudate should be {} ml/mm but {}".format(0.1, fixedpoint.extrudate))

        points = fixedpoint.points()


def show_animation(points):
    # first set up the figure, the axis, and the plot element we want to animate
    fig = plt.figure()
    ax = plt.axes(xlim=(-20, 20), ylim=(-20, 20))
    line, = ax.plot([], [], lw=2)

    frame_size = 200
    frame_point_size = len(points) / frame_size
    # initialization function: plot the background of each frame
    def init():
        line.set_data([], [])
        return line,

    # animation function.  this is called sequentially
    def animate(i):
        frame_points = points[: frame_point_size * i]
        x = map(lambda point: point.x, frame_points)
        y = map(lambda point: point.y, frame_points)
        line.set_data(x, y)
        return line,

    # call the animator.  blit=true means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=frame_size, interval=20, blit=True)
    anim.save("test.gif", writer="imagemagick", fps=4)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    #suite.addTest(TestProcess("test_circle"))
    #suite.addTest(TestProcess("test_spiral"))
    suite.addTest(TestProcess("test_fixedpoint"))

    unittest.TextTestRunner().run(suite)
