from ..common.grid import Grid, Node
from ..week2.bresenham import bresenham
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

from PyQt5.QtCore import Qt


def liang_barsk(winMin, winMax, p1, p2, func):
    u1 = 0
    u2 = 1
    dx = p2[0] - p1[0]
    dy = 0

    def clip_test(p, q, u1, u2):
        res = True
        r = 0
        if p < 0:
            r = q / p
            if r > u2:
                res = False
            elif r > u1:
                u1 = r
        else:
            if p > 0:
                r = q / p
                if r < u1:
                    res = False
                elif r < u2:
                    u2 = r
        return res, u1, u2

    res, u1, u2 = clip_test(-dx, p1[0] - winMin[0], u1, u2)
    if res:
        res, u1, u2 = clip_test(dx, winMax[0] - p1[0], u1, u2)
        if res:
            dy = p2[1] - p1[1]
            res, u1, u2 = clip_test(-dy, p1[1] - winMin[1], u1, u2)
            if res:
                res, u1, u2 = clip_test(dy, winMax[1] - p1[1], u1, u2)
                if res:
                    if u2 < 1:
                        p2 = (p1[0] + u2 * dx, p1[1] + u2 * dy)
                    if u1 > 0:
                        p1 = (p1[0] + u1 * dx, p1[1] + u1 * dy)
                    bresenham(
                        [round(p1[0]), round(p1[1])], [round(p2[0]), round(p2[1])], func
                    )


class LiangGrid(Grid):
    def __init__(self, rec, **params):
        super().__init__(**params)

        assert len(rec) == 2
        self.rec = rec

        def func(x, y):
            self.toggle(x, y, state=2)

        p0 = rec[0]
        p1 = rec[1]
        bresenham(list(p0), [p1[0], p0[1]], func)
        bresenham(list(p0), [p0[0], p1[1]], func)
        bresenham([p0[0], p1[1]], list(p1), func)
        bresenham([p1[0], p0[1]], list(p1), func)

        self.p = None

    def dispach(self, node, event):
        if event.button() == Qt.LeftButton:
            if self.p is None:
                self.p = (node.x, node.y)
            else:
                liang_barsk(
                    self.rec[0], self.rec[1], self.p, (node.x, node.y), self.toggle
                )
                self.p = None


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    gui = LiangGrid(n=50, rec=[(5, 5), (45, 25)])
    gui.show()
    sys.exit(app.exec_())
