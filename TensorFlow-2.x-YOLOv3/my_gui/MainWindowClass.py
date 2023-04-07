import sys
from multiprocessing import Queue, Lock
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import Qt

from my_gui.Emitter import *


qt_creator_file = "./my_gui/test.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, queue_to_yolo: Queue, queue_from_yolo: Queue, emitter: Emitter, lock: Lock):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)






