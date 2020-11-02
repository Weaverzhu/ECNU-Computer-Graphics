from ..common.grid import Grid, Node
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from queue import Queue

DELTAS = [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]


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

    def translate(self, vec):
        ps = []
        for n in self.selected:
            ps.append((n.x, n.y))
            n.toggle(0)
        self.selected = []
        for p in ps:
            x = p
            y = (x[0] + vec[0], x[1] + vec[1])
            if self.check(y[0], y[1]):
                self.get_node(y[0], y[1]).toggle(1)

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

    def set_mode_funcs(self, button_text):
        def func():
            self.switch_mode(button_text)

        return func


if __name__ == "__main__":
    import sys

    print("fuck")
    app = QtWidgets.QApplication(sys.argv)
    func_text = ["translation", "rotaltion", "scalation", "load"]
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
