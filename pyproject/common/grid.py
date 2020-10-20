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
    QPushButton
)

from .color import COLOR

from PyQt5.QtCore import Qt


class Node(QFrame):
    def toggle(self, state):
        self.on = state
        self.update()

    def set_color(self, color):
        self.__color = color
        css = "background-color: {};border: 1px solid black;".format(
            COLOR[color])
        self.setStyleSheet(css)

    def get_color(self, color):
        return self.__color

    def update(self):
        if self.on == 1:
            self.set_color("ORANGE")
        elif self.on == 0:
            self.set_color("DEFAULT")
        elif self.on == 2:
            self.set_color("RED")

    def mousePressEvent(self, event):
        self.call_back(self, event)
        pass

    def __init__(self, size, mainWindow, x, y, call_back):
        super(Node, self).__init__(mainWindow)
        self.setFixedSize(size, size)
        self.grid = mainWindow
        self.on = 0
        self.update()

        self.x = x
        self.y = y
        self.call_back = call_back

    def __str__(self):
        return "<Node x={}, y={}, state={}>".format(self.x, self.y, self.on)


class Button:
    pass


class Grid(QWidget):
    def __init__(self, n, size=500, buttons=[]):
        super().__init__()
        self.n = n
        self.size = size
        self.setFixedSize(size, size)
        self.setStyleSheet("background-color: #283747;")
        grid_size = size // n
        self.grid = [
            [
                Node(grid_size, self, j, self.n - 1 - i, self.dispach)
                for i in range(n)
            ]
            for j in range(n)
        ]

        for i in range(n):
            for j in range(n):
                node = self.grid[i][j]
                node.move(i * grid_size, j * grid_size)

        self.click_queue = []

    def dispach(self, node, event):
        if event.button() == Qt.RightButton:
            self.right_click(node)
        else:
            self.grid_click(node)

    def right_click(self, node):
        pass

    def grid_click(self, node):
        pass

    def toggle_func(self, state):
        def func(x, y, s=state):
            self.toggle(x, y, state)
        return func

    def get_node(self, x, y):
        return self.grid[x][self.n - 1 - y]

    def toggle(self, x, y, state=1):
        n = self.n
        if x < 0 or x >= n or y < 0 or y >= n:
            return
        self.get_node(x, y).toggle(state)

    pass


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    gui = Grid(10)
    gui.toggle(5, 5)
    gui.show()
    sys.exit(app.exec_())
