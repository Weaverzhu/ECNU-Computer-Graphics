from ..common.grid import Grid, Node
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

import math
from queue import Queue

from ..week3.circle import draw_circle
from ..week4.polygon_fill import polygon_fill

import numpy as np

DELTAS = [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def norm(a):
    return math.sqrt(a[0] ** 2 + a[1] ** 2)


class Shape:
    def __init__(self, shape, data):
        self.shape = shape
        self.data = data

    @staticmethod
    def readf(fileName):
        with open(fileName, "r") as f:
            l = f.readline()
            cls = l[:-1]
            dat = dict()
            if cls == "polygon":
                n = int(f.readline())
                dat["n"] = n
                dat["p"] = []
                for i in range(n):
                    p = tuple(map(int, f.readline().split()))
                    dat["p"].append(p)

            elif cls == "circle":
                l1 = f.readline()
                l2 = f.readline()
                # print("l1: {}l2: {}".format(l1, l2))
                bp = tuple(map(int, l1.split()))
                p1 = tuple(map(int, l2.split()))
                dat["bp"] = bp
                dat["p1"] = p1

        return Shape(cls, dat)


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
        def func(x, y):
            if self.check(x, y):
                self.selected.append(self.get_node(x, y))
                self.toggle(x, y, 2)

        print("switch mode {}".format(button_text))
        self.mode = button_text
        if self.mode != "translation":
            s = Shape.readf("info.txt")

            if s.shape == "polygon":
                p = [self.get_node(x, y) for x, y in s.data["p"]]
                for ps in p:
                    func(ps.x, ps.y)
                polygon_fill(p, func)
            elif s.shape == "circle":
                bp = s.data["bp"]
                p1 = s.data["p1"]
                dx = bp[0] - p1[0]
                dy = bp[1] - p1[1]
                r = int(math.sqrt(dx ** 2 + dy ** 2) + 0.5)
                draw_circle(bp[0], bp[1], r, func)
            self.shape = s

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

        s = self.shape
        if s.shape == "polygon":
            ps = s.data["p"]
            newp = []
            for p in ps:
                vec = np.array([[p[0] - bp[0]], [p[1] - bp[1]]])
                # print(vec, A)
                vec = np.matmul(A, vec)
                # print(vec)
                vec = [int(vec[0][0]), int(vec[1][0])]
                vec = (vec[0] + bp[0], vec[1] + bp[1])
                if self.check(vec[0], vec[1]):
                    newp.append(self.get_node(vec[0], vec[1]))

            polygon_fill(newp, self.toggle)
        elif s.shape == "circle":
            bp = s.data["bp"]
            p1 = s.data["p1"]
            dx = bp[0] - p1[0]
            dy = bp[1] - p1[1]
            r = math.sqrt(dx ** 2 + dy ** 2)
            r = int(r + 0.5)
            draw_circle(bp[0], bp[1], r, self.toggle)

    def scale(self):
        s = self.shape
        print("scale")
        bp = self.left_clicked[0].get_cord()
        v1 = self.left_clicked[1].get_cord()
        v2 = self.left_clicked[2].get_cord()

        # print(bp, v1, v2)

        for p in self.selected:
            p.toggle(0)
        self.selected = []

        v1[0] -= bp[0]
        v2[0] -= bp[0]
        v1[1] -= bp[1]
        v2[1] -= bp[1]

        d1 = norm(v1)
        d2 = norm(v2)
        if s.shape == "polygon":
            ps = s.data["p"]
            np = []
            for p in ps:
                vec = [p[0] - bp[0], p[1] - bp[1]]
                vec[0] *= d2 / d1
                vec[1] *= d2 / d1
                vec[0] += bp[0]
                vec[1] += bp[1]
                vec = list(map(int, vec))
                print(vec)
                if self.check(vec[0], vec[1]):
                    np.append(self.get_node(vec[0], vec[1]))
            print(np)
            polygon_fill(np, self.toggle)
        elif s.shape == "circle":

            bp = s.data["bp"]
            p1 = s.data["p1"]
            dx = bp[0] - p1[0]
            dy = bp[1] - p1[1]
            r = math.sqrt(dx ** 2 + dy ** 2) * d2 / d1
            r = int(r + 0.5)
            draw_circle(bp[0], bp[1], r, self.toggle)

    def dispach(self, node, event):
        if event.button() == Qt.RightButton and self.mode == "translation":
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

    app = QtWidgets.QApplication(sys.argv)
    func_text = ["translation", "rotation", "scalation", "load"]
    gui = Trans2DGrid(n=50, button_texts=func_text)
    funcs = []
    for t in func_text:
        if t == "load":
            continue
        funcs.append(gui.set_mode_funcs(t))
    funcs.append(gui.load)
    gui.connect_btn_funcs(funcs)
    gui.show()
    sys.exit(app.exec_())
