from ..common.grid import Grid
from PyQt5 import QtWidgets


if __name__ == "__main__":

    import sys

    app = QtWidgets.QApplication(sys.argv)
    gui = Grid(n=10, button_texts=["btn1", "btn2"])
    gui.show()
    sys.exit(app.exec_())