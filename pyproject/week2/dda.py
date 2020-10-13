from ..common.grid import Grid, Node
from PyQt5 import QtWidgets


def dda(p0, p1, func):
    dx = p1[0] - p0[0]
    dy = p1[1] - p0[1]
    offset = int(abs(dx) if abs(dx) > abs(dy) else abs(dy))
    sx = dx / offset
    sy = dy / offset
    x = p0[0]
    y = p0[1]
    for i in range(offset + 1):
        func(round(x), round(y))
        x = x + sx
        y = y + sy


class DDAGrid(Grid):
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


if __name__ == "__main__":

    import sys

    app = QtWidgets.QApplication(sys.argv)
    gui = DDAGrid(n=10, line_func=dda)
    gui.show()
    sys.exit(app.exec_())
