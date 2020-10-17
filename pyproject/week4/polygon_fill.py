from ..common.grid import Grid, Node
from ..common.geometry import Vector2, Point2, Line2
from PyQt5 import QtWidgets
from ..week2.bresenham import bresenham

from typing import List
from collections import defaultdict

INF = 1000000000



def polygon_fill(p: List[Node], func: callable):
    lines = []
    n = len(p)
    point_map = defaultdict(list)
    point_by_y = defaultdict(list)

    for i in range(n):
        a = p[i]
        ta = (a.x, a.y)
        point_by_y[a.y].append(a.x)
        b = p[(i+1)%n]
        tb = (b.x, b.y)

        point_map[ta].append(tb)
        point_map[tb].append(ta)

        a = Point2(a.x, a.y)
        b = Point2(b.x, b.y)
        lines.append(Line2(a, b))

    lines.sort(key=lambda l: l.y_bound())

    events = []
    for i in range(lines):
        l = lines[i]
        yb = l.y_bound()
        events.append((yb[0], -i-1))
        events.append((yb[1], i))
        
    events.sort()

    miny = events[0][0]
    maxy = events[-1][0]
    
    lines_set = set()
    ecnt = 0

    for y in range(miny, maxy+1):
        # endpoint in p
        while ecnt < len(events) and events[ecnt][0] <= y:
            e = events[ecnt]
            ecnt += 1
            if e[1] < 0:
                idx = -e[1] - 1
                lines_set.remove(lines[idx])
            else:
                idx = e[1]
                lines_set.add(lines[idx])
        
        cross = []
        for x in point_by_y[y]:
            ano = point_map[(x, y)]
            assert len(ano) == 2, "should be another 2 points, x={}, y={}".format(x, y)
            
            if (ano[0][1] >= y) != (ano[1][1] >= y):
                w = 2
            else:
                w = 1
            
            cross.append((x, w))

        for l in lines_set:
            indicator, x = l.get_x(y)
            assert indicator != -1, "shouldn't be not having cross point, y={}".format(y)

            if indicator == 1:
                cross.append((int(x + 0.5), 1))

        cross.sort()

        cur = 0
        cross.append((INF, 0))
        n = len(cross)
        for i in range(n-1):
            x1 = cross[i][0]
            w = cross[i][1]
            x2 = cross[i+1][0]
            cur += w
            if cur % 2 == 1:
                for x in range(x1, x2+1):
                    func(x, y)
        
        

class PolygonFillGrid(Grid):
    def __init__(self, fill_func, **params):
        super().__init__(**params)

        self.fill_func = fill_func
        self.p = []
        self.s = []

    def grid_click(self, node: Node):
        self.p.append(node)
        self.toggle(node.x, node.y)

        buf = []
        def set_pixel_with_check(x: int, y: int):
            buf.append((x, y))

        if len(self.p) > 1:
            a = self.p[-1]
            b = self.p[-2]
            self.toggle(a.x, a.y, 0)
            self.toggle(b.x, b.y, 0)
            buf = []
            bresenham([a.x, a.y], [b.x, b.y], set_pixel_with_check)
            buf = set(buf)
            for p in buf:
                self.toggle(p[0], p[1], 1)

            
        if self.p.count(node) > 1:
            
            print("polygon")
            self.fill_func(self.p, self.toggle)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    gui = PolygonFillGrid(n=20, fill_func=polygon_fill)
    gui.show()
    sys.exit(app.exec_())