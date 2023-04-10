import sys
import cv2
from pygrabber.dshow_graph import FilterGraph
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

        self.emitter = emitter
        self.emitter.daemon = True
        self.emitter.start()
        self.to_yolo = queue_to_yolo
        self.from_yolo = queue_from_yolo
        self.lock = lock
        self.graph = FilterGraph()

        self.videoDevices.addItems(["File System"] + self.graph.get_input_devices())

        self.nextButton.pressed.connect(self.send_image_to_yolo)
        self.emitter.image_available.connect(self.get_image_from_yolo)
        self.browserPathButton.pressed.connect(self.getImagesDirectory)

    def getImagesDirectory(self):
        self.browserPathLineEdit.setText(QtWidgets.QFileDialog.getExistingDirectory(self, "Выберете папку с изображениями",
                                                   "./", QtWidgets.QFileDialog.Option.ShowDirsOnly))


    def send_image_to_yolo(self):
        self.lock.acquire()
        im = "C:\\Users\\User\\PycharmProjects\\CNN1\\TensorFlow-2.x-YOLOv3\\IMAGES\\B0015_0001.png"
        self.to_yolo.put("image")
        self.to_yolo.put(im)


    def get_image_from_yolo(self):
        image = self.from_yolo.get()
        qformat = QtGui.QImage.Format.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QtGui.QImage.Format.Format_RGBA8888
            else:
                qformat = QtGui.QImage.Format.Format_RGB888
            img = QtGui.QImage(image.data,
                               image.shape[1],
                               image.shape[0],
                               image.strides[0],  # <--- +++
                               qformat)
            img = img.rgbSwapped()
            self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(img))
            self.imageLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lock.release()

    def closeEvent(self, event):
        self.lock.acquire(block=True)
        self.to_yolo.put("exit")
        while True:
            ex_ = self.from_yolo.get()
            print(ex_ == "exit")
            if ex_ == "exit":
                break
            continue
        QtWidgets.QMainWindow.closeEvent(self, event)
