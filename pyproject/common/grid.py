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
    QPushButton,
)

from .color import COLOR

from PyQt5.QtCore import Qt


class Node(QFrame):
    def toggle(self, state):
        self.on = state
        self.update()

    def set_color(self, color):
        self.__color = color
        css = "background-color: {};border: 1px solid black;".format(COLOR[color])
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

    def keyPressEvent(self, event):
        pass

    def __init__(self, size, mainWindow, x, y, call_back, keyboard=None):
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

    def get_cord(self):
        return [self.x, self.y]


PADDING = 50
PANEL = 200


class Grid(QWidget):
    def __init__(self, n, size=500, button_texts=[]):
        super().__init__()
        self.n = n
        self.size = size
        self.setFixedSize(size + PADDING * 2, size + PADDING + PANEL)
        # self.setStyleSheet("background-color: #283747;")

        base = self.init_grid(size, n)
        self.click_queue = []
        self.buttons = []
        self.init_button(button_texts, base)

    def init_grid(self, size, n):
        grid_size = size // n
        self.grid = [
            [
                Node(
                    grid_size,
                    self,
                    j,
                    self.n - 1 - i,
                    self.dispach,
                    self.keyboard_dispach,
                )
                for i in range(n)
            ]
            for j in range(n)
        ]

        for i in range(n):
            for j in range(n):
                node = self.grid[i][j]
                node.move(i * grid_size + PADDING, j * grid_size + PADDING)

        return (n - 1) * grid_size + PADDING

    def init_button(self, button_texts, base):
        n_buttons = len(button_texts)

        if n_buttons == 0:
            return

        num = 0
        for text in button_texts:
            btn = QPushButton(text=text, parent=self)
            self.buttons.append(btn)
            btn.move(PADDING + num * (PADDING + btn.size().width()), base + PADDING)
            num += 1

    def dispach(self, node, event):
        if event.button() == Qt.RightButton:
            self.right_click(node)
        else:
            self.grid_click(node)

    def keyboard_dispach(self, event):
        pass

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

    def set_node(self, x, y, node):
        self.grid[x][self.n - 1 - y] = node

    def toggle(self, x, y, state=1):
        n = self.n
        if x < 0 or x >= n or y < 0 or y >= n:
            return
        self.get_node(x, y).toggle(state)

    def connect_btn_funcs(self, funcs):
        num = 0
        while num < len(self.buttons):
            f = funcs[num]
            if f is not None:
                # print("connect {}".format(f))
                self.buttons[num].clicked.connect(f)
            num += 1

    def dump(self, fileName="save.txt"):
        with open(fileName, "w") as f:
            for i in range(self.n):
                for j in range(self.n):
                    f.write("{} {} {}\n".format(i, j, self.get_node(i, j).on))

    def load(self, fileName="save.txt"):
        fileName = "save.txt"
        with open(fileName, "r") as f:
            for i in range(self.n):
                for j in range(self.n):
                    l = f.readline()
                    x, y, status = map(int, l.split())
                    self.toggle(x, y, status)

    pass


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    gui = Grid(10)
    gui.toggle(5, 5)
    gui.show()
    sys.exit(app.exec_())
