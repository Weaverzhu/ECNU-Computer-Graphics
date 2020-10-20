from ..common.grid import Grid, Node
from ..common.geometry import Vector2, Point2, Line2

from PyQt5 import QtWidgets
from ..week2.bresenham import bresenham

from typing import List
from collections import defaultdict

from queue import Queue

OPTIONS = [
    Point2(0, 1),
    Point2(0, -1),
    Point2(1, 0),
    Point2(-1, 0)
]

STATUS_DEF = {
    "BORDER": 2,
    "DEFAULT": 0,
    "FILL": 1
}

__dbg = 0


def flood_fill(st: Point2, g, func: callable):
    q = Queue()
    q.put(st)
    func(st[0], st[1])
    while not q.empty():
        u = q.get()
        for o in OPTIONS:
            v = o + u
            status = g.get_node(v[0], v[1]).on
            if status == 0:
                func(v[0], v[1])
                q.put(v)
        # global __dbg
        # __dbg += 1
        # if __dbg == 5:
        #     exit()

    pass


class FloodFillGrid(Grid):
    def __init__(self, fill_func, **params):
        super().__init__(**params)
        self.fill_func = fill_func
        self.p = []
        self.s = []

    def grid_click(self, node):
        self.toggle(node.x, node.y)
        p = [node.x, node.y]
        if len(self.p) > 0:
            last = self.p[-1]
            bresenham(last, p, self.toggle_func(STATUS_DEF["BORDER"]))
        self.p.append([node.x, node.y])
        pass

    def right_click(self, node):
        self.p.clear()
        flood_fill(Point2(node.x, node.y), self,
                   self.toggle_func(STATUS_DEF["FILL"]))
        pass


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    gui = FloodFillGrid(n=30, fill_func=flood_fill)
    gui.show()
    sys.exit(app.exec_())
