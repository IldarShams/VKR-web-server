from multiprocessing import Process, Queue, Lock
from PyQt5.QtCore import pyqtSignal, QThread
from my_gui.Emitter import *
import os

os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import cv2
import numpy as np
import tensorflow as tf
from pygrabber.dshow_graph import FilterGraph
from yolov3.utils import detect_image, detect_realtime, detect_video, Load_Yolo_model, detect_video_realtime_mp
from yolov3.configs import *


class YoloProcess(Process):
    def __init__(self, from_mainwin: Queue, to_mainwin: Queue, to_emitter: Pipe, status_lock : Lock):
        super().__init__()
        self.commands = from_mainwin
        self.send_im = to_mainwin
        self.pipe_to_emitter = to_emitter
        self.status_lock = status_lock
        # self.graph = FilterGraph()
        # self.device = None

    def run(self):
        yolo = Load_Yolo_model()
        command = ""
        while True:
            print("YOLO: Нейронка ожидает ввод")
            command = self.commands.get()
            if command == "exit":
                print("YOLO: выход")
                self.send_im.put("exit")
                break
            if command == "image":
                im = self.commands.get()
                print("YOLO: Изображение получено")
                # print(im)
                # cv2.imshow("im", im)
                image = detect_image(yolo, im, "./IMAGES/plate_1_detect.jpg", input_size=YOLO_INPUT_SIZE,
                                     show=True, CLASSES=TRAIN_CLASSES, rectangle_colors=(255, 0, 0))
                print("YOLO: Изображение обработано")
                self.send_im.put(image)
                self.pipe_to_emitter.send("OK")
            # if command == "video":
            #     cap = self.commands.get()
            #     print("YOLO: cap получен")
            #     while True:
            #         # Capture frame-by-frame
            #         ret, frame = cap.read()
            #         # if frame is read correctly ret is True
            #         if not ret:
            #             print("Can't receive frame (stream end?). Exiting ...")
            #             break
            #         # Our operations on the frame come here
            #         image = detect_image(yolo, frame, "./IMAGES/plate_1_detect.jpg", input_size=YOLO_INPUT_SIZE,
            #                              show=True, CLASSES=TRAIN_CLASSES, rectangle_colors=(255, 0, 0))
            #         # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #         # Display the resulting frame
            #         cv2.imshow('frame', image)
            #         if cv2.waitKey(1) == ord('q'):
            #             break
            #     # When everything done, release the capture
            #     cap.release()
            #     cv2.destroyAllWindows()
            # exit(0)
