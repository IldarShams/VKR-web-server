from PyQt6.QtWidgets import *

from my_gui.MessageWindowClass import *
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import QSize, Qt
from random import choice


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)


class MessageWindow(QMainWindow):

    def __init__(self):
        super(MessageWindow, self).__init__()

        self.setWindowTitle("My App")
        self.label = QLabel()
        self.setCentralWidget(self.label)

