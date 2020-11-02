from ..common.grid import Grid, Node
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

import math
from queue import Queue

import numpy as np

DELTAS = [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def norm(a):
    return math.sqrt(a[0] ** 2 + a[1] ** 2)


class Trans2DGrid(Grid):
    def __init__(self, **params):
        self.selected = []
        self.mode = "translation"
        super().__init__(**params)
        self.left_clicked = []

    def clear(self, clear_status=1):
        print("clear")
        for n in self.selected:
            n.toggle(clear_status)
        self.selected = []
        self.left_clicked = []

    def check(self, tx, ty):
        return tx >= 0 and tx < self.n and ty >= 0 and ty < self.n

    def select(self, node):
        print("select", node.x, node.y)
        q = Queue()
        q.put(node)
        self.selected.append(node)
        node.set_color("RED")
        while not q.empty():
            u = q.get()
            for d in DELTAS:
                v = (u.x + d[0], u.y + d[1])

                if self.check(v[0], v[1]) and self.get_node(v[0], v[1]).on == 1:
                    self.get_node(v[0], v[1]).toggle(2)
                    q.put(self.get_node(v[0], v[1]))
                    self.selected.append(self.get_node(v[0], v[1]))

        pass

    def switch_mode(self, button_text):
        print("switch mode {}".format(button_text))
        self.mode = button_text

    def get_selected_cords(self):
        ps = []
        for n in self.selected:
            ps.append((n.x, n.y))
            n.toggle(0)
        self.selected = []
        return ps

    def translate(self, vec):
        ps = self.get_selected_cords()
        for p in ps:
            x = p
            y = (x[0] + vec[0], x[1] + vec[1])
            if self.check(y[0], y[1]):
                self.get_node(y[0], y[1]).toggle(1)

        pass

    def rotate(self):
        print("rotate")
        bp = self.left_clicked[0].get_cord()
        ps = self.get_selected_cords()

        v1 = self.left_clicked[1].get_cord()
        v2 = self.left_clicked[2].get_cord()

        # print(bp, v1, v2)

        v1[0] -= bp[0]
        v2[0] -= bp[0]
        v1[1] -= bp[1]
        v2[1] -= bp[1]
        # print(bp, v1, v2)

        theta = math.acos(dot(v1, v2) / norm(v1) / norm(v2))

        c = math.cos(theta)
        s = math.sin(theta)

        print(theta * 180 / math.pi)

        A = np.array([[c, -s], [s, c]])

        for p in ps:
            vec = np.array([[p[0] - bp[0]], [p[1] - bp[1]]])
            # print(vec, A)
            vec = np.matmul(A, vec)
            # print(vec)
            vec = [int(vec[0][0]), int(vec[1][0])]
            vec = (vec[0] + bp[0], vec[1] + bp[1])
            if self.check(vec[0], vec[1]):
                self.get_node(vec[0], vec[1]).toggle(1)

    def scale(self):
        print("scale")
        bp = self.left_clicked[0].get_cord()
        ps = self.get_selected_cords()

        v1 = self.left_clicked[1].get_cord()
        v2 = self.left_clicked[2].get_cord()

        # print(bp, v1, v2)

        v1[0] -= bp[0]
        v2[0] -= bp[0]
        v1[1] -= bp[1]
        v2[1] -= bp[1]

        d1 = norm(v1)
        d2 = norm(v2)

        for p in ps:
            vec = [p[0] - bp[0], p[1] - bp[1]]
            vec[0] *= d2 / d1
            vec[1] *= d2 / d1
            vec[0] += bp[0]
            vec[1] += bp[1]
            vec = list(map(int, vec))
            if self.check(vec[0], vec[1]):
                self.toggle(vec[0], vec[1], 1)
        pass

    def dispach(self, node, event):
        if event.button() == Qt.RightButton:
            print("right")
            if node.on == 0:
                self.clear()
            else:
                self.select(node)
        elif event.button() == Qt.LeftButton and len(self.selected) > 0:
            if self.mode == "translation":
                if len(self.left_clicked) < 1:
                    self.left_clicked.append(node)
                else:
                    self.left_clicked.append(node)
                    n0 = self.left_clicked[0]
                    n1 = self.left_clicked[1]
                    vec = (n1.x - n0.x, n1.y - n0.y)
                    self.translate(vec)
                    self.clear()
            elif self.mode == "rotation":
                if len(self.left_clicked) < 2:
                    self.left_clicked.append(node)
                else:
                    self.left_clicked.append(node)
                    self.rotate()
                    self.clear()
            elif self.mode == "scalation":
                if len(self.left_clicked) < 2:
                    self.left_clicked.append(node)
                else:
                    self.left_clicked.append(node)
                    self.scale()
                    self.clear()

    def set_mode_funcs(self, button_text):
        def func():
            self.switch_mode(button_text)

        return func


if __name__ == "__main__":
    import sys

    print("fuck")
    app = QtWidgets.QApplication(sys.argv)
    func_text = ["translation", "rotation", "scalation", "load"]
    gui = Trans2DGrid(n=30, button_texts=func_text)
    funcs = []
    for t in func_text:
        if t == "load":
            continue
        funcs.append(gui.set_mode_funcs(t))
    funcs.append(gui.load)
    gui.connect_btn_funcs(funcs)
    gui.show()
    sys.exit(app.exec_())
