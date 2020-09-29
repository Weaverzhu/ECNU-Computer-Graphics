from ..common.grid import Grid, Node
from math import sqrt


def draw_circle(xc, yc, r, set_pixel):
    def plot_points(pt):
        for si in [-1, 1]:
            for sj in [-1, 1]:
                set_pixel(xc + si * pt[0], yc + sj * pt[1])
                set_pixel(xc + si * pt[1], yc + sj * pt[0])

    p = 1 - r
    pt = [0, r]
    plot_points(pt)
    while pt[0] < pt[1]:
        pt[0] += 1
        if p < 0:
            p += 2 * pt[0] + 1
        else:
            pt[1] -= 1
            p += 2 * (pt[0] - pt[1]) + 1
        plot_points(pt)


class CircleGrid(Grid):
    def __init__(self, circle_func, **params):
        super().__init__(**params)
        self.circle_func = circle_func
        self.p = None

    def grid_click(self, node):
        if self.p is None:
            self.p = [node.x, node.y]
        else:
            dx = self.p[0] - node.x
            dy = self.p[1] - node.y
            r = int(sqrt(dx ** 2 + dy ** 2) + 0.5)
            draw_circle(self.p[0], self.p[1], r, self.toggle)
            self.p = None


import sys
from PyQt5 import QtWidgets

app = QtWidgets.QApplication(sys.argv)
gui = CircleGrid(n=50, circle_func=draw_circle)
gui.show()
sys.exit(app.exec_())