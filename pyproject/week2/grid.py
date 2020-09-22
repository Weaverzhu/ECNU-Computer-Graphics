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
from settings import FIXED_SIZE


class Node(QFrame):
    def toggle(self):
        self.on = not self.on
        self.update()

    def update(self):
        if self.on:
            self.setStyleSheet("background-color: #935115;border: 1px solid black;")
        else:
            self.setStyleSheet("background-color: #283747;border: 1px solid black;")

    def __init__(self, size, mainWindow):
        super(Node, self).__init__(mainWindow)
        self.setFixedSize(size, size)

        self.on = False
        self.update()


class Grid(QWidget):
    def __init__(self, n, size=FIXED_SIZE):
        super().__init__()
        self.n = n
        self.size = size
        self.setFixedSize(FIXED_SIZE, FIXED_SIZE)
        self.setStyleSheet("background-color: #283747;")
        grid_size = sizes // n
        self.grid = [[Node(grid_size, self) for i in range(n)] for j in range(n)]

        for i in range(n):
            for j in range(n):
                node = self.grid[i][j]
                node.move(i * grid_size, j * grid_size)

    def toggle(self, x, y):
        self.grid[x][y].toggle()

    pass


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    gui = Grid(10)
    gui.toggle(5, 5)
    gui.show()

    sys.exit(app.exec_())
