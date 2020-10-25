from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDesktopWidget, QStyleFactory, QWidget,
                             QGridLayout, QHeaderView, QTableWidgetItem, QMessageBox, QFileDialog,
                             QSlider, QLabel, QLineEdit, QPushButton, QTableWidget, QHBoxLayout, QVBoxLayout, QFrame)
from PyQt5.QtGui import QPalette, QColor, QBrush
from PyQt5.QtCore import Qt
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg
import numpy as np
import pyqtgraph.exporters as pe
import qdarkstyle
import requests
import sys
import time
import random
import json
import datetime
import re

COLOR = {
    "red": "#ff0000",
    "green": "#00ff00",
    "blue": "#0000ff",
    "white": "#000000",
    "black": "#ffffff"
}


class ColorBlock(QFrame):
    def __init__(self, color, size, parent, **params):
        super().__init__(parent, **params)

        self.setStyleSheet("background-color: {}".format(COLOR[color]))

        self.setFixedSize(size[0], size[1])


class TestWindow(QWidget):

    def __init__(self, **params):
        super().__init__(**params)
        self.setFixedSize(800, 800)

        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch(1)
        c1 = ColorBlock("green", (100, 100), self)
        self.button_layout.addWidget(c1)

        c2 = ColorBlock("red", (100, 100), self)
        self.button_layout.addWidget(c2)

        c3 = ColorBlock("white", (100, 100), self)
        self.button_layout.addWidget(c3)

        self.vbox = QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addWidget(ColorBlock("blue", (400, 400), self))

        self.vbox.addStretch(1)
        self.vbox.addLayout(self.button_layout)

        # self.setLayout(self.button_layout)
        self.setLayout(self.vbox)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TestWindow()
    app.exit(app.exec_())
