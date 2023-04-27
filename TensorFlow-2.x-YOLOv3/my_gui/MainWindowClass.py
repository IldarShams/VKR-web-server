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
        self.device = None

        self.currentImage = None
        self.currentImageYolo = None

        try:
            self.videoDevices.addItems(["File System"] + self.graph.get_input_devices())
        except Exception as e:
            self.videoDevices.addItems(["File System"])

        self.nextButton.pressed.connect(lambda: self.nextImage(True))
        self.backButton.pressed.connect(lambda: self.nextImage(False))
        self.emitter.image_available.connect(self.getImageFromYolo)
        self.browserPathButton.pressed.connect(self.getImagesDirectory)
        self.videoDevices.currentIndexChanged.connect(self.videoDeviceChanged)
        self.browserPathLineEdit.textChanged.connect(self.imagesPathChanged)
        self.showBoxesRB.clicked.connect(self.showBB_changed)
        self.images = None
        self.browserPathLineEdit.setText("")

        # test section
        self.rb = QtWidgets.QRadioButton()
        self.l = QtWidgets.QLabel()
        self.test = QtWidgets.QComboBox()
        self.but = QtWidgets.QPushButton()
        self.but.setEnabled(True)

        # print(self.imageLabel.size[0])
        # self.but.pressed.connect()
        self.rb.isChecked()
        # self.test.currentText()
        # self.rb.clicked()
        self.lineedit = QtWidgets.QLineEdit()
    # test section
#Секция ГУИ
    # Изменение способа ввода изображения
    def videoDeviceChanged(self):
        if self.videoDevices.currentIndex() == 0:
            self.browserPathButton.setEnabled(True)
            self.browserPathLineEdit.setEnabled(True)
            self.nextButton.setEnabled(True)
            self.backButton.setEnabled(True)
            # self.device = None

        else:
            self.browserPathButton.setEnabled(False)
            self.browserPathLineEdit.setEnabled(False)
            self.nextButton.setEnabled(False)
            self.backButton.setEnabled(False)
            # self.device = self.graph.get_input_devices().index(self.videoDevices.currentText())
            # cap = cv2.VideoCapture(self.device)
            # if not cap.isOpened():
            #     print("Main: Cannot open camera")
            # self.to_yolo.put("video")
            # print("Main: Отправка cap'a к yolo")
            # self.to_yolo.put(cap)

    # Переход к след изобр в папке, обработка в йоло
    def nextImage(self, direction: bool):
        try:
            use_yolo = self.showBoxesRB.isChecked()
            if use_yolo:
                print("Main: взятие лока")
                if not self.lock.acquire(block=False):
                    print("Main: yolo занята, нет возможности перейти к след. изобр")
                    return
            if direction:
                self.currentImage += 1
            else:
                self.currentImage -= 1
            self.currentImage = self.currentImage % len(self.images)
            self.currentImageYolo = None
            if use_yolo:
                self.sendImageToYolo(self.images[self.currentImage])
            self.putImageToLabel()
        except AttributeError as e:
            print(str(e))
            print("Путь не задан")
        except Exception as e:
            print(str(e))
            print("Что то не так!")
    # "C:\\Users\\User\\PycharmProjects\\CNN1\\TensorFlow-2.x-YOLOv3\\IMAGES\\B0015_0001.png"

    # Изменение пути к папке с изобр
    def getImagesDirectory(self):
        self.browserPathLineEdit.setText(
            QtWidgets.QFileDialog.getExistingDirectory(self, "Выберете папку с изображениями",
                                                       "./", QtWidgets.QFileDialog.Option.ShowDirsOnly))

    # Обновление генератора
    def imagesPathChanged(self):
        self.getImagesFromDir(self.browserPathLineEdit.text())

    #Вывод изображения на окно: форматирование и выбор йоло или сурс
    def putImageToLabel(self):
        if self.currentImageYolo is None or not self.showBoxesRB.isChecked():
            image = self.resizeImage(cv2.imread(self.images[self.currentImage]))
        else:
            image = self.currentImageYolo
        self.showImage(image)

    #Вывод изображения на окно: вывод в лайбл
    def showImage(self, image):
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

    #Закрытие окна
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

    # Показать ограничивающие области радио батон чек
    def showBB_changed(self, show_bb: bool):
        if show_bb:
            if self.currentImageYolo is None:
                print("Main: взятие лока")
                if not self.lock.acquire(block=False):
                    print("Main: yolo занята, нет возможности перейти к след. изобр")
                    return
                self.sendImageToYolo(self.images[self.currentImage])
            else:
                self.putImageToLabel()
        else:
            self.putImageToLabel()


    # Секция ГУИ

    # Секция йоло
    def sendImageToYolo(self, im: str):
        self.to_yolo.put("image")
        print("Main: Отправка изображения к yolo")
        self.to_yolo.put(im)

    def getImageFromYolo(self):
        self.currentImageYolo = self.resizeImage(self.from_yolo.get())
        print("Main: релиз лока")
        self.lock.release()
        self.putImageToLabel()
    # Секция йоло

    # Секция утилиты
    #резайз изобр под корректный вывод в лайбл
    def resizeImage(self, image):
        try:
            w_w = self.imageLabel.size().width()
            w_h = self.imageLabel.size().height()
            # print(w_w, w_h)
            im_h = image.shape[0]
            im_w = image.shape[1]
            # print(im_w, im_h)
            if im_w > w_w:
                k = im_w / w_w
                im_w = w_w
                im_h = round(im_h / k)
            if im_h > w_h:
                k = im_h / w_h
                im_h = w_h
                im_w = round(im_w / k)
            # print(im_w, im_h)
            im = cv2.resize(image, (im_w, im_h))
            return im
        except Exception as e:
            print(e)
            return image

    #Генератор изобр для ввода из папки
    def getImagesFromDir(self, path):
        self.images = []
        if path == "":
            self.currentImage = None
            return
        try:
            for image in os.listdir(path):
                if image.__contains__(".png") or image.__contains__(".jpg"):
                    self.images.append(path + "/" + image)
            if len(self.images) > 0:
                self.currentImage = -1
            else:
                self.currentImage = None
            print(self.images)
            print(self.currentImage)
        except os.error:
            print("os.error")

# Секция утилиты