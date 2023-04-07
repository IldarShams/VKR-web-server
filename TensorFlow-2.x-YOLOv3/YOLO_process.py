from multiprocessing import Process, Queue, Lock
from PyQt5.QtCore import pyqtSignal, QThread
from my_gui.Emitter import *
import os

os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import cv2
import numpy as np
import tensorflow as tf
from yolov3.utils import detect_image, detect_realtime, detect_video, Load_Yolo_model, detect_video_realtime_mp
from yolov3.configs import *


class YoloProcess(Process):
    def __init__(self, from_mainwin: Queue, to_mainwin: Queue, to_emitter: Pipe, status_lock : Lock):
        super().__init__()
        self.commands = from_mainwin
        self.send_im = to_mainwin
        self.pipe_to_emitter = to_emitter
        self.status_lock = status_lock

    def run(self):
        yolo = Load_Yolo_model()
        command = ""
        while True:
            print("2: Нейронка ожидает ввод")
            command = self.commands.get()
            if command == "exit":
                print("2: Test process govna prinal huini i okruglyaetsa")
                break
            if command == "image":
                im = self.commands.get()
                print(im)
                # cv2.imshow("im", im)
                image = detect_image(yolo, im, "./IMAGES/plate_1_detect.jpg", input_size=YOLO_INPUT_SIZE,
                                     show=True, CLASSES=TRAIN_CLASSES, rectangle_colors=(255, 0, 0))
                print("2: Изображение обработано")
                self.send_im.put(image)
                self.pipe_to_emitter.send("OK")
        exit(0)
