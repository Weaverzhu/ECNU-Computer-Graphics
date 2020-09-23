# 计算机图形学 第二周实践报告

+ 姓名：朱桐
+ 学号：10175102111

## 界面

简单实用 `PyQt5` 搞了一个网格

```py
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
        grid_size = size // n
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

```

## DDA 算法

走 x,y 轴长的那一个，然后分别累次计算 y 值四舍五入

```py
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
```

## Bresenham 算法

由于像素都是浮点数，所以可以用整数比较替换浮点数四舍五入，于是使用 Bresenham 算法

```py
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
```