import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QApplication,
    QStackedWidget,
    QVBoxLayout,
    QGridLayout,
    QFrame,
)

from PyQt5.QtCore import Qt


class Node(QFrame):
    def toggle(self, state=None):
        if state is None:
            self.on = not self.on
        else:
            self.on = state
        self.update()

    def update(self):
        if self.on:
            self.setStyleSheet("background-color: #935115;border: 1px solid black;")
        else:
            self.setStyleSheet("background-color: #283747;border: 1px solid black;")

    def mousePressEvent(self, event):
        self.call_back(self)
        pass

    def __init__(self, size, mainWindow, x, y, call_back):
        super(Node, self).__init__(mainWindow)
        self.setFixedSize(size, size)
        self.grid = mainWindow
        self.on = False
        self.update()

        self.x = x
        self.y = y
        self.call_back = call_back

    def __str__(self):
        return "<Node x={}, y={}>".format(self.x, self.y)


class Grid(QWidget):
    def __init__(self, n, size=500):
        super().__init__()
        self.n = n
        self.size = size
        self.setFixedSize(size, size)
        self.setStyleSheet("background-color: #283747;")
        grid_size = size // n
        self.grid = [
            [
                Node(grid_size, self, j, self.n - 1 - i, self.grid_click)
                for i in range(n)
            ]
            for j in range(n)
        ]

        for i in range(n):
            for j in range(n):
                node = self.grid[i][j]
                node.move(i * grid_size, j * grid_size)

        self.click_queue = []

    def grid_click(self, node):
        pass

    def toggle(self, x, y, state=True):
        n = self.n
        if x < 0 or x >= n or y < 0 or y >= n:
            return
        self.grid[x][self.n - 1 - y].toggle(state)


    pass


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    gui = Grid(10)
    gui.toggle(5, 5)
    gui.show()
    sys.exit(app.exec_())
