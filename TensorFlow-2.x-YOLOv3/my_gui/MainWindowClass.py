import sys
import cv2
import os
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
        self.videoDevices.currentIndexChanged.connect(self.videoDeviceChanged)
        self.browserPathLineEdit.textChanged.connect(self.imagesPathChanged)
        self.images = None
        self.browserPathLineEdit.setText("")

        # test section
        self.l = QtWidgets.QLabel()
        self.test = QtWidgets.QComboBox()
        self.but = QtWidgets.QPushButton()
        self.but.setEnabled(True)

        # print(self.imageLabel.size[0])
        self.lineedit = QtWidgets.QLineEdit()
        # test section

    def videoDeviceChanged(self):
        if self.videoDevices.currentIndex() == 0:
            self.browserPathButton.setEnabled(True)
            self.browserPathLineEdit.setEnabled(True)
            self.nextButton.setEnabled(True)
            self.backButton.setEnabled(True)

        else:
            self.browserPathButton.setEnabled(False)
            self.browserPathLineEdit.setEnabled(False)
            self.nextButton.setEnabled(False)
            self.backButton.setEnabled(False)

    def getImagesDirectory(self):
        self.browserPathLineEdit.setText(
            QtWidgets.QFileDialog.getExistingDirectory(self, "Выберете папку с изображениями",
                                                       "./", QtWidgets.QFileDialog.Option.ShowDirsOnly))

    def imagesPathChanged(self):
        if self.browserPathLineEdit.text() == "":
            self.images = self.imageGenerator(None)
        else:
            self.images = self.imageGenerator(self.browserPathLineEdit.text())

    def send_image_to_yolo(self):
        try:
            im = self.images.__next__()
            self.lock.acquire()
            # print(self.images.__next__())
            self.to_yolo.put("image")
            self.to_yolo.put(im)
        except StopIteration as si:
            print(str(si))
            self.imagesPathChanged()
            self.send_image_to_yolo()
        except AttributeError as e:
            print(str(e))
            print("Путь не задан")
        except Exception as e:
            print(str(e))
            print("Что то не так!")
        # "C:\\Users\\User\\PycharmProjects\\CNN1\\TensorFlow-2.x-YOLOv3\\IMAGES\\B0015_0001.png"

    def get_image_from_yolo(self):
        image = self.resizeImage(self.from_yolo.get())
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
        # self.lock.acquire(block=True)
        self.to_yolo.put("exit")
        # while True:
        #     ex_ = self.from_yolo.get()
        #     print(ex_ == "exit")
        #     if ex_ == "exit":
        #         break
        #     continue
        QtWidgets.QMainWindow.closeEvent(self, event)

    def imageGenerator(self, path):
        try:
            for image in os.listdir(path):
                if image.__contains__(".png") or image.__contains__(".jpg"):
                    yield os.path.join(path, image)
        except os.error:
            print("os.error")

    def resizeImage(self, image):
        try:
            w_w = self.imageLabel.size().width()
            w_h = self.imageLabel.size().height()
            print(w_w, w_h)
            im_h = image.shape[0]
            im_w = image.shape[1]
            print(im_w, im_h)
            if im_w > w_w:
                k = im_w / w_w
                im_w = w_w
                im_h = round(im_h / k)
            if im_h > w_h:
                k = im_h / w_h
                im_h = w_h
                im_w = round(im_w / k)
            print(im_w, im_h)
            im = cv2.resize(image, (im_w, im_h))
            return im
        except Exception as e:
            print(e)
            return image
