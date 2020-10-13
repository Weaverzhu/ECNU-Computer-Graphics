from ..common.grid import Grid, Node
from PyQt5 import QtWidgets


def bresenham(p0, p1, func):
    fi = 0
    se = 1
    d = [abs(p0[fi] - p1[fi]), abs(p0[se] - p1[se])]
    if d[fi] < d[se]:
        fi, se = se, fi
    if p0[fi] > p1[fi]:
        p0, p1 = p1, p0
    func(p0[0], p0[1])

    dt = 1 if p0[se] < p1[se] else -1

    p = 2 * d[se] - d[fi]
    while p0[fi] < p1[fi]:
        if p > 0:
            p = p - 2 * d[fi]
            p0[se] = p0[se] + dt

        p0[fi] = p0[fi] + 1
        p = p + 2 * d[se]
        func(p0[0], p0[1])

class BresenhanGrid(Grid):
    def __init__(self, line_func, **params):
        super().__init__(**params)

        self.line_func = line_func
        self.p = None

    def grid_click(self, node: Node):
        if self.p is None:
            self.p = [node.x, node.y]
        else:
            self.line_func(self.p, [node.x, node.y], self.toggle)
            self.p = None

def main():

    import sys

    app = QtWidgets.QApplication(sys.argv)
    gui = BresenhanGrid(n=10, line_func=bresenham)
    gui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()