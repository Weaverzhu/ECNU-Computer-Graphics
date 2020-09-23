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


x0, y0, x1, y1 = map(
    int, input("dda algorithm: please input p0(x, y) and p1(x, y): \n").split()
)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
dda([x0, y0], [x1, y1], window.g.toggle)
# sys.exit(app.exec_())
app.exec_()
