from ..common.grid import Grid, Node
from ..week4.polygon_fill import polygon_fill
from ..week2.bresenham import bresenham
from PyQt5.QtCore import Qt

from ..common.geometry import Point2, Line2
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QApplication,
    QStackedWidget,
    QVBoxLayout,
    QGridLayout,
    QFrame,
    QPushButton,
)

def middle(x, l, r):
    return x >= l and x <= r

def in_border(p, border):
    return middle(p[0], border[0][0], border[1][0]) and middle(p[1], border[0][1], border[1][1])


class PolyClipGrid(Grid):
    def __init__(self, border, **params):
        super().__init__(**params)
        p0 = border[0]
        p1 = border[1]
        self.border = border

        def fill(x, y):
            self.toggle(x, y, 2)

        bresenham([p0[0], p0[1]], [p1[0], p0[1]], fill)
        bresenham([p0[0], p0[1]], [p0[0], p1[1]], fill)
        bresenham([p0[0], p1[1]], [p1[0], p1[1]], fill)
        bresenham([p1[0], p0[1]], [p1[0], p1[1]], fill)

        self.p = []

    def dispach(self, node, event):

        def func(x, y):
            if in_border([x, y], self.border):
                self.toggle(x, y)
            else:
                self.toggle(x, y, 0)
        
        if event.button() == Qt.LeftButton:
            p = (node.x, node.y)
            self.toggle(p[0], p[1])
            if len(self.p) > 0 and p == self.p[0]:
                polygon_fill([self.get_node(p[0], p[1]) for p in self.p], func)
                self.p = []
            else:
                self.p.append(p)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    gui = PolyClipGrid(n=50, border=[(5, 5), (45, 25)])
    gui.show()
    sys.exit(app.exec_())