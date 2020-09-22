from PyQt5.QtWidgets import QGridLayout, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets
import sys
from grid import Grid
from settings import FIXED_SIZE

import os, time


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        lay = self.layout()
        self.setFixedSize(FIXED_SIZE, FIXED_SIZE + 100)
        self.g = Grid(20)
        lay.addChildWidget(self.g)


def dda(p0, p1, func):
    dx = abs(p0[0] - p1[0])
    dy = abs(p0[1] - p1[1])
    offset = int(dx if dx > dy else dy)
    sx = dx / offset
    sy = dy / offset
    x = p0[0]
    y = p0[1]
    timer = QTimer()
    for i in range(offset):
        func(round(x), round(y))
        x = x + sx
        y = y + sy


def bresenham(p0, p1, func):
    fi = 0
    se = 1
    d = [abs(p0[fi] - p1[fi]), abs(p0[se] - p1[se])]
    if d[fi] < d[se]:
        fi, se = se, fi

    x = p0[fi]
    y = p0[se]
    func(x, y)
    p = 2 * d[se] - d[fi]
    while x < p1[fi]:
        if p > 0:
            p = p - 2 * d[fi]
            y = y + 1

        x = x + 1
        p = p + 2 * d[se]
        func(x, y)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
bresenham([1, 0], [5, 9], window.g.toggle)
sys.exit(app.exec_())
app = QtWidgets.QApplication(sys.argv)