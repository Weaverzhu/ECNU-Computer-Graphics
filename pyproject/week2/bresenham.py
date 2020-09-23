from grid import Grid

from PyQt5 import QtWidgets
import sys


def bresenham(p0, p1, func):
    fi = 0
    se = 1
    d = [abs(p0[fi] - p1[fi]), abs(p0[se] - p1[se])]
    if d[fi] < d[se]:
        fi, se = se, fi
    if p0[fi] > p1[fi]:
        p0, p1 = p1, p0
    func(p0[0], p0[1])
    p = 2 * d[se] - d[fi]
    while p0[fi] < p1[fi]:
        if p > 0:
            p = p - 2 * d[fi]
            p0[se] = p0[se] + 1

        p0[fi] = p0[fi] + 1
        p = p + 2 * d[se]
        func(p0[0], p0[1])


x0, y0, x1, y1 = map(
    int, input("bresenham algorithm: please input p0(x, y) and p1(x, y): \n").split()
)

app = QtWidgets.QApplication(sys.argv)
window = Grid(20)
window.show()
bresenham([x0, y0], [x1, y1], window.toggle)
sys.exit(app.exec_())
app = QtWidgets.QApplication(sys.argv)