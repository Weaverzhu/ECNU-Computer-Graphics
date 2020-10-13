from ..common.grid import Grid, Node
from PyQt5 import QtWidgets
from ..week2.bresenham import bresenham

from typing import List
from collections import defaultdict

INF = 1000000000


def polygon_bound(p: list) -> list:
    buf = []
    res = []

    def set_pixel(x, y):
        buf.append((x, y))

    n = len(p)
    for i in range(0, n):
        a = p[i]
        b = p[(i + 1) % n]
        a = [a.x, a.y]
        b = [b.x, b.y]
        buf = []
        bresenham(a, b, set_pixel)
        for node in buf:
            res.append(node)

    return res


def polygon_fill(p: list, func: callable):
    bounds = polygon_bound(p)
    dat = defaultdict(list)
    miny = INF
    maxy = 0
    for n in bounds:
        dat[n[1]].append(n[0])
        miny = min([miny, n[1]])
        maxy = max([maxy, n[1]])

    print("maxy={}, miny={}".format(maxy, miny))

    for y in range(miny, maxy + 1):
        j = 0
        l = dat[y]
        l.sort()
        siz = len(l)
        print("y={}, siz={}".format(y, siz))
        assert (
            siz % 2 == 0 or siz == 1
        ), "siz should be even, but it is {}, y={}".format(siz, y)
        if siz == 1:
            func(l[0][0], l[0][1])
            continue
        while j < siz:
            for x in range(l[j], l[j + 1] + 1):
                func(x, y)
            j += 2


class PolygonFillGrid(Grid):
    def __init__(self, fill_func, **params):
        super().__init__(**params)

        self.fill_func = fill_func
        self.p = []
        self.s = []

    def grid_click(self, node: Node):
        self.p.append(node)
        self.toggle(node.x, node.y)
        if self.p.count(node) > 1:
            ind = self.p.index(node)
            self.p = self.p[ind:]  # normalize the point array
            self.fill_func(self.p, self.toggle)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    gui = PolygonFillGrid(n=20, fill_func=polygon_fill)
    gui.show()
    sys.exit(app.exec_())