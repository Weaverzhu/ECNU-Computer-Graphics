from ..common.grid import Grid, Node
from ..week4.polygon_fill import polygon_fill
from ..week2.bresenham import bresenham
from PyQt5.QtCore import Qt

from ..common.geometry import Point2, Line2


def middle(l, r, x):
    return x >= l and x <= r

def in_border(p, border):
    return middle(p[0], border[0][0], border[1][0]) and middle(p[1], border[0][1], border[1][1])

def cross(border, q0, q1):
    p0 = border[0]
    p1 = border[1]
    q0 = Point2(q0[0], q0[1])
    q1 = Point2(q1[0], q1[1])
    q = Line2(q0, q1)

    res = []

    # left
    indicator, res = q.get_y(p0[0])
    if indicator == 0:
        return 0, None
    elif indicator == 1:
        res.append((1, (p0[0], round(res))))

    # bottom
    indicator, res = q.get_x(p0[1])
    if indicator == 0:
        return 0, None
    elif indicator == 1:
        res.append((1, (round(res), p0[1])))

    # right
    indicator, res = q.get_y(p1[0])
    if indicator == 0:
        return 0, None
    elif indicator == 1:
        res.append((1, (p1[0], round(res))))

    # up
    indicator, res = q.get_x(p1[1])
    if indicator == 0:
        return 0, None
    elif indicator == 1:
        res.append((1, (round(res), p1[1])))

    return 1, res


def polygon_clip(p, border, func):
    n = len(p)
    for i in range(n):
        p0 = p[i]
        p1 = p[(i + 1) % n]
        indi, res = cross(border, p0, p1)

    pass


class PolyClipGrid(Grid):
    def __init__(self, border, **params):
        super().__init__(**params)
        p0 = border[0]
        p1 = border[1]
        self.border = border

        def fill(x, y):
            self.toggle(x, y, 2)

        bresenham(p0, (p1[0], p0[1]), fill)
        bresenham(p0, (p0[0], p1[1]), fill)
        bresenham((p0[0], p1[1]), p1, fill)
        bresenham((p1[0], p0[1]), p1, fill)

        self.p = []

    def dispach(self, node, event):
        p = (node.x, node.y)
        if event == Qt.LeftButton:
            if p == self.p[0]:
                polygon_clip(p, self.border, self.toggle)
            pass