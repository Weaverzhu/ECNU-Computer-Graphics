from grid import Grid
import sys
from PyQt5 import QtWidgets


def dda(p0, p1, func):
    dx = p1[0] - p0[0]
    dy = p1[1] - p0[1]
    offset = int(abs(dx) if abs(dx) > abs(dy) else abs(dy))
    sx = dx / offset
    sy = dy / offset
    x = p0[0]
    y = p0[1]
    timer = QTimer()
    for i in range(offset):
        print(x, y)
        func(round(x), round(y))
        x = x + sx
        y = y + sy


x0, y0, x1, y1 = map(
    int, input("bresenham algorithm: please input p0(x, y) and p1(x, y): \n").split()
)

app = QtWidgets.QApplication(sys.argv)
window = Grid(20)
window.show()
dda([x0, y0], [x1, y1], window.toggle)
sys.exit(app.exec_())
app = QtWidgets.QApplication(sys.argv)